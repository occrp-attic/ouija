
ouija.controller('TableIndexController', ['$scope', '$http', 'tables',
  function($scope, $http, tables) {
    $scope.data = tables;
}]);


ouija.controller('TableViewController', ['$scope', '$http', 'table', 'data',
  function($scope, $http, table, data) {
    $scope.table = table;
    $scope.data = data;
    $scope.moreLoading = false;

    $scope.loadMore = function() {
      if (!$scope.data.next_url || $scope.moreLoading) {
        return;
      }
      $scope.moreLoading = true;
      $http.get($scope.data.next_url).then(function(res) {
        $scope.data.results = $scope.data.results.concat(res.data.results);
        $scope.data.next_url = res.data.next_url;
        $scope.moreLoading = false;
      });
    }
}]);
