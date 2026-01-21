let alertId = null;

function setButtonsForStatus(status) {
  const btnAck = qs("btnAck");
  const btnClose = qs("btnClose");
  const btnReopen = qs("btnReopen");

  // Reglas simples:
  // - open: puedes ack/close
  // - ack: puedes close/reopen
  // - closed: puedes reopen
  btnAck.disabled = (status !== "open");
  btnClose.disabled = (status === "closed");
  btnReopen.disabled = (status !== "ack" && status !== "closed");
}

function renderAlert(a) {
  qs("title").textContent = `Alerta #${a.id}`;
  qs("subtitle").textContent = `status=${a.status} · group_key=${a.group_key ?? "—"}`;

  qs("v_id").textContent = a.id;
  qs("v_status").textContent = a.status;
  qs("v_status").className = statusBadgeClass(a.status);
  qs("v_group_key").textContent = a.group_key ?? "—";
  qs("v_rule_id").textContent = a.rule_id;
  qs("v_event_id").textContent = a.event_id;
  qs("v_created_at").textContent = fmtDate(a.created_at);
  qs("v_updated_at").textContent = fmtDate(a.updated_at);
  qs("v_title").textContent = a.title;

  setButtonsForStatus(a.status);
}

async function loadDetail() {
  const err = qs("errorBox");
  const info = qs("infoBox");
  hide(err); hide(info);

  try {
    const a = await apiFetch(`/alerts/${alertId}`);
    renderAlert(a);
  } catch (e) {
    show(err, `Error cargando alerta: ${e.message}`);
  }
}

async function updateStatus(nextStatus) {
  const err = qs("errorBox");
  const info = qs("infoBox");
  hide(err); hide(info);

  try {
    const a = await apiFetch(`/alerts/${alertId}`, {
      method: "PATCH",
      body: { status: nextStatus }
    });
    renderAlert(a);
    show(info, `Estado actualizado a: ${a.status}`);
  } catch (e) {
    show(err, `Error actualizando estado: ${e.message}`);
  }
}

function init() {
  alertId = getQueryParam("id");
  if (!alertId) {
    show(qs("errorBox"), "Falta parámetro ?id= en la URL.");
    return;
  }

  qs("btnAck").addEventListener("click", () => updateStatus("ack"));
  qs("btnClose").addEventListener("click", () => updateStatus("closed"));
  qs("btnReopen").addEventListener("click", () => updateStatus("open"));

  loadDetail();
}

document.addEventListener("DOMContentLoaded", init);
