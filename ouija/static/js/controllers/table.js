
ouija.controller('TableIndexController', ['$scope', '$http', 'tables',
  function($scope, $http, tables) {
    $scope.data = tables;
}]);


ouija.controller('TableViewController', ['$scope', '$http', 'table', 'data',
  function($scope, $http, table, data) {
    $scope.table = table;
    $scope.tabledata = data;
}]);
