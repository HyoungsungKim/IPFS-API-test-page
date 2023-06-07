import React, { useState, useEffect } from 'react';
import { Contract, ethers } from 'ethers';
import Button from '@mui/material/Button';

// Deployed in Goerli
import ERC4907ContractInfo from './contract/ERC-4907/ERC4907.json';
const CONTRACT_ADDRESS = "0xA05D10F3A145c38928BB298b49502886ab8f601f"

export interface Metadata {
    country: string
}

export async function fetchMetadata(url: string): Promise<any> {
    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error('Failed to fetch JSON data');
      }
      const metadata: Metadata = await response.json();
      return metadata;
    } catch (error) {
      console.error('Error:', error);
      throw error;
    }
}

export function ConnectWallet(props: { web3Provider: ethers.BrowserProvider | undefined }) {
    const { web3Provider } = props

    const [account, setAccount] = useState<string>()

    const connectHandler = async () => {
        if (web3Provider) {
            await web3Provider.send("eth_requestAccounts", []);
            const signer = await web3Provider.getSigner()
            const userAccount = signer.address
            setAccount(userAccount)
        }
    }

    return (
        <Button variant="outlined" size="small" color="inherit" disabled={!web3Provider} onClick={async () => {
            await connectHandler()
        }}>{account ? account : "Connect account"}</Button>
    )
}

export async function mintNFT(
    web3Provider: ethers.BrowserProvider,
    URI: string | undefined
) {
    const abi = ERC4907ContractInfo.abi;
    const signer = await web3Provider.getSigner()
    const contract = new Contract(CONTRACT_ADDRESS, abi, signer)
    const ownerAddress = await signer.getAddress()
    const mintingResult = await contract.mintNFT(ownerAddress, URI ? URI : "")
    const recipt = await mintingResult.wait()

    return recipt

}   

export async function getNFTUId(
    web3Provider: ethers.BrowserProvider,
    tokenId: number
) {
    const abi = ERC4907ContractInfo.abi;
    const signer = await web3Provider.getSigner()
    const contract = new Contract(CONTRACT_ADDRESS, abi, signer)
    const uid = await contract.tokenURI(tokenId)

    return uid
}   