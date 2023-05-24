import { NextApiRequest, NextApiResponse } from 'next';
import { getIpfsClient } from "../../../common/connect-IPFS"

//curl -X GET http://localhost:3000/api/v1/ipfs-ping
export default async function handler(req: NextApiRequest, res: NextApiResponse) {
    try {
        const ipfsAddress = process.env.IPFS_ADDRESS
        if (!ipfsAddress) {
            throw new Error("Invalid IPFS address. Check environment variables again.")
        }
        const ipfs = await getIpfsClient(ipfsAddress)
        if(!ipfs){
            throw new Error("Failed to connect to IPFS instance")
        }

        if (req.method === 'GET') {
            res.status(200).json({message:'pong'})
        }
    } catch (error) {
        console.error('Error:', error);
        res.status(500).json({ error: 'Failed to interact with IPFS. Check IPFS address or IPFS status' });
    }
}