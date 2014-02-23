// Array Remove - By John Resig (MIT Licensed)
Array.prototype.remove = function(from, to) {
    var rest = this.slice((to || from) + 1 || this.length);
    this.length = from < 0 ? this.length + from : from;
    return this.push.apply(this, rest);
};

var app = angular.module('app', ['appControllers', 'appServices', 'ui.router', 'ui.bootstrap']).run(['$http', function($http) {
    $http.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
}]).run(['$rootScope', function($rootScope) {
    $rootScope.state_machine = function($state, season_id, team_id, player_id) {
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

app.config(['$stateProvider', '$urlRouterProvider', function($stateProvider, $urlRouterProvider) {
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
    $stateProvider.state('team_chosen.edit', {
        url: "edit/",
        onEnter: function($stateParams, $state, $modal) {
            $modal.open({
                templateUrl: '/static/partials/team.detail.html',
                controller: "TeamDetail"
            }).result.then(function() {
                // nothing
            }, function(result) {
                return $state.transitionTo("team_chosen", {team_id: $state.params.team_id});
            });
        }
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
}]);
