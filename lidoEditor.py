from pathlib import Path
from x3ml import getMapping
import LidoRDFConverter as LRC 
from lxml import etree

class Mapper():
    def __init__(self, fileName=''):
        self.mappings = getMapping(fileName)
        self.graph = LRC.makeResultGraph()
    
    def info(self):
        infoElem = etree.Element('info')
        etree.SubElement(infoElem,'title').text='A mapping of LIDO V1.0 to CIDOC 6.0'
        etree.SubElement(infoElem,'general_description').text='Administrative Metadata Only'
      
        attr = {'type':'', 'version':''}
        etree.SubElement(
            etree.SubElement(
                etree.SubElement(infoElem,'source'),'source_info'),'source_schema',attrib=attr).text='LIDO v1.0'
       
        attr = {'type':'rdfs', 'schema_file':'cidoc_crm_v6.0-draft-2015January.rdfs', 'version':'6.0'}
        etree.SubElement(
            etree.SubElement(
                etree.SubElement(infoElem,'target'),'target_info'),'target_schema',attrib=attr).text='CIDOC-CRM'
       
        miElem = etree.SubElement(infoElem,'mapping_info')
        etree.SubElement(miElem,'mapping_created_by_org')
        etree.SubElement(miElem,'mapping_created_by_person')
        etree.SubElement(miElem,'in_collaboration_with')
    
        ediElem = etree.SubElement(infoElem,'example_data_info')
        etree.SubElement(ediElem,'example_data_from')
        etree.SubElement(ediElem,'example_data_contact_person')
        etree.SubElement(ediElem,'example_data_source_record')
        etree.SubElement(ediElem,'generator_policy_info')
        etree.SubElement(ediElem,'example_data_target_record')
        etree.SubElement(ediElem,'thesaurus_info')
        return infoElem
    
    def ns(self):
        elem = etree.Element('namespaces')
        etree.SubElement(elem,'namespace', attrib={'prefix':'rdfs','uri':'http://www.w3.org/2000/01/rdf-schema#'})
        etree.SubElement(elem,'namespace', attrib={'prefix':'xsd','uri':'http://www.w3.org/2001/XMLSchema#'})
        etree.SubElement(elem,'namespace', attrib={'prefix':'crm','uri':'http://www.cidoc-crm.org/cidoc-crm/'})
        return elem
    
    def toXML(self):
        xmlns_uris = {'xsi': 'http://www.w3.org/2001/XMLSchema-instance/x3ml_v1.0.xsd'}
        root =  etree.Element('x3ml',nsmap=xmlns_uris)
        root.set('source_type','xpath')
        root.set('version','1.0')
        root.append(self.info())
        root.append(self.ns())
        mElement = etree.SubElement(root,'mappings')
        for m in self.mappings:
            mElement.append(m.toXML())
        return root
    
    def tostring(self):
        return etree.tostring(self.toXML(), pretty_print=True,xml_declaration=True, encoding='UTF-8')

def testMapper(**kw):
    str = Mapper('defaultMapping.x3ml').tostring()
    if kw.get('print',None):
        print(str.decode(), end='')
    if fn:=kw.get('file',None):
        with open(fn,'w') as fid:
            fid.write(str.decode())

def fromFile(fname):
    with open(fname,'r') as fid:
        return fid.read()
    return ''

def toFile(fname,data):
    if data:
        with open(fname,'w') as fid:
            fid.write(data)
            return fname

def dlft3MFile(): return './defaultMapping.x3ml'
def dlftLidoFile(): return './defaultLido.xml'

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
    return {'sourceTxt':fromFile(dlftLidoFile()),'mappings':mappings}

def processRequest(request):
    workFile = 'tmp.xml'
    fmt = 'turtle'
    result = '<no-data/>'
    if xmlFile := toFile(workFile,request.json['xmlData']):
        mapping = request.json['mapping']
        if mappingFile := toFile('mapping.x3ml',mapping):
            converter = LRC.LidoRDFConverter(mappingFile)
            graph,_ = converter.processXML(xmlFile)
            result = graph.serialize(format=fmt)
    return result




