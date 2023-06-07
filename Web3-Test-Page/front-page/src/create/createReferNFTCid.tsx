import React, { useState, useRef } from "react";
import { Contract, ethers } from 'ethers';
import { Button, ButtonProps } from '@mui/material';
import {
    Box,
    Typography,
} from '@mui/material';

import { getNFTUId, fetchMetadata } from "../common/web3Utils"
import type {Metadata} from "../common/web3Utils"


interface ReferNFTIdProps extends ButtonProps {
    web3Provider: ethers.BrowserProvider | undefined;
    tokenId: number | undefined
    setMetadata: React.Dispatch<React.SetStateAction<Metadata | undefined>>
};

export function ReferNFTIdBox(props: ReferNFTIdProps) {
    const { web3Provider, tokenId, setMetadata} = props;
    const [tokenCid, setTokenCid] = useState<number | undefined>()

    const handleRefer = async () => {
        try {
            if (!web3Provider) {
                throw new Error("A wallet is not connected.")
            }

            if (!tokenId) {
                throw new Error("Upload data to IPFS first")
            }
            const receipt = await getNFTUId(web3Provider, tokenId)
            setTokenCid(receipt)
            console.log(receipt)

            const metaData = await fetchMetadata(`https://ipfs.io/ipfs/${receipt}`)
            if (metaData) {
                setMetadata(metaData)
            } else {
                throw new Error("Invalid Metadata url")
            }            
        } catch (err: unknown) {
            console.error(err)
        }
    }


    return (
        <Box sx={{ marginBottom: 2, textAlign: 'center' }}>
            <Typography color="inherit" align="center" noWrap sx={{ padding: '16px' }}>
                Get a cid by a token Id
            </Typography>
            {/* Upload Button */}
            <Button variant="contained" onClick={handleRefer} disabled={!web3Provider} sx={{ marginBottom: '4px' }}>
                Get CID
            </Button>
            {
                tokenCid ?
                    <a href={`https://ipfs.io/ipfs/${tokenCid}`} target="_blank" rel="noopener noreferrer">
                        {tokenCid}
                    </a> :
                    <Typography></Typography>
            }
        </Box>

    );
}