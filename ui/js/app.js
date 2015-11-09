var ouija = angular.module('ouija', ['ngRoute', 'ngAnimate',
  'ui.bootstrap', 'angulartics', 'angulartics.piwik', 'infinite-scroll']);

ouija.config(['$routeProvider', '$analyticsProvider', '$compileProvider',
    function($routeProvider, $analyticsProvider, $compileProvider) {

  $routeProvider.when('/', {
    templateUrl: 'home.html',
    controller: 'HomeController',
    resolve: {
      metadata: loadMetadata,
      summary: loadSummary,
      collections: loadCollections
    }
  });

  $routeProvider.when('/tables/:id', {
    templateUrl: 'tables/view.html',
    controller: 'EntityController',
    reloadOnSearch: false,
    resolve: {
      bind: loadEntityBind,
      metadata: loadMetadata
    }
  });

  $routeProvider.when('/queries/:id', {
    templateUrl: 'queries/view.html',
    controller: 'CollectionController',
    reloadOnSearch: false,
    resolve: {
      collection: loadCollection,
      metadata: loadMetadata
    }
  });

  $routeProvider.otherwise({
    redirectTo: '/'
  });

  $compileProvider.debugInfoEnabled(false);
}]);
