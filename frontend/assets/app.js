// Configurable: si sirves el frontend desde otro puerto/host, ajusta esto.
const API_BASE = "http://localhost:8000"; // mismo host/puerto que el backend

function qs(id) { return document.getElementById(id); }

function show(el, msg) {
  el.textContent = msg;
  el.classList.remove("hidden");
}
function hide(el) {
  el.textContent = "";
  el.classList.add("hidden");
}

function fmtDate(isoOrDate) {
  try {
    const d = new Date(isoOrDate);
    return d.toLocaleString();
  } catch {
    return String(isoOrDate ?? "");
  }
}

function statusBadgeClass(status) {
  // Sin colores específicos; mantenemos estilo neutro con borde.
  return "badge";
}

async function apiFetch(path, { method = "GET", query = null, body = null } = {}) {
  const url = new URL(API_BASE + path, window.location.origin);
  if (query) {
    Object.entries(query).forEach(([k, v]) => {
      if (v === null || v === undefined || v === "") return;
      url.searchParams.set(k, String(v));
    });
  }

  const init = {
    method,
    headers: { "Accept": "application/json" },
  };

  if (body !== null) {
    init.headers["Content-Type"] = "application/json";
    init.body = JSON.stringify(body);
  }

  const res = await fetch(url.toString(), init);
  const text = await res.text();
  let data = null;
  try { data = text ? JSON.parse(text) : null; } catch { /* noop */ }

  if (!res.ok) {
    const detail = data?.detail ?? text ?? `HTTP ${res.status}`;
    throw new Error(detail);
  }
  return data;
}

function getQueryParam(name) {
  const u = new URL(window.location.href);
  return u.searchParams.get(name);
}

function setQueryParams(params) {
  const u = new URL(window.location.href);
  Object.entries(params).forEach(([k, v]) => {
    if (v === null || v === undefined || v === "") u.searchParams.delete(k);
    else u.searchParams.set(k, String(v));
  });
  window.history.replaceState({}, "", u.toString());
}
