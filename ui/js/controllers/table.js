
ouija.controller('TableController', ['$scope', '$http', 'bind', 'metadata',
  function($scope, $http, bind, metadata) {

  $scope.bind = bind;
  $scope.data = bind.data;
  $scope.metadata = metadata;

}]);
