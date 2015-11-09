
ouija.factory('tablesService', ['$route', '$location', '$q', '$http', '$analytics',
    function($route, $location, $q, $http, $analytics) {
  var query = {};

  var ensureArray = function(data) {
    if (!angular.isDefined(data)) {
      return [];
    }
    return data;
  };

  var get = function() {
    query = {};
    return query;
  };

  var set = function(name, val) {
    query = get();
    query[name] = val;
    $location.path('/tables').search(query);
  }

  var clear = function() {
    $location.search({});
  };

  var execute = function() {
    var dfd = $q.defer(),
        query = get();

    $http.get('/api/tables', {}).then(function(res) {
      dfd.resolve(res.data);
    }, function(err) {
      dfd.reject(err);
    });
    return dfd.promise;
  };

  get();

  return {
      state: query,
      get: get,
      set: set,
      clear: clear,
      execute: execute,
  };

}]);

var loadTables = ['tablesService', function(tablesService) {
  return tablesService.get();
}];
