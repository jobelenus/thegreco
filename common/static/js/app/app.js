var app = angular.module('app', ['appControllers', 'appServices', 'ui.router']).run(['$http', function($http) {
    $http.defaults.headers.common.Authorization = 'Basic YWRtaW46cGFzc3dvcmQ=';
    $http.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
}]).run(['$rootScope', function($rootScope) {
    $rootScope.state_machine = function($scope, $state, season_id, team_id, player_id) {
        if(player_id && !team_id && !season_id) {
            $state.transitionTo('player_chosen', {player_id: player_id});
        } else if(season_id && !team_id && !player_id) {
            $state.transitionTo('season_chosen', {season_id: season_id});
        } else if(team_id && !season_id && !player_id) {
            $state.transitionTo('team_chosen', {team_id: team_id});
        } else if(player_id && team_id) {
            $state.transitionTo('player_team_chosen', {player_id: player_id, team_id: team_id});
        } else if(season_id && team_id) {
            $state.transitionTo('season_team_chosen', {season_id: season_id, team_id: team_id});
        } else if(player_id && season_id) {
            $state.transitionTo('season_player_chosen', {player_id: player_id, season_id: season_id});
        } else {
            $state.transitionTo('home');
        }
    };
    $rootScope.$on('$stateChangeStart', function() {
        $('nav .nav .spinner').css('display','block');
    });
    $rootScope.$on('$stateChangeSuccess', function() {
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
        url: "team/{team_id}/",
        parent: "home"
    });
    $stateProvider.state('season_chosen', {
        url: "season/{season_id}/",
        parent: "home"
    });
    $stateProvider.state('player_chosen', {
        url: "player/{player_id}/",
        parent: "home"
    });
    $stateProvider.state('season_team_chosen', {
        url: "team/{team_id}/season/{season_id}/",
        parent: "home"
    });
    $stateProvider.state('season_player_chosen', {
        url: "season/{season_id}/player/{player_id}/",
        parent: "home"
    });
    $stateProvider.state('player_team_chosen', {
        url: "player/{player_id}/team/{team_id}/",
        parent: "home"
    });
});
