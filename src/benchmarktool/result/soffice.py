'''
Created on Jan 20, 2010

@author: Roland Kaminski
'''

from zipfile import ZipFile
from StringIO import StringIO

class Spreadsheet:
    def __init__(self, benchmark, columns, measures):
        self.instSheet = InstanceTable(benchmark, columns, measures)
        
    def finish(self):
        self.instSheet.finish()
        
    def printSheet(self, out):
        zipFile = ZipFile(out, "w")
        out = StringIO()
        out.write('''\
<?xml version="1.0" encoding="UTF-8"?>\
<office:document-content xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0" xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0" xmlns:number="urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0" xmlns:presentation="urn:oasis:names:tc:opendocument:xmlns:presentation:1.0" xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0" xmlns:chart="urn:oasis:names:tc:opendocument:xmlns:chart:1.0" xmlns:dr3d="urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0" xmlns:math="http://www.w3.org/1998/Math/MathML" xmlns:form="urn:oasis:names:tc:opendocument:xmlns:form:1.0" xmlns:script="urn:oasis:names:tc:opendocument:xmlns:script:1.0" xmlns:ooo="http://openoffice.org/2004/office" xmlns:ooow="http://openoffice.org/2004/writer" xmlns:oooc="http://openoffice.org/2004/calc" xmlns:dom="http://www.w3.org/2001/xml-events" xmlns:xforms="http://www.w3.org/2002/xforms" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:rpt="http://openoffice.org/2005/report" xmlns:of="urn:oasis:names:tc:opendocument:xmlns:of:1.2" xmlns:rdfa="http://docs.oasis-open.org/opendocument/meta/rdfa#" xmlns:field="urn:openoffice:names:experimental:ooxml-odf-interop:xmlns:field:1.0" xmlns:formx="urn:openoffice:names:experimental:ooxml-odf-interop:xmlns:form:1.0" office:version="1.2">\
<office:scripts/>\
<office:font-face-decls>\
<style:font-face style:name="Liberation Sans" svg:font-family="'Liberation Sans'" style:font-family-generic="swiss" style:font-pitch="variable"/>\
<style:font-face style:name="DejaVu Sans" svg:font-family="'DejaVu Sans'" style:font-family-generic="system" style:font-pitch="variable"/>\
</office:font-face-decls>\
<office:automatic-styles>\
<style:style style:name="co1" style:family="table-column">\
<style:table-column-properties fo:break-before="auto" style:column-width="0.8925in"/>\
</style:style>\
<style:style style:name="ro1" style:family="table-row">\
<style:table-row-properties style:row-height="0.178in" fo:break-before="auto" style:use-optimal-row-height="true"/>\
</style:style>\
<style:style style:name="ta1" style:family="table" style:master-page-name="Default">\
<style:table-properties table:display="true" style:writing-mode="lr-tb"/>\
</style:style>\
</office:automatic-styles>\
<office:body>\
<office:spreadsheet>''')
        self.instSheet.printSheet(out)
        out.write('''</office:spreadsheet></office:body></office:document-content>''')
        zipFile.writestr("mimetype", '''application/vnd.oasis.opendocument.spreadsheet''')
        zipFile.writestr("content.xml", out.getvalue())
        zipFile.writestr("META-INF/manifest.xml", '''\
<?xml version="1.0" encoding="UTF-8"?>\
<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0">\
<manifest:file-entry manifest:media-type="application/vnd.oasis.opendocument.spreadsheet" manifest:version="1.2" manifest:full-path="/"/>\
<manifest:file-entry manifest:media-type="text/xml" manifest:full-path="content.xml"/>\
<manifest:file-entry manifest:media-type="text/xml" manifest:full-path="Basic/Standard/Functions.xml"/>\
<manifest:file-entry manifest:media-type="text/xml" manifest:full-path="Basic/Standard/script-lb.xml"/>\
<manifest:file-entry manifest:media-type="" manifest:full-path="Basic/Standard/"/>\
<manifest:file-entry manifest:media-type="text/xml" manifest:full-path="Basic/script-lc.xml"/>\
<manifest:file-entry manifest:media-type="" manifest:full-path="Basic/"/>\
</manifest:manifest>\
''')
        zipFile.writestr("Basic/script-lc.xml", '''\
<?xml version="1.0" encoding="UTF-8"?>\
<!DOCTYPE library:libraries PUBLIC "-//OpenOffice.org//DTD OfficeDocument 1.0//EN" "libraries.dtd">\
<library:libraries xmlns:library="http://openoffice.org/2000/library" xmlns:xlink="http://www.w3.org/1999/xlink">\
<library:library library:name="Standard" library:link="false"/>\
</library:libraries>\
''')
        zipFile.writestr("Basic/Standard/script-lb.xml", '''\
<?xml version="1.0" encoding="UTF-8"?>\
<!DOCTYPE library:library PUBLIC "-//OpenOffice.org//DTD OfficeDocument 1.0//EN" "library.dtd">\
<library:library xmlns:library="http://openoffice.org/2000/library" library:name="Standard" library:readonly="false" library:passwordprotected="false">\
<library:element library:name="Functions"/>\
</library:library>\
''')
        zipFile.writestr("Basic/Standard/Functions.xml", '''\
<?xml version="1.0" encoding="UTF-8"?>\
<!DOCTYPE script:module PUBLIC "-//OpenOffice.org//DTD OfficeDocument 1.0//EN" "module.dtd">\
<script:module xmlns:script="http://openoffice.org/2000/script" script:name="Functions" script:language="StarBasic">\
Function SDSUM(a, b)
    If Not IsArray( a ) Then
        If IsNumeric( a ) Then
            SDSUM = a
        Else
            SDSUM = 0
        End If
    Else
        Dim s As double
        For i = 1 To ubound( a, 1 )
            For j = 1 To ubound( a, 2 )
                Dim x As double
                Dim y As double
                If IsNumeric( a( i, j ) ) Then
                    x = a( i, j )
                Else
                    x = 0
                End If
                  If IsNumeric( b( i, j ) ) Then
                    y = b( i, j )
                Else
                    y = 0
                End If
                s = s + (x - y)^2
            Next j
        Next i
        SDSUM = s
    End If
End Function
Function GEOMDIST(a, b)
    GEOMDIST = SDSUM(a,b)^0.5
End Function
</script:module>
''')
        zipFile.close()
        
    def addRunspec(self, runspec):
        self.instSheet.addRunspec(runspec)
        
class Cell:
    def __init__(self):
        pass

class StringCell:
    def __init__(self, val):
        self.val = val
    
    def printSheet(self, out):
        out.write('<table:table-cell office:value-type="string"><text:p>{0}</text:p></table:table-cell>'.format(self.val))

class FloatCell:
    def __init__(self, val):
        self.val = val
    
    def printSheet(self, out):
        out.write('<table:table-cell office:value-type="float" office:value="{0}"/>'.format(self.val))

class FormulaCell:
    def __init__(self, val):
        self.val = val
    
    def printSheet(self, out):
        out.write('<table:table-cell table:formula="{0}" office:value-type="float"/>'.format(self.val))

class Table:
    def __init__(self):
        self.content = []
    
    def add(self, row, col, cell):
        while len(self.content) <= row: 
            self.content.append([])
        rowRef = self.content[row]
        while len(rowRef) <= col:
            rowRef.append(None)
        rowRef[col] = cell

    def cellIndex(self, row, col):
        radix = ord("Z") - ord("A") + 1
        ret   = ""
        while col >= 0:
            rem = col % radix
            ret = chr(rem + ord("A")) + ret
            col = col / radix - 1
        return ret + str(row + 1)

    def printSheet(self, out):
        out.write('<table:table table:name="Instances" table:style-name="ta1" table:print="false"><table:table-column table:style-name="co1" table:default-cell-style-name="Default"/>')
        for row in self.content:
            out.write('<table:table-row table:style-name="ro1">')
            for cell in row:
                if cell == None:
                    out.write('<table:table-cell office:value-type="string"><text:p></text:p></table:table-cell>')
                else:
                    cell.printSheet(out)
            out.write('</table:table-row>')
        out.write('</table:table>')
    
class InstanceTable(Table):
    def __init__(self, benchmark, columns, measures):
        Table.__init__(self)
        self.benchmark = benchmark
        self.columns   = columns
        self.results   = {}
        self.measures  = measures
        self.lines     = 0
        self.machines  = set()
        self.lastcol   = None
        row = 2
        for instance in self.benchmark.list:
            instance = instance.values()[0]
            self.add(row, 0, StringCell(instance.benchclass.name + "/" + instance.name))
            row += instance.maxRuns
            self.lines += instance.maxRuns
        
        self.resultOffset = row
        self.add(self.resultOffset + 1, 0, StringCell("SUM"))
        self.add(self.resultOffset + 2, 0, StringCell("AVG"))
        self.add(self.resultOffset + 3, 0, StringCell("DEV"))
        self.add(self.resultOffset + 4, 0, StringCell("DST"))
    
    def addFooter(self, col):
        self.add(self.resultOffset + 1, col, FormulaCell("of:=SUM([.{0}:.{1}])".format(self.cellIndex(2, col), self.cellIndex(self.resultOffset - 1, col))))
        self.add(self.resultOffset + 2, col, FormulaCell("of:=AVERAGE([.{0}:.{1}])".format(self.cellIndex(2, col), self.cellIndex(self.resultOffset - 1, col))))
        self.add(self.resultOffset + 3, col, FormulaCell("of:=STDEV([.{0}:.{1}])".format(self.cellIndex(2, col), self.cellIndex(self.resultOffset - 1, col))))
    
    def finish(self):
        col = 1
        floatOccur = {}
        for column in sorted(self.columns.columns):
            column.offset = col
            self.add(0, col, StringCell(column.genName(len(self.machines) > 1)))
            if self.measures == "": measures = sorted(column.width)
            else: measures = self.measures
            add = 0
            for name in measures:
                if name in column.content:
                    self.add(1, column.offset + add, StringCell(name))
                    for line, cell in column.content[name]:
                        self.add(2 + line, column.offset + add, cell)
                    if column.type[name] == "float":
                        if not name in floatOccur: floatOccur[name] = set() 
                        floatOccur[name].add(col)
                        self.addFooter(col + add)
                    add += 1
            if add == 0: add = 1    
            col += add
        self.lastcol = col
        self.add(0, col, StringCell("virtual best"))
        for name in measures:
            if name in floatOccur:
                self.add(1, col, StringCell(name))
                for row in xrange(2, self.resultOffset):
                    minRange = ""
                    for colRef in sorted(floatOccur[name]):
                        if minRange != "": 
                            minRange += ";" 
                        minRange += "[.{0}]".format(self.cellIndex(row, colRef))
                    self.add(row, col, FormulaCell("of:=MIN({0})".format(minRange)))
                    self.addFooter(col)
                for colRef in sorted(floatOccur[name]):
                    self.add(self.resultOffset + 4, colRef, FormulaCell("of:=GEOMDIST([.{0}:.{1}];[.{2}:.{3}])".format(self.cellIndex(2, colRef), self.cellIndex(self.resultOffset - 1, colRef), self.cellIndex(2, col), self.cellIndex(self.resultOffset - 1, col))))
                col+= 1
            
    def addRunspec(self, runspec):
        column = self.columns.getColumn(runspec)
        self.machines.add(column.machine)
        for classresult in runspec.classresults:
            for instresult in classresult.instresults:
                for run in instresult.runs:
                    if self.measures == "": measures = sorted(run.measures.keys())
                    else: measures = self.measures
                    for name in measures:
                        if name in run.measures:
                            valueType, value = run.measures[name]
                            if valueType != "float": valueType = "string"
                            column.addCell(instresult.instance.line + run.number - 1, name, valueType, value)

class Column:
    def __init__(self, setting, machine):
        self.setting  = setting
        self.machine  = machine
        self.content  = {}
        self.type     = {}
    
    def genName(self, addMachine):
        res = self.setting.system.name + "-" + self.setting.system.version + "/" + self.setting.name
        if addMachine:
            res += " ({0})".format(self.machine.name) 
        return res         
    
    def __cmp__(self, other):
        return cmp((self.setting.system.order, self.setting.order, self.machine.name), (other.setting.system.order, other.setting.order, other.machine.name))
    
    def __hash__(self):
        return hash((self.setting, self.machine))
    
    def addCell(self, line, name, valueType, value):
        if type == "float": cell = FloatCell(float(value))
        else: cell = StringCell(value)
        self.type[name] = valueType
        if not name in self.content:
            self.content[name] = []
        self.content[name].append((line, cell))
