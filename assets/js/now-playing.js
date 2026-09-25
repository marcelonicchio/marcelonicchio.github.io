(() => {
  const widgets = [...document.querySelectorAll("[data-now-playing]")];
  if (!widgets.length) return;

  const POLL_MS = 60_000;

  const update = async (widget) => {
    const endpoint = widget.dataset.endpoint;
    if (!endpoint || document.visibilityState !== "visible") return;

    try {
      const response = await fetch(endpoint, {
        method: "GET",
        mode: "cors",
        credentials: "omit",
        cache: "no-store",
        headers: { Accept: "application/json" },
      });

      if (!response.ok) {
        widget.hidden = true;
        return;
      }

      const payload = await response.json();
      if (payload.status !== "playing" || !payload.item?.spotify_url) {
        widget.hidden = true;
        return;
      }

      const item = payload.item;
      const link = widget.querySelector("[data-now-playing-link]");
      const artwork = widget.querySelector("[data-now-playing-art]");
      const title = widget.querySelector("[data-now-playing-title]");
      const creator = widget.querySelector("[data-now-playing-creator]");
      const context = widget.querySelector("[data-now-playing-context]");

      link.href = item.spotify_url;
      title.textContent = item.name || "";
      creator.textContent = (item.creators || []).join(", ");
      context.textContent = item.context_name || "";

      if (item.image?.url) {
        artwork.src = item.image.url;
        artwork.alt = "";
        artwork.hidden = false;
      } else {
        artwork.removeAttribute("src");
        artwork.hidden = true;
      }

      widget.hidden = false;
    } catch {
      widget.hidden = true;
    }
  };

  const refreshAll = () => widgets.forEach(update);
  refreshAll();

  const timer = window.setInterval(refreshAll, POLL_MS);

  document.addEventListener("visibilitychange", () => {
    if (document.visibilityState === "visible") refreshAll();
  });

  window.addEventListener("pagehide", () => window.clearInterval(timer), { once: true });
})();
