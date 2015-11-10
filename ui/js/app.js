var ouija = angular.module('ouija', ['ngRoute', 'ngAnimate',
  'ui.bootstrap', 'angulartics', 'angulartics.piwik', 'infinite-scroll']);

ouija.config(['$routeProvider', '$analyticsProvider', '$compileProvider',
    function($routeProvider, $analyticsProvider, $compileProvider) {

  $routeProvider.when('/', {
    templateUrl: 'home.html',
    controller: 'HomeController',
    resolve: {}
  });

  $routeProvider.when('/tables/', {
    templateUrl: 'tables/list.html',
    controller: 'TableController',
    resolve: {
      tables: function(tablesService) { tablesService.listTables() },
    }
  });

  $routeProvider.when('/tables/:id', {
    templateUrl: 'tables/view.html',
    controller: 'TableController',
    resolve: {
      table: function(tablesService) { tablesService.getTable() },
    }
  });

/*
  $routeProvider.when('/queries/', {
    templateUrl: 'queries/list.html',
    controller: 'QueryController',
    reloadOnSearch: false,
    resolve: {
      collection: loadQueryList,
    }
  });

  $routeProvider.when('/queries/:id', {
    templateUrl: 'queries/view.html',
    controller: 'QueryController',
    reloadOnSearch: false,
    resolve: {
      collection: loadQueryBind,
    }
  });
*/

  $routeProvider.otherwise({
    redirectTo: '/'
  });

  $compileProvider.debugInfoEnabled(false);
}]);
