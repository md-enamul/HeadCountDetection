/* camera.js - live webcam: getUserMedia -> send frames to /api/detect-frame */
(() => {
  const video = document.getElementById("video"), overlay = document.getElementById("overlay");
  if (!video) return;
  const grab = document.createElement("canvas");
  const btnStart = document.getElementById("btnStart"), btnStop = document.getElementById("btnStop"),
        btnClear = document.getElementById("btnClear"), liveCount = document.getElementById("liveCount"),
        liveStatus = document.getElementById("liveStatus"), hint = document.getElementById("camHint");
  let stream = null, timer = null, inFlight = false, peak = 0, frames = 0;

  function setStatus(text, cls) { liveStatus.textContent = text; liveStatus.className = "badge " + cls; }

  async function start() {
    try {
      stream = await navigator.mediaDevices.getUserMedia({ video: { width: 640, height: 480 }, audio: false });
    } catch (e) { toast("Camera blocked or not found. Allow camera access in the browser.", "error"); return; }
    video.srcObject = stream; await video.play();
    overlay.width = grab.width = video.videoWidth; overlay.height = grab.height = video.videoHeight;
    hint.style.display = "none"; peak = 0; frames = 0;
    btnStart.disabled = true; btnStop.disabled = false;
    setStatus("Detecting", "bg-success");
    timer = setInterval(sendFrame, 300);
  }

  function sendFrame() {
    if (inFlight || !stream) return;
    inFlight = true;
    grab.getContext("2d").drawImage(video, 0, 0);
    grab.toBlob(async blob => {
      try {
        const fd = new FormData(); fd.append("frame", blob, "frame.jpg");
        const r = await api("/api/detect-frame", { method: "POST", body: fd });
        if (!stream) return;
        frames++; peak = Math.max(peak, r.total_faces);
        liveCount.textContent = r.total_faces; draw(r.faces);
      } catch (e) { setStatus("Error", "bg-danger"); }
      finally { inFlight = false; }
    }, "image/jpeg", 0.7);
  }

  function draw(faces) {
    const ctx = overlay.getContext("2d"); ctx.clearRect(0, 0, overlay.width, overlay.height);
    ctx.strokeStyle = "#00ff00"; ctx.lineWidth = 3;
    faces.forEach(f => ctx.strokeRect(f.x, f.y, f.w, f.h));
  }

  async function stop() {
    clearInterval(timer); timer = null;
    if (stream) stream.getTracks().forEach(t => t.stop());
    stream = null; video.srcObject = null;
    overlay.getContext("2d").clearRect(0, 0, overlay.width, overlay.height);
    hint.style.display = ""; btnStart.disabled = false; btnStop.disabled = true;
    setStatus("Stopped", "bg-secondary");
    if (frames > 0) {   // one summary record per session, not per frame
      try {
        await api("/api/webcam-session", { method: "POST", headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ total_faces: peak }) });
        toast(`Session saved: ${peak} face(s) at peak.`);
      } catch (e) { toast(e.message, "error"); }
    }
  }

  function clearResults() { peak = 0; liveCount.textContent = 0; overlay.getContext("2d").clearRect(0, 0, overlay.width, overlay.height); }

  btnStart.onclick = start; btnStop.onclick = stop; btnClear.onclick = clearResults;
  window.addEventListener("beforeunload", () => stream && stream.getTracks().forEach(t => t.stop()));
})();
