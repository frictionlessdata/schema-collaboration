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

export function onExitApplication(data) {
  let destinationUrl = getParameterFromUrlByName('source', window.location)

  if (window.last_saved_schema === undefined || // it has not been saved yet... we don't know if there are changes but just in case
    data !== window.last_saved_schema)          // data now is different to the last saved data
  {
      if (window.confirm('If you continue you will lose the changes in this session')) {
          window.location.href = destinationUrl
      }
  }
  else {
      window.location.href = destinationUrl
  }
}