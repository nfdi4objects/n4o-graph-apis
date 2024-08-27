const sparql = query => fetch('/api/sparql?' + new URLSearchParams({query}))
  .then(res => res.json())
  .then(res => res.results.bindings)

$(document).ready(() => {
  $("[data-sparql]").each((i,e) => {
    const query = $(e).attr("data-sparql")
    $(e).attr("href", "/sparql#"+new URLSearchParams({query}))
  })
})
