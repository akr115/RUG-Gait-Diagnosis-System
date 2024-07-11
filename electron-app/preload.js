const { exec } = require("child_process");

var resultBack = exec(`python3 backend/app.py`);
console.log(resultBack);
if(resultBack.exitCode == 0 || resultBack.exitCode == null) {
  console.log("success");
  var resultFront = exec(`npm front-end start`);
  console.log(resultFront);
}

console.log("this file was called");