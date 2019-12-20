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

var getAllCookies = function(){
  // var regExpert = /access_token=(.[^;]*)/ig;
  // var neededCookieValue = regExpert.exec(document.cookie);
  // console.log("AAAAAAAAAAAAAAAAAAA " + neededCookieValue[1]);


  if (document.cookie.includes("access_token")) {
    console.log("On access_token");
    // document.cookie = "bridgeCookieForAccess=abc";
    var regExpert = /access_token=(.[^;]*)/ig;
    var neededCookieValue = regExpert.exec(document.cookie);
    document.cookie = "bridgeCookieForAccess=" + neededCookieValue[1];
    // console.log("HALOOOOOOO: " + document.cookie.indexOf("bridgeCookieForAccess"));
  } else {
    console.log("Ei ollut access_tokenia");

  }
  var keyValuePairs = document.cookie.split(";");
  var cookiesList = [];
  for (var i=0; i<keyValuePairs.length; i++){
    var iterablePair = keyValuePairs[i].split("=");
    cookiesList[(iterablePair[0]+'').trim()] = unescape(iterablePair.slice(1).join('=').trim());
  }
  // console.log(cookiesList)
  return cookiesList;
}

function check_cookie_name(name) 
    {
      var match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
      if (match) {
        console.log(match[2]);
      }
      else{
           console.log('--something went wrong---');
      }
   }

// console.log("Onko tässä järkeä?" + check_cookie_name("refresh_token"));


console.log(getAllCookies());


// var cookiesInUse = getAllCookies();


// alert(JSON.stringify(cookiesInUse));


// var array = [" hello"," goodbye"," no"];
// array = array.map(function (el) {
//   return el.trim();
// });