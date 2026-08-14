const sparql = body => fetch('/api/sparql', {method: "POST", body, headers: { "Content-Type": "application/sparql-query" }})
  .then(res => res.json())

const commonPrefixes = {
  crm: "http://www.cidoc-crm.org/cidoc-crm/",
  dcat: "http://www.w3.org/ns/dcat#",
  dct: "http://purl.org/dc/terms/",
  foaf: "http://xmlns.com/foaf/0.1/",
  schema: "http://schema.org/",
  skos: "http://www.w3.org/2004/02/skos/core#",
  void: "http://rdfs.org/ns/void#",
  wd: "http://www.wikidata.org/entity/",
  dc: "http://purl.org/dc/elements/1.1/",
  dct: "http://purl.org/dc/terms/",
  foaf: "http://xmlns.com/foaf/0.1/",
  wgs: "http://www.w3.org/2003/01/geo/wgs84_pos#",
  terminology: `${graphBase}terminology/`,
  collection: `${graphBase}collection/`,
  mappings: `${graphBase}mappings/`,
  bartoc: "http://bartoc.org/en/node/",
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
  const sparqlPrefixes = Object.entries(commonPrefixes).map(([k,v]) => `PREFIX ${k}: <${v}>`).join("\n")+"\n"

  $("div[data-sparql-table]").each((i,e) => {
    const query = sparqlPrefixes + $(e).attr("data-sparql-table")
    const yasr = new Yasr(e, { prefixes: commonPrefixes })
    sparql(query).then(res => yasr.setResponse(res))
  })
})
