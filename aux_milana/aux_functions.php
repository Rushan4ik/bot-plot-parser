<?php

function createTableDB()
{
  require("constant.php");
  require_once(ABSPATH . 'wp-admin/includes/upgrade.php');

  $result = Array();
  $table_name = $DB_tablename;
  if($wpdb->get_var("show tables like '$table_name'") != $table_name) {
    $sql = "CREATE TABLE " . $table_name . " (
  	  id mediumint(9) NOT NULL AUTO_INCREMENT,
  	  name tinytext NOT NULL,
  	  playlist text NOT NULL,
  	  url VARCHAR(255),
  	  UNIQUE KEY id (id)
  	);";

    $result[$table_name] = dbDelta($sql);
  }
  $table_name = $DB_tablename_opt;
  if($wpdb->get_var("show tables like '$table_name'") != $table_name) {
    $sql = "CREATE TABLE " . $table_name . " (
  	  name VARCHAR(10) NOT NULL,
      value VARCHAR(20),
  	  PRIMARY KEY (name)
  	);";

    $result[$table_name] = dbDelta($sql);

    $sql_data = array("name" => "parsepid");
    $sql_format = array("%s");
    $wpdb->insert($DB_tablename_opt, $sql_data, $sql_format);
  }

  return $result;
}

function getPlaylistsFromDB()
{
  require("constant.php");

  $sql_result = $wpdb->get_results("SELECT DISTINCT playlist FROM $DB_tablename ORDER BY id DESC");

  $playlists = array();
  foreach($sql_result as $pl)
  {
    $playlists[] = $pl->playlist;
  }

  return $playlists;
}

function getCountRows($playlistname)
{
  require("constant.php");

  return $sql_result = $wpdb->get_var("SELECT COUNT(*) FROM $DB_tablename WHERE playlist = '$playlistname'");
}

function getCountRowsWhithUrl($playlistname)
{
  require("constant.php");

  return $wpdb->get_var("SELECT COUNT(*) FROM $DB_tablename WHERE playlist = '$playlistname' AND url IS NOT NULL AND url != 'NONE'");
}

function getCountRowsNoneUrl($playlistname)
{
  require("constant.php");

  return $wpdb->get_var("SELECT COUNT(*) FROM $DB_tablename WHERE playlist = '$playlistname' AND url = 'NONE'");
}

function getRowWithoutUrl()
{
  require("constant.php");

  return $wpdb->get_row("SELECT id, name FROM $DB_tablename WHERE url IS NULL");
}

function removePlaylist($playlist)
{
  require("constant.php");

  return $wpdb->delete($DB_tablename, array('playlist' => $playlist), array('%s'));
}

function getTracksForPlaylist($playlist)
{
  require("constant.php");

  $sql_result = $wpdb->get_results("SELECT name, url FROM $DB_tablename WHERE playlist = '$playlist'");// AND url != 'NONE' AND url IS NOT NULL");

  return $sql_result;

}

// function getTrackUrl($traname)
// {
//   require("constant.php");
//
//   $trackName = $traname;
//
//   $traname = "https://www.beatport.com/search?q=" . urlencode($traname);
//   $crlsite = curl_init($traname);
//
//   curl_setopt($crlsite, CURLOPT_RETURNTRANSFER, true);
//
//   $crlresult = curl_exec($crlsite);
//
//   if(curl_error($crlsite)) {
//     echo "error" . curl_error($crlsite);
//   }
//
//   curl_close($crlsite);
//
//   $doc = new DOMDocument();
//   $doc->validateOnParse = false;
//   libxml_use_internal_errors(true);
//   $doc->loadHTML($crlresult);
//   libxml_clear_errors();
//
//   $string = $doc->getElementById('data-objects')->nodeValue;
//   $string = substr($string, strpos($string, "window.Playables = ")+19);
//   $string = substr($string, 0, strpos($string, "]};")+2);
//
//   $arr = json_decode($string);
//
//   if(count($arr->tracks))
//   {
//     // // OLD
//     // if(count($arr->tracks[0]->preview->mp4->url))
//     // {
//     //   return $arr->tracks[0]->preview->mp4->url;
//     // }
//     // else {
//     //   return $arr->tracks[0]->preview->mp3->url;
//     // }
//     // // OLD end
//
//     $current_track = Array("url" => "NONE", "symb" => -50);
//
//     foreach ($arr->tracks as $track) {
//       if($track->component == "Search Results - Tracks")
//       {
//         $symbols_comp = 0;
//         $perc = 0;
//         $levensht = 0;
//         foreach ($track->artists as $artist) {
//           // $symbols_comp += similar_text($traname, $artist->name);
//           // similar_text($trackName, $artist->name,$perc);
//           // $symbols_comp += $perc;
//           $levensht += levenshtein($trackName, $artist->name, 5, 5, 1);
//         }
//         // $symbols_comp += similar_text($traname, $track->name);
//         similar_text($trackName, $track->name,$perc);
//         //$symbols_comp += $perc;
//         $symbols_comp += $perc / (levenshtein($trackName, $track->name, 5, 5, 1) + 0.0000001);
//         // $symbols_comp += similar_text($traname, $track->mix);
//         similar_text($trackName, $track->mix,$perc);
//         $symbols_comp += $perc;
//
//         //$levensht = levenshtein($trackName, $artist->name, 5, 5, 1);
//         $symbols_comp = $symbols_comp - $levensht;
//
//         if($current_track['symb'] < $symbols_comp) {
//           if(count($track->preview->mp4->url))
//           {
//             $current_track['url'] = $track->preview->mp4->url;
//           }
//           else {
//             $current_track['url'] = $track->preview->mp3->url;
//           }
//           // $current_track['url'] = $track->preview->mp3->url;
//           $current_track['symb'] = $symbols_comp;
//         }
//       }
//     }
//
//     return $current_track['url'];
//   }
//   else {
//     return "NONE";
//   }
// }
//
// function cleanTrackName($trname)
// {
//   // $vars = explode(".", $trname);
//   //
//   // if(is_numeric($vars[0]))
//   // {
//   //   $trname = $vars[1];
//   // }
//   $trname = str_replace(array("\r", "\n"), "", $trname); //"\"", "'",
//   $trname = trim($trname);
//
//   return $trname;
// }

// function setTrackUrl($id, $url)
// {
//   require("constant.php");
//
//   $sql_data = array("url" => $url);
//   $sql_where = array("id" => $id);
//   $sql_format = array("%s");
//   $sql_where_format = array("%d");
//   return $wpdb->update($DB_tablename, $sql_data, $sql_where, $sql_format, $sql_where_format);
// }
//
// function setParsePid($pid)
// {
//   require("constant.php");
//
//   $sql_data = array("value" => $pid);
//   $sql_where = array("name" => "parsepid");
//   $sql_format = array("%d");
//   $sql_where_format = array("%s");
//
//   return $wpdb->update($DB_tablename_opt, $sql_data, $sql_where, $sql_format, $sql_where_format);
// }
//
// function getParsePid()
// {
//   require("constant.php");
//
//   return $wpdb->get_var("SELECT value FROM $DB_tablename_opt WHERE name = 'parsepid'");
//
//   // $idmem = $wpdb->get_var("SELECT value FROM $DB_tablename_opt WHERE name = 'parsepid'");
//   //
//   // if(!strlen($idmem)
//   // {
//   //   return false;
//   // }
//   //
//   // // $systemid = 864; // Системный идентификатор сегмента общей памяти
//   // $mode = "a"; // Режим доступа
//   // $permissions = 0755; // Разрешения для сегмента общей памяти
//   // $size = 1024; // Размер сегмента в байтах
//   //
//   // $shmid = shmop_open($SHM_key, $mode, $permissions, $size);
//   //
//   // if(!$shmid)
//   // {
//   //   return false;
//   // }
//   //
//   // $pid = shmop_read($shmid, 0, shmop_size($shmid));
//   //
//   // shmop_close($shmid);
//   //
//   // if(!strlen($pid))
//   // {
//   //   return false;
//   // }
//   //
//   // return $pid;
// }
?>
