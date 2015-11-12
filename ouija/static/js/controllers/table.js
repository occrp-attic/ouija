
ouija.controller('TablesController', ['$scope', '$http', 'tables',
  function($scope, $http, tables) {

    $scope.data = tables;
}]);


ouija.controller('TableController', ['$scope', '$http', 'table', 'data',
  function($scope, $http, table, data) {
    $scope.table = table;
    $scope.tabledata = data;
}]);
