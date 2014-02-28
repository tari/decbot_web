angular.module('decbot', [
    // Module dependencies
    'ngResource',
    'infinite-scroll'
]);

angular.module('decbot').factory('Quotes', [
    '$resource',
    function($resource) {
        var Quotes = $resource('/api/quotes/:id')
        return Quotes;
    }
]);

angular.module('decbot').controller('QuotesCtrl', [
    // Controller dependencies
    '$scope',
    'Quotes',
    
    function($scope, Quotes) {
        $scope.quotes = [];

        var last_page = 1;
        var more_pages = true;

        $scope.moreQuotes = function() {
            if (!more_pages) return;

            var request = Quotes.get({'page': last_page}, function() {
                last_page++;

                var results = request['results'];
                for (var i = 0; i < request.count; i++) {
                    $scope.quotes.push(results[i]);
                }

                more_pages = request.next != null;
            });
        };
        $scope.moreQuotes();
    }
]);
