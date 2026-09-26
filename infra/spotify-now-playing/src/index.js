const SPOTIFY_AUTHORIZE_URL = "https://accounts.spotify.com/authorize";
const SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token";
const SPOTIFY_NOW_URL =
  "https://api.spotify.com/v1/me/player/currently-playing?additional_types=track,episode";

const PUBLIC_ORIGIN = "https://marcelonicchio.com";
const REDIRECT_URI = "https://now.marcelonicchio.com/auth/callback";
const NOW_CACHE_SECONDS = 30;
const STATE_TTL_SECONDS = 600;
const ACCESS_TOKEN_SAFETY_MS = 90_000;

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: corsHeaders() });
    }

    if (request.method !== "GET") {
      return json({ status: "method_not_allowed" }, 405);
    }

    try {
      if (url.pathname === "/now-playing") {
        return await nowPlaying(request, env, ctx);
      }
      if (url.pathname === "/auth/login") {
        return await authLogin(url, env);
      }
      if (url.pathname === "/auth/callback") {
        return await authCallback(url, env);
      }
      if (url.pathname === "/auth/disconnect") {
        return await authDisconnect(url, env);
      }
      if (url.pathname === "/health") {
        return json({ ok: true, service: "marcelonicchio-now-playing" });
      }
      return json({ status: "not_found" }, 404);
    } catch (error) {
      console.error(error);
      return json({ status: "unavailable" }, 503);
    }
  },
};

async function nowPlaying(request, env, ctx) {
  const cache = caches.default;
  const cacheKey = new Request(new URL("/now-playing", request.url), {
    method: "GET",
  });
  const cached = await cache.match(cacheKey);
  if (cached) return cached;

  const token = await getAccessToken(env);
  if (token.status !== "ok") {
    return json({ status: token.status }, token.status === "reauth_required" ? 401 : 503);
  }

  let spotify = await fetch(SPOTIFY_NOW_URL, {
    headers: { Authorization: `Bearer ${token.access_token}` },
  });

  if (spotify.status === 401) {
    await env.SPOTIFY_STATE.delete("access_token");
    const retryToken = await getAccessToken(env);
    if (retryToken.status !== "ok") {
      return json({ status: retryToken.status }, 401);
    }
    spotify = await fetch(SPOTIFY_NOW_URL, {
      headers: { Authorization: `Bearer ${retryToken.access_token}` },
    });
  }

  if (spotify.status === 204) {
    return cacheResponse(cache, cacheKey, json({ status: "idle" }), ctx);
  }

  if (spotify.status === 429) {
    return json(
      {
        status: "rate_limited",
        retry_after: Number(spotify.headers.get("Retry-After") || 60),
      },
      429,
    );
  }

  if (!spotify.ok) {
    console.error("Spotify currently-playing failed", spotify.status, await spotify.text());
    return json({ status: "unavailable" }, 503);
  }

  const payload = await spotify.json();
  if (!payload || !payload.item) {
    return cacheResponse(cache, cacheKey, json({ status: "idle" }), ctx);
  }

  const item = normalizeItem(payload.item);
  if (!item) {
    return cacheResponse(cache, cacheKey, json({ status: "unsupported" }), ctx);
  }

  const response = json({
    status: payload.is_playing ? "playing" : "paused",
    is_playing: Boolean(payload.is_playing),
    progress_ms: payload.progress_ms ?? null,
    fetched_at: Date.now(),
    item,
  });

  return cacheResponse(cache, cacheKey, response, ctx);
}

function normalizeItem(item) {
  if (item.type === "track") {
    const image = bestImage(item.album?.images || []);
    return {
      type: "track",
      name: item.name,
      creators: (item.artists || []).map((artist) => artist.name),
      context_name: item.album?.name || "",
      duration_ms: item.duration_ms ?? null,
      explicit: Boolean(item.explicit),
      spotify_url: item.external_urls?.spotify || "",
      image,
    };
  }

  if (item.type === "episode") {
    const image = bestImage(item.images || item.show?.images || []);
    return {
      type: "episode",
      name: item.name,
      creators: item.show?.name ? [item.show.name] : [],
      context_name: item.show?.name || "",
      duration_ms: item.duration_ms ?? null,
      explicit: Boolean(item.explicit),
      spotify_url: item.external_urls?.spotify || "",
      image,
    };
  }

  return null;
}

function bestImage(images) {
  if (!images.length) return null;
  const sorted = [...images].sort((a, b) => (b.width || 0) - (a.width || 0));
  const image = sorted[0];
  return image?.url
    ? { url: image.url, width: image.width || null, height: image.height || null }
    : null;
}

async function getAccessToken(env) {
  const stored = await env.SPOTIFY_STATE.get("access_token", { type: "json" });
  if (
    stored?.access_token &&
    Number(stored.expires_at || 0) > Date.now() + ACCESS_TOKEN_SAFETY_MS
  ) {
    return { status: "ok", access_token: stored.access_token };
  }

  const refresh = await env.SPOTIFY_STATE.get("refresh_token", { type: "json" });
  if (!refresh?.refresh_token) return { status: "not_authorized" };

  const result = await fetch(SPOTIFY_TOKEN_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      Authorization: `Basic ${btoa(`${env.SPOTIFY_CLIENT_ID.trim()}:${env.SPOTIFY_CLIENT_SECRET.trim()}`)}`,
    },
    body: new URLSearchParams({
      grant_type: "refresh_token",
      refresh_token: refresh.refresh_token,
    }),
  });

  const body = await result.json().catch(() => ({}));

  if (!result.ok) {
    if (body.error === "invalid_grant") {
      await Promise.all([
        env.SPOTIFY_STATE.delete("refresh_token"),
        env.SPOTIFY_STATE.delete("access_token"),
      ]);
      return { status: "reauth_required" };
    }
    console.error("Spotify token refresh failed", result.status, body.error);
    return { status: "unavailable" };
  }

  if (body.refresh_token) {
    await env.SPOTIFY_STATE.put(
      "refresh_token",
      JSON.stringify({
        refresh_token: body.refresh_token,
        authorized_at: refresh.authorized_at || Date.now(),
      }),
    );
  }

  const access = {
    access_token: body.access_token,
    expires_at: Date.now() + Number(body.expires_in || 3600) * 1000,
  };
  await env.SPOTIFY_STATE.put("access_token", JSON.stringify(access));
  return { status: "ok", access_token: access.access_token };
}

async function authLogin(url, env) {
  if (!(await adminAuthorized(url.searchParams.get("key"), env.ADMIN_KEY))) {
    return new Response("Not found", { status: 404 });
  }

  const state = await createState(env.STATE_SECRET);
  const target = new URL(SPOTIFY_AUTHORIZE_URL);
  target.searchParams.set("client_id", env.SPOTIFY_CLIENT_ID);
  target.searchParams.set("response_type", "code");
  target.searchParams.set("redirect_uri", REDIRECT_URI);
  target.searchParams.set("scope", "user-read-currently-playing");
  target.searchParams.set("state", state);

  return Response.redirect(target.toString(), 302);
}

async function authCallback(url, env) {
  const error = url.searchParams.get("error");
  if (error) {
    return htmlPage("Autorização cancelada", "O Spotify não concedeu acesso ao status de reprodução.", 400);
  }

  const code = url.searchParams.get("code");
  const state = url.searchParams.get("state");
  if (!code || !(await validState(state, env.STATE_SECRET))) {
    return htmlPage("Autorização inválida", "O callback não passou na validação de segurança.", 400);
  }

  const result = await fetch(SPOTIFY_TOKEN_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      Authorization: `Basic ${btoa(`${env.SPOTIFY_CLIENT_ID.trim()}:${env.SPOTIFY_CLIENT_SECRET.trim()}`)}`,
    },
    body: new URLSearchParams({
      grant_type: "authorization_code",
      code,
      redirect_uri: REDIRECT_URI,
    }),
  });

  const body = await result.json().catch(() => ({}));
  if (!result.ok || !body.refresh_token || !body.access_token) {
    console.error("Spotify authorization exchange failed", result.status, body.error);
    return htmlPage("Falha na autorização", "Não foi possível concluir a conexão com o Spotify.", 502);
  }

  const now = Date.now();
  await Promise.all([
    env.SPOTIFY_STATE.put(
      "refresh_token",
      JSON.stringify({ refresh_token: body.refresh_token, authorized_at: now }),
    ),
    env.SPOTIFY_STATE.put(
      "access_token",
      JSON.stringify({
        access_token: body.access_token,
        expires_at: now + Number(body.expires_in || 3600) * 1000,
      }),
    ),
  ]);

  return htmlPage(
    "Spotify conectado",
    "O status “Ouvindo agora” está autorizado. Esta autorização precisará ser renovada em aproximadamente seis meses.",
    200,
  );
}

async function authDisconnect(url, env) {
  if (!(await adminAuthorized(url.searchParams.get("key"), env.ADMIN_KEY))) {
    return new Response("Not found", { status: 404 });
  }
  await Promise.all([
    env.SPOTIFY_STATE.delete("refresh_token"),
    env.SPOTIFY_STATE.delete("access_token"),
  ]);
  return htmlPage("Spotify desconectado", "Os tokens locais foram apagados do Worker.", 200);
}

async function createState(secret) {
  const issued = Math.floor(Date.now() / 1000).toString();
  const signature = await hmac(secret, issued);
  return `${issued}.${signature}`;
}

async function validState(state, secret) {
  if (!state || !state.includes(".")) return false;
  const [issued, signature] = state.split(".", 2);
  const timestamp = Number(issued);
  if (!Number.isFinite(timestamp)) return false;
  const age = Math.floor(Date.now() / 1000) - timestamp;
  if (age < 0 || age > STATE_TTL_SECONDS) return false;
  const expected = await hmac(secret, issued);
  return constantTimeEqual(signature, expected);
}

async function hmac(secret, value) {
  const encoder = new TextEncoder();
  const key = await crypto.subtle.importKey(
    "raw",
    encoder.encode(secret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"],
  );
  const signature = await crypto.subtle.sign("HMAC", key, encoder.encode(value));
  return base64url(new Uint8Array(signature));
}

async function adminAuthorized(provided, expected) {
  if (!provided || !expected) return false;
  const encoder = new TextEncoder();
  const [a, b] = await Promise.all([
    crypto.subtle.digest("SHA-256", encoder.encode(provided)),
    crypto.subtle.digest("SHA-256", encoder.encode(expected)),
  ]);
  return bytesEqual(new Uint8Array(a), new Uint8Array(b));
}

function constantTimeEqual(a, b) {
  return bytesEqual(new TextEncoder().encode(a), new TextEncoder().encode(b));
}

function bytesEqual(a, b) {
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i += 1) diff |= a[i] ^ b[i];
  return diff === 0;
}

function base64url(bytes) {
  let raw = "";
  for (const byte of bytes) raw += String.fromCharCode(byte);
  return btoa(raw).replaceAll("+", "-").replaceAll("/", "_").replace(/=+$/g, "");
}

function cacheResponse(cache, key, response, ctx) {
  const cached = new Response(response.body, response);
  cached.headers.set("Cache-Control", `public, max-age=${NOW_CACHE_SECONDS}`);
  ctx.waitUntil(cache.put(key, cached.clone()));
  return cached;
}

function corsHeaders() {
  return {
    "Access-Control-Allow-Origin": PUBLIC_ORIGIN,
    "Access-Control-Allow-Methods": "GET, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Vary": "Origin",
  };
}

function json(payload, status = 200) {
  return new Response(JSON.stringify(payload), {
    status,
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "Cache-Control": "no-store",
      "X-Content-Type-Options": "nosniff",
      ...corsHeaders(),
    },
  });
}

function htmlPage(title, message, status) {
  return new Response(
    `<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${escapeHtml(title)}</title><body style="font:16px system-ui;background:#0a0a0b;color:#f3f0eb;padding:48px;max-width:720px;margin:auto"><h1>${escapeHtml(title)}</h1><p>${escapeHtml(message)}</p></body></html>`,
    {
      status,
      headers: {
        "Content-Type": "text/html; charset=utf-8",
        "Cache-Control": "no-store",
        "X-Content-Type-Options": "nosniff",
      },
    },
  );
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}
