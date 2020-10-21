import "./index.css";
import 'react-toastify/dist/ReactToastify.css';
import datapackageUI from "datapackage-ui/lib";

// import EditorSchemaCollaborationButtons from "./EditorSchemaCollaborationButtons";
const { EditorSchemaCollaborationButtons } = require('./EditorSchemaCollaborationButtons')

console.log(EditorSchemaCollaborationButtons)

datapackageUI.render(
  datapackageUI.EditorPackage,
  {
    descriptor: {},
    Buttons: EditorSchemaCollaborationButtons
  },
  document.getElementById("root")
);
