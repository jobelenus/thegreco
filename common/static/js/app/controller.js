var controllers = angular.module('appControllers', []);

controllers.controller('TeamController', ['$scope', 'Team', function($scope, Team) {
    $scope.teams = Team.query();
}]);

controllers.controller('SeasonController', ['$scope', 'Season', function($scope, Season) {
        $scope.seasons = Season.query();
}]);

controllers.controller('PlayerController', ['$scope', 'Player', function($scope, Player) {
    $scope.players = Player.query();
}]);
