var services = angular.module('appServices', ['ngResource']);

services.factory('Team', ['$resource',
  function($resource){
    return $resource('/rest/common/:teamId', {}, {
      query: {method:'GET', params:{teamId:'teams'}, isArray:true}
    });
  }]);

services.factory('Player', ['$resource',
  function($resource){
    return $resource('/rest/common/:playerId', {}, {
      query: {method:'GET', params:{playerId:'players'}, isArray:true}
    });
  }]);

services.factory('Season', ['$resource',
  function($resource){
    return $resource('/rest/common/:seasonId', {}, {
      query: {method:'GET', params:{seasonId:'seasons'}, isArray:true}
    });
  }]);
