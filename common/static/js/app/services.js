var services = angular.module('appServices', ['djangoRESTResources']);

services.factory('Team', ['djResource',
  function($resource){
    return $resource('/rest/common/:teamId/', {}, {
      query: {method:'GET', params:{teamId:'teams'}, isArray:true}
    });
  }]);

services.factory('Player', ['djResource',
  function($resource){
    return $resource('/rest/common/:playerId/', {}, {
      query: {method:'GET', params:{playerId:'players'}, isArray:true}
    });
  }]);

services.factory('Season', ['djResource',
  function($resource){
    return $resource('/rest/common/:seasonId/', {}, {
      query: {method:'GET', params:{seasonId:'seasons'}, isArray:true}
    });
  }]);
