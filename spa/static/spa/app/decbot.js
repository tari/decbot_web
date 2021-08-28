"use strict";

let decbot = angular.module('decbot', [
    // Module dependencies
    'ngResource',
    'ngRoute',
    'infinite-scroll',
    'highcharts-ng',
    'angular-loading-bar',
]);

decbot.filter('join', function () {
    return function join(array, separator, prop) {
        if (!Array.isArray(array)) {
            return array; // if not array return original - can also throw error
        }

        return (!angular.isUndefined(prop) ? array.map(function (item) {
            return item[prop];
        }) : array).join(separator);
    };
});

decbot.config([
    '$locationProvider',
    function($lp) {
        $lp.html5Mode(true).hashPrefix('!');
    }
]).run([
    '$location',
    function($location) {
        // If there was a redirect to the single-page app, it gave
        // us the actual requested URL. Set our path to that.
        let search = $location.search();
        if ('redirect_src' in search) {
            let target = decodeURIComponent(search['redirect_src']);
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
                templateUrl: decbot_spa_partial('quote-list.html'),
                controller: 'QuoteListCtrl'
            }).
            when('/quotes/:quoteId', {
                templateUrl: decbot_spa_partial('quote-single.html'),
                controller: 'QuoteDetailCtrl'
            }).
            when('/scores/', {
                templateUrl: decbot_spa_partial('score-summary.html'),
                controller: 'ScoreSummaryCtrl'
            }).
            when('/scores/:name', {
                templateUrl: decbot_spa_partial('score-single.html'),
                controller: 'ScoreDetailCtrl'
            }).
            otherwise({
                redirectTo: '/scores/'
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
            let links = element.find('a');
            let urlMap = {};
            let currentLocation;
            let activeClass = attrs.navMenu || 'nav-active';

            for (let i = 0; i < links.length; i++) {
                let link = angular.element(links[i]);
                urlMap[link.attr('href')] = link;
            }

            scope.$on('$routeChangeSuccess', function() {
                let target = urlMap[$location.path()];

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
        return $resource('/api/quotes/:id');
    }
]);

decbot.controller('QuoteListCtrl', [
    // Controller dependencies
    '$scope',
    'Quotes',
    
    function($scope, Quotes) {
        $scope.quotes = [];
        $scope.more_loading = false;
        $scope.decbot_spa_partial = decbot_spa_partial;

        let last_page = 1;
        let more_pages = true;

        $scope.moreQuotes = function() {
            if (!more_pages) return;
            $scope.more_loading = true;

            let request = Quotes.get({'page': last_page}, function() {
                last_page++;
                $scope.more_loading = false;

                let results = request['results'];
                for (let i = 0; i < results.length; i++) {
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
        let qid = $routeParams.quoteId;

        $scope.quote = Quotes.get({id: qid});
    }
]);

decbot.factory('Scores', [
    '$resource',
    function($resource) {
        return $resource('/api/scores/:name');
    }
]);

decbot.factory('ScoreLogs', [
    '$resource',
    function($resource) {
        return $resource('/api/scores-log/:name');
    }
]);

decbot.controller('ScoreDetailCtrl', [
    '$scope',
    '$routeParams',
    'Scores',
    'ScoreLogs',

    function($scope, $routeParams, Scores, ScoreLogs) {
        let name = $routeParams.name;

        let score_aggregate = 0;
        // We need to sequence ScoreLog get after Score get so the aggregate is
        // updated properly, so set more_loading initially, to be cleared by
        // Score get completion, thus unblocking ScoreLog fetch.
        $scope.more_loading = true;
        $scope.object = Scores.get({name: name}, function(data) {
            score_aggregate = data.score;
            $scope.more_loading = false;
        });

        $scope.changes = [];
        $scope.last_changed = "at an indeterminate time";
        $scope.chartData = [];

        let last_page = 1;
        $scope.more_pages = true;
        $scope.more = function() {
            if (!$scope.more_pages) return;
            $scope.more_loading = true;

            ScoreLogs.get({'name': name, 'page': last_page}, function (data) {
                $scope.more_loading = false;
                $scope.chartConfig.loading = false;
                $scope.more_pages = data.next != null;

                if (last_page === 1 && data.count > 0) {
                    // First item's timestamp is the newest.
                    $scope.last_changed = data.results[0].timestamp;
                }
                if (data.count === 0) {
                    // No history exists. Inject a single data point into the
                    // chart.
                    $scope.chartData.push([0, 0], [Date.now(), score_aggregate]);
                    return;
                }
                last_page++;

                for (let i = 0; i < data.count; i++) {
                    let entry = data.results[i];
                    entry.aggregate = score_aggregate;

                    $scope.changes.push(entry);
                    $scope.chartData.unshift([
                        Date.parse(entry.timestamp),
                        score_aggregate
                    ]);

                    score_aggregate += -entry.change;
                }
            });

        $scope.chartConfig = {
            options: {
                chart: {
                    type: 'area',
                    zoomType: 'xy'
                },
                credits: { enabled: false },
                tooltip: {
                    crosshairs: true,
                },
                legend: { enabled: false },
                yAxis: {
                    type: 'linear',
                    title: { text: 'Score' },
                },
            },
            series: [{name: 'Score', data: $scope.chartData}],
            title: {
                text: 'Score history for ' + name,
            },
            xAxis: {
                type: 'datetime',
                labels: {
                    rotation: -75,
                    overflow: false,
                },
                title: { text: 'Time' },
            },
            loading: true,
        };
        }
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

        let last_page = 1;
        let more_pages = true;
        // Items with equal score should have same rank
        let last_score = Infinity;
        let rank = 0;

        $scope.moreScores = function() {
            if (!more_pages) return;
            $scope.more_loading = true;
            $scope.chartConfig.loading = false;

            let request = Scores.get({'page': last_page}, function() {
                $scope.more_loading = false;
                last_page++;

                let results = request['results'];
                for (let i = 0; i < results.length; i++) {
                    let result = results[i];
                    if (result.score < last_score) {
                        rank += 1;
                    }
                    last_score = result.score;
                    result.rank = rank;
                    $scope.scores.push(result);

                    let s = result.score;
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
                        let s = this.y;
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
