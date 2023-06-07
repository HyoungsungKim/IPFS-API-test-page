import React, { useState, useRef } from "react";
import { Contract, ethers } from 'ethers';
import { Button, ButtonProps } from '@mui/material';
import {
    Box,
    Typography,
} from '@mui/material';

import { mintNFT } from "../common/web3Utils"


interface MintNFTProps extends ButtonProps {
    web3Provider: ethers.BrowserProvider | undefined;
    cid: string | undefined
};

export function MintNFTBox(props: MintNFTProps) {
    const { web3Provider, cid } = props;

    const handleMint = async () => {
        try {
            if (!web3Provider) {
                throw new Error("A wallet is not connected.")
            }

            if (!cid) {
                throw new Error("Upload data to IPFS first")
            }
            const receipt = await mintNFT(web3Provider, cid)
            console.log(receipt)
        } catch (err: unknown) {
            console.error(err)
        }
    }


    return (
        <Box sx={{ marginBottom: 2, textAlign: 'center' }}>
            <Typography color="inherit" align="center" noWrap sx={{ padding: '16px' }}>
                Mint NFT using the latest uploaded file to IPFS
            </Typography>
            {/* Upload Button */}
            <Button variant="contained" onClick={handleMint} disabled={!web3Provider} sx={{ marginBottom: '4px' }}>
                Mint NFT
            </Button>
        </Box>

    );
}