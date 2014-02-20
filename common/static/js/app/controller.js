var controllers = angular.module('appControllers', []);

controllers.controller('TeamController', ['$scope', 'Team', '$state', function($scope, Team, $state) {
    $scope.teams = Team.query();
    console.log('team', $state);
}]);

controllers.controller('SeasonController', ['$scope', 'Season', '$state', function($scope, Season, $state) {
    $scope.seasons = Season.query();
    console.log('season', $state);
}]);

controllers.controller('PlayerController', ['$scope', 'Player', '$state', function($scope, Player, $state) {
    $scope.players = Player.query();
    console.log('player', $state);
}]);
