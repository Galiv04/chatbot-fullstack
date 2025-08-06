import React, { useState } from "react";
import { uploadFile } from "../api";

function FileUpload() {
  const [file, setFile] = useState(null);
  const [uploaded, setUploaded] = useState(false);

  async function handleUpload() {
    if (file) {
      await uploadFile(file);
      setUploaded(true);
      setTimeout(() => setUploaded(false), 1400);
      setFile(null);
    }
  }

  return (
    <div>
      <input type="file" onChange={e => setFile(e.target.files[0])} />
      <button onClick={handleUpload} disabled={!file}>
        Upload
      </button>
      {uploaded && <span> Uploaded!</span>}
    </div>
  );
}

export default FileUpload;
