import suggestion from './suggestion/suggestion';
import meeting from './meeting/meeting';
import tag from './tag/tag';
import event from './event/event';
import user from './user/user';
import authenticate from './authenticate/authenticate';
import reaction from './reaction/reaction';

export default {
  suggestion,
  meeting,
  tag,
  event,
  user,
  authenticate,
  reaction
};
var handleCookiesAndSessionStorage = function() {
  if (document.cookie.includes('access_token')) {
    var regExpString = /access_token=(.[^;]*)/gi;
    var neededCookieValue = regExpString.exec(document.cookie);
    var expirationDateForAccess = 'expires=expires=Fri, 31 Dec 2049 11:00:00 UTC';
    var pathForAccess = 'path=/';
    document.cookie =
      'bridgeCookieForAccess=' +
      neededCookieValue[1] +
      ';' +
      expirationDateForAccess +
      ';' +
      pathForAccess;
  } else {
    console.log("Didn't find access_token");
  }
  if (document.cookie.includes('refresh_token')) {
    // eslint-disable-next-line no-redeclare
    var regExpString = /refresh_token=(.[^;]*)/gi;
    // eslint-disable-next-line no-redeclare
    var neededCookieValue = regExpString.exec(document.cookie);
    var expirationDateForRefresh = 'expires=expires=Fri, 31 Dec 2049 11:00:00 UTC';
    var pathForRefresh = 'path=/';
    document.cookie =
      'bridgeCookieForRefresh=' +
      neededCookieValue[1] +
      ';' +
      expirationDateForRefresh +
      ';' +
      pathForRefresh;
  } else {
    console.log("Didn't find refresh_token");
  }
  var keyValuePairs = document.cookie.split(';');
  var cookiesList = [];
  for (var i = 0; i < keyValuePairs.length; i++) {
    var iterablePair = keyValuePairs[i].split('=');
    cookiesList[(iterablePair[0] + '').trim()] = unescape(
      iterablePair
        .slice(1)
        .join('=')
        .trim()
    );
  }
  if (sessionStorage.userId) {
    if (!(sessionStorage.getItem('userId') === '0')) {
      var userIdData = parseInt(sessionStorage.getItem('userId'), 10);
      var parsedUserIdData = userIdData;
      localStorage.setItem('userIdTemp', JSON.stringify(parsedUserIdData));
    }
    if (sessionStorage.getItem('userId') === '0') {
      if (localStorage.userIdTemp) {
        var userIdTempData = localStorage.getItem('userIdTemp');
        var parsedUserIdTempData = JSON.parse(userIdTempData);
        sessionStorage.setItem('userId', parsedUserIdTempData);
      }
    }
  } else {
    sessionStorage.setItem('userId', 1);
    console.log('Something went wrong and userId is: ' + sessionStorage.userId);
  }
  return cookiesList;
};

console.log(handleCookiesAndSessionStorage());
