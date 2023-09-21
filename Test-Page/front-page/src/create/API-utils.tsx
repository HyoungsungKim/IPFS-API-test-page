import React, { useState, useRef } from "react";
import axios from 'axios';
import { Button, ButtonProps } from '@mui/material';
import { FileLoaderButton } from './utils';

import type { IPFSHTTPClient } from "ipfs-http-client";

interface FileUploaderProps extends ButtonProps {
    ipfs: IPFSHTTPClient;
    file: File | null
    setCids: React.Dispatch<React.SetStateAction<string[] | undefined>>
};


function FileUploadAPI(props: FileUploaderProps) {
    const { ipfs, file, setCids } = props;
    const cidsRef = useRef<string[]>([])

    const [tag, setTag] = useState('');
    const [response, setResponse] = useState<string>('');

    const handleJsonChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setTag(event.target.value);
    };

    const uploadFile = async () => {
        const formData = new FormData();
        if (file) {
            formData.append('file', file);
            const jsonBlob = new Blob([JSON.stringify({ json: tag })], { type: 'application/json' });
            formData.append('json', jsonBlob);
            
            console.log(formData)
            try {
                const res = await axios.post(`${process.env.REACT_APP_API_SERVER_ADDRESS_PORT}/api/v1/add`, formData, {
                    headers: { 'Content-Type': 'multipart/form-data' }
                });
                console.log(res)
                setResponse(res.data.metadataCid);
                
                cidsRef.current.push(res.data.metadataCid)
                let updatedCids = [...cidsRef.current];
                setCids(updatedCids);
            } catch (err: unknown) {
                setResponse('Error: ' + err);
            }
        }
    };

    return (
        <div>
            <input type="text" placeholder="Tags" value={tag} onChange={handleJsonChange} />
            <Button onClick={uploadFile}>Upload to IPFS</Button>;
            <p>{response}</p>
        </div>
    );
}

export {FileUploadAPI};
