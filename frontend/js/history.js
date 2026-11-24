/* history.js - dashboard stats + history table */
async function loadDashboard() {
  const s = await api("/api/statistics");
  totalFaces.textContent = s.total_faces; totalSessions.textContent = s.total_sessions;
  imageCount.textContent = s.image_detections; webcamCount.textContent = s.webcam_detections;
  recentBody.innerHTML = s.recent.length ? s.recent.map(r =>
    `<tr><td>#${r.id}</td><td>${esc(r.detection_type)}</td><td>${r.total_faces}</td>
     <td>${esc(r.detection_date)} ${esc(r.detection_time)}</td></tr>`).join("")
    : `<tr><td colspan="4" class="text-muted text-center py-4">No detections yet. Try the Face Detection page.</td></tr>`;
  try {
    const h = await api("/api/health");
    sysStatus.className = "badge " + (h.model_loaded ? "bg-success" : "bg-danger");
    sysStatus.textContent = h.model_loaded ? "Backend online - model loaded" : "Model not loaded";
  } catch { sysStatus.className = "badge bg-danger"; sysStatus.textContent = "Backend offline"; }
}

let records = [];
async function loadHistory() {
  records = (await api("/api/history")).records;
  historyBody.innerHTML = records.length ? records.map(r =>
    `<tr><td>#${r.id}</td><td><span class="badge badge-live">${esc(r.detection_type)}</span></td>
     <td>${r.total_faces}</td><td>${esc(r.detection_date)}</td><td>${esc(r.detection_time)}</td>
     <td>${esc(r.image_filename) || "-"}</td>
     <td class="text-end"><button class="btn btn-sm btn-outline-primary me-1" onclick="viewRec(${r.id})"><i class="bi bi-eye"></i></button>
     <button class="btn btn-sm btn-outline-danger" onclick="delRec(${r.id})"><i class="bi bi-trash"></i></button></td></tr>`).join("")
    : `<tr><td colspan="7" class="text-muted text-center py-4">No history yet.</td></tr>`;
}

function viewRec(id) {
  const r = records.find(x => x.id === id); if (!r) return;
  modalBody.innerHTML = `<dl class="row mb-0"><dt class="col-5">ID</dt><dd class="col-7">#${r.id}</dd>
    <dt class="col-5">Type</dt><dd class="col-7">${esc(r.detection_type)}</dd>
    <dt class="col-5">Total faces</dt><dd class="col-7">${r.total_faces}</dd>
    <dt class="col-5">Date</dt><dd class="col-7">${esc(r.detection_date)}</dd>
    <dt class="col-5">Time</dt><dd class="col-7">${esc(r.detection_time)}</dd>
    <dt class="col-5">Image file</dt><dd class="col-7">${esc(r.image_filename) || "-"}</dd></dl>`;
  new bootstrap.Modal(document.getElementById("recModal")).show();
}

async function delRec(id) {
  if (!confirm(`Delete record #${id}?`)) return;
  try { await api(`/api/history/${id}`, { method: "DELETE" }); toast("Record deleted."); loadHistory(); }
  catch (e) { toast(e.message, "error"); }
}

document.addEventListener("DOMContentLoaded", () => {
  if (document.getElementById("recentBody")) loadDashboard().catch(e => toast(e.message, "error"));
  if (document.getElementById("historyBody")) loadHistory().catch(e => toast(e.message, "error"));
});
