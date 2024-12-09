from pathlib import Path
from x3ml import getMapping, ExP
import LidoRDFConverter as LRC 
from lxml import etree

def dlftMappingFile(): return './defaultMapping.x3ml'
def dlftLidoFile(): return './defaultLido.xml'

def workFolder(): return './work'
def workMappingFile(): return workFolder()+'/mapping.x3ml'
def workLidoFile(): return workFolder()+'/lido.xml'

def updateExP(X:ExP,p:str,e:str):
    X.path = p
    X.entity = e
    #print(X)
 
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
        return etree.tostring(self.toXML(), pretty_print=True,xml_declaration=True, encoding='UTF-8').decode()
    
    def dispatch(self, mode, request):
        '''parses request and dispatches the mode'''
        val = lambda x : request.json[x]
        mIndex = int(val('mappingIndex'))
        match(mode):
            case 0:
                S = ExP(val('path'),val('entity'))
                self.setDomainValues(mIndex,S)
            case 1:
                lIndex = int(val('linkIndex'))
                P = ExP(val('path'),val('property'))
                O = ExP(val('path'),val('entity'))
                self.setLinkValues(mIndex,lIndex, P,O)
            case 2:
                lIndex = int(val('linkIndex'))
                print("dispatch ", mode, lIndex)
                self.mappings[mIndex].POs.pop(lIndex)
     
    def setDomainValues(self, mappingIndex, S):
        '''Changes the mapping domain settings'''
        if mappingIndex < len(self.mappings):
            updateExP(self.mappings[mappingIndex].S, S.path, S.entity)
            self.store()
        
    def setLinkValues(self, mappingIndex, linkIndex, P, O):
        '''Changes the link settings'''
        if mappingIndex < len(self.mappings):
            po_list = self.mappings[mappingIndex].POs
            if linkIndex < len(po_list):
                updateExP(po_list[linkIndex].P, P.path, P.entity)
                updateExP(po_list[linkIndex].O, O.path, O.entity)
                self.store()
    
    def store(self):
        toFile(workMappingFile(),self.tostring())

def makeWorkspace():
    Path(workFolder()).mkdir(exist_ok=True)
    mFile = Path(workMappingFile())
    if not mFile.exists():
        mFile.write_text(Path(dlftMappingFile()).read_text())
    sFile = Path(workLidoFile())
    if not sFile.exists():
        sFile.write_text(Path(dlftLidoFile()).read_text())
    return Mapper(mFile)

def testMapper(**kw):
    str = Mapper('defaultMapping.x3ml').tostring()
    if kw.get('print',None):
        print(str, end='')
    if fn:=kw.get('file',None):
        with open(fn,'w') as fid:
            fid.write(str)

def fromFile(fname):
    with open(fname,'r') as fid:
        return fid.read()
    return ''

def toFile(fname,data):
    if data:
        with open(fname,'w') as fid:
            fid.write(data)
            return fname


def dfltLidoText(): 
    return fromFile(dlftLidoFile())

def workLidoText():
    return fromFile(workLidoFile())

def processRequest(request):
    fmt = 'turtle'
    result = '<no-data/>'
    if xmlFile := toFile(workLidoFile(),request.json['xmlData']):
        converter = LRC.LidoRDFConverter(workMappingFile())
        graph,_ = converter.processXML(xmlFile)
        result = graph.serialize(format=fmt)
    return result


