const axios = require('axios')
const { toast } = require('react-toastify')

const getParameterFromUrlByName = require('./SchemaCollaborationUtils').getParameterFromUrlByName

export function onSaveToServer(data) {
  // Example found in https://codereviewvideos.com/course/symfony-3-with-reactjs-and-angular/video/react-create-post
  const uuid = getParameterFromUrlByName('load')

  let url = '/api/datapackage/' + uuid + '/'
  let method = 'PUT'

  return axios(url, {
    method: method,
    data: data,
  })
    .then((res) => {
      // TODO: move this from here: the user of this function should do this
      // eslint-disable-next-line no-undef
      toast.info('Saved! UUID: ' + res.data.uuid, {
        className: 'toast-info'
      })
      return res
    })
    .catch((err) => err)
}
