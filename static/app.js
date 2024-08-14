async function cypherQuery(api, query) {
  return fetch(api, { method: "POST", body: query }).then(res => res.json())
}

function showCypherResult(result, elem) {
  if (!Array.isArray(result)) {
    elem.innerHTML = "Invalid response!"
    return
  } 
  elem.innerHTML = `Got ${result.length} records`

  if (!result.length) return

  const table = document.createElement('table');
  table.className = "table"
  elem.appendChild(table)

  const keys = Object.keys(result[0])
  const tr = table.insertRow()
  keys.forEach(key => {
    const th = document.createElement('th')
    th.textContent = key
    tr.appendChild(th)
  })

  result.forEach(row => {
    const tr = table.insertRow()
    keys.forEach(key => {
      var td = tr.insertCell()
      var value
      // TODO: show depending in type
      if (typeof row[key] == "object") {
        // TODO: serialize in PG format
        value = JSON.stringify(row[key])
      } else {
          value = row[key]
      }
      td.textContent = value
    })
  })
}

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('cypherForm')
  const resultElem = document.getElementById('cypherResult')
  const cypherApi = "/api/cypher"
  if (form) {
    form.addEventListener('submit', async e => {
      e.preventDefault()
      resultElem.innerHTML = ''
      const fields = Object.fromEntries(new FormData(form))
      cypherQuery(cypherApi, fields.query).then(result => {
          console.log(resultElem)
        showCypherResult(result, resultElem)
      })      
      return
    })
  }
})
