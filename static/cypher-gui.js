function showCypherResult(result, elem) {
  elem.innerHTML = ''

  // TODO: show duration
    
  if (!Array.isArray(result)) {
    $(`<div class="errorResult"><div class="redOutline">
    <p>Unable to get response from endpoint. Possible reasons:</p>
    <ul>
      <li>Endpoint is down</li>
    </ul>
    </div></div>`).appendTo(elem)
    return
  } 

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
  new DataTable(table)
}

class CypherEditor extends CodeMirror {
    constructor(elem, config) {
        config.mode = 'cypher'
        super(elem, config)
    
        this.endpoint = config.endpoint

        const buttons = $(`<div class="yasqe_buttons" />`)
        const queryBtn = $(`<button class="yasqe_queryButton" title="Run query" aria-label="Run query" >Run query</button>`)
        buttons.append(queryBtn)
    /*
          const queryEl = drawSvgStringAsElement(imgs.query);
          addClass(queryEl, "queryIcon");
          this.queryBtn.appendChild(queryEl);
          */
        queryBtn.on('click', () => { this.query() })
      
        //  this.updateQueryButton()

        buttons.appendTo(this.getWrapperElement())

        this.on("query", this.handleQuery)
        this.on("queryResponse", this.handleQueryResponse)
        this.on("queryAbort", this.handleQueryAbort)
    }

    handleQuery(editor, req) {
        editor.req = req
        // editor.updateQueryButton()
    }
  
    handleQueryResponse(editor, res, duration) {
        console.log("QUERY RESPONSE")
        editor.lastQueryDuration = duration
        editor.req = undefined
        // editor.updateQueryButton()
    }
  
    handleQueryAbort(editor, req) {
        editor.req = undefined
        // this.updateQueryButton()
    }

    abortQuery() {
        if (this.req) {
            // this.req.abort(); TODO
            this.emit("queryAbort", this.req);
        }
    }

    async query() {
        if (this.req) {
            this.abortQuery()
            return
        }

        const cypher = this.getValue()
        const queryStart = Date.now()

        this.emit("query", cypher)

        return fetch(this.endpoint, { method: "POST", body: cypher })
          .then(res => res.json())
          .then(res => { this.emit("queryResponse", res, Date.now() - queryStart) })
          .catch(e => {
              // (if (e instanceof Error && e.message === "Aborted") { TODO: don't do anything
              console.error(e)
              this.emit("queryResponse", null, Date.now() - queryStart) 
          })
    }

    emit(name, ...data) {
        CodeMirror.signal(this, name, this, ...data)
    }
}

document.addEventListener('DOMContentLoaded', () => {
  const textarea = document.getElementById('cypherform')
  const editor = new CypherEditor(e => textarea.parentNode.replaceChild(e, textarea), {
    endpoint: "/api/cypher",

    // CodeMirror:
    value: textarea.value,
    indentWithTabs: true,
    smartIndent: true,
    lineNumbers: true,
    matchBrackets: true,
    autofocus: true,
    theme: "default"
  })

  const resultElem = document.getElementById('cypherResult')

  editor.on("queryResponse", (editor, res) => {
    showCypherResult(res, resultElem)
  })

  $('#examples').on('change', e => {
    editor.setValue(e.target.value)
    editor.query()
  })
})
