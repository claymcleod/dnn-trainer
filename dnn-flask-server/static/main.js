var data = {}
$(function () {
  var session_id;

  function handleFileSelect(evt) {
    var file = evt.target.files[0];
    Papa.parse(file, {
       complete: function(results) {
         data["data"] = results.data;
         var $active = $('.wizard .nav-tabs li.active');
         $active.next().removeClass('disabled');
         nextTab($active);

         var s = $("<select id=\"labelselect\" name=\"selectName\" />");
         for(var val in results.data[0]) {
           $("<option />", {value: results.data[0][val].toString(), text: results.data[0][val].toString()}).appendTo(s);
         }

         $('#label').append(s)
        }
    });
  }

  function updateSessionStatus() {
    $.get("api/"+session_id, function( data ) {
      json = JSON.parse(data)
      parsed_number = json.length
      percent = (parsed_number / 1000.0) * 100.0
      console.log(Math.round(percent))
      $('#progressbar').width(Math.round(percent).toString()+"%")
      if (percent >= 100.0) {
        var $active = $('.wizard .nav-tabs li.active');
        $active.next().removeClass('disabled');
        nextTab($active);
      }
    })
  }

  $('#file').change(function (evt) {
    handleFileSelect(evt)
  })

  $('#start').click(function () {
    data["label"] = $('#labelselect').val()
    $.ajax({
      data: JSON.stringify(data),
      type: 'post',
      contentType: "application/json; charset=utf-8",
      url: "/start",
      success: function(data) {
        session_id = data.session_id
        $('#session_id').text(session_id);
        $('#results_link').attr('href','/view/'+session_id);
        console.log("Session id:", session_id)
        setInterval(updateSessionStatus, 1000)
      }
    });
  })
})
