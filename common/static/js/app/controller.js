var controllers = angular.module('appControllers', []);

//Base List Controller

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

    $scope.deferred = $q.defer();
    $scope._resources = Resource.query({}, function() {
        $scope.deferred.resolve();
        self.stop_spinner();
    });
    var set = function() {
        $scope.deferred.promise.then(function() {
            $scope.resources = $scope._resources.filter(self.filter_function, self);
        });
    };
    $scope.$on('$stateChangeSuccess', function() {
        self.update_param_id();
        set();
    });
};

// TeamController

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

// Season Controller

var SeasonController = function($scope, Resource, $state, $q) {
    ListController.call(this, $scope, Resource, $state, $q);

    $scope.$on('updateSeason', function(event, deferred, season) {
        $scope.deferred.promise.then(function() {
            for(var i in $scope._resources) {
                if($scope._resources[i].id == season.id) {
                    $scope._resources[i] = season;
                }
            }
        });
        deferred.resolve();
    });
};
SeasonController.prototype = Object.create(ListController.prototype);
SeasonController.prototype.update_state_machine = function(season_id) {
    this.$scope.state_machine(this.$state, season_id, this.$state.params.team_id, this.$state.params.player_id);
};
SeasonController.prototype.stop_spinner = function() {
    $('.season .panel .spinner').css('display', 'none');
};
SeasonController.prototype.update_param_id = function() {
    if(this.$state.params.season_id) {
        this.$scope.selected.id = this.$state.params.season_id;
    }
};
SeasonController.prototype.filter_function = function(season) {
    if(this.$state.params.team_id) {
        for(var i in season.teams) {
            if(season.teams[i].id == this.$state.params.team_id) {
                if(this.$state.params.player_id) {
                    for(var j in season.players) {
                        if(this.$state.params.player_id == season.players[j]) {
                            return season;
                        }
                    }
                } else {
                    return season;
                }
            }
        }
        return null;
    } else if(this.$state.params.player_id) {
        for(var k in season.players) {
            if(this.$state.params.player_id == season.players[k]) {
                return season;
            }
        }
        return null;
    } else {
        return season;
    }
};
controllers.controller('SeasonController', ['$scope', 'Season', '$state', '$q', SeasonController]);

var PlayerController = function($scope, Resource, $state, $q) {
    ListController.call(this, $scope, Resource, $state, $q);
};
PlayerController.prototype = Object.create(ListController.prototype);
PlayerController.prototype.update_state_machine = function(player_id) {
    this.$scope.state_machine(this.$state, this.$state.params.season_id, this.$state.params.team_id, player_id);
};
PlayerController.prototype.stop_spinner = function() {
    $('.player .panel .spinner').css('display', 'none');
};
PlayerController.prototype.update_param_id = function() {
    if(this.$state.params.player_id) {
        this.$scope.selected.id = this.$state.params.player_id;
    }
};
PlayerController.prototype.filter_function = function(player) {
    if(this.$state.params.team_id) {
        for(var i in player.season_teams) {
            if(player.season_teams[i].team == this.$state.params.team_id) {
                if(this.$state.params.season_id) {
                    if(player.season_teams[i].season == this.$state.params.season_id) {
                        return player;
                    }
                } else {
                    return player;
                }
            }
        }
        return null;
    } else if(this.$state.params.season_id) {
        for(var j in player.seasons) {
            if(player.seasons[j] == this.$state.params.season_id) {
                return player;
            }
        }
        return null;
    } else {
        return player;
    }
};
controllers.controller('PlayerController', ['$scope', 'Player', '$state', '$q', PlayerController]) ;    

controllers.controller('TeamDetail', ['$scope', 'TeamDetail', '$state', '$rootScope', '$q', function($scope, TeamDetail, $state, $rootScope, $q) {
    $scope.form = {season: 0};
    $scope.messages = {};
    $scope.team = TeamDetail.get({id: $state.params.team_id});
    $scope.add = function() {
        if($scope.form.season === 0) {
            $scope.messages.choose_error = true;
        } else {
            TeamDetail.add_season({'id': $scope.team.id, 'season': $scope.form.season}, function(team) {
                $scope.messages.success = true;
                $scope.form.season = 0;
                $scope.team = team;
                var promises = [];
                for(var i in team.seasons) {
                    var deferred = $q.defer();
                    promises.push(deferred);
                    $rootScope.$broadcast('updateSeason', deferred, team.seasons[i]);
                }
                $q.all(promises).then(function() {
                    $rootScope.$broadcast('$stateChangeSuccess');
                });
            }, function() {
                $scope.messages.an_error = true;
            });
        }
    };
    $scope.dismiss = function() {
        $scope.$dismiss();
    };
}]);

controllers.controller('PlayerDetail', ['$scope', 'PlayerDetail', '$state', '$rootScope', function($scope, PlayerDetail, $state, $rootScope) {
    $scope.form = {season: 0, team: 0};
    $scope.messages = {error: "Sorry, it didn't work"};
    $scope.player = PlayerDetail.get({id: $state.params.player_id});
    $scope.add = function() {
        if($scope.form.season === 0) {
            $scope.messages.choose_error = true;
        } else {
            PlayerDetail.add_season({'id': $scope.player.id, 'season': $scope.form.season}, function(player) {
                $scope.messages.success = true;
                $rootScope.$broadcast('$stateChangeSuccess');
                $scope.form.season = 0;
                $scope.player = player;
            }, function(resp) {
                $scope.messages.an_error = true;
                if(resp.data.error) {
                    $scope.messages.error = resp.data.error;
                }
            });
        }
    };
    $scope.dismiss = function() {
        $scope.$dismiss();
    };
}]);

/*
import common
t = common.Team.objects.get(id=1)
t.seasons.remove(t.seasons.all()[2])
exit()
*/
