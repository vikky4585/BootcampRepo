function buildMetadata(sample) {

    // BONUS: Build the Gauge Chart
    // buildGauge(data.WFREQ);
    d3.json(`/metadata/${sample}`).then((data) => {
      d3.select("#sample-metadata").html("")

      Object.entries(data).forEach(([k,v]) => {
        console.log(k + ":" + v);
        d3.select("#sample-metadata")
          .append("p").style("text-size:","6px").text(k + ":" + v)
          .append("br")
      })
    });
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
    var piedata = [
      {
        values: otuObj.map(d => d["sample_value"]),
        labels: otuObj.map(d => d["otu_id"]),
        type: "pie"
      }
    ]

    Plotly.newPlot("pie",piedata);

    var trace = {
      x: otuObj.map(d => d["otu_id"]),
      y: otuObj.map(d => d["sample_value"]),
      mode: 'markers',
      marker: {
        size: otuObj.map(d => d["sample_value"]),
        color: otuObj.map(d => d["otu_id"])
      }

    }
    Plotly.newPlot("bubble",[trace]);


  }
  
  );


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
