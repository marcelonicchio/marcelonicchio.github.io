# Marcelo Nicchio — Now Playing Worker

Small Cloudflare Worker used by the HUB home page to expose Marcelo's current Spotify playback status without exposing Spotify credentials in the public GitHub Pages repository.

## Architecture

Spotify Web API -> Cloudflare Worker -> https://marcelonicchio.com/

The public endpoint is:

- `GET /now-playing`

Owner-only OAuth endpoints:

- `GET /auth/login?key=<ADMIN_KEY>`
- `GET /auth/callback`
- `GET /auth/disconnect?key=<ADMIN_KEY>`

## Spotify app

Create a Development Mode app in Spotify for Developers.

Recommended values:

- App name: `Marcelo Nicchio Now Playing`
- Website: `https://marcelonicchio.com/`
- Redirect URI: `https://now.marcelonicchio.com/auth/callback`
- Scope requested by the Worker: `user-read-currently-playing`

Development Mode currently requires the app owner to have Spotify Premium.

## Cloudflare

Deploy this directory as a Worker named `marcelonicchio-now-playing`.

Bind one Workers KV namespace as:

- `SPOTIFY_STATE`

Set these Worker secrets:

- `SPOTIFY_CLIENT_ID`
- `SPOTIFY_CLIENT_SECRET`
- `ADMIN_KEY` — a long random private value used only by Marcelo for owner routes.
- `STATE_SECRET` — another long random private value used to sign OAuth state.

Then add the Custom Domain:

- `now.marcelonicchio.com`

Do not commit any secret or refresh token to GitHub.

## First authorization

After the Worker and Custom Domain are live, visit:

`https://now.marcelonicchio.com/auth/login?key=<ADMIN_KEY>`

Authorize the Spotify account. The callback stores the refresh token in Workers KV.

Spotify refresh tokens currently expire after six months. Revisit the same owner login URL when reauthorization is required.

## Data behavior

The Worker returns only the data required by the public Home widget: current item type, title, creators, album/show name, Spotify URL, artwork URL, playback state and timing fields.

No Spotify audio is proxied or streamed by this Worker.
