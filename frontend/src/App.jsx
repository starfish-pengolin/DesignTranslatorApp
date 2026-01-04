import React, { useState, useRef } from "react";
import axios from "axios";
import "./index.css";

export default function App() {
  const [file, setFile] = useState(null);
  const [outputName, setOutputName] = useState("");
  const [status, setStatus] = useState("");
  const [progress, setProgress] = useState(0);
  const inputRef = useRef();

  function onDrop(ev) {
    ev.preventDefault();
    const f = ev.dataTransfer.files && ev.dataTransfer.files[0];
    if (f) setFile(f);
  }
  function onDragOver(ev) { ev.preventDefault(); }

  async function doExport() {
    if (!file) { setStatus("Select or drop a file."); return; }
    setStatus("Uploading...");
    setProgress(10);
    const fd = new FormData();
    fd.append("file", file);
    fd.append("name", outputName || "exported");
    try {
      const resp = await axios.post("/api/export", fd, {
        responseType: "blob",
        onUploadProgress: (p) => setProgress(Math.round((p.loaded / p.total) * 80) + 10),
      });
      const url = window.URL.createObjectURL(new Blob([resp.data]));
      const a = document.createElement("a");
      a.href = url;
      a.download = resp.headers["content-disposition"]?.split("filename=")[1] || "export.stl";
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
      setStatus("Export complete");
      setProgress(100);
    } catch (err) {
      setStatus("Error: " + (err?.response?.data?.error || err.message));
      setProgress(0);
    }
  }

  async function doGenerate() {
    if (!file) { setStatus("Select or drop a file."); return; }
    setStatus("Uploading...");
    const fd = new FormData();
    fd.append("file", file);
    fd.append("name", outputName || "blender_import");
    try {
      const resp = await axios.post("/api/generate_script", fd, { responseType: "blob" });
      const url = window.URL.createObjectURL(new Blob([resp.data]));
      const a = document.

