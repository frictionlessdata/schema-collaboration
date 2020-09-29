const axios = require('axios')
const getParameterFromUrlByName = require('./SchemaCollaborationUtils').getParameterFromUrlByName

export function onSaveToServer(data) {
  // Example found in https://codereviewvideos.com/course/symfony-3-with-reactjs-and-angular/video/react-create-post
  const uuid = getParameterFromUrlByName('load')

  let url = ''
  let method = ''
  // eslint-disable-next-line no-undef

  if (uuid === null) {
    url = '/api/datapackage/'
    method = 'POST'
  } else {
    url = '/api/datapackage/' + uuid + '/'
    method = 'PUT'
  }

  return axios(url, {
    method: method,
    data: data,
  })
    .then((res) => {
      console.log(res)
      // TODO: move this from here: the user of this function should do this
      // eslint-disable-next-line no-undef
      alert('Saved. Your UUID: ' + res.data.uuid)
      return res
    })
    .catch((err) => err)
}
