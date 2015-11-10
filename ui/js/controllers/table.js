
ouija.controller('TableController', ['$scope', '$http', 'tables',
  function($scope, $http, tables) {

    $scope.bind = tables;
    $scope.data = tables.data;

}]);
