
spindle.directive('ouijaTable', [function() {
  return {
    restrict: 'E',
    scope: {
      'bind': '='
    },
    templateUrl: 'entities/table.html',
    link: function (scope, element, attrs, model) {
    }
  };
}]);
