document.addEventListener("DOMContentLoaded", () => {
  const editor = new Yasqe(document.getElementById("yasqe"), {
    requestConfig: {
      endpoint: "/api/sparql",
      method: "POST",
    },
    sparql: { showQueryButton: true },
  })

  const yasr = new Yasr(document.getElementById("yasr"), {
    prefixes: editor.getPrefixesFromQuery,
  })

  editor.on("queryResponse", (instance, res) => yasr.setResponse(res))

  $("#examples").on("change", e => {
    editor.setValue(e.target.value)
    if (e.target.value != "") editor.query()
  })

  if (window.location.hash?.startsWith("#query=")) {
    editor.query()
  }
})
