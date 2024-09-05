const sparql = query => fetch('/api/sparql?' + new URLSearchParams({query}))
  .then(res => res.json())
  .then(res => res.results.bindings)

$(document).ready(() => {
  $("[data-sparql]").each((i,e) => {
    const query = $(e).attr("data-sparql")
    $(e).attr("href", "/sparql#"+new URLSearchParams({query}))
  })
 console.log("WTF")
  $("a[data-sparql-value]").each((i,e) => {
    const query = $(e).attr("data-sparql-value")
    $(e).attr("href", "/sparql#"+new URLSearchParams({query}))
    sparql(query).then(res => {
      res = Object.values(res[0]||{})[0]
      $(e).text(res ? res.value : "???")
    })
  })
})
