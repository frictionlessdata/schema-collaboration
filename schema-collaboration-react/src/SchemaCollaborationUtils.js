export function getParameterFromUrlByName(name, url) {
  // Copied and slightly changed from https://stackoverflow.com/a/901144/9294284
  // (it seems to be CC-BY-SA 4.0, I might replace this after prototyping)
  if (!url) url = window.location.href

  name = name.replace(/[[\]]/g, '\\$&')
  var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)')
  var results = regex.exec(url)
  if (!results) return null
  if (!results[2]) return ''
  return decodeURIComponent(results[2].replace(/\+/g, ' '))
}

export function onExitApplication() {
  window.location.href = getParameterFromUrlByName('source', window.location)
}