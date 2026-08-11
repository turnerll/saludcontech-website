// Reverse proxy for PostHog: keeps analytics traffic first-party so ad blockers
// do not drop it. Mirrors the COMPA '/ingest' pattern. PostHog uses the
// X-Forwarded-For header for IP-based geolocation, so forward the client IP.
const POSTHOG_HOST = "https://us.i.posthog.com";

export async function onRequest(context) {
  const url = new URL(context.request.url);
  const path = url.pathname.replace(/^\/ingest/, "") || "/";
  const target = POSTHOG_HOST + path + url.search;

  const headers = new Headers(context.request.headers);
  headers.set("host", new URL(POSTHOG_HOST).host);
  const clientIp = context.request.headers.get("cf-connecting-ip");
  if (clientIp) headers.set("x-forwarded-for", clientIp);

  const init = {
    method: context.request.method,
    headers: headers,
    redirect: "manual",
  };
  if (context.request.method !== "GET" && context.request.method !== "HEAD") {
    init.body = context.request.body;
  }

  return fetch(target, init);
}
