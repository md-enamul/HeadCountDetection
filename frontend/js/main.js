/* main.js - shared: sidebar, toasts, API helper, button spinner */
const NAV = [["dashboard","Dashboard","bi-speedometer2"],["detection","Face Detection","bi-camera-video"],
             ["history","History","bi-clock-history"],["about","About Project","bi-info-circle"]];

document.addEventListener("DOMContentLoaded", () => {
  const side = document.getElementById("sidebar");
  if (!side) return;
  const page = document.body.dataset.page;
  side.innerHTML = `<div class="brand"><i class="bi bi-people-fill fs-4"></i>HeadCount AI</div>` +
    NAV.map(([id, label, icon]) =>
      `<a href="${id}.html" class="${id === page ? "active" : ""}"><i class="bi ${icon}"></i>${label}</a>`).join("");
  const wrap = document.createElement("div");
  wrap.className = "toast-wrap"; wrap.id = "toasts";
  document.body.appendChild(wrap);
});

function toast(message, type = "success") {
  const el = document.createElement("div");
  el.className = `toast align-items-center text-bg-${type === "error" ? "danger" : "success"} border-0 show mb-2`;
  el.innerHTML = `<div class="d-flex"><div class="toast-body"></div>
    <button class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button></div>`;
  el.querySelector(".toast-body").textContent = message;
  document.getElementById("toasts").appendChild(el);
  setTimeout(() => el.remove(), 4000);
}

async function api(url, options) {
  let res, data;
  try { res = await fetch(url, options); } catch { throw new Error("Cannot reach the server. Is run.py running?"); }
  try { data = await res.json(); } catch { data = {}; }
  if (!res.ok || data.success === false) throw new Error(data.error || `Request failed (${res.status})`);
  return data;
}

function busy(btn, on) {
  if (on) { btn.dataset.html = btn.innerHTML; btn.disabled = true;
    btn.innerHTML = `<span class="spinner-border spinner-border-sm me-2"></span>Working...`; }
  else { btn.disabled = false; btn.innerHTML = btn.dataset.html || btn.innerHTML; }
}

function esc(s) { const d = document.createElement("div"); d.textContent = s ?? ""; return d.innerHTML; }
