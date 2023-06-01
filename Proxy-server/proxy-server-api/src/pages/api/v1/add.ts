import { NextApiRequest, NextApiResponse } from 'next';
import fs from 'fs';
import formidable, { Fields, Files, File } from 'formidable';

import { getIpfsClient } from "../../../common/connect-IPFS"

export const config = {
  api: {
    bodyParser: false
  }
}

// curl -X POST -H "Content-Type: multipart/form-data" -F "file=@./testFile/Lenna.png" -F "json=@./testFile/test.json" http://localhost:3000/api/v1/add
export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const ipfsAddress = process.env.IPFS_ADDRESS;
  console.log(ipfsAddress);
  try {
    if (!ipfsAddress) {
      throw new Error("Invalid IPFS address. Check environment variables again.");
    }

    const ipfs = await getIpfsClient(ipfsAddress);
    if (!ipfs) {
      throw new Error("Failed to connect to IPFS instance");
    }

    if (req.method !== 'POST') {
      return res.status(405).json({ error: 'Method Not Allowed' });
    }


    const { fields, files }: { fields: formidable.Fields, files: formidable.Files } = await new Promise<{ fields: Fields, files: Files }>((resolve, reject) => {
      const form = new formidable.IncomingForm({ keepExtensions: true, multiples: true, allowEmptyFiles: false });
      form.parse(req, async (err, fields: formidable.Fields, files: formidable.Files) => {
        if (err) {
          console.error('Error parsing form: ', err);
          // Send an error response to the client
          res.status(400).json({ error: 'Error parsing form data' });
          // End the response
          res.end();
          reject(err);
        } else {
          resolve({ fields, files });
        }
      });
    });


    const { file, json } = files as { file: formidable.File, json: formidable.File };
    console.log(json)
    const { filepath: filePath } = file
    const fileData = fs.readFileSync(filePath);
    const fileContent = new Blob([fileData], {type: file.mimetype || ''})

    const jsonData = JSON.parse(fs.readFileSync((json as File).filepath, 'utf-8'));

    const addedFile = await ipfs.add({
      path: file.originalFilename || '',
      content: fileContent
    })

    const metadata = await (async () => {
      jsonData.cid = addedFile.cid.toString()
      const metadataJson = {...file.toJSON(), ...jsonData}
      const jsonBuffer = Buffer.from(JSON.stringify(metadataJson));
      return await ipfs.add({
        path: `${file.originalFilename}_metadata.json`,
        content: jsonBuffer,
      })
    })()

    // Clean up temporary files
    fs.unlinkSync(filePath);
    fs.unlinkSync((json as File).filepath);

    // Return a success response
    res.status(200).json({
      fileCid: addedFile.cid.toString(),
      metadataCid: metadata.cid.toString(),
      message: `File upload and arguments processed successfully.`
    });

    console.log(metadata)
  }

  catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Failed to interact with IPFS. Check IPFS address or IPFS status' });
  }
}
