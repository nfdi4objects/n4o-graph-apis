// TODO: add more prefixes and reuse in app.py
const knownPrefixes = {
  crm: "http://www.cidoc-crm.org/cidoc-crm/",
  crmdig: "http://www.cidoc-crm.org/extensions/crmdig/",
  lrmoo: "http://www.cidoc-crm.org/extensions/lrmoo/",
  crmsci: "http://www.cidoc-crm.org/extensions/crmsci/",
  crminf: "http://www.cidoc-crm.org/extensions/crminf/",
  crmgeo: "http://www.cidoc-crm.org/extensions/crmgeo/",
  crmarcheo: "http://www.cidoc-crm.org/extensions/crmarcheo/",
  crmtex: "http://www.cidoc-crm.org/extensions/crmtex/",
  dc: "http://purl.org/dc/elements/1.1/",
  dct: "http://purl.org/dc/terms/",
  dctype: "http://purl.org/dc/dcmitype/",
  foaf: "http://xmlns.com/foaf/0.1/",
  geo: "http://www.opengis.net/ont/geosparql#",
  n4oc: "https://graph.nfdi4objects.net/collection/",
  owl: "http://www.w3.org/2002/07/owl#>",
  rdf: "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
  rdfs: "http://www.w3.org/2000/01/rdf-schema#",
  skos: "http://www.w3.org/2004/02/skos/core#",
  wd: "http://www.wikidata.org/entity/",
  wgs: "http://www.w3.org/2003/01/geo/wgs84_pos#",
  xsd: "http://www.w3.org/2001/XMLSchema#",
  owl: "http://www.w3.org/2002/07/owl#",
}

document.addEventListener("DOMContentLoaded", () => {
  const editor = new Yasqe(document.getElementById("yasqe"), {
    requestConfig: {
      endpoint: "/api/sparql",
      method: "POST",
    },
    sparql: { showQueryButton: true },
  })

  const prefixes = () => {
    const editorPrefixes = editor.getPrefixesFromQuery()
    return { ...knownPrefixes, ...editorPrefixes }
  }

 const yasr = new Yasr(document.getElementById("yasr"), { prefixes })

  editor.on("queryResponse", (instance, res) => yasr.setResponse(res))

  $("#examples").on("change", e => {
    editor.setValue(e.target.value)
    if (e.target.value != "") editor.query()
  })

  if (window.location.hash?.startsWith("#query=")) {
    editor.query()
  }
})
