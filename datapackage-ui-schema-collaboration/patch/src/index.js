require('./styles/base.css')
require('regenerator-runtime/runtime')
const { render } = require('./render')
const { EditorSchema } = require('./components/EditorSchema')
const { EditorPackage } = require('./components/EditorPackage')
const { EditorSchemaCollaborationButtons } = require('./components/EditorSchemaCollaborationButtons')

// Module API

module.exports = {
  render,
  EditorSchema,
  EditorPackage,
  EditorSchemaCollaborationButtons,
}

