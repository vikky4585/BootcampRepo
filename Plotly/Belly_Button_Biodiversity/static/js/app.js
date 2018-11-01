function buildMetadata(sample) {

  // @TODO: Complete the following function that builds the metadata panel

  // Use `d3.json` to fetch the metadata for a sample
    // Use d3 to select the panel with id of `#sample-metadata`

    // Use `.html("") to clear any existing metadata

    // Use `Object.entries` to add each key and value pair to the panel
    // Hint: Inside the loop, you will need to use d3 to append new
    // tags for each key-value in the metadata.

    // BONUS: Build the Gauge Chart
    // buildGauge(data.WFREQ);
}

function convert2ObjList(data){
  var dataObjList = []
  for(var x =0; x < data["otu_ids"].length; x++){
    var dataObj = {};
    dataObj["otu_id"] = data["otu_ids"][x];
    dataObj["sample_value"] = data["sample_values"][x];
    dataObj["otu_label"] = data["otu_labels"][x];
    dataObjList.push(dataObj);

  }
  return dataObjList;
}

function buildCharts(sample) {



  d3.json(`/samples/${sample}`).then((data) => {

    var dataList = convert2ObjList(data);
    var otuObj = dataList.sort((a,b) => b["sample_value"] - a["sample_value"]).splice(0,10);

    var pieVal = otuObj.map(d => d["sample_value"]);

    //pie
    var d = [
      {
        values: otuObj.map(d => d["sample_value"]),
        labels: otuObj.map(d => d["otu_id"]),
        type: "pie"
      }
    ]

    Plotly.newPlot("pie",d)
  }
  
  );

    // @TODO: Build a Bubble Chart using the sample data

    // @TODO: Build a Pie Chart
    // HINT: You will need to use slice() to grab the top 10 sample_values,
    // otu_ids, and labels (10 each).
}

function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");

  // Use the list of sample names to populate the select options
  d3.json("/names").then((sampleNames) => {
    sampleNames.forEach((sample) => {
      selector
        .append("option")
        .text(sample)
        .property("value", sample);
    });

    // Use the first sample from the list to build the initial plots
    const firstSample = sampleNames[0];
    buildCharts(firstSample);
    buildMetadata(firstSample);
  });
}

function optionChanged(newSample) {
  // Fetch new data each time a new sample is selected
  console.log("on change")
  buildCharts(newSample);
  buildMetadata(newSample);
}

// Initialize the dashboard
init();
