
ouija.controller('AppController', ['$scope', '$rootScope', '$http', '$location', 'sessionService',
  function($scope, $rootScope, $http, $location, sessionService) {

    $scope.session = {'logged_in': false, 'user': {}};
    $scope.routeLoaded = false;
    $scope.routeFailed = false;

    $rootScope.$on("$routeChangeStart", function (event, next, current) {
        $scope.routeLoaded = false;
        $scope.routeFailed = false;
        $scope.routeLoadTime = new Date();
    });

    $rootScope.$on("$routeChangeSuccess", function (event, next, current) {
        $scope.routeLoaded = true;
        var loadTime = new Date() - $scope.routeLoadTime;
        console.log('Loaded route, took:', loadTime, 'ms');
    });

    $rootScope.$on("$routeChangeError", function (event, next, current) {
        $scope.routeFailed = true;
    });

    sessionService.get().then(function(session) {
        $scope.session = session;
    });

}]);
