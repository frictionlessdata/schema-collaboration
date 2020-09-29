const axios = require('axios')
const React = require('react')
const { connect } = require('react-redux')

const onSaveToServer = require('./SchemaCollaborationSaveToServer').onSaveToServer
const getParameterFromUrlByName = require('./SchemaCollaborationUtils').getParameterFromUrlByName

// Pure components

function EditorButtonsPure({
  encodedDescriptor,

  // Handlers
  onUploadChange,
  onValidateClick,

  onLoadFromServer,
}) {
  return (
    <div>
      {/* Upload */}
      <label
        className="btn btn-lg btn-success"
        title="Upload a data package from your local drive"
        htmlFor="load-descriptor"
      >
        <input
          type="file"
          id="load-descriptor"
          value=""
          style={{ display: 'none' }}
          onChange={onUploadChange}
        />
        Upload
      </label>

      {/* Validate */}
      <button
        className="btn btn-lg btn-info"
        title="Validate the data package verifying its metadata"
        onClick={onValidateClick}
      >
        Validate
      </button>

      {/* Download */}
      <a
        className="btn btn-lg btn-success"
        href={`data: ${encodedDescriptor}`}
        download="datapackage.json"
        title="Download the data package to your local drive"
      >
        Download
      </a>

      {/* Save to server */}
      <button
        className="btn btn-lg btn-info"
        title="Save current schema to the server"
        onClick={() => onSaveToServer(`${decodeURIComponent(encodedDescriptor)}`)}
      >
        Save to server
      </button>

      {/* Load from server */}
      <button
        className="btn btn-lg btn-info"
        title="Load from the server"
        onClick={onLoadFromServer}
      >
        Load from the server
      </button>
    </div>
  )
}

// Handlers

const mapDispatchToProps = (dispatch) => ({
  onUploadChange: (ev) => {
    const reader = new window.FileReader()
    reader.readAsText(ev.target.files[0])
    reader.onload = () => {
      dispatch({
        type: 'UPLOAD_PACKAGE',
        payload: JSON.parse(reader.result),
      })
    }
  },

  onValidateClick: () => {
    dispatch({
      type: 'VALIDATE_PACKAGE',
    })
  },

  onLoadFromServer: () => {
    const uuid = getParameterFromUrlByName('load')
    axios.get('/api/datapackage/' + uuid + '/').then((resp) => {
      console.log(resp.data)
      dispatch({
        type: 'UPLOAD_PACKAGE',
        payload: resp.data,
      })
    })
  },
})

// Wrappers

const EditorButtons = connect(null, mapDispatchToProps)(EditorButtonsPure)

// System

module.exports = {
  // Public
  EditorButtons,

  // Private
  EditorButtonsPure,
}
