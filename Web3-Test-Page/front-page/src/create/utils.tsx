import React, { useState, useRef } from "react";
import { Button, ButtonProps } from '@mui/material';
import {
  Container,
  Paper,
  Typography,
  TextField,
  Grid,
  Card,
  CardContent,
  CardMedia
} from '@mui/material';

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
  const { setFile } = props;

  const handleFileLoad = (event: React.ChangeEvent<HTMLInputElement>) => {
    const fileList = event.target.files;
    if (!fileList || fileList.length === 0) {
      return;
    }

    const file = fileList[0];
    setFile(file)
  };

  return (
    <Button variant="contained" component="label">
      Load File
      <input type="file" hidden onChange={handleFileLoad} />
    </Button>
  );
}

function FileUploaderButton(props: FileUploaderProps) {
  const { ipfs, file, setCids } = props;
  const cidsRef = useRef<string[]>([])

  const uploadFile = async () => {
    if (file) {
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
    }
  };

  return <Button onClick={uploadFile}>Upload to IPFS</Button>;
}

function UploadFileAndMetadataForm(props: FileUploaderProps) {
  const { ipfs, file, setCids } = props;
  const [description1, setDescription1] = useState<string>('');
  const [description2, setDescription2] = useState<string>('');

  const cidsRef = useRef<string[]>([])

  const handleDescription1Change = (event: React.ChangeEvent<HTMLInputElement>) => {
    setDescription1(event.target.value);
  };

  const handleDescription2Change = (event: React.ChangeEvent<HTMLInputElement>) => {
    setDescription2(event.target.value);
  };


  const handleUpload = async () => {
    if (file) {
      const fileBuffer = await file.arrayBuffer()
      const fileContent = new Blob([fileBuffer], { type: file.type })

      const addedFile = await ipfs.add({
        path: file.name,
        content: fileContent
      }, { wrapWithDirectory: true })

      cidsRef.current.push(addedFile.cid.toString())
      let updatedCids = [...cidsRef.current];
      setCids(updatedCids);

      const metadata = {
        fileProperties: {
          name: file.name,
          size: file.size,
          type: file.type,
        },
        cid: addedFile.cid.toString(),
        description1,
        description2,
        // Add other metadata fields here
      };
      const metadataJson  = JSON.stringify(metadata)

      const addedJson = await ipfs.add({
        path: `${file.name}.json`,
        content: metadataJson 
      }, { wrapWithDirectory: true })

      cidsRef.current.push(addedJson.cid.toString())
      updatedCids = [...cidsRef.current];
      setCids(updatedCids);

      console.log(addedFile)
      console.log(addedJson)
    }
  };

  return (
    <Container maxWidth="md">
      <Paper elevation={3} sx={{ padding: 2, maxWidth: 600 }}>
        <Typography variant="h5" component="h2" gutterBottom>
          Upload Image and Metadata
        </Typography>

        {/* File Preview */}
        {file && (
          <Card sx={{ maxWidth: 400, marginBottom: 2 }}>
            {file.type.startsWith('image/') ? (
              <CardMedia component="img" src={URL.createObjectURL(file)} alt="File Preview" />
            ) : (
              <CardContent>
                <Typography variant="body2" color="textSecondary">
                  No preview available
                </Typography>
              </CardContent>
            )}
          </Card>
        )}

        {/* Metadata Inputs */}
        <Grid container spacing={2} sx={{ marginTop: 2 }}>
          <Grid item xs={12}>
            <TextField
              label="Description 1"
              value={description1}
              onChange={handleDescription1Change}
              fullWidth
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              label="Description 2"
              value={description2}
              onChange={handleDescription2Change}
              fullWidth
            />
          </Grid>
        </Grid>

        {/* Upload Button */}
        <Button variant="contained" onClick={handleUpload} disabled={!file}>
          Upload
        </Button>
      </Paper>
    </Container>
  );
}

export { FileLoaderButton, FileUploaderButton, UploadFileAndMetadataForm }
