var data = {}
$(function () {
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

  function updateSessionStatus(session_id) {
    $.get("api/"+session_id, function( data ) {
      json = JSON.parse(data)
      console.log(json)
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
        si = data.session_id
        $('#session_id').text(si);
        console.log("Session id:", si)
        setInterval(updateSessionStatus(si), 1000)
      }
    });
  })
})
