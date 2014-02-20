var app = angular.module('app', ['appControllers', 'appServices', 'ui.router']).run(function($http) {
    $http.defaults.headers.common.Authorization = 'Basic YWRtaW46cGFzc3dvcmQ=';
    $http.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
});

app.config(function($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise("/");
    $stateProvider.state("home", {
        url: "/",
        views: {
            'team': { controller: 'TeamController', templateUrl: '/static/partials/team.view.html' },
            'player': { controller: 'PlayerController', templateUrl: '/static/partials/player.view.html' },
            'season': { controller: 'SeasonController', templateUrl: '/static/partials/season.view.html' }
        }
    }).state('team.chosen', {
        url: "/team/:teamId/",
        controller: function($scope) {
            console.log('state', $scope);
        }
    });
});
