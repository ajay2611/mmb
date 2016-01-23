//how to use
//call rebind on every page

window.onload = function() {

  reBind();
};

function reBind () {

    if( $('#myplayer').html().length < 5 )
  {
    $.get('http://localhost:8000/logic/api/return_player/', function (data) {

      $('#myplayer').html(data);

    })
  }

  var alinks = {
    index: {
      title: "Home Page",
      url: "./",
      content: ""
    },
    settings: {
      title: "Contact",
      url: "contact.html",
      content: ""
    }
  }

  var navLinks = document.querySelectorAll('.load-content');
  var contentElement = document.getElementById('content_div');

  var updateContent = function(stateObj) {

    if (stateObj) {
      contentElement.innerHTML = stateObj.content;
    }
  };

  var loadContent = function(url, callback) {
    var request = new XMLHttpRequest();

    request.onload = function(response) {
      alinks[url.split('.')[0]].content = response.target.response;
      alert(response.target.response);
      var pageData = alinks[url.split('.')[0]];
      updateContent(dataFromPage);
      callback();
    };

    request.open('get',  url, true);
    request.send();
  };

  for (var i = 0; i < navLinks.length; i++) {
    navLinks[i].addEventListener('click', function(e) {
      e.preventDefault();
      var pageURL = this.attributes['href'].value;
      loadContent(pageURL, function() {
        var dataFromPage = alinks[pageURL.split('.')[0]];
        history.pushState(dataFromPage, dataFromPage.title, pageURL);
      });
    });
  }
  window.addEventListener('popstate', function(event) {
    updateContent(event.state);
  });

  loadContent('/', function() {
    history.replaceState(alinks.index, alinks.index.title, '');
  });

}
