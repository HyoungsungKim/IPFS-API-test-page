import type { IPFSHTTPClient } from "ipfs-http-client";
import type {IPFSEntry} from "ipfs-core-types/src/root"

export async function lsCids(
    ipfs: IPFSHTTPClient | undefined,
    cids: string[]
  ): Promise<IPFSEntry[]> {
    if (!ipfs) {
      return [];
    }
  
    const lsCidResult: IPFSEntry[] = [];
    for (const cid of cids) {
      for await (const resultPart of ipfs.ls(cid)) {
        lsCidResult.push(resultPart);
      }
    }
  
    return lsCidResult;
  }