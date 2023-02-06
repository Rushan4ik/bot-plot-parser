<?php
/*
 * Plugin Name: Аудиоплеер (recoded) с CSV-плейлистами (vds-dev.ru)
 * Description: Плагин для импорта плейлистов в формате .csv на сайт, и вставки в записи/страницы, recoded by Milana
 * Author URI:  nourl.com
 * Author:      Милана
 * Version:     2.0
 */

add_action('admin_menu', 'mt_add_pages');
function mt_add_pages() {
  add_management_page('Импорт плейлистов для аудиоплеера vds-dev ver 2', 'Импорт CSV-плейлистов v2', 8, __FILE__, 'mt_toplevel_page');
}
function mt_toplevel_page() {
  include("adm-import-playlists.html");
}

add_action( 'admin_enqueue_scripts', 'loadScript' );
function loadScript() {
  wp_register_script( 'vdsdev-beatportparser-script', plugins_url( 'assets/js/script.js', __FILE__ ) );
  wp_enqueue_script( 'vdsdev-beatportparser-script' );
}

add_action( 'wp_footer', 'vdsdev_parserbeatport_block_post_assets' );
function vdsdev_parserbeatport_block_post_assets(){
  wp_enqueue_script(
 		'vdsdev-parserbeatport-playlist-post-js',
		plugin_dir_url( __FILE__ ) . 'assets/js/vdsdev-parserbeatport-playlist-post.js',
		array( 'jquery', 'wp-mediaelement' ),
		filemtime( dirname( __FILE__ ) . '/assets/js/vdsdev-parserbeatport-playlist-post.js' )
	);
  wp_localize_script( 'vdsdev-parserbeatport-playlist-post-js', 'cc_ajax_object', array( 'ajax_url' => admin_url( 'admin-ajax.php' )));
	wp_enqueue_style(
		'vdsdev-parserbeatport-playlist-post-css',
		plugin_dir_url( __FILE__ ) . 'assets/css/vdsdev-parserbeatport-playlist-post.css',
		array( 'wp-mediaelement' ),
		filemtime( dirname( __FILE__ ) . '/assets/css/vdsdev-parserbeatport-playlist-post.css' )
	);
}

add_action( 'enqueue_block_editor_assets', 'vdsdev_parserbeatport_block_assets' );
function vdsdev_parserbeatport_block_assets(){
  wp_enqueue_script(
 		'vdsdev-parserbeatport-playlist-js',
		plugin_dir_url( __FILE__ ) . 'assets/js/vdsdev-parserbeatport-playlist.js',
		array( 'jquery', 'wp-blocks', 'wp-element', 'wp-editor', 'wp-i18n' ),
		filemtime( dirname( __FILE__ ) . '/assets/js/vdsdev-parserbeatport-playlist.js' )
	);
	wp_enqueue_style(
		'vdsdev-parserbeatport-playlist-css',
		plugin_dir_url( __FILE__ ) . 'assets/css/vdsdev-parserbeatport-playlist.css',
		array( 'wp-edit-blocks' ),
		filemtime( dirname( __FILE__ ) . '/assets/css/vdsdev-parserbeatport-playlist.css' )
	);
}

add_action('admin_enqueue_scripts', 'ajax_functions');
function ajax_functions()
{
?>
  <script type="text/javascript" >

    var vdsdevParsingSTate = false;
    var vdsdevParsingInterval;

    function writeMeSubmit(form)
    {
      if(jQuery('#filename')[0].files.length == 0)
      {
        alert("Выберите файл(ы)");
        return false;
      }
      var formData = new FormData();
      jQuery.each(jQuery('#filename')[0].files, function(i, file) {
        formData.append('filename[]', file);
      });
      formData.append('action', "vdsdev-parsebeatport_upload-tracklist");
      formData.append('_ajax_nonce', '<?php echo wp_create_nonce( 'ajax_writeMeSubmit_nonce' ); ?>');
      jQuery.ajax({
        url: ajaxurl,
        type: "POST",
        dataType : "json",
        processData: false,
        contentType: false,
        data: formData,
        success: function(data) {
          // alert(JSON.stringify(data));
          if(data.proc_files){
            var resdata = data.proc_files;
            var html = "<dl>";
            for (var key in resdata)
            {
              var sAdded = "Добавлено: " + resdata[key].added;
              var sUpdated = "Обновлено: " + resdata[key].updated;
              var sErrors = "Ошибки: " + resdata[key].errors;
              var dd = "<dd>" + sAdded + "</dd><dd>" + sUpdated + "</dd><dd>" + sErrors + "</dd>";
              html = html + "<dt>" + key + "</dt>" + dd;
            }
            html = html + "</dl>";
            html = html + "<button onclick='jQuery(&quot;#message_form&quot;).html(&quot;&quot;);'>Скрыть</button>";
            jQuery('#message_form').html('<p>' + html + '</p>');
            updateDataParse();
            // setTimeout(function() { jQuery('#message_form').html(' '); }, 10000);
          }else{
            jQuery('#message_form').html('<p>Файл не был загружен!<br>' + data.descr + '</p>');
            // setTimeout(function() { jQuery('#message_form').html(' '); }, 60000);
          }
        },
        error: function(w,q,e){
          alert(e);
        }
      });

      jQuery("#formfile")[0].reset();

      return false;
    }

    function updateDataParse()
    {
      jQuery.ajax({
        url: ajaxurl,
        type: "POST",
        dataType : "json",
        contentType: "application/x-www-form-urlencoded; charset=UTF-8",
        data: {
          action: "vdsdev-parsebeatport_update-data-parse",
          _ajax_nonce: '<?php //echo wp_create_nonce( 'ajax_writeMeSubmit_nonce' ); ?>'
        },
        success: function(data) {
          if(data) { duUpdateDataParse(data); }
        }
      });

      return false;
    }

    // function startParse()
    // {
    //   jQuery.ajax({
    //     url: ajaxurl,
    //     type: "POST",
    //     dataType : "json",
    //     contentType: "application/x-www-form-urlencoded; charset=UTF-8",
    //     data: {
    //       action: "vdsdev-parsebeatport_start-parse",
    //       _ajax_nonce: '<?php //echo wp_create_nonce( 'ajax_writeMeSubmit_nonce' ); ?>'
    //     },
    //     success: function(data) {
    //       if(!data)
    //       {
    //         setParsingState(false);
    //       }
    //       else {
    //         if(vdsdevParsingSTate) {  }
    //       }
    //     }
    //   });
    //
    //   return false;
    // }

    // function btnStartParse()
    // {
    //   if(vdsdevParsingSTate)
    //   {
    //     setParsingState(false);
    //   }
    //   else {
    //     setParsingState(true);
    //     vdsdevParsingInterval = setInterval(startParse, 1000);
    //   }
    // }

    // function setParsingState(state)
    // {
    //   vdsdevParsingSTate = state;
    //   if(vdsdevParsingSTate)
    //   {
    //     jQuery("#vdsdev-parsebutton").html("Остановить парс");
    //   }
    //   else {
    //     jQuery("#vdsdev-parsebutton").html("Парсить");
    //     clearInterval(vdsdevParsingInterval);
    //   }
    // }

    // function checkParseProc()
    // {
    //   jQuery.ajax({
    //     url: ajaxurl,
    //     type: "POST",
    //     dataType : "json",
    //     contentType: "application/x-www-form-urlencoded; charset=UTF-8",
    //     data: {
    //       action: "vdsdev-parsebeatport_check-parse-proc",
    //       _ajax_nonce: '<?php //echo wp_create_nonce( 'ajax_writeMeSubmit_nonce' ); ?>'
    //     },
    //     success: function(data) {
    //       if(!data) { alert(data); }
    //     }
    //   });
    //
    //   return false;
    // }

  </script>
<?php
}

register_activation_hook( __FILE__, 'plugin_activation' );
function plugin_activation()
{
  require_once("aux_functions.php");
  foreach(createTableDB() as $key => $value)
  {
    echo $key . " - " . $value;
  }
}

add_action('wp_ajax_vdsdev-parsebeatport_upload-tracklist', 'ajax_upload_tracklist');
function ajax_upload_tracklist()
{
  require_once("constant.php");
  require_once("aux_functions.php");
  global $wpdb;
  $arrRes["proc_files"] = [];

  //
  // $arrRes["proc_files"] = $_FILES;
  // echo json_encode($arrRes);
  // wp_die();

for($i = 0; $i < count($_FILES['filename']['name']); $i++)
{
    if (!empty($_FILES['filename']['tmp_name'][$i]))
    {
      $tmp_name = $_FILES['filename']['tmp_name'][$i];
      $file_name = $_FILES['filename']['name'][$i];
      $file_basename = pathinfo($file_name, PATHINFO_BASENAME);
      $handle_file = fopen($tmp_name, "r");
      $line = fgets($handle_file);
      $line = str_replace(array("\r", "\n"),"", $line);
      $CSV_col_indexes = str_getcsv($line, ";", '"', "\\");
      $CSV_col_indexes = array_flip($CSV_col_indexes);


      $arrRes["proc_files"][$file_basename]["added"] = 0;
      $arrRes["proc_files"][$file_basename]["updated"] = 0;
      $arrRes["proc_files"][$file_basename]["errors"] = 0;

      while ( ( $line = fgets($handle_file) ) !== FALSE ) {
        $line = str_replace(array("\r", "\n"),"", $line);
        $csv_data = str_getcsv($line, ";", '"', "\\");

        $pl_name = pathinfo($file_name, PATHINFO_FILENAME);
        $track['name'] = $csv_data[$CSV_col_indexes['str_search_track']];
        $track['url'] = $csv_data[$CSV_col_indexes['url_chosen_track']];

        $sql_table = $DB_tablename;

        $qsltrname = $track['name'];
        $sql_result = $wpdb->get_results("SELECT id FROM $sql_table WHERE name = '$qsltrname' AND playlist = '$pl_name'");
        if(!$sql_result)
        {
          $sql_data = array("name" => $track['name'], "playlist" => $pl_name, "url" => $track['url']);
          $sql_format = array("%s", "%s", "%s");

          $res = $wpdb->insert($sql_table, $sql_data, $sql_format);

          if($res)
          {
            $arrRes["proc_files"][$file_basename]["added"] += $res;
          }
          else {
            $arrRes["proc_files"][$file_basename]["errors"]++;
          }
        }
        else {
          $sql_data = array("url" => $track['url']);
          $sql_where = array("name" => $track['name'], "playlist" => $pl_name);
          $sql_data_format = array("%s");
          $sql_where_format = array("%s", "%s");

          $res = $wpdb->update($sql_table, $sql_data, $sql_where, $sql_data_format, $sql_where_format);

          if($res >= 0)
          {
            $arrRes["proc_files"][$file_basename]["updated"] += $res;
          }
          else {
            $arrRes["proc_files"][$file_basename]["errors"]++;
          }
        }

      }
    }
  }

  echo json_encode($arrRes);
  wp_die();

  // $arResult['ok'] = "N";
  // $arResult['descr'] = "Не удалось прочитать файл!";

  // if (!empty($_FILES['filename']['tmp_name']))
  // {
  //   $arResult['ok'] = "Y";
  //   $arResult['descr'] = "";
  //
  //   // $lt_array = file($_FILES['filename']['tmp_name']);
  //   $handle_file = fopen($_FILES['filename']['tmp_name'], "r")
  //   // $counter_writed = 0;
  //   // $counter_founded = 0;
  //
  //   // $CSV_col_names = array_flip(fgets($handle_file))
  //
  //   for($i=1; $i < count($lt_array); $i++)
  //   {
  //     // $tr_name = cleanTrackName($lt_array[$i]);
  //
  //     // if(strlen($tr_name))
  //     // {
  //     //   $pl_name = pathinfo($_FILES['filename']['name'], PATHINFO_FILENAME);
  //     //
  //     //   $sql_table = $DB_tablename;
  //     //   $sql_data = array("name" => $tr_name, "playlist" => $pl_name);
  //     //   $sql_format = array("%s", "%s");
  //     //
  //     //   $sql_result = $wpdb->get_results("SELECT id FROM $sql_table WHERE name = '$tr_name' AND playlist = '$pl_name'");
  //     //   if(!$sql_result)
  //     //   {
  //     //     $wpdb->insert($sql_table, $sql_data, $sql_format);
  //     //     $counter_writed++;
  //     //   }
  //     //   else {
  //     //     $counter_founded++;
  //     //   }
  //     // }
  //   }
  // }
}

add_action('wp_ajax_vdsdev-parsebeatport_update-data-parse', 'ajax_update_data_parse');
function ajax_update_data_parse()
{
  require_once("aux_functions.php");
  $playlists = getPlaylistsFromDB();

  $arResult = array();
  foreach($playlists as $pl)
  {
    $arResult[$pl]['total'] = getCountRows($pl);
    $arResult[$pl]['whithurl'] = getCountRowsWhithUrl($pl);
    $arResult[$pl]['noneurl'] = getCountRowsNoneUrl($pl);
  }

  echo json_encode($arResult);
  wp_die();
}

add_action('wp_ajax_vdsdev-parsebeatport_remove-playlist', 'ajax_remove_playlist');
function ajax_remove_playlist()
{
  require_once("aux_functions.php");

  $arResult['res'] = removePlaylist($_POST['playlistname']);
  echo json_encode($arResult);
  wp_die();
}

add_action('wp_ajax_vdsdev-parsebeatport_start-parse', 'ajax_start_parse');
function ajax_start_parse()
{
  require_once("aux_functions.php");

  $res = false;

  $row = getRowWithoutUrl();
  if($row)
  {
    $tr_url = getTrackUrl($row->name);
    $result = setTrackUrl($row->id, $tr_url);
    $res = true;
  }

  echo json_encode($res);
  wp_die();
}


add_action('wp_ajax_vdsdev-parsebeatport_check-parse-proc', 'ajax_check_parse_proc');
function ajax_check_parse_proc()
{
  require_once("aux_functions.php");

  $pid = getParsePid();
  if($pid)
  {
    $arResult['pgid'] = posix_getpgid(getParsePid());
  }

  $arResult['pid'] = $pid;
  echo json_encode($arResult);
  wp_die();
}

add_action('wp_ajax_vdsdev-parsebeatport_get-playlist', 'ajax_get_playlist');
add_action('wp_ajax_nopriv_vdsdev-parsebeatport_get-playlist', 'ajax_get_playlist');
function ajax_get_playlist()
{
  require_once("aux_functions.php");
  $arResult = getTracksForPlaylist($_POST['playlist']);

  echo json_encode($arResult);
  wp_die();
}

?>
