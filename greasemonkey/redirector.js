// ==UserScript==
// @name        YT2Invidio
// @namespace   de.izzysoft
// @author      Izzy
// @description Point YouTube links to Invidious, Twitter to Nitter, Instagram to Bibliogram, Reddit to Teddit
// @license     CC BY-NC-SA
// @include     *
// @version     1.5.3
// @run-at      document-idle
// @grant       unsafeWindow
// @homepageURL https://codeberg.org/izzy/userscripts
// @require     https://greasemonkey.github.io/gm4-polyfill/gm4-polyfill.js
// ==/UserScript==

// Default Config
const defaultConfig = {
  hosts: {invidious: "invidious.datgizmo.de", nitter: "nitter.datgizmo.de", bibliogram: "bibliogram.datgizmo.de", teddit: "teddit.net"},
  invProxy: 0
};

console.log(defaultConfig.hosts);
//console.log(obj.hosts.hasOwnProperty('bibliogram')); // true


// Get the Invidious instance to use for rewrite
function doRewrite() {
  GM.getValue('YT2IConfig',JSON.stringify(defaultConfig)).then(function(result) {
    rewriteLinks(result);
  });
}

// Do the actual rewrite
function rewriteLinks(config) {
  console.log(`Using '${config}' for rewrite`);
  var cfg = JSON.parse(config);
  var videohost = cfg.hosts.invidious;
  var nitterhost = cfg.hosts.nitter;
  var bibliogramhost = cfg.hosts.bibliogram;
  var teddithost = cfg.hosts.teddit;
  var invProxy = 'local=0';
  if ( cfg.invProxy == 1 ) { invProxy = 'local=1'; }
  console.log('Invidious: '+videohost+', Params: '+invProxy);
  console.log('Nitter: '+nitterhost);
  console.log('Bibliogram: '+bibliogramhost);
  console.log('Teddit: '+teddithost);
  // --=[ document links ]=--
  console.log('Checking '+document.links.length+' links for YT, Twitter, Insta, Reddit & Co.');
  for(var i = 0; i < document.links.length; i++) {
    var elem = document.links[i];

    if (videohost != '' && elem.href.match(/((www|m)\.)?youtube.com(\/(watch\?v|playlist\?list)=[a-z0-9_-]+)/i)) {
      if (location.hostname != videohost) { elem.href='https://'+videohost+RegExp.$3+'&'+invProxy; }
    } else if (videohost != '' && elem.href.match(/((www|m)\.)?youtu.be\/([a-z0-9_-]+)/i)) {
      if (location.hostname != videohost) { elem.href='https://'+videohost+'/watch?v='+RegExp.$3+'?'+invProxy; }
    } else if (videohost != '' && elem.href.match(/((www|m)\.)?youtube.com(\/channel\/[a-z0-9_-]+)/i)) {
      if (location.hostname != videohost) { elem.href='https://'+videohost+RegExp.$3+'?'+invProxy; }

    // Twitter
    } else if (nitterhost != '' && elem.href.match(/(mobile\.)?twitter\.com\/([^&#]+)/i)) {
      if (location.hostname != nitterhost) elem.href='https://'+nitterhost+'/'+RegExp.$2;
    }

    // Bibliogram
    else if (bibliogramhost != '' && elem.href.match(/(www\.)?instagram\.com\/(p|tv)\/([^&#/]+)/i)) { // profile
      if (location.hostname != bibliogramhost) {
        elem.href = 'https://'+bibliogramhost+'/p/' + RegExp.$3;
      }
    } else if (bibliogramhost != '' && elem.href.match(/(www\.)?instagram\.com\/([^&#/]+)/i)) { // image or video
      if (location.hostname != bibliogramhost) {
        elem.href = 'https://'+bibliogramhost+'/u/' + RegExp.$2;
      }
    }

    // Teddit
    else if (teddithost != '' && elem.href.match(/((www|old)\.)?reddit.com\/(.*)/i)) {
      if (location.hostname != teddithost) { elem.href = 'https://'+teddithost+'/'+RegExp.$3; }
    }

  }

  // --=[ embedded links ]=--
  // based on https://greasyfork.org/en/scripts/394841-youtube-to-invidio-us-embed
  if (videohost != '')  {
    var src, dataSrc, iframes = document.getElementsByTagName('iframe');
    var embProxy
    console.log('Checking '+iframes.length+' frames for embedded videos');
    for (var i = 0; i < iframes.length; i++) {
      src = iframes[i].getAttribute('src');
      dataSrc = false;
      if ( src == null ) { src = iframes[i].getAttribute('data-s9e-mediaembed-src'); dataSrc = true; }
      if ( src == null ) continue;
      if ( src.match(/((www|m)\.)?youtube.com(\/(watch\?v|playlist\?list)=[a-z0-9_-]+)/i) || src.match(/((www|m)\.)?youtube.com(\/(channel|embed)\/[a-z0-9_-]+)/i) ) {
        if ( RegExp.$4 == 'channel' || RegExp.$4 == 'embed' ) { embProxy = '?'+invProxy; }
        else { embProxy = '&'+invProxy; }
        if ( dataSrc ) {
          iframes[i].setAttribute('data-s9e-mediaembed-src','https://'+videohost+RegExp.$3+embProxy);
        } else {
          iframes[i].setAttribute('src','https://'+videohost+RegExp.$3+embProxy);
        }
        iframes[i].setAttribute('frameborder', '0');
        iframes[i].setAttribute('allowfullscreen', '1');
      }
    }
  }

  console.log('Rewrite done.');
}

doRewrite()
