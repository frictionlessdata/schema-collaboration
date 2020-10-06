import React from "react";
import "./index.css";
import datapackageUI from "datapackage-ui/lib";

function Buttons() {
  return <div>test</div>;
}

datapackageUI.render(
  datapackageUI.EditorPackage,
  {
    descriptor: {},
    Buttons: Buttons,
  },
  document.getElementById("root")
);
