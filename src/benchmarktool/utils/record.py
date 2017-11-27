#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Searchable Result Statistics for Instances"""

import sys
import logging
import json
import hashlib

from benchmarktool.runscript.parser import Parser as RunscriptParser
from benchmarktool.result.parser import Parser as ResultParser

LOG = logging.getLogger('custom')

class Records(object):
    """Results statistics records for instances."""

    def __init__(self, runscript_path, result_path, stats_file=sys.stdout, horizon_enc=False):
        """Init.

        :param stats_file: file to write and read stats from.

        """
        self._runscript_path = runscript_path
        self._result_path = result_path
        self._stats_file = stats_file
        self._horizon_enc = horizon_enc
        self._global_data = {} # combined data from runscript and result XML files
        self._staged_data = {} # instance data staged for writing

    def _write_stats(self):
        """Records stats of an instance.

        :param instance_path: path to the instance file
        :param stats: statistic dictionary to store

        """
        if self._horizon_enc:
            LOG.debug("Recording horizon to encoding files!")
            for inst_path in self._staged_data:
                if self._staged_data[inst_path]['measures'].has_key('calls'):
                    calls = int(float(self._staged_data[inst_path]['measures']['calls'][1]))
                    status = self._staged_data[inst_path]['measures']['status'][1]
                    if status == 'SATISFIABLE':
                        horizon = calls - 1
                    elif status == 'UNKNOWN':
                        LOG.info("""Run for %s did not finish (result status: %s),
                        assuming horizon = #calls + 1""", inst_path, status)
                        horizon = calls
                    else:
                        LOG.error("Run for %s finished with unknown status %s, skipping!",
                                  inst_path, status)
                        continue
                    self._write_horizon_enc(inst_path, horizon)
                else:
                    LOG.error("No \'calls\' key in measures for %s, skipped!", inst_path)
        else:
            LOG.debug("Recording to %s:", str(self._stats_file))
            with self._stats_file as ofile:
                json.dump(self._staged_data, ofile, sort_keys=True, indent=4)

    def _write_horizon_enc(self, inst_path, horizon):
        """ For the given instance (path), writes an encoding that defines its minimum
            horizon into the same directory.

        """
        LOG.debug("Writing horizon encoding for instance %s with horizon %s",
                  inst_path, str(horizon))
        suffix = '__hor' + ('-' + self._horizon_enc if self._horizon_enc != 'default' else '')
        with open(inst_path + suffix, 'w') as hor_file:
            hor_file.write("#const horizon={}.".format(horizon))

    def _stage_inst(self, inst_path, measures):
        """Stages instance data for writing to storage file.

        """
        LOG.debug("Staging inst path %s with measures:\n%s",
                  inst_path, json.dumps(measures, sort_keys=True, indent=4))
        self._staged_data[inst_path] = {'measures' : measures,
                                        'md5' :
                                        hashlib.md5(open(inst_path, 'rb').read()).hexdigest()}

    def _aggregate_data(self):
        """Aggregates data from runscript and result XML.

        """
        runscript = RunscriptParser().parse(self._runscript_path)

        # Extract instance paths
        for _, benchmark in runscript.benchmarks.items():
            self._global_data[benchmark.name] = {'paths' : [], 'classes' : {}}
            for elem in benchmark.elements:
                LOG.debug(benchmark.name + ": " + elem.path)
                self._global_data[benchmark.name]['paths'].append(elem.path)

        result = ResultParser().parse(self._result_path)
        for _, benchmark in result.benchmarks.items():
            classes = self._global_data[benchmark.name]['classes']
            LOG.debug('* Benchmark name: %s', str(benchmark.name))
            for bmclass in benchmark.classes.values():
                classes[bmclass.name] = {'id' : bmclass.id, 'instances' : {}}
                LOG.debug('** Class name: %s', str(bmclass.name))
                for inst_id, instance in bmclass.instances.items():
                    LOG.debug('*** Instance ' + str(inst_id) + " : " + instance.name)
                    classes[bmclass.name]['instances'][str(inst_id)] = {'name' : instance.name,
                                                                        'runs' : {}}

        for _, project in result.projects.items():
            for runspec in project:
                for classresult in runspec:
                    _class = self._global_data[runspec.benchmark.name]['classes'][classresult.benchclass.name]
                    LOG.debug("* Class name: %s", str(classresult.benchclass.name))
                    for instresult in classresult.instresults:
                        LOG.debug("** Instance ID / name: %s : %s", str(instresult.instance.id),
                                  instresult.instance.name)
                        inst = _class['instances'][str(instresult.instance.id)]
                        for run in instresult.runs:
                            LOG.debug("*** Run measures: %s", str(run.measures))
                            inst['runs'][run.number] = run.measures
        LOG.debug("Combined Benchmark Records:\n%s",
                  json.dumps(self._global_data, sort_keys=True, indent=4))

    def store_stats(self):
        """Store statistical instance data.

        """
        self._aggregate_data()
        for bm_name in self._global_data:
            if len(self._global_data[bm_name]['paths']) > 1:
                LOG.error("""More than 1 path for benchmark %s,
                hence cannot record instance stats disambiguously!""",
                          bm_name)
            else:
                path = self._global_data[bm_name]['paths'][0]
            for class_name in self._global_data[bm_name]['classes']:
                _class = self._global_data[bm_name]['classes'][class_name]
                for inst in _class['instances']:
                    inst_path = "{}{}/{}".format(path, class_name,
                                                 _class['instances'][inst]['name'])
                    measures = _class['instances'][inst]['runs'][1]
                    self._stage_inst(inst_path, measures)
        self._write_stats()
