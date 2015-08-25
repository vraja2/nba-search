requirejs.config({
  paths: {
    jquery: "/static/bower_libs/jquery/dist/jquery.min",
    jqueryUI: "/static/bower_libs/jquery-ui/jquery-ui.min",
    backbone: "/static/bower_libs/backbone/backbone-min",
    underscore: "/static/bower_libs/underscore/underscore",
    visualsearch: "/static/bower_libs/visualsearch/build-min/visualsearch",
  },
  shim: {
    underscore: {
      exports: '_'
    },
    backbone: {
      deps: ['underscore', 'jquery'],
      exports: 'Backbone'
    },
    visualsearch: {
      deps: ['backbone', 'jqueryUI']
    }
  }
});

require(["jquery", "visualsearch"], function($) {
  $.getJSON('/static/data/player_list.json', function(plist) {
    $(document).ready(function() {
      window.visualSearch = VS.init({
        removedFacet : function (facet, query, options) {},
        container  : $('#search_box_container'),
        query      : '',
        showFacets : true,
        unquotable : [
          'text',
          'account',
          'filter',
          'access'
        ],
        callbacks  : {
          search : function(query, searchCollection) {
            var $query = $('#search_query');
            var count  = searchCollection.size();
            $query.stop().animate({opacity : 1}, {duration: 300, queue: false});
            $query.html('<span class="raquo">&raquo;</span> You searched for: ' +
                        '<b>' + (query || '<i>nothing</i>') + '</b>. ' +
                        '(' + count + ' facet' + (count==1 ? '' : 's') + ')');
            clearTimeout(window.queryHideDelay);
            window.queryHideDelay = setTimeout(function() {
              $query.animate({
                opacity : 0
              }, {
                duration: 1000,
                queue: false
              });
            }, 2000);
          },
          facetMatches : function(callback) {
            var facets = [
                'teammates-of', 'rebounds', 'points',
              ];

              var currentFacets = visualSearch.searchQuery.pluck("category");

              facets = facets.filter(function (el) {
                  return currentFacets.indexOf(el) < 0;
              });

              callback(facets);

          },
          valueMatches : function(facet, searchTerm, callback) {
            switch (facet) {
            case 'rebounds':
              callback(['0-5','6-10','11-15','16-20','21+'],{preserveOrder: true});
              break;
            case 'points':
              callback(['0-5','6-10','11-15','16-20','21-25','26-30','31-35','36+'],{preserveOrder: true});
              break;
            case 'teammates-of':
                callback(plist);
                break;

            }
          },
        },
      });
    });
  });
});
