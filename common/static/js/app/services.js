var services = angular.module('appServices', ['djangoRESTResources']);

services.factory('Team', ['djResource',
  function($resource){
    return $resource('/rest/common/teams/:id', {}, {
      query: {method:'GET', params:{}, isArray:true}
    });
  }]);

services.factory('TeamDetail', ['djResource',
  function($resource){
    return $resource('/rest/common/teams/:id/detail/', {}, {
      query: {method:'GET', params:{}, isArray:true}
    });
  }]);

services.factory('Player', ['djResource',
  function($resource){
    return $resource('/rest/common/players/:id', {}, {
      query: {method:'GET', params:{}, isArray:true}
    });
  }]);

services.factory('Season', ['djResource',
  function($resource){
    return $resource('/rest/common/seasons/:id/', {}, {
      query: {method:'GET', params:{}, isArray:true}
    });
  }]);
