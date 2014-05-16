"use strict";

var decbot = angular.module('decbot', [
    // Module dependencies
    'ngResource',
    'ngRoute',
    'infinite-scroll',
    'highcharts-ng'
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
            when('/scores/', {
                templateUrl: '/static/partials/score-summary.html',
                controller: 'ScoreSummaryCtrl'
            }).
            when('/scores/:name', {
                templateUrl: '/static/partials/score-single.html',
                controller: 'ScoreDetailCtrl'
            }).
            otherwise({
                redirectTo: '/quotes/'
            });
    }
]);

// Simple nav menu, derived from Ryan Kaskel's example:
// https://ryankaskel.com/blog/2013/05/27/a-different-approach-to-angularjs-navigation-menus
decbot.directive('navMenu', [
    '$location',
    '$log',
    function($location, $log) {
        return function(scope, element, attrs) {
            var links = element.find('a');
            var urlMap = {};
            var currentLocation;
            var activeClass = attrs.navMenu || 'nav-active';

            for (var i = 0; i < links.length; i++) {
                var link = angular.element(links[i]);
                urlMap[link.attr('href')] = link;
            }

            scope.$on('$routeChangeSuccess', function() {
                var target = urlMap[$location.path()];

                if (target) {
                    if (currentLocation) {
                        currentLocation.removeClass(activeClass);
                    }
                    currentLocation = target;
                    currentLocation.addClass(activeClass);
                } else {
                    $log.warn("Nav doesn't recognize path: " +
                              $location.path());
                }
            });
        };
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
        $scope.more_loading = false;

        var last_page = 1;
        var more_pages = true;

        $scope.moreQuotes = function() {
            if (!more_pages) return;
            $scope.more_loading = true;

            var request = Quotes.get({'page': last_page}, function() {
                last_page++;
                $scope.more_loading = false;

                var results = request['results'];
                for (var i = 0; i < results.length; i++) {
                    $scope.quotes.push(results[i]);
                }

                more_pages = request.next != null;
            });
        };
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

decbot.factory('Scores', [
    '$resource',
    function($resource) {
        return $resource('/api/scores/:name');
    }
]);

decbot.controller('ScoreDetailCtrl', [
    '$scope',
    '$routeParams',
    'Scores',

    function($scope, $routeParams, Scores) {
        var name = $routeParams.name;

        $scope.object = Scores.get({name: name});
    }
]);

decbot.controller('ScoreSummaryCtrl', [
    '$scope',
    'Scores',
    '$http',
    function($scope, Scores, $http) {
        $scope.aggregate_score = "unknown";
        $scope.aggregate_names = "unknown";

        $http.get('/api/totals/score').success(function (data) {
            $scope.aggregate_score = data['total'];
            $scope.aggregate_names = data['names'];
        });

        $scope.scores = [];
        $scope.uScores = [];
        $scope.uNames = [];
        $scope.more_loading = false;

        var last_page = 1;
        var more_pages = true;
        // Items with equal score should have same rank
        var last_score = Infinity;
        var rank = 0;

        $scope.moreScores = function() {
            if (!more_pages) return;
            $scope.more_loading = true;
            $scope.chartConfig.loading = false;

            var request = Scores.get({'page': last_page}, function() {
                $scope.more_loading = false;
                last_page++;

                var results = request['results'];
                for (var i = 0; i < results.length; i++) {
                    var result = results[i];
                    if (result.score < last_score) {
                        rank += 1;
                    }
                    last_score = result.score;
                    result.rank = rank;
                    $scope.scores.push(result);

                    var s = result.score;
                    // Emulate matplotlib's `symlog` scale by making the scale
                    // linear for all scores less than 1. 0 => 1e-1, 1 => 1e-2
                    // and so forth.
                    if (s <= 0) {
                        s = Math.pow(10, s - 1);
                    }
                    $scope.uScores.push(s);
                    $scope.uNames.push(result.name);
                }

                more_pages = request.next != null;
            });
        };

        $scope.chartConfig = {
            options: {
                chart: {
                    type: 'area',
                    zoomType: 'xy'
                },
                credits: { enabled: false },
                tooltip: {
                    formatter: function() {
                        var s = this.y;
                        if (s < 1) {
                            s = Math.round(Math.log(s) / Math.LN10) + 1;
                        }
                        return this.x + '<br />' + s;
                    }
                },
                legend: { enabled: false },
                yAxis: {
                    type: 'logarithmic',
                    minorTickInterval: 0.1,
                    labels: {
                        formatter: function() {
                            if (this.value < 1) {
                                return Math.round(Math.log(this.value) / Math.LN10) + 1;
                            } else {
                                return this.value;
                            }
                        }
                    },
                    title: { text: null },
                },
            },
            series: [{name: 'Score', data: $scope.uScores}],
            title: {
                text: 'Top 50 (log<sub>10</sub>)',
                useHTML: true,
            },
            xAxis: {
                categories: $scope.uNames,
                startOnTick: true,
                labels: {
                    rotation: -75,
                    overflow: false,
                },
                currentMin: 0,
                currentMax: 49
            },
            loading: true,
        };
    }
]);
