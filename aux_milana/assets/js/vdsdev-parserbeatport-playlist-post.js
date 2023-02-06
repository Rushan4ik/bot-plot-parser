Playlist = function(elemInput, elemplayerwraper, playercontrols, elemplayer, ajaxObj) {
  this.list = this.inputListFromAJAXObject(ajaxObj);
  this.current = 0;
  this.playing = false;
  this.repeatmode = 0;
  this.volumeStep = 0.05;
  this.curtimeStep = 5;
  this.elements = {
    inputThis: elemInput,
    playlist: this.createPlaylistElement(elemInput),
    tracks: Array(),
    playerWraper: elemplayerwraper,
    playerElem: elemplayer,
    playerControls: playercontrols,
    nameTrackInPlayer: null
  };
  this.classes = {
    currentTrack: "current",
    statPlay: "play",
    statPause: "pause",
    btnPlayPause: "btn-play-pause",
    btnNext: "btn-next",
    btnPrev: "btn-prev"
  };
  this.symbols = {
    play: '',//"►",
    pause: '',//"⎪⎪",//"⏸",//"⎪⎪",
    next: '',//"►►",
    prev: ''//"◄◄"
  };
  this.controls = {
    playpause: null,
    next: null,
    prev: null
  };
  this.player = this.createPlayer(elemplayer);

  this.createTrackElements();
  this.createButtonElements();
  this.setCurrentTrack(0);

  this.elements.playerElem.bind("ended", this.actionNext.bind(this));
};

Playlist.prototype.createPlayer = function(player_element) {
  var outval;
  player_element.mediaelementplayer({
    defaultAudioWidth: "100%",
    defaultAudioHeight: "50px",
    startVolume: 1,
    enableKeyboard: false,
    success: function(player, node) {
      outval = player;
    }
  });

  var blockTrackName = jQuery("<div>", {
    class: "vdsdev-audioplayer-trackname-inner-mediaplayer"
  });
  jQuery("#vdsdev-audioplayer-wraper > .mejs-container.mejs-audio > .mejs-inner > .mejs-controls > .mejs-time-rail > span").append(blockTrackName);
  this.elements.nameTrackInPlayer = blockTrackName;

  return outval;
}

Playlist.prototype.inputListFromAJAXObject = function(obj)
{
  var out = Array();

  for(i in obj) {
    out.push(obj[i]);
  }
  return out;
}

Playlist.prototype.createTrackElements = function() {
  var list = this.list;

  for(tr_num in list) {
    var new_elem = jQuery("<li>", {
      text: (Number.parseInt(tr_num) + 1) + ". " + list[tr_num].name,
      //url: list[tr_num].url,
      number: tr_num
    });
    new_elem.click(this.clickTrack.bind(this));
    this.elements.tracks.push(new_elem);
    this.elements.playlist.append(new_elem);
  }
};

Playlist.prototype.createButtonElements = function() {
  var playpause = jQuery("<button>", {
    class: "vdsdev-controls " + this.classes.btnPlayPause,
    text: this.symbols.play
  }).click(this.actionPlayPause.bind(this)).focus(this.actionBlurFocus);
  var next = jQuery("<button>", {
    class: "vdsdev-controls " + this.classes.btnNext,
    text: this.symbols.next
  }).click(this.actionNext.bind(this)).focus(this.actionBlurFocus);
  var prev = jQuery("<button>", {
    class: "vdsdev-controls " + this.classes.btnPrev,
    text: this.symbols.prev
  }).click(this.actionPrev.bind(this)).focus(this.actionBlurFocus);

  jQuery(".mejs-controls .mejs-mute button, .mejs-controls .mejs-unmute button").focus(this.actionBlurFocus);

  let keydownFunc = this.actionKeyDown.bind(this);

  jQuery("body").keydown(function(e) {
    return keydownFunc(e);
  });

  this.controls.playpause = playpause;
  this.controls.next = next;
  this.controls.prev = prev;

  this.elements.playerControls.append(prev);
  this.elements.playerControls.append(playpause);
  this.elements.playerControls.append(next);
}

Playlist.prototype.clickTrack = function(myEvent) {
  //alert(jQuery(this).attr("number"));
  var numtrack = Number.parseInt(jQuery(myEvent.currentTarget).attr("number"));
  var track = this.list[numtrack];

  if(numtrack == this.current) {
    this.actionPlayPause();
  }
  else {
    this.setCurrentTrack(numtrack);
    this.actionPlay();
  }
};

Playlist.prototype.setCurrentTrack = function (cur) {
  this.elements.tracks[this.current].removeClass(this.classes.currentTrack);
  this.current = cur;
  this.elements.tracks[cur].addClass(this.classes.currentTrack);

  this.elements.nameTrackInPlayer.html(this.list[cur].name);

  this.player.setSrc(this.list[cur].url);
}

Playlist.prototype.createPlaylistElement = function(elemInput) {
  var new_elem = jQuery("<ul style='padding:0;'>");
  jQuery(elemInput).append(new_elem);
  return new_elem;
};

Playlist.prototype.getCurrentTrack = function() {
  return this.list[this.current];
};

Playlist.prototype.actionNext = function ()
{
  var numtrack = this.current;
  (numtrack >= this.list.length - 1) ? numtrack = 0 : numtrack++;

  this.setCurrentTrack(numtrack);
  this.actionPlay();
};

Playlist.prototype.actionPrev = function() {
  var numtrack = this.current;
  (this.current == 0) ? numtrack = this.list.length - 1 : numtrack--;

  this.setCurrentTrack(numtrack);
  this.actionPlay();
}

Playlist.prototype.actionStop = function() {
  this.player.setCurrentTime(0);
  this.actionPause();
}

Playlist.prototype.actionPlay = function() {
  this.playing = true;
  this.elements.playlist.removeClass(this.classes.statPause);
  this.elements.playlist.addClass(this.classes.statPlay);

  // this.controls.playpause.html(this.symbols.pause);
  this.controls.playpause.addClass("pause");

  if(this.list[this.current].url == "NONE")
  {
    this.elements.nameTrackInPlayer.html("soon...");
    this.actionStop();
  }
  else {
    this.player.play();
  }
}

Playlist.prototype.actionPause = function() {
  this.playing = false;
  this.elements.playlist.removeClass(this.classes.statPlay);
  this.elements.playlist.addClass(this.classes.statPause);

  // this.controls.playpause.html(this.symbols.play);
  this.controls.playpause.removeClass("pause");

  this.player.pause();
}

Playlist.prototype.actionPlayPause = function() {
  var plpa = !this.playing;
  plpa ? this.actionPlay() : this.actionPause();
}

Playlist.prototype.actionVolTop = function() {
  var vol = this.player.getVolume() + this.volumeStep;
  if(vol > 1) vol = 1;
  this.player.setVolume(vol);
}

Playlist.prototype.actionVolBot = function() {
  var vol = this.player.getVolume() - this.volumeStep;
  if(vol < 0) vol = 0;
  this.player.setVolume(vol)
}

Playlist.prototype.actionCurTimeLeft = function() {
  var curtime = this.player.getCurrentTime() - this.curtimeStep;
  // if(curtime < 0) curtime = 0;
  this.player.setCurrentTime(curtime)
}

Playlist.prototype.actionCurTimeRight = function() {
  var curtime = this.player.getCurrentTime() + this.curtimeStep;
  // if(curtime < 0) curtime = 0;
  this.player.setCurrentTime(curtime)
}

Playlist.prototype.actionBlurFocus = function() {
  this.blur();
}

Playlist.prototype.actionKeyDown = function(e) {
  // alert(e.which);
  if (e.which == 32) { // space
    // alert("space");
    this.actionPlayPause();
    return false;
  }
  if (e.ctrlKey && e.which == 37) { // ctrl left
    // alert("left");
    this.actionPrev();
    return false;
  }
  if (e.ctrlKey && e.which == 39) { // ctrl right
    // alert("right");
    this.actionNext();
    return false;
  }
  if (e.which == 37) { // left
    // alert("left");
    this.actionCurTimeLeft();
    return false;
  }
  if (e.which == 39) { // right
    // alert("right");
    this.actionCurTimeRight();
    return false;
  }
  if (e.which == 38) { // top
    // alert("right");
    this.actionVolTop();
    return false;
  }
  if (e.which == 40) { // bottom
    // alert("right");
    this.actionVolBot();
    return false;
  }
}


var block = jQuery("div.wp-block-vdsdev-parse-beatport-vdsdev-parserbeatport-playlist");
var playlist = block.attr("playlist");
jQuery.ajax({
  url: cc_ajax_object.ajax_url, //ajaxurl,
  type: "POST",
  dataType : "json",
  contentType: "application/x-www-form-urlencoded; charset=UTF-8",
  data: {
    action: "vdsdev-parsebeatport_get-playlist",
    playlist: playlist
  },
  success: function(data) {
    if(data)
    {

      var player_wraper = jQuery("<div id='vdsdev-audioplayer-wraper'>");
      var player_controls = jQuery("<div id='vdsdev-audioplayer-controls'>")
      var player_elem = jQuery("<audio id='vdsdev-audioplayer'>");
      player_wraper.append(player_controls).append(player_elem);
      block.append(player_wraper);

      var myplaylist = new Playlist(block, player_wraper, player_controls, player_elem, data);



      // var player = new MediaElementPlayer('player', {
      //   src: "https://geo-samples.beatport.com/track/da11a696-0a4a-4cd3-865c-03e4bbea7bc0.LOFI.mp3",
      //   success: function(mediaElement, originalNode, instance) {
      //   }
      // });

      // block.append("<audio class='vdsdev-parserbeatport-player' src='" + data[0].url + "' controls>");
      // block.append("<ul>");
      // var ul = block.children("ul");
      //
      // for(line in data)
      // {
      //   var li = jQuery("<li>", {
      //     text: data[line].name,
      //     onclick: 'setPlayerTrack(this,"' + data[line].url + '")'
      //   });
      //   ul.append(li);
      //   // ul.append("<li url='" + data[line].url + "'" + ">" + data[line].name + "</li>");
      // }
    }
  }
});

function setPlayerTrack(elem, url)
{
  var parent = jQuery(elem).parent();
  jQuery(parent).children("li").each((item, i) => {
    if(i != elem)
    {
      jQuery(i).removeClass("play");
      jQuery(i).removeClass("pause");
    }
  });

  if(jQuery(elem).hasClass("play"))
  {
    jQuery(elem).removeClass("play");
    jQuery(elem).addClass("pause");
    jQuery("audio.vdsdev-parserbeatport-player").trigger("pause");
  }
  else if (jQuery(elem).hasClass("pause"))
  {
    jQuery(elem).removeClass("pause");
    jQuery(elem).addClass("play");
    jQuery("audio.vdsdev-parserbeatport-player").trigger("play");
  }
  else {
    jQuery(elem).addClass("play");
    jQuery("audio.vdsdev-parserbeatport-player").attr("src", url).trigger("play");
    //jQuery("figure.wp-block-audio>audio").attr("src", url).trigger("play");
  }
  // alert(url);
}
// jQuery(block).children("ul").children("li").click(function(){
//   alert("test");
// });
