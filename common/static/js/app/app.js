var app = angular.module('app', ['appControllers', 'appServices', 'djangoRESTResources']).run(function($http) {
    $http.defaults.headers.common.Authorization = 'Basic YWRtaW46cGFzc3dvcmQ=';
    $http.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
});
