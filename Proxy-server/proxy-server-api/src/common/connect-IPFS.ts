import { create } from "ipfs-http-client";
import type { IPFSHTTPClient } from "ipfs-http-client";

export async function getIpfsClient(address: string): Promise<IPFSHTTPClient> {
    try {
        const http = create({ url: address });
        const id = await http.id();
        if (id) {
            return http;
        } else {
            throw new Error("Failed to connect to IPFS instance");
        }
    } catch (error) {
        console.error(error);
        throw new Error("Failed to connect to IPFS instance");
    }
}

export default getIpfsClient;
