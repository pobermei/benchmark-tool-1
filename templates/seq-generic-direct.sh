#!/bin/bash
# http://www.cril.univ-artois.fr/~roussel/runsolver/

cd "$(dirname $0)"

#top -n 1 -b > top.txt

[[ -e .finished ]] || echo "{run.file}" | "{run.root}/programs/{run.solver}" {run.args} &>log

touch .finished
