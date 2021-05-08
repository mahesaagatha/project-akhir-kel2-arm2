$(document).ready(function () {
  selesai();
});

var myArrayhvac = [];

function selesai() {
  setTimeout(function () {
    update();
    buildTablehvac(myArrayhvac);
    selesai();
  }, 2000);
}

//fungcion update
function update() {
  $.ajax({
    url: '/database',
    data: 'rvhvac',
    dataType: 'JSON',
    type: 'GET',
    success: function (data) {
      myArrayhvac = data.rvhvac;
      console.log(data);

      $('#result').html();
      $('#result').append(data.htmlresponse);
    },
  });
}

//motor----
function buildTablehvac(data) {
  var table = document.getElementById('myhvac');
  $('#myhvac').empty();

  for (var i = 0; i < data.length; i++) {
    var event_data = '';

    event_data += '<tr>';
    event_data += '<td>' + (i + 1) + '</td>';
    event_data += '<td>' + data[i].tanggal + '</td>';
    event_data += '<td>' + data[i].in_condensor + '</td>';
    event_data += '<td>' + data[i].out_condensor + '</td>';
    event_data += '<td>' + data[i].in_evaporator + '</td>';
    event_data += '<td>' + data[i].out_evaporator + '</td>';
    event_data += '<td>' + data[i].compressor + '</td>';
    event_data += '<td>' + data[i].room + '</td>';
    event_data += '</tr>';

    $('#myhvac').append(event_data);
  }
}
