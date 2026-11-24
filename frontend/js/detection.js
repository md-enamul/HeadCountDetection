/* detection.js - image upload detection */
(() => {
  const input = document.getElementById("imgInput");
  if (!input) return;
  const preview = document.getElementById("imgPreview"), result = document.getElementById("imgResult"),
        btnDetect = document.getElementById("btnDetect"), btnReset = document.getElementById("btnReset"),
        count = document.getElementById("imgCount");
  let file = null;

  input.onchange = () => {
    file = input.files[0] || null;
    if (!file) return;
    if (!file.type.startsWith("image/")) { toast("Please choose an image file.", "error"); return reset(); }
    if (file.size > 10 * 1024 * 1024) { toast("Image is larger than 10 MB.", "error"); return reset(); }
    preview.src = URL.createObjectURL(file); preview.classList.remove("d-none");
    result.classList.add("d-none"); btnDetect.disabled = false;
  };

  btnDetect.onclick = async () => {
    if (!file) return;
    busy(btnDetect, true);
    try {
      const fd = new FormData(); fd.append("image", file);
      const r = await api("/api/detect-image", { method: "POST", body: fd });
      result.src = r.processed_image; result.classList.remove("d-none"); preview.classList.add("d-none");
      count.textContent = r.total_faces;
      toast(`${r.total_faces} face(s) detected and saved to history.`);
    } catch (e) { toast(e.message, "error"); }
    finally { busy(btnDetect, false); }
  };

  function reset() {
    file = null; input.value = ""; preview.classList.add("d-none"); result.classList.add("d-none");
    preview.removeAttribute("src"); count.textContent = 0; btnDetect.disabled = true;
  }
  btnReset.onclick = reset;
})();
