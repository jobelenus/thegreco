var controllers = angular.module('appControllers', []);

controllers.controller('TeamController', ['$scope', 'Team', '$state', function($scope, Team, $state) {
    $scope.teams = Team.query();
    $scope.selected_id = 0;
    if($state.params.team_id) {
        $scope.selected_id = $state.params.team_id;
    }
    $scope.choose = function(team_id) {
        if($state.params.player_id) {
            $state.go('player_team_chosen', {player_id: $state.params.player_id, team_id: team_id});
        } else if($state.params.season_id) {
            $state.go('season_team_chosen', {season_id: $state.params.season_id, team_id: team_id});
        } else {
            $state.go('team_chosen', {team_id: team_id});
        }
    };
}]);

controllers.controller('SeasonController', ['$scope', 'Season', '$state', function($scope, Season, $state) {
    $scope._seasons = Season.query({}, function() {
        $scope.seasons = $scope._seasons.filter(function(season) {
            if($state.params.team_id) {
                for(var i in season.teams) {
                    if(season.teams[i].id == $state.params.team_id) {
                        return season;
                    }
                }
                return null;
            } else {
                return season;
            }
        });
    });
    console.log('season', $state);
}]);

controllers.controller('PlayerController', ['$scope', 'Player', '$state', function($scope, Player, $state) {
    $scope.players = Player.query();
    console.log('player', $state);
}]);
