
function doUpdateListOfTracklists(data)
{
  jQuery('#vdsdev-list-of-tracklists').html('');
  for(i in data)
  {

    var delbut = "<button onClick='deleteFile(&quot;" + i + "&quot;)'>Удалить</button>";

    var noneurls = "";
    if(data[i].noneurls)
    {
      noneurls = ", Ненайденных ссылок: " + data[i].noneurls;
    }

    var status = "";
    if(data[i].status == 'Y')
    {
      status = "Парс завершен";
    }
    else if(data[i].status == 'M')
    {
      status = "Парс запущен";
    }
    else if(data[i].status == 'N')
    {
        status = "<button onClick='startParse(&quot;" + i + "&quot;)'>Парсить</button>";
    }
    else {
      status = data[i].status;
    }
    jQuery('#vdsdev-list-of-tracklists').append('<li>' + i + " - " + delbut + status + noneurls + '</li>');
  };
}

function duUpdateDataParse(data)
{
  jQuery('#vdsdev-data-parse').html('<tr><th>Плейлист</th><th>Всего треков</th><th>URL найден</th><th>URL не найден</th><th>Нужно парсить</th>');
  for(i in data)
  {
    var filename = "<b>" + i + "</b>";
    var total = data[i]['total'];
    var whithurl = data[i]['whithurl'];
    var noneurl = data[i]['noneurl'];

    jQuery('#vdsdev-data-parse').append('<tr><td><button onClick="removePlayList(&#39;' + i + '&#39;)">Удалить</button> <button onclick="copyHTMLToClipBoard(&#39;' + i + '&#39;)">Копировать</button> ' + filename + "</td><td>" + total + "</td><td>" + whithurl + "</td><td>" + noneurl + '</td><td>' + (parseInt(total, 10)-parseInt(whithurl, 10)-parseInt(noneurl, 10)) + '</td></tr>');
  };
}

function copyHTMLToClipBoard(str)
{

  str = '<div class="wp-block-vdsdev-parse-beatport-vdsdev-parserbeatport-playlist" playlist="' + str + '"></div>';

  let tmp   = document.createElement('INPUT'), // Создаём новый текстовой input
  focus = document.activeElement; // Получаем ссылку на элемент в фокусе (чтобы не терять фокус)

  tmp.value = str; // Временному input вставляем текст для копирования

  document.body.appendChild(tmp); // Вставляем input в DOM
  tmp.select(); // Выделяем весь текст в input
  document.execCommand('copy'); // Магия! Копирует в буфер выделенный текст (см. команду выше)
  document.body.removeChild(tmp); // Удаляем временный input
  focus.focus(); // Возвращаем фокус туда, где был
}

function removePlayList(plname)
{
  // var question = confirm("Вы точно хотите удалить плейлист " + plname + "?");
  if(confirm("Вы точно хотите удалить плейлист " + plname + "?"))
  {
    jQuery.ajax({
      url: ajaxurl,
      type: "POST",
      dataType : "json",
      contentType: "application/x-www-form-urlencoded; charset=UTF-8",
      data: {
        action: "vdsdev-parsebeatport_remove-playlist",
        // _ajax_nonce: '<?php //echo wp_create_nonce( 'ajax_writeMeSubmit_nonce' ); ?>',
        playlistname: plname,
      },
      success: function(data) {
        if(data) { alert("Удалено " + data['res'] + " треков"); }
      }
    });
  }
}

function deleteFile(filename)
{
  var formData = new FormData();
  formData.append('filename', filename);
  jQuery.ajax({
    url: "deletefile.php",
    type: "POST",
    dataType : "json",
    cache: false,
    contentType: false,
    processData: false,
    data: formData,
    success: function(data) {}
  });

  return false;
}

// function startParse(filename)
// {
//   var formData = new FormData();
//   formData.append('filename', filename);
//   jQuery.ajax({
//     url: "parser.php",
//     type: "POST",
//     dataType : "json",
//     cache: false,
//     contentType: false,
//     processData: false,
//     data: formData,
//     success: function(data) {}
//   });
//
//   return false;
// }

function test()
{
  alert("test");
}
