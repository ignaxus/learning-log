const CACHE_NAME = "learning-log-v1";
const urlsToCache = [
    "/",
    "/static/manifest.json",
    "/static/offline.html",
    "/static/icon/favicon.ico",
    "/static/icon/icon-192.png",
    "/static/icon/icon-512.png",
    "/static/icon/apple-touch-icon.png"
];

// 逐个缓存，避免 addAll 原子失败导致全部丢弃
self.addEventListener("install", (event) => {
    event.waitUntil(
        (async () => {
            const cache = await caches.open(CACHE_NAME);
            const results = await Promise.allSettled(
                urlsToCache.map((url) =>
                    cache.add(url).catch((err) => {
                        console.warn(`[SW] 缓存失败: ${url}`, err);
                    })
                )
            );
            const failed = results.filter((r) => r.status === "rejected");
            if (failed.length > 0) {
                console.warn(`[SW] ${failed.length} 个资源缓存失败，继续安装`);
            }
        })()
    );
    self.skipWaiting();
});

// 激活时清理旧缓存
self.addEventListener("activate", (event) => {
    event.waitUntil(
        (async () => {
            const cacheNames = await caches.keys();
            await Promise.all(
                cacheNames
                    .filter((name) => name !== CACHE_NAME)
                    .map((name) => caches.delete(name))
            );
        })()
    );
    self.clients.claim();
});

// 拦截网络请求
self.addEventListener("fetch", (event) => {
    const request = event.request;

    // 不拦截 chrome-extension:// 等非 http(s) 请求
    if (!request.url.startsWith("http")) return;

    event.respondWith(networkFirstWithOfflineFallback(event));
});

async function networkFirstWithOfflineFallback(event) {
    const request = event.request;
    const isNavigation = request.mode === "navigate";

    try {
        const response = await fetch(request);

        // 仅缓存成功的 GET 响应
        if (request.method === "GET" && response.ok) {
            const cache = await caches.open(CACHE_NAME);
            // 导航请求只缓存 / 首页，避免缓存大量页面
            if (!isNavigation || request.url === new URL("/", location.origin).href) {
                cache.put(request, response.clone());
            }
        }

        return response;
    } catch {
        // 网络失败 → 尝试缓存
        const cached = await caches.match(request);
        if (cached) return cached;

        // 缓存未命中
        if (isNavigation) {
            // 导航请求 → 返回离线兜底页面
            const offline = await caches.match("/static/offline.html");
            return offline || new Response("离线中", { status: 503 });
        }

        // 子资源（图片/字体等）→ 返回空响应，避免把 HTML 当图片解析
        return new Response("", { status: 408, statusText: "Request Timeout" });
    }
}