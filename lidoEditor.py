from pathlib import Path
from x3ml import getMapping
from LidoRDFConverter import LidoRDFConverter

def fromFile(fname):
    with open(fname,'r') as fid:
        return fid.read()
    return ''

def toFile(fname,data):
    if data:
        with open(fname,'w') as fid:
            fid.write(data)
            return fname

def dlft3MFile(): return './lido2rdf.x3ml'
def dlftLidoFile(): return './example.xml'

def dfltLidoText(): 
    return fromFile(dlftLidoFile())

def checkX3File():
    f = Path('./mapping.x3ml')
    if f.exists(): 
        return f
    f = Path(dlft3MFile())
    if f.exists(): 
        return f
    return Path()

def getConfig():
    x3mlFile = checkX3File()
    mappings = getMapping(x3mlFile)
    return {'mappingTxt': fromFile(x3mlFile),'sourceTxt':fromFile(dlftLidoFile()),'mappings':mappings}

def processRequest(request):
    workFile = 'tmp.xml'
    fmt = 'turtle'
    result = '<no-data/>'
    if xmlFile := toFile(workFile,request.json['xmlData']):
        mapping = request.json['mapping']
        if mappingFile := toFile('mapping.x3ml',mapping):
            converter = LidoRDFConverter(mappingFile)
            graph,_ = converter.processXML(xmlFile)
            result = graph.serialize(format=fmt)
    return result




