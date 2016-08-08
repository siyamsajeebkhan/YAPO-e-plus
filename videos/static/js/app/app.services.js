angular.module('helper', []).factory('helperService', function ($rootScope, $localStorage, $sessionStorage) {
    $rootScope.$storage = $sessionStorage;
    
    $rootScope.savedData = {};
    $rootScope.savedData2 = [];

    // $rootScope.$storage.scArray ;
    

    function set(data) {
        $rootScope.$storage.scArray = data;
        
        // console.log('helperService data1 is' + angular.toJson(savedData));
    }

    function get() {
        return $rootScope.$storage.scArray;
    }


    function set2(data) {
        // console.log('helperService import data2 is' + angular.toJson(data));
        $rootScope.savedData2 = data;
        // console.log('helperService data2 is' + angular.toJson(savedData2));
    }

    function get2() {
        return $rootScope.savedData2;
    }


    function packageDataAndHeaders(data, headers) {
        data = angular.fromJson(data);


        // console.log("This is headers: " + angular.toJson(headers()));
        //
        // console.log("Data length: " + data.length);

        var b = [data, "-6"];

        // console.log("b[0].length: " + b[0].length);

        if (headers().link != undefined) {

            b[1] = headers().link;


        }

        return b;
    }

    function resourceToArray(resource){
        var ans = [];
        for (var i in resource){
            if (angular.isObject(resource[i])){
                ans.push(resource[i])
            }
        }
        return ans;
    }

    return {
        set: set,
        get: get,
        set2: set2,
        get2: get2,
        packageDataAndHeaders: packageDataAndHeaders,
        resourceToArray: resourceToArray
    }

});


angular.module('pager', []).factory('pagerService', function (Actor, ActorAlias, ActorTag, Scene, SceneTag, Website) {

        var _prevPage = "";
        var _nextPage = "";
        var _currentPage = 0;
        var _pageOffset = 0;
        var _pageLimit = 50;

        var _callId = 0;
        var _maxPage = -6;


        var itemsToAdd = [];
        var _temp = {};

        var _pageType = "";
        var _searchTerm = "";
        var _pk = "";
        var _sortBy = "";
        var _actorTagId = "";
        var _sceneId = "";
        var _actorId = "";
        var _sceneTagId = "";
        var _websiteId = "";
        var _folderId = "";
    var _runnerUp = "";

        function nextPageInput(input) {

            if ("currentPage" in input) {
                if (input["currentPage"] != undefined) {
                    _currentPage = input["currentPage"];
                    if (_currentPage == '0') {
                        _pageOffset = 0;
                        _searchTerm = "";
                        _pk = "";
                        _actorTagId = "";
                        _sceneId = "";
                        _actorId = "";
                        _sceneTagId = "";
                        _websiteId = "";
                        _folderId = "";

                    }
                }

            }

            if ("pageType" in input) {
                _pageType = input["pageType"];
            }

            if ("searchTerm" in input) {
                _searchTerm = input["searchTerm"];
            }

            if ("pk" in input) {
                _pk = input["pk"];
            }

            if ("sortBy" in input) {
                _sortBy = input["sortBy"];
            }


            if ("searchTerm" in input) {
                _searchTerm = input["searchTerm"];
            }

            if ("actorTag" in input) {
                if (input["actorTag"] != undefined) {
                    _actorTagId = input["actorTag"].id;
                }

            }

            if ("scene" in input) {
                if (input["scene"] != undefined) {
                    _sceneId = input["scene"].id;
                }

            }

            if ("actor" in input) {
                if (input["actor"] != undefined) {
                    _actorId = input["actor"].id;
                }
            }


            if ("sceneTag" in input) {

                if (input["sceneTag"] != undefined) {
                    _sceneTagId = input["sceneTag"].id;
                }

            }

            if ("website" in input) {
                if (input["website"] != undefined) {
                    _websiteId = input["website"].id;
                }

            }

            if ("folder" in input) {
                if (input["folder"] != undefined) {
                    if (angular.isObject(input["folder"])) {
                        _folderId = input["folder"].id;
                    } else {
                        _folderId = input["folder"];
                    }
                    
                }

            }

            if ("isRunnerUp" in input) {
                if (input["isRunnerUp"] != undefined) {
                    if (input["isRunnerUp"]) {
                        _runnerUp = 1
                    } else {
                        _runnerUp = ""
                    }

                } else {
                    _runnerUp = ""
                }

            }


        }


        function getNextPage(input) {

            nextPageInput(input);

            console.log("Current page is: " + _currentPage + " Max page is: " + _maxPage);
            _callId++;
            console.log("app.service: Call id is: " + _callId + " app-service: nextPageTriggered");

            if (_currentPage >= _maxPage && _maxPage > 0) {
                console.log("app.service:  Call id is: " + _callId + " currentPage is : " + currentPage + " and maxPage is: " + _maxPage);
                return;
            }


            if (_currentPage != 0) {
                _pageOffset = _pageLimit * (_currentPage - 1);
                _currentPage = _currentPage + 1;
            } else {
                _pageOffset = _pageLimit * _currentPage;
                _currentPage = _currentPage + 1;
            }


            if (_pageType == 'Actor') {

                itemsToAdd = Actor.query({
                    offset: _pageOffset,
                    limit: _pageLimit,
                    search: _searchTerm,
                    actor_tags: _actorTagId,
                    scenes: _sceneId,
                    pk: _pk,
                    sortBy: _sortBy,
                    is_runner_up: _runnerUp
                    // ordering: _ordering
                });

            } else if (_pageType == 'ActorAlias') {
                itemsToAdd = ActorAlias.query({
                    offset: _pageOffset,
                    limit: _pageLimit,
                    search: _searchTerm,
                    actors: _actorId,

                    // ordering: _ordering

                })
            } else if (_pageType == 'ActorTag') {
                itemsToAdd = ActorTag.query({
                    offset: _pageOffset,
                    limit: _pageLimit,
                    actors: _actorId,
                    search: _searchTerm,
                    sortBy: _sortBy,
                    is_runner_up: _runnerUp
                    // ordering: _ordering
                })
            } else if (_pageType == 'Scene') {
                itemsToAdd = Scene.query({
                    offset: _pageOffset,
                    limit: _pageLimit,
                    actors: _actorId,
                    scene_tags: _sceneTagId,
                    websites: _websiteId,
                    folders_in_tree: _folderId,
                    search: _searchTerm,
                    sortBy: _sortBy,
                    is_runner_up: _runnerUp

                })
            } else if (_pageType == 'SceneTag') {
                itemsToAdd = SceneTag.query({
                    offset: _pageOffset,
                    limit: _pageLimit,
                    actors: _actorId,
                    scenes: _sceneId,
                    search: _searchTerm,
                    sortBy: _sortBy,
                    is_runner_up: _runnerUp
                })
            } else if (_pageType == 'Website') {
                itemsToAdd = Website.query({
                    offset: _pageOffset,
                    limit: _pageLimit,
                    scenes: _sceneId,
                    search: _searchTerm,
                    sortBy: _sortBy,
                    is_runner_up: _runnerUp
                })
            }


            return itemsToAdd;

        }

        return {
            getNextPage: getNextPage
        }

    }
);


angular.module('scopeWatch', []).factory('scopeWatchService', function ($rootScope, Actor) {

    function sceneChanged(newScene) {

        console.log("app-service-scopeWatch: sceneChanged was triggered! ");
        $rootScope.$broadcast("sceneChanged", newScene);

    }

    function addActorToList(actorToAdd) {

        console.log("app-service-scopeWatch: addActorToList was triggered! ");
        $rootScope.$broadcast("addActorToList", actorToAdd);

    }

    function sceneLoaded(scene) {

        console.log("app-service-scopeWatch: sceneLoaded was triggered! ");
        $rootScope.$broadcast("sceneLoaded", scene);

    }


    function actorTagLoaded(actorTag) {

        console.log("app-service-scopeWatch: actorTagLoaded was triggered! ");
        $rootScope.$broadcast("actorTagLoaded", actorTag);

    }

    function actorLoaded(actor) {

        console.log("app-service-scopeWatch: actorLoaded was triggered! ");
        $rootScope.$broadcast("actorLoaded", actor);

    }

    function actorChaned(actor) {

        console.log("app-service-scopeWatch: actorChaned was triggered! ");
        $rootScope.$broadcast("actorChaned", actor);

    }

    function actorTagSelected(actorTag) {

        console.log("app-service-scopeWatch: actorTagSelected was triggered! ");
        $rootScope.$broadcast("actorTagSelected", actorTag);

    }

    function addActorTagToList(actorTag) {

        console.log("app-service-scopeWatch: addActorTagToList was triggered! ");
        $rootScope.$broadcast("addActorTagToList", actorTag);

    }

    function searchTermChanged(searchTerm) {

        console.log("app-service-scopeWatch: searchTermChanged was triggered! ");
        $rootScope.$broadcast("searchTermChanged", searchTerm);

    }

    function sortOrderChanged(sortOrderChanged) {

        console.log("app-service-scopeWatch: searchTermChanged was triggered! ");
        $rootScope.$broadcast("sortOrderChanged", sortOrderChanged);

    }

    function sceneTagLoaded(sceneTag) {

        console.log("app-service-scopeWatch: searchTermChanged was triggered! ");
        $rootScope.$broadcast("sceneTagLoaded", sceneTag);

    }

    function websiteLoaded(website) {

        console.log("app-service-scopeWatch: websiteLoaded was triggered! ");
        $rootScope.$broadcast("websiteLoaded", website);

    }


    function actorSelected(actor) {

        console.log("app-service-scopeWatch: actorSelected was triggered! ");
        $rootScope.$broadcast("actorSelected", actor);

    }


    function websiteSelected(website) {

        console.log("app-service-scopeWatch: websiteSelected was triggered! ");
        $rootScope.$broadcast("websiteSelected", website);

    }

    function sceneTagSelected(sceneTag) {

        console.log("app-service-scopeWatch: websiteSelected was triggered! ");
        $rootScope.$broadcast("sceneTagSelected", sceneTag);

    }

    function addWebsiteToList(website) {

        console.log("app-service-scopeWatch: addWebsiteToList was triggered! ");
        $rootScope.$broadcast("addWebsiteToList", website);

    }

    function addSceneTagToList(sceneTag) {

        console.log("app-service-scopeWatch: addSceneTagToList was triggered! ");
        $rootScope.$broadcast("addSceneTagToList", sceneTag);

    }

    function folderOpened(folder) {

        console.log("app-service-scopeWatch: folderOpened was triggered! ");
        $rootScope.$broadcast("folderOpened", folder);

    }


    function paginationInit(paginationInfo) {

        console.log("app-service-scopeWatch: paginationInit was triggered! ");
        $rootScope.$broadcast("paginationInit", paginationInfo);

    }

    function paginationChange(paginationInfo) {

        console.log("app-service-scopeWatch: paginationChange was triggered! ");
        $rootScope.$broadcast("paginationChange", paginationInfo);

    }

    function addAliasToList(aliasToAdd) {

        console.log("app-service-scopeWatch: addAliasToList was triggered! ");
        $rootScope.$broadcast("addAliasToList", aliasToAdd);

    }

    function runnerUpChanged(runnerUp) {

        console.log("app-service-scopeWatch: runnerUpChanged was triggered! ");
        $rootScope.$broadcast("runnerUpChanged", runnerUp);

    }


    return {
        sceneChanged: sceneChanged,
        addActorToList: addActorToList,
        sceneLoaded: sceneLoaded,
        actorTagLoaded: actorTagLoaded,
        actorLoaded: actorLoaded,
        actorChaned: actorChaned,
        actorTagSelected: actorTagSelected,
        addActorTagToList: addActorTagToList,
        searchTermChanged: searchTermChanged,
        sortOrderChanged: sortOrderChanged,
        sceneTagLoaded: sceneTagLoaded,
        websiteLoaded: websiteLoaded,
        actorSelected: actorSelected,
        websiteSelected: websiteSelected,
        sceneTagSelected: sceneTagSelected,
        addWebsiteToList: addWebsiteToList,
        addSceneTagToList: addSceneTagToList,
        folderOpened: folderOpened,
        paginationInit: paginationInit,
        paginationChange: paginationChange,
        addAliasToList: addAliasToList,
        runnerUpChanged: runnerUpChanged


    }

});