import React, { useState } from "react";
import { Button, ButtonProps } from '@mui/material';

import { create } from "ipfs-http-client";
import type { IPFSHTTPClient } from "ipfs-http-client";

interface FileUploaderProps extends ButtonProps {
  ipfs: IPFSHTTPClient;
  fileBlob: Blob;
  setCid: React.Dispatch<React.SetStateAction<string | undefined>>
};

interface FileLoaderProps extends ButtonProps {
  setFile: React.Dispatch<React.SetStateAction<Blob | undefined>>
};

function FileLoaderButton(props: FileLoaderProps) {
  const { setFile } = props;

  const handleFileLoad = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const fileList = event.target.files;
    if (!fileList || fileList.length === 0) {
      return;
    }
    const fileReader = new FileReader();
    fileReader.onload = async () => {
      const content = fileReader.result as string;
      let file: Blob;
      if (fileList[0].type === "image/png") {
        file = new Blob([content], { type: "image/png" });
      } else if (fileList[0].type === "image/jpeg") {
        file = new Blob([content], { type: "image/jpeg" });
      } else {
        file = new Blob([content]);
      }
      setFile(file)
    };
    fileReader.readAsText(fileList[0]);
  };

  return (
    <Button variant="contained" component="label">
      Upload File
      <input type="file" hidden onChange={handleFileLoad} />
    </Button>
  );
}

function FileUploaderButton(props: FileUploaderProps) {
  const { ipfs, fileBlob, setCid } = props;
  const uploadFile = async () => {
    const fileContent = await fileBlob.arrayBuffer();
    const addedFile = await ipfs.add(fileContent);
    setCid(addedFile.cid.toString())
    console.log(addedFile.cid.toString())

  };

  return <Button onClick={uploadFile}>Upload to IPFS</Button>;
}


export { FileLoaderButton, FileUploaderButton }
