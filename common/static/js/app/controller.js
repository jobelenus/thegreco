var controllers = angular.module('appControllers', []);

var ListController = function($scope, Resource, $state, $q) {
    var self = this;
    self.$scope = $scope;
    self.$state = $state;
    $scope.selected = {id: 0};
    $scope.choose = function(resource_id) {
        if($scope.selected.id == resource_id) {
            $scope.selected.id = 0;
            resource_id = 0;
        }
        self.update_state_machine(resource_id);
    };

    var deferred = $q.defer();
    $scope._resources = Resource.query({}, function() {
        deferred.resolve();
        self.stop_spinner();
    });
    var set = function() {
        deferred.promise.then(function() {
            $scope.teams = $scope._resources.filter(self.filter_function, self);
        });
    };
    $scope.$on('$stateChangeSuccess', function() {
        self.update_param_id();
        set();
    });
};
ListController.prototype.update_state_machine = function(resource_id) {
    alert('Implement me');
};
ListController.prototype.stop_spinner = function() {
    alert('Implement me');
};
ListController.prototype.update_param_id = function() {
    alert('Implement me');
};
ListController.filter_function = function(resource) {
    alert('Implement me');
};

var TeamController = function($scope, Resource, $state, $q) {
    ListController.call(this, $scope, Resource, $state, $q);
};
TeamController.prototype = Object.create(ListController.prototype);

TeamController.prototype.update_state_machine = function(team_id) {
    this.$scope.state_machine(this.$state, this.$state.params.season_id, team_id, this.$state.params.player_id);
};

TeamController.prototype.stop_spinner = function() {
    $('.team .panel .spinner').css('display', 'none');
};

TeamController.prototype.update_param_id = function() {
    if(this.$state.params.team_id) {
        this.$scope.selected.id = this.$state.params.team_id;
    }
};

TeamController.prototype.filter_function = function(team) {
    if(this.$state.params.season_id) {
        for(var i in team.seasons) {
            if(team.seasons[i] == this.$state.params.season_id) {
                if(this.$state.params.player_id) {
                    for(var j in team.season_players) {
                        if(this.$state.params.player_id == team.season_players[j].player) {
                            return team;
                        }
                    }
                } else {
                    return team;
                }
            }
        }
        return null;
    } else if(this.$state.params.player_id) {
        for(var k in team.season_players) {
            if(this.$state.params.player_id == team.season_players[k].player) {
                return team;
            }
        }
        return null;
    } else {
        return team;
    }
};

controllers.controller('TeamController', ['$scope', 'Team', '$state', '$q', TeamController]);

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
        $('.season .panel .spinner').css('display', 'none');
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
        $('.player .panel .spinner').css('display', 'none');
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
