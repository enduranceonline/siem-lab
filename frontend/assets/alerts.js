let state = {
  limit: 50,
  offset: 0,
  status: "",
  group_key: "",
};

function readStateFromUrl() {
  const u = new URL(window.location.href);
  state.limit = Number(u.searchParams.get("limit") ?? "50");
  state.offset = Number(u.searchParams.get("offset") ?? "0");
  state.status = u.searchParams.get("status") ?? "";
  state.group_key = u.searchParams.get("group_key") ?? "";
}

function syncForm() {
  qs("limit").value = String(state.limit);
  qs("status").value = state.status;
  qs("group_key").value = state.group_key;
}

function syncUrl() {
  setQueryParams({
    limit: state.limit,
    offset: state.offset,
    status: state.status,
    group_key: state.group_key,
  });
}

function renderRows(alerts) {
  const tb = qs("alertsTbody");
  tb.innerHTML = "";

  if (!alerts || alerts.length === 0) {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td colspan="9" class="muted">Sin resultados</td>`;
    tb.appendChild(tr);
    return;
  }

  for (const a of alerts) {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td class="mono">${a.id}</td>
      <td><span class="${statusBadgeClass(a.status)}">${a.status}</span></td>
      <td class="muted">—</td>
      <td class="mono">${a.group_key ?? "—"}</td>
      <td>${escapeHtml(a.title)}</td>
      <td class="mono">${a.rule_id}</td>
      <td class="mono">${a.event_id}</td>
      <td class="mono">${fmtDate(a.created_at)}</td>
      <td><a class="btn" href="./alert.html?id=${encodeURIComponent(a.id)}">Ver</a></td>
    `;
    tb.appendChild(tr);
  }
}

function escapeHtml(s) {
  return String(s ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

async function loadAlerts() {
  const err = qs("errorBox");
  const info = qs("infoBox");
  hide(err); hide(info);

  qs("alertsTbody").innerHTML = `<tr><td colspan="9" class="muted">Cargando…</td></tr>`;

  try {
    const data = await apiFetch("/alerts", {
      query: {
        limit: state.limit,
        offset: state.offset,
        status: state.status || null,
        group_key: state.group_key || null,
      }
    });

    renderRows(data);

    qs("resultMeta").textContent =
      `limit=${state.limit} · offset=${state.offset} · resultados=${data.length}`;

    // UX: si vuelve vacío y offset>0, probablemente te pasaste de página.
    if (data.length === 0 && state.offset > 0) {
      show(info, "No hay más resultados en esta página. Prueba con Prev.");
    }

    qs("btnPrev").disabled = state.offset <= 0;
    // Next: no sabemos total; habilitamos siempre. Si vacía, el mensaje guía.
    qs("btnNext").disabled = false;

  } catch (e) {
    show(err, `Error cargando alertas: ${e.message}`);
  }
}

function init() {
  readStateFromUrl();
  syncForm();

  qs("filtersForm").addEventListener("submit", (ev) => {
    ev.preventDefault();
    state.status = qs("status").value.trim();
    state.group_key = qs("group_key").value.trim();
    state.limit = Number(qs("limit").value);
    state.offset = 0; // aplicar filtros resetea paginación
    syncUrl();
    loadAlerts();
  });

  qs("btnClear").addEventListener("click", () => {
    state.status = "";
    state.group_key = "";
    state.offset = 0;
    syncForm();
    syncUrl();
    loadAlerts();
  });

  qs("btnPrev").addEventListener("click", () => {
    state.offset = Math.max(0, state.offset - state.limit);
    syncUrl();
    loadAlerts();
  });

  qs("btnNext").addEventListener("click", () => {
    state.offset = state.offset + state.limit;
    syncUrl();
    loadAlerts();
  });

  qs("btnRefresh").addEventListener("click", () => loadAlerts());

  loadAlerts();
}

document.addEventListener("DOMContentLoaded", init);
