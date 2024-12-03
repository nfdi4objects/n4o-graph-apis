from pathlib import Path
from x3ml import getMapping
import LidoRDFConverter as LRC 
from lxml import etree



class Info():
    def __init__(self, var=None):
        self.var = var

    def toXML(self):
        xml = etree.fromstring('<info><title>A mapping of LIDO V1.0 to CIDOC 6.0</title></info>')
        return xml
    

class Mapper():
    def __init__(self, fileName=''):
        self.mappings = getMapping(fileName)
        self.graph = LRC.makeResultGraph()
    
    def info(self):
        return '''<info>
                    <title>A mapping of LIDO V1.0 to CIDOC 6.0</title>
                    <general_description>Administrative Metadata Only</general_description>
                    <source>
                        <source_info>
                            <source_schema type="" version="">LIDO v1.0</source_schema>
                        </source_info>
                    </source>
                    <target>
                        <target_info>
                            <target_schema schema_file="cidoc_crm_v6.0-draft-2015January.rdfs" type="rdfs" version="6.0">CIDOC-CRM</target_schema>
                        </target_info>
                    </target>
                    <mapping_info>
                        <mapping_created_by_org/>
                        <mapping_created_by_person/>
                        <in_collaboration_with/>
                    </mapping_info>
                    <example_data_info>
                        <example_data_from/>
                        <example_data_contact_person/>
                        <example_data_source_record/>
                        <generator_policy_info/>
                        <example_data_target_record/>
                        <thesaurus_info/>
                    </example_data_info>
                  </info>'''

    def ns(self):
        return '''<namespaces>
        <namespace prefix="rdfs" uri="http://www.w3.org/2000/01/rdf-schema#"/>
        <namespace prefix="xsd" uri="http://www.w3.org/2001/XMLSchema#"/>
        <namespace prefix="crm" uri="http://www.cidoc-crm.org/cidoc-crm/"/>
        </namespaces>'''

    def toXML(self):
        xmlns_uris = {'xsi': 'http://www.w3.org/2001/XMLSchema-instance/x3ml_v1.0.xsd'}
        root =  etree.Element('x3ml',nsmap=xmlns_uris)
        root.set('source_type','xpath')
        root.set('version','1.0')
        root.append(etree.fromstring(self.info()))
        root.append(etree.fromstring(self.ns()))
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




