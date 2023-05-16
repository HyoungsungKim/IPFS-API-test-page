import React, { useState, useRef } from "react";
import { Button, ButtonProps } from '@mui/material';

import { create } from "ipfs-http-client";
import type { IPFSHTTPClient } from "ipfs-http-client";

interface FileUploaderProps extends ButtonProps {
  ipfs: IPFSHTTPClient;
  file: File | null
  setCids: React.Dispatch<React.SetStateAction<string[] | undefined>>
};

interface FileLoaderProps extends ButtonProps {
  setFile: React.Dispatch<React.SetStateAction<File | null>>;
};

function FileLoaderButton(props: FileLoaderProps) {
  const { setFile  } = props;

  const handleFileLoad = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const fileList = event.target.files;
    if (!fileList || fileList.length === 0) {
      return;
    }

    const file = fileList[0];
    setFile(file)
  };

  return (
    <Button variant="contained" component="label">
      Upload File
      <input type="file" hidden onChange={handleFileLoad} />
    </Button>
  );
}

function FileUploaderButton(props: FileUploaderProps) {
  const { ipfs, file, setCids } = props;
  const cidsRef = useRef<string[]>([])

  const uploadFile = async () => {
    if(file){
      const fileBuffer = await file.arrayBuffer()
      const fileContent = new Blob([fileBuffer], { type: file.type })

      const addedFile = await ipfs.add({
       path: file.name,
       content: fileContent
      }, { wrapWithDirectory: true })
      cidsRef.current.push(addedFile.cid.toString())
      const updatedCids = [...cidsRef.current];
      setCids(updatedCids);

      console.log(addedFile)
      console.log(addedFile.cid.toString())
             
      /*
      for (let cid of cidsRef.current) {
        for await (const resultPart of ipfs.ls(cid)) {
          console.log(resultPart)
        }
      }
      */
    }    
  };

  return <Button onClick={uploadFile}>Upload to IPFS</Button>;
}


export { FileLoaderButton, FileUploaderButton }
