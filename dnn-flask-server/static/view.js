$(function () {
  session_id = document.location.pathname.replace('/view/', '')
  accuracy = []
  hidden_layers = []
  training_time = []
  $.get('/api/'+session_id, function (data) {
    data = JSON.parse(data)
    for (item in data) {
      accuracy.push(data[item].result)
      training_time.push(data[item].training_time)
      hidden_layers.push(data[item].hidden_size)
    }

    var scatter_trace = {
      x: hidden_layers,
      y: accuracy,
      mode: 'markers',
      type: 'scatter'
    };

    var scatter_layout = {
      title:'Hidden Layers vs. Accuracy',
      xaxis: {
        title: 'Hidden Layers'
      },
      yaxis: {
        title: 'Accuracy'
      }
    };

    scatter_data = [scatter_trace]

	  Plotly.newPlot('scatter-plot', scatter_data, scatter_layout);

    var scatter_trace = {
      x: hidden_layers,
      y: training_time,
      mode: 'markers',
      type: 'scatter'
    };

    var scatter_layout = {
      title:'Hidden Layers vs. Training Time',
      xaxis: {
        title: 'Hidden Layers'
      },
      yaxis: {
        title: 'Training Time'
      }
    };

    scatter_data = [scatter_trace]

	  Plotly.newPlot('hlvtt', scatter_data, scatter_layout);
  })

  $.get('/fft/'+session_id, function (data) {
    data = JSON.parse(data)
    ffts = []
    indicies = []
    for (item in data) {
      ffts.push(data[item])
      indicies.push(parseInt(item))
    }

    var scatter_trace = {
      x: indicies,
      y: ffts,
      mode: 'markers',
      type: 'scatter'
    };

    var scatter_layout = {
      title:'FFT Analysis',
      xaxis: {
        title: 'Frequency'
      },
      yaxis: {
        title: 'Magnitude'
      }
    };

    scatter_data = [scatter_trace]

	  Plotly.newPlot('fft', scatter_data, scatter_layout);
  })
})
