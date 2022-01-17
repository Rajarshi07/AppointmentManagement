var objQueryString = {};
function getParameterByName(name = "") {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}

function removeQString(key) {
    var urlValue = document.location.href;
    var searchUrl = location.search;//Get query string value
    if (key != "") {
        oldValue = getParameterByName(key);
        removeVal = key + "=" + oldValue;
        if (searchUrl.indexOf('?' + removeVal + '&') != "-1") {
            urlValue = urlValue.replace('?' + removeVal + '&', '?');
        }
        else if (searchUrl.indexOf('&' + removeVal + '&') != "-1") {
            urlValue = urlValue.replace('&' + removeVal + '&', '&');
        }
        else if (searchUrl.indexOf('?' + removeVal) != "-1") {
            urlValue = urlValue.replace('?' + removeVal, '');
        }
        else if (searchUrl.indexOf('&' + removeVal) != "-1") {
            urlValue = urlValue.replace('&' + removeVal, '');
        }
    }
    else {
        var searchUrl = location.search;
        urlValue = urlValue.replace(searchUrl, '');
    }
    history.replaceState({ state: 1, rand: Math.random() }, '', urlValue);
}

function changeUrl(key, value) {
    var searchUrl = location.search;  //Get query string value
    if (searchUrl.indexOf("?") == "-1") {
        var urlValue = '?' + key + '=' + value;
        history.pushState({ state: 1, rand: Math.random() }, '', urlValue);
    }
    else {  //Check for key in query string, if not present
        if (searchUrl.indexOf(key) == "-1") {
            var urlValue = searchUrl + '&' + key + '=' + value;
        }
        else {	//If key present in query string
            oldValue = getParameterByName(key);
            if (searchUrl.indexOf("?" + key + "=") != "-1") {
                urlValue = searchUrl.replace('?' + key + '=' + oldValue, '?' + key + '=' + value);
            }
            else {
                urlValue = searchUrl.replace('&' + key + '=' + oldValue, '&' + key + '=' + value);
            }
        }
        history.replaceState({ state: 1, rand: Math.random() }, '', urlValue);
    }
    objQueryString.key = value;
}