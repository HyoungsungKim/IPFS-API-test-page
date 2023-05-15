import type { IPFSHTTPClient } from "ipfs-http-client";

export function loadCidList(ipfs: IPFSHTTPClient | undefined): Record<string, any> {
    if(!ipfs){
        return {}
    }

    const fetchFiles = async() => {
        const list = await ipfs.files.ls("/")
        const fileList: Record<string, any> = {}
        for await (const file of list) {
            fileList[file.name] = file
        }

        return fileList
    }
    
    return fetchFiles()
}