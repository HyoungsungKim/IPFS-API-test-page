import React, {useState, useEffect} from 'react';
import { ethers } from 'ethers';
import Button from '@mui/material/Button';
import ERC721Abi from '../../contract-abi/ERC-721/MyNFT.json'

export function ConnectWallet(props: {web3Provider: ethers.BrowserProvider | undefined}) {
    const {web3Provider} = props

    const [account, setAccount] = useState<string>()

    const connectHandler = async () => {
        if(web3Provider) {
            await web3Provider.send("eth_requestAccounts", []);
            const signer = await web3Provider.getSigner()
            const userAccount = signer.address
            setAccount(userAccount)
        }
    }

    return (
        <Button variant="outlined" size="small" color="inherit" disabled={!web3Provider} onClick={async () => {
            await connectHandler()
        }}>{account ? account : "Connect account" }</Button>
    )
}