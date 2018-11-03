
function buildGauge(frequency){

var level = frequency;

// Trig to calc meter point
var degrees = 10 - level,
     radius = .5;
var radians = degrees * Math.PI / 180;
var x = radius * Math.cos(radians);
var y = radius * Math.sin(radians);

// Path: may have to change to create a better triangle
var mainPath = 'M -.0 -0.025 L .0 0.025 L ',
     pathX = String(x),
     space = ' ',
     pathY = String(y),
     pathEnd = ' Z';
var path = mainPath.concat(pathX,space,pathY,pathEnd);
console.log("path " + path + "x " + pathX + " y " + pathY)
var data = [{ type: 'scatter',
   x: [0], y:[0],
    marker: {size: 28, color:'850000'},
    showlegend: false,
    name: 'frequency',
    text: level,
    hoverinfo: 'text+name'},
  { values: [50/9, 50/9, 50/9, 50/9, 50/9, 50/9,50/9,50/9,50/9, 50],
  rotation: 90,
  text: ['8-9', '7-8', '6-7', '5-6','4-5', '3-4','2-3','1-2','0-1', ''],
  textinfo: 'text',
  textposition:'inside',
  marker: {colors:['rgba(14, 127, 0, .5)', 'rgba(110, 154, 22, .5)',
                         'rgba(170, 202, 42, .5)', 'rgba(202, 209, 95, .5)',
                         'rgba(210, 206, 145, .5)', 'rgba(232, 226, 202, .5)','rgba(14, 127, 0, .5)', 'rgba(110, 154, 22, .5)',
                         'rgba(170, 202, 42, .5)',
                         'rgba(255, 255, 255, 0)']},
  labels: ['8-9', '7-8', '6-7', '5-6','4-5', '3-4','2-3','1-2','0-1', ''],
  hoverinfo: 'label',
  hole: .5,
  type: 'pie',
  showlegend: false
}];

var layout = {
  shapes:[{
      type: 'path',
      path: path,
      fillcolor: '850000',
      line: {
        color: '850000'
      }
    }],
  title: 'Frequency 0-10',
  height: 600,
  width: 600,
  xaxis: {zeroline:false, showticklabels:false,
             showgrid: false, range: [-1, 1]},
  yaxis: {zeroline:false, showticklabels:false,
             showgrid: false, range: [-1, 1]}
};

Plotly.newPlot('gauge', data, layout);

}


function buildMetadata(sample) {

    // BONUS: Build the Gauge Chart
    d3.json(`/metadata/${sample}`).then((data) => {
      d3.select("#sample-metadata").html("");

      Object.entries(data).forEach(([k,v]) => {
        d3.select("#sample-metadata")
          .append("p").style("text-size:","6px").text(k + ":" + v)
          .append("br")
      });
      buildGauge(data.WFREQ);

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
