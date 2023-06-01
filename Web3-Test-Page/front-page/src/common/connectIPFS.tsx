import { useState, useEffect } from "react";

import { create } from "ipfs-http-client";
import type { IPFSHTTPClient } from "ipfs-http-client";

export function getIpfsClient(address: string): Promise<[IPFSHTTPClient | undefined, boolean]> {
  return new Promise(async (resolve) => {
    try {
      const http = await create({ url: address });
      console.log(http)
      const id = await http.id()
      //const isOnline = await http.isOnline();
      if(id) {
        resolve([http, true]);
      } else {
        resolve([http, false]);
      }

    } catch (err: unknown) {
      console.error(err);
      resolve([undefined, false]);
    }
  });
}