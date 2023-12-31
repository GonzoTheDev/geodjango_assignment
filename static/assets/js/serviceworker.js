// Define the name of the cache
const CACHE_NAME = 'geodjango-assignment-v3';

// Define URLs to cache
const urlsToCache = [
  '/static/assets/style.css', 
];

// Install a service worker
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

// Cache and return requests
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);

  // Check for POST request or login/logout URL
  if (event.request.method !== 'GET' || url.pathname.startsWith('/accounts/login') || 
      url.pathname.startsWith('/accounts/logout') ||
      url.pathname.startsWith('/admin/login') || 
      url.pathname.startsWith('/admin/logout')) {
    // Handle via network
    event.respondWith(fetch(event.request));
    return;
  }

  // Apply network-first strategy for login/logout/admin pages
  if (url.pathname.startsWith('/accounts/login') || url.pathname.startsWith('/accounts/logout') ||
      url.pathname.startsWith('/admin/login') || url.pathname.startsWith('/admin/logout') || url.pathname.startsWith('/')) {
    event.respondWith(
      fetch(event.request).catch(() => caches.match(event.request))
    );
    return;
  }

  // Apply cache-first strategy for other requests
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        if (response) {
          // Cache hit - return response
          return response;
        }

        // Fetch and cache
        const fetchRequest = event.request.clone();
        return fetch(fetchRequest).then(
          response => {
            if (!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }

            const responseToCache = response.clone();
            caches.open(CACHE_NAME)
              .then(cache => {
                cache.put(event.request, responseToCache);
              });

            return response;
          }
        );
      })
  );
});

// Update a service worker
self.addEventListener('activate', event => {
  const cacheWhitelist = [CACHE_NAME];

  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

