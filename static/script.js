let csvData = [];

document.getElementById('csvFile').addEventListener('change', function (e) {
  const file = e.target.files[0];
  Papa.parse(file, {
    header: true,
    skipEmptyLines: true,
    complete: function(results) {
      csvData = results.data;
      alert("CSV loaded successfully!");
    }
  });
});

function findMatch() {
  const district = document.getElementById('district').value.trim().toLowerCase();
  const soilColor = document.getElementById('soilColor').value.trim().toLowerCase();
  const ph = parseFloat(document.getElementById('ph').value);
  const rainfall = parseFloat(document.getElementById('rainfall').value);
  const temp = parseFloat(document.getElementById('temp').value);

  const match = csvData.find(row => 
    row["District Name"]?.trim().toLowerCase() === district &&
    row["Soil Color"]?.trim().toLowerCase() === soilColor &&
    parseFloat(row["pH"]) === ph &&
    parseFloat(row["Rainfall (mm)"]) === rainfall &&
    parseFloat(row["Temperature (°C)"]) === temp
  );

  const output = document.getElementById('output');
  if (match) {
    const {
      ["District Name"]: _,
      ["Soil Color"]: __,
      ["pH"]: ___,
      ["Rainfall (mm)"]: ____,
      ["Temperature (°C)"]: _____,
      ...rest
    } = match;
    output.textContent = JSON.stringify(rest, null, 2);
  } else {
    output.textContent = "No match found.";
  }
}
