
ouija.factory('tablesService', ['$q', '$http', function($q, $http) {

    function listTables() {
        var dfd = $q.defer();
        var request = $http({
            method: "get",
            url: "/api/tables",
            params: {},
            data: {}
        });
        request.then(
            function(response) {
                dfd.resolve(response.data);
            }, function(error) {
                dfd.resolve(error);
            }
        );
        return dfd.promise;
    };

    function getTable(tablename) {
        var dfd = $q.defer();
        var request = $http({
            method: "post",
            url: "/api/table/" + tablename,
            params: {},
            data: {}
        });
        request.then(
            function(response) {
                dfd.resolve(response.data);
            },
            function(error) {
                dfd.resolve(error);
            }
        );
        return dfd.promise;
    };

    return {
        "listTables": listTables,
        "getTable": getTable,
    };

}]);
