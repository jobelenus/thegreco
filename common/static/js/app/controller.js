var controllers = angular.module('appControllers', []);

var state_machine = function($scope, $state, season_id, team_id, player_id) {
    if(player_id && !team_id && !season_id) {
        $state.go('player_chosen', {player_id: player_id});
    } else if(season_id && !team_id && !player_id) {
        $state.go('season_chosen', {season_id: season_id});
    } else if(team_id && !season_id && !player_id) {
        $state.go('team_chosen', {team_id: team_id});
    } else if(player_id && team_id) {
        $state.go('player_team_chosen', {player_id: player_id, team_id: team_id});
    } else if(season_id && team_id) {
        $state.go('season_team_chosen', {season_id: season_id, team_id: team_id});
    } else if(player_id && season_id) {
        $state.go('season_player_chosen', {player_id: player_id, season_id: season_id});
    } else {
        $state.go('home');
    }
};

controllers.controller('TeamController', ['$scope', 'Team', 'Player', '$state', function($scope, Team, Player, $state) {
    $scope.selected_id = 0;
    if($state.params.team_id) {
        $scope.selected_id = $state.params.team_id;
    }
    $scope.choose = function(team_id) {
        if($scope.selected_id == team_id) {
            $scope.selected_id = 0;
            team_id = 0;
        }
        state_machine($scope, $state, $state.params.season_id, team_id, $state.params.player_id);
    };
    $scope._teams = Team.query({}, function() {
        $scope.teams = $scope._teams.filter(function(team) {
            if($state.params.season_id) {
                for(var i in team.seasons) {
                    if(team.seasons[i] == $state.params.season_id) {
                        if($state.params.player_id) {
                            for(var j in team.season_players) {
                                if($state.params.player_id == team.season_players[j].player) {
                                    return team;
                                }
                            }
                        } else {
                            return team;
                        }
                    }
                }
                return null;
            } else if($state.params.player_id) {
                for(var k in team.season_players) {
                    if($state.params.player_id == team.season_players[k].player) {
                        return team;
                    }
                }
                return null;
            } else {
                return team;
            }
        });
    });
}]);

controllers.controller('SeasonController', ['$scope', 'Season', 'Player', '$state', function($scope, Season, Player, $state) {
    $scope.selected_id = 0;
    if($state.params.season_id) {
        $scope.selected_id = $state.params.season_id;
    }
    $scope.choose = function(season_id) {
        if($scope.selected_id == season_id) {
            $scope.selected_id = 0;
            season_id = 0;
        }
        state_machine($scope, $state, season_id, $state.params.team_id, $state.params.player_id);
    };
    $scope._seasons = Season.query({}, function() {
        $scope.seasons = $scope._seasons.filter(function(season) {
            if($state.params.team_id) {
                for(var i in season.teams) {
                    if(season.teams[i].id == $state.params.team_id) {
                        if($state.params.player_id) {
                            for(var j in season.players) {
                                if($state.params.player_id == season.players[j]) {
                                    return season;
                                }
                            }
                        } else {
                            return season;
                        }
                    }
                }
                return null;
            } else if($state.params.player_id) {
                for(var k in season.players) {
                    if($state.params.player_id == season.players[k]) {
                        return season;
                    }
                }
                return null;
            } else {
                return season;
            }
        });
    });
}]);

controllers.controller('PlayerController', ['$scope', 'Player', '$state', function($scope, Player, $state) {
    $scope.selected_id = 0;
    if($state.params.player_id) {
        $scope.selected_id = $state.params.player_id;
    }
    $scope.choose = function(player_id) {
        if($scope.selected_id == player_id) {
            $scope.selected_id = 0;
            player_id = 0;
        }
        state_machine($scope, $state, $state.params.season_id, $state.params.team_id, player_id);
    };
    $scope._players = Player.query({}, function() {
        $scope.players = $scope._players.filter(function(player) {
            if($state.params.team_id) {
                for(var i in player.season_teams) {
                    if(player.season_teams[i].team == $state.params.team_id) {
                        if($state.params.season_id) {
                            if(player.season_teams[i].season == $state.params.season_id) {
                                return player;
                            }
                        } else {
                            return player;
                        }
                    }
                }
                return null;
            } else if($state.params.season_id) {
                for(var j in player.seasons) {
                    if(player.seasons[j] == $state.params.season_id) {
                        return player;
                    }
                }
                return null;
            } else {
                return player;
            }
        });

    });
}]);
