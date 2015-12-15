$(document).ready(function(){

  var currentsong = "";

  var myPlaylist = new jPlayerPlaylist({
    jPlayer: "#jplayer_N",
    cssSelectorAncestor: "#jp_container_N"
  }, [
    {
      title:"Awari",
      artist:"iit Singh",
      mp3:"/media/Awari.mp3",
      poster: "/static/images/m0.jpg"
    }
  ], {
    playlistOptions: {
      enableRemoveControls: true,
      autoPlay: false
    },
    swfPath: "js/jPlayer",
    supplied: "webmv, ogv, m4v, oga, mp3",
    smoothPlayBar: true,
    keyEnabled: true,
    audioFullScreen: false
  });

  $(document).on($.jPlayer.event.pause, myPlaylist.cssSelector.jPlayer,  function(){
    $('.musicbar').removeClass('animate');
    $('.jp-play-me').removeClass('active');
    $('.jp-play-me').parent('li').removeClass('active');
    
  });

  $(document).on($.jPlayer.event.play, myPlaylist.cssSelector.jPlayer,  function(){
    $('.musicbar').addClass('animate');
  });

  $(document).on('click', '.jp-play-me', function(e){
    e && e.preventDefault();
    var $this = $(e.target);
    if (!$this.is('a')) $this = $this.closest('a');
    $('.jp-play-me').not($this).removeClass('active');
    $('.jp-play-me').parent('li').not($this.parent('li')).removeClass('active');
    $this.toggleClass('active');
    $this.parent('li').toggleClass('active');
    if( !$this.hasClass('active') ){
      $("#jplayer_N").jPlayer("pause");
    }
    else {
      if(currentsong == $(this).attr("data-mp3")) {
        $("#jplayer_N").jPlayer("play");
      }
      else {
        $("#jplayer_N").jPlayer("setMedia", {
              mp3: $(this).attr("data-mp3"), 
              title: $(this).attr("name"),
          });
        currentsong = $(this).attr("data-mp3");
        $("#jplayer_N").jPlayer("play");
      }
    }
  });

  $(document).on('click', '.fa-plus-circle', function(e) {
    e && e.preventDefault();
    var $this = $(e.target);
    myPlaylist.add({
      title: $(this).attr("name"),
      artist: "test artist",
      mp3: $(this).attr("data-mp3"),
      poster: ""
    });
    $(this).toggleClass("fa-plus-circle fa-check-circle text-info", 200);
  });

  // video

  $("#jplayer_1").jPlayer({
    ready: function () {
      $(this).jPlayer("setMedia", {
        title: "Big Buck Bunny",
        m4v: "http://flatfull.com/themes/assets/video/big_buck_bunny_trailer.m4v",
        ogv: "http://flatfull.com/themes/assets/video/big_buck_bunny_trailer.ogv",
        webmv: "http://flatfull.com/themes/assets/video/big_buck_bunny_trailer.webm",
        poster: "images/m41.jpg"
      });
    },
    swfPath: "js",
    supplied: "webmv, ogv, m4v",
    size: {
      width: "100%",
      height: "auto",
      cssClass: "jp-video-360p"
    },
    globalVolume: true,
    smoothPlayBar: true,
    keyEnabled: true
  });

});