var controllers = angular.module('appControllers', []);

controllers.controller('TeamController', ['$scope', 'Team', '$state', '$q', function($scope, Team, $state, $q) {
    $scope.selected = {id: 0};
    $scope.choose = function(team_id) {
        if($scope.selected.id == team_id) {
            $scope.selected.id = 0;
            team_id = 0;
        }
        $scope.state_machine($state, $state.params.season_id, team_id, $state.params.player_id);
    };

    var deferred = $q.defer();
    $scope._teams = Team.query({}, function() {
        deferred.resolve();
    });
    var set = function() {
        if($state.params.team_id) {
            $scope.selected.id = $state.params.team_id;
        }
        deferred.promise.then(function() {
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
    };
    $scope.$on('$stateChangeSuccess', function() {
        set();
    });
}]);

controllers.controller('SeasonController', ['$scope', 'Season', '$state', '$q', function($scope, Season, $state, $q) {
    $scope.selected = {id: 0};
    $scope.choose = function(season_id) {
        if($scope.selected.id == season_id) {
            $scope.selected.id = 0;
            season_id = 0;
        }
        $scope.state_machine($state, season_id, $state.params.team_id, $state.params.player_id);
    };
    var deferred = $q.defer();
    $scope._seasons = Season.query({}, function() {
        deferred.resolve();
    });
    var set = function() {
        if($state.params.season_id) {
            $scope.selected.id = $state.params.season_id;
        }
        deferred.promise.then(function() {
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
    };
    $scope.$on('$stateChangeSuccess', function() {
        set();
    });
}]);

controllers.controller('PlayerController', ['$scope', 'Player', '$state', '$q', function($scope, Player, $state, $q) {
    $scope.selected = {id: 0};
    $scope.choose = function(player_id) {
        if($scope.selected.id == player_id) {
            $scope.selected.id = 0;
            player_id = 0;
        }
        $scope.state_machine($state, $state.params.season_id, $state.params.team_id, player_id);
    };
    var deferred = $q.defer();
    $scope._players = Player.query({}, function() {
        deferred.resolve();
    });
    var set = function() {
        if($state.params.player_id) {
            $scope.selected.id = $state.params.player_id;
        }
        deferred.promise.then(function() {
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
    };
    $scope.$on('$stateChangeSuccess', function() {
        set();
    });
}]);

controllers.controller('TeamDetail', ['$scope', 'TeamDetail', '$state', '$rootScope', function($scope, TeamDetail, $state, $rootScope) {
    $scope.form = {season: 0};
    $scope.messages = {};
    $scope.team = TeamDetail.get({id: $state.params.team_id});
    $scope.add = function() {
        if($scope.form.season === 0) {
            $scope.messages.choose_error = true;
        } else {
            $scope.team.seasons.push($scope.form.season);
            $scope.team.$save(function() {
                $scope.messages.success = true;
                $rootScope.$broadcast('$stateChangeSuccess');  // update the other controllers with the new data
                $scope.form.season = 0;
                for(var i in $scope.team.seasons_not_in) {
                    if($scope.team.seasons_not_in[i].id == $scope.form.season) {
                        $scope.team.seasons_not_in.remove(i);
                    }
                }
            }, function() {
                $scope.messages.an_error = true;
            });
        }
    };
    $scope.dismiss = function() {
        $scope.$dismiss();
    };
}]);
