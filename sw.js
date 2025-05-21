var VERSION = 'v2';

var cacheFirstFiles = [
  // ADDME: Add paths and URLs to pull from cache first if it has been loaded before. Else fetch from network.
  // If loading from cache, fetch from network in the background to update the resource. Examples:
  // 'assets/img/logo.png',
  // 'assets/models/controller.gltf',
  'static/logo.png',
  'static/512x512.png',
  'static/logo.png',
  'static/512x512.png',
  'static/images/favicon.ico',
  'static/images/focus_sport-fb-removebg-preview.png',
  'static/images/businesswoman-using-tablet-analysis.jpg',
  'static/images/images-removebg-preview.png',
  'static/images/journalist-is-searching-for-false-news-10961423-8798212.png',
  'static/images/images.jpg',
  'static/images/faq_graphic.jpg',
  'static/css/bootstrap.min.css',
  'static/css/bootstrap-icons.css',
  'static/css/main.css',
  'static/css/templatemo-topic-listing.css',
  'static/js/jquery.min.js',
  'static/js/bootstrap.bundle.min.js',
  'static/js/jquery.sticky.js',
  'static/js/click-scroll.js',
  'static/js/custom.js',
  'static/js/script.js',
  'static/manifest.json',
  'static/app.js'
];

var networkFirstFiles = [
  // ADDME: Add paths and URLs to pull from network first. Else fall back to cache if offline. Examples:
  // 'index.html',
  // 'build/build.js',
  // 'css/index.css'
  'templates/index.html',
  'templates/index1.html',
  'templates/takafa.html',
  'templates/news.html',
  'templates/contact.html',
  'templates/arabec.html',
  'templates/login.html',
  'templates/post-add.html'
];

// Below is the service worker code.

var cacheFiles = cacheFirstFiles.concat(networkFirstFiles);

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(VERSION).then(cache => {
      return cache.addAll(cacheFiles);
    })
  );
});

self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') { return; }
  if (networkFirstFiles.indexOf(event.request.url) !== -1) {
    event.respondWith(networkElseCache(event));
  } else if (cacheFirstFiles.indexOf(event.request.url) !== -1) {
    event.respondWith(cacheElseNetwork(event));
  } else {
    event.respondWith(fetch(event.request));
  }
});

// If cache else network.
// For images and assets that are not critical to be fully up-to-date.
// developers.google.com/web/fundamentals/instant-and-offline/offline-cookbook/
// #cache-falling-back-to-network
function cacheElseNetwork (event) {
  return caches.match(event.request).then(response => {
    function fetchAndCache () {
       return fetch(event.request).then(response => {
        // Update cache.
        caches.open(VERSION).then(cache => cache.put(event.request, response.clone()));
        return response;
      });
    }

    // If not exist in cache, fetch.
    if (!response) { return fetchAndCache(); }

    // If exists in cache, return from cache while updating cache in background.
    fetchAndCache();
    return response;
  });
}

// If network else cache.
// For assets we prefer to be up-to-date (i.e., JavaScript file).
function networkElseCache (event) {
  return caches.match(event.request).then(match => {
    if (!match) { return fetch(event.request); }
    return fetch(event.request).then(response => {
      // Update cache.
      caches.open(VERSION).then(cache => cache.put(event.request, response.clone()));
      return response;
    }) || response;
  });
}
