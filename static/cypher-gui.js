function showCypherResult(result, elem) {
  elem.innerHTML = ''
  elem.className = "dataTables_wrapper no-footer"

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
  elem.appendChild(table)

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
      var value, mode
      if (typeof row[key] == "object") {
        // TODO: serialize in PG format if type=edge / node / graph
        value = JSON.stringify(row[key])
        mode = "javascript"
      } else {
        value = row[key]
      }
      if (mode) {
        td.className = "cm-s-idea"
        CodeMirror.runMode(value, mode, td)
      } else {
        td.textContent = value
      }
    })
  })

  $(table).DataTable({
      dom: "tip",
      pageLength: 50,
      lengthChange: true,
      deferRender: true,
      orderClasses: false,
      language: {
        paginate: { first: "&lt;&lt;", last: "&gt;&gt;", next: "&gt;", previous: "&lt;", },
      },
    })

}

class CypherEditor extends CodeMirror {
    constructor(elem, config) {
        config.mode = 'cypher'
        super(elem, config)
        this.endpoint = config.endpoint
    
        // TODO
        //if (window.location.hash) {
        // console.log(window.location.has)
        //}


        const buttons = $(`<div class="yasqe_buttons" />`)
        this.queryBtn = $(`<button class="yasqe_queryButton" title="Run query" aria-label="Run query" />`)
        buttons.append(this.queryBtn)
    /*
          const queryEl = drawSvgStringAsElement(imgs.query);
          addClass(queryEl, "queryIcon");
          this.queryBtn.appendChild(queryEl);
          */
      this.queryBtn.on('click', () => { this.query() })

        $(`<div class="svgImg queryIcon"><svg xmlns="http://www.w3.org/2000/svg" xml:space="preserve" height="81.9" width="72.9" version="1.1" y="0px" x="0px" viewBox="0 0 72.900002 81.900002" aria-hidden="true"><path id="queryIcon" d="m69.6 35.2-60.3-34.3c-2.2-1.2-4.4-1.2-6.4 0s-2.9 3.4-2.9 5.6v68.8c0 2.2 1.2 4.4 2.9 5.6 1 0.5 2.2 1 3.4 1s2.2-0.5 2.9-1l60.3-34.3c2.2-1.2 3.4-3.4 3.4-5.6s-1.1-4.3-3.3-5.8z"></path><path id="loadingIcon" d="m61.184 36.167-48.73-27.719c-1.7779-0.96976-3.5558-0.96976-5.172 0-1.6163 0.96976-2.3436 2.7476-2.3436 4.5255v55.599c0 1.7779 0.96976 3.5558 2.3436 4.5255 0.80813 0.40407 1.7779 0.80813 2.7476 0.80813 0.96975 0 1.7779-0.40406 2.3436-0.80813l48.73-27.719c1.7779-0.96976 2.7476-2.7476 2.7476-4.5255s-0.88894-3.475-2.6668-4.6872z" fill="none"></path></svg></div><div class="svgImg warningIcon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 66.399998 66.399998" aria-hidden="true"><g><path d="M33.2 0C14.9 0 0 14.9 0 33.2c0 18.3 14.9 33.2 33.2 33.2 18.3 0 33.2-14.9 33.2-33.2C66.4 14.9 51.5 0 33.2 0zm0 59.4C18.7 59.4 7 47.6 7 33.2 7 18.7 18.8 7 33.2 7c14.4 0 26.2 11.8 26.2 26.2 0 14.4-11.8 26.2-26.2 26.2z"></path><path d="M33.1 45.6c-1.4 0-2.5.5-3.5 1.5-.9 1-1.4 2.2-1.4 3.6 0 1.6.5 2.8 1.5 3.8 1 .9 2.1 1.3 3.4 1.3 1.3 0 2.4-.5 3.4-1.4 1-.9 1.5-2.2 1.5-3.7 0-1.4-.5-2.6-1.4-3.6-.9-1-2.1-1.5-3.5-1.5zM33.3 12.4c-1.5 0-2.8.5-3.7 1.6-.9 1-1.4 2.4-1.4 4.2 0 1.1.1 2.9.2 5.6l.8 13.1c.2 1.8.4 3.2.9 4.1.5 1.2 1.5 1.8 2.9 1.8 1.3 0 2.3-.7 2.9-1.9.5-1 .7-2.3.9-4l1.1-13.4c.1-1.3.2-2.5.2-3.8 0-2.2-.3-3.9-.8-5.1-.5-1-1.6-2.2-4-2.2z"></path></g></svg></div>`).appendTo(this.queryBtn)

        this.updateQueryButton()

        buttons.appendTo(this.getWrapperElement())

        this.on("query", this.handleQuery)
        this.on("queryResponse", this.handleQueryResponse)
        this.on("queryAbort", this.handleQueryAbort)
    }

    handleQuery(editor, req) {
        editor.req = req
        editor.updateQueryButton()
    }
  
    handleQueryResponse(editor, res, duration) {
        editor.lastQueryDuration = duration
        editor.req = undefined
        editor.updateQueryButton()
    }
  
    handleQueryAbort(editor, req) {
        editor.req = undefined
        editor.updateQueryButton()
    }

    abortQuery() {
        if (this.req) {
            // this.req.abort(); TODO
            this.emit("queryAbort", this.req);
        }
    }

    updateQueryButton() {
        this.queryBtn.toggleClass("busy", !!this.req)
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
