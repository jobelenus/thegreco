var app = angular.module('app', ['appControllers', 'appServices', 'ui.router']).run(['$http', function($http) {
    $http.defaults.headers.common.Authorization = 'Basic YWRtaW46cGFzc3dvcmQ=';
    $http.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
}]).run(['$rootScope', function($rootScope) {
    $rootScope.$on('$stateChangeStart', function() {
        $('nav .nav .spinner').css('display','block');
    });
    $rootScope.$on('$viewContentLoaded', function() {
        // is run N times b/c N controllers fire it
        $('nav .nav .spinner').css('display','none');
    });
}]);

app.config(function($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise("/");
    $stateProvider.state("home", {
        url: "/",
        views: {
            'team': { controller: 'TeamController', templateUrl: '/static/partials/team.view.html' },
            'player': { controller: 'PlayerController', templateUrl: '/static/partials/player.view.html' },
            'season': { controller: 'SeasonController', templateUrl: '/static/partials/season.view.html' }
        }
    });
    $stateProvider.state('team_chosen', {
        url: "/team/{team_id}/",
        // TODO: how not to duplicate this!
        views: {
            'team': { controller: 'TeamController', templateUrl: '/static/partials/team.view.html' },
            'player': { controller: 'PlayerController', templateUrl: '/static/partials/player.view.html' },
            'season': { controller: 'SeasonController', templateUrl: '/static/partials/season.view.html' }
        }
    });
    $stateProvider.state('season_chosen', {
        url: "/season/{season_id}/",
        // TODO: how not to duplicate this!
        views: {
            'team': { controller: 'TeamController', templateUrl: '/static/partials/team.view.html' },
            'player': { controller: 'PlayerController', templateUrl: '/static/partials/player.view.html' },
            'season': { controller: 'SeasonController', templateUrl: '/static/partials/season.view.html' }
        }
    });
    $stateProvider.state('player_chosen', {
        url: "/player/{player_id}/",
        views: {
            'team': { controller: 'TeamController', templateUrl: '/static/partials/team.view.html' },
            'player': { controller: 'PlayerController', templateUrl: '/static/partials/player.view.html' },
            'season': { controller: 'SeasonController', templateUrl: '/static/partials/season.view.html' }
        }
    });
    $stateProvider.state('season_team_chosen', {
        url: "/team/{team_id}/season/{season_id}/",
        views: {
            'team': { controller: 'TeamController', templateUrl: '/static/partials/team.view.html' },
            'player': { controller: 'PlayerController', templateUrl: '/static/partials/player.view.html' },
            'season': { controller: 'SeasonController', templateUrl: '/static/partials/season.view.html' }
        }
    });
    $stateProvider.state('season_player_chosen', {
        url: "/season/{season_id}/player/{player_id}/",
        views: {
            'team': { controller: 'TeamController', templateUrl: '/static/partials/team.view.html' },
            'player': { controller: 'PlayerController', templateUrl: '/static/partials/player.view.html' },
            'season': { controller: 'SeasonController', templateUrl: '/static/partials/season.view.html' }
        }
    });
    $stateProvider.state('player_team_chosen', {
        url: "/player/{player_id}/team/{team_id}/",
        views: {
            'team': { controller: 'TeamController', templateUrl: '/static/partials/team.view.html' },
            'player': { controller: 'PlayerController', templateUrl: '/static/partials/player.view.html' },
            'season': { controller: 'SeasonController', templateUrl: '/static/partials/season.view.html' }
        }
    });
});
