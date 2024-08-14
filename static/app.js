async function cypherQuery(api, query) {
  return fetch(api, { method: "POST", body: query }).then(res => res.json())
}

function showCypherResult(result, elem) {
  if (!Array.isArray(result)) {
    elem.innerHTML = "Invalid response!"
    return
  } 
  elem.innerHTML = ''

  if (!result.length) return

  const table = document.createElement('table')
  table.className = "display"
  const thead = document.createElement('thead')
  const tbody = document.createElement('tbody')
  table.appendChild(thead)
  table.appendChild(tbody)

  const keys = Object.keys(result[0])
  const tr = thead.insertRow()
  tr.appendChild(document.createElement('th'))
  keys.forEach(key => {
    const th = document.createElement('th')
    th.textContent = key
    tr.appendChild(th)
  })

  result.forEach((row, i) => {
    const tr = tbody.insertRow()
    var td = tr.insertCell()
    td.textContent = i+1
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

  elem.appendChild(table)
  table = new DataTable(table) //'#cypherResult');
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
