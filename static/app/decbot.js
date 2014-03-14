var decbot = angular.module('decbot', [
    // Module dependencies
    'ngResource',
    'ngRoute',
    'infinite-scroll'
]);

decbot.config([
    '$locationProvider',
    function($lp) {
        $lp.html5Mode(true).hashPrefix('!');
    }
]).run([
    '$location',
    function($location) {
        // If there was a redirect to the single-page app, it gave
        // us the actual requested URL. Set out path to that.
        var search = $location.search();
        if ('redirect_src' in search) {
            var target = decodeURIComponent(search['redirect_src']);
            $location.path(target);

            delete search['redirect_src'];
            $location.search(search);

            $location.replace();
        }
    }
]);

decbot.config([
    '$routeProvider',
    function($routeProvider) {
        $routeProvider.
            when('/quotes/', {
                templateUrl: '/static/partials/quote-list.html',
                controller: 'QuoteListCtrl'
            }).
            when('/quotes/:quoteId', {
                templateUrl: '/static/partials/quote-single.html',
                controller: 'QuoteDetailCtrl'
            }).
            otherwise({
                redirectTo: '/quotes/'
            });
    }
]);

decbot.factory('Quotes', [
    '$resource',
    function($resource) {
        var Quotes = $resource('/api/quotes/:id')
        return Quotes;
    }
]);

decbot.controller('QuoteListCtrl', [
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

decbot.controller('QuoteDetailCtrl', [
    '$scope',
    '$routeParams',
    'Quotes',

    function($scope, $routeParams, Quotes) {
        var qid = $routeParams.quoteId;

        $scope.quote = Quotes.get({id: qid});
    }
]);
