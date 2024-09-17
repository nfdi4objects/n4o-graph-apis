const sparql = body => fetch('/api/sparql', {method: "POST", body, headers: { "Content-Type": "application/sparql-query" }})
  .then(res => res.json())

const prefixes = {
  crm: "http://www.cidoc-crm.org/cidoc-crm/",
  dcat: "http://www.w3.org/ns/dcat#",
  dct: "http://purl.org/dc/terms/",
  foaf: "http://xmlns.com/foaf/0.1/",
  n4oc: "https://graph.nfdi4objects.net/collection/",
  schema: "http://schema.org/",
  skos: "http://www.w3.org/2004/02/skos/core#",
  void: "http://rdfs.org/ns/void#",
  wd: "http://www.wikidata.org/entity/",
  dc: "http://purl.org/dc/elements/1.1/",
  dct: "http://purl.org/dc/terms/",
  foaf: "http://xmlns.com/foaf/0.1/",
  wgs: "http://www.w3.org/2003/01/geo/wgs84_pos#"
}

$(document).ready(() => {

  $("[data-sparql]").each((i,e) => {
    const query = $(e).attr("data-sparql")
    $(e).attr("href", "/sparql#"+new URLSearchParams({query}))
  })

  $("a[data-sparql-value]").each((i,e) => {
    const query = $(e).attr("data-sparql-value")
    $(e).attr("href", "/sparql#"+new URLSearchParams({query}))
    sparql(query).then(res => {
      res = res?.results?.bindings || []
      res = Object.values(res[0]||{})[0]
      $(e).text(res ? res.value : "???")
    })
  })

  // TODO: only include prefixes used in the query
  const sparqlPrefixes = Object.entries(prefixes).map(([k,v]) => `PREFIX ${k}: <${v}>`).join("\n")+"\n"

  $("div[data-sparql-table]").each((i,e) => {
    const query = sparqlPrefixes + $(e).attr("data-sparql-table")
    const yasr = new Yasr(e, { prefixes })
    sparql(query).then(res => yasr.setResponse(res))
  })
})
