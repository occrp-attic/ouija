var ouija = angular.module('ouija', ['ngRoute', 'ngAnimate', 'ui.bootstrap', 'infinite-scroll']);

ouija.config(['$routeProvider', '$compileProvider',
    function($routeProvider, $compileProvider) {

  $routeProvider.when('/', {
    templateUrl: 'tables/index.html',
    controller: 'TableIndexController',
    resolve: {
      tables: function(tablesService) {
        return tablesService.listTables()
      }
    }
  });

  $routeProvider.when('/tables/:id', {
    templateUrl: 'tables/view.html',
    controller: 'TableViewController',
    resolve: {
      table: ['tablesService', '$route', function(tablesService, $route) {
        return tablesService.getTable($route.current.params.id)
      }],
      data:  ['tablesService', '$route', function(tablesService, $route) {
        return tablesService.getTableRows($route.current.params.id)
      }]
    }
  });

  // $routeProvider.otherwise({
  //   redirectTo: '/'
  // });

  // $compileProvider.debugInfoEnabled(false);
}]);
