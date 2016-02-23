/**
 * Created by ajay on 3/2/16.
 */

(function() {
    var BASE_URL= 'localhost:8000';
    window.App = {
        Models: {},
        Collections: {},
        Views: {},
        Router: {}
    };

    App.Router = Backbone.Router.extend({
        routes: {
            '': 'index',
            'show/:username': 'show',
            'download/*random': 'download',
            'search/:query': 'search',
            '*other': 'default'
        },

        index: function() {
            $( "#ajax-content" ).load('index', function(html_data) {
                console.log( "index. Load was performed." );
            });
        },

        show: function(username) {
            $( "#ajax-content" ).load('/users/profile/'+username +'/', function(html_data) {
                console.log( "user-profile. Load was performed." );
            });
        },

        download: function(random) {
            $(document.body).append("download route has been called.. with random equals : " + random);
        },

        search: function(query) {
            $(document.body).append("Search route has been called.. with query equals : " + query);
        },

        default: function(other) {
            console.log('This route is not hanled.. you tried to access:');
            //$(document.body).append("This route is not hanled.. you tried to access: " + other);
        }

    });

    var ApplicationView = Backbone.View.extend({

          //bind view to body element (all views should be bound to DOM elements)
          el: $('body'),

          //observe navigation click events and map to contained methods
          events: {
              'click a.navbar-brand.text-lt': 'viewProfile',
              'click ul.pills li.about-pill a': 'displayAbout',
              'click ul.pills li.contact-pill a': 'displayContact'
          },

          //called on instantiation
          initialize: function(){
              //set dependency on ApplicationRouter
              this.router = new App.Router();

              //call to begin monitoring uri and route changes
              Backbone.history.start();
          },

          viewProfile: function(){
              //update url and pass true to execute route method
              this.router.navigate("show/admin", true);
          },

          displayAbout: function(){
              //update url and pass true to execute route method
              this.router.navigate("about", true);
          },

          displayContact: function(){
              //update url and pass true to execute route method
              this.router.navigate("contact", true);
          }

    });

    //load application
    new ApplicationView();

})();