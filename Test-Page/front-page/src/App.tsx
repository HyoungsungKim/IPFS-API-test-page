import React, { useState, useEffect } from 'react';
import { AppBar, Box, Button, Container, Chip, Divider, Grid, Paper, Stack, TextField, Typography } from '@mui/material';
import { Table, TableBody, TableCell, TableRow } from '@mui/material';

import { CreateTabPanel } from './create/createView';
import type { IPFSHTTPClient } from "ipfs-http-client";
//import type {MFSEntry} from "ipfs-core-types/src/files"


import { getIpfsClient } from "./common/connectIPFS";
import { loadCidList } from "./common/loadCidList"

interface commonProps {
	ipfs: IPFSHTTPClient | undefined
	setIpfs: React.Dispatch<React.SetStateAction<IPFSHTTPClient | undefined>>
}

function App() {
	return (
		<Layout />
	);
}


function Layout(): JSX.Element {
	const [loading, setLoading] = useState(false)
	const [success, setSuccess] = useState(true)
	const [ipfs, setIpfs] = useState<IPFSHTTPClient | undefined>(undefined)

	useEffect(() => {
		setSuccess(!loading)
	}, [loading])

	return (
		<div>
			<AppBar
				position="absolute"
				color="default"
				elevation={0}
				sx={{
					position: 'relative',
					borderBottom: (t) => `1px solid ${t.palette.divider}`,
				}}
			>
				<Typography variant="h6" color="inherit" align="center" noWrap>
					IPFS API test page
				</Typography>
			</AppBar>


			<Divider orientation="vertical" flexItem />

			<Grid container >
				<Grid item xs={6}>
					<Controller ipfs={ipfs} setIpfs={setIpfs} />
				</Grid>

				<Grid item xs={6}>
					<View ipfs={ipfs} setIpfs={setIpfs} />
				</Grid>
			</Grid>

		</div>
	)
}

function Controller(props: commonProps): JSX.Element {
	const { ipfs, setIpfs } = props
	// 도커 ip로 하면 연결안됨 -> 서버 IP 주소 사용해야함
	const [ipfsAddress, setIpfsAddress] = useState<string>("http://10.252.107.31:5001") //process.env.REACT_APP_IPFS_ADDRESS_PORT?.toString() ?? "http://localhost:5001")
	const [ipfsOnline, setIpfsOnline] = useState<boolean>(false)

	useEffect(() => {
		getIpfsClient(ipfsAddress).then(([client, online]) => {
			setIpfs(client);
			setIpfsOnline(online);
			if (client) {
				setIpfs(client);
			}
		});
	}, [ipfsAddress]);

	return (
		<Container component="div" maxWidth="lg" sx={{ mb: 4 }}>
			<Paper variant="outlined" sx={{ my: { xs: 3, md: 6 }, p: { xs: 2, md: 3 } }}>
				<Box sx={{ borderBottom: 1, borderColor: 'transparent', marginBottom: 2, display: 'flex', justifyContent: 'center', alignItems: 'center', textAlign: 'center' }}>
					<Chip label={ipfsOnline ? "IPFS online" : "IPFS offline"} color={ipfsOnline ? "success" : "error"} />
					<Typography variant="body1" sx={{ marginLeft: 1 }}>
						{ipfsAddress}
					</Typography>
				</Box>

				<CreateTabPanel ipfs={ipfs} />
				<Divider />

			</Paper>
		</Container>
	)
}


function View(props: commonProps): JSX.Element {
	const { ipfs, setIpfs } = props
	/*
	const [fileList, setFileList] = useState<MFSEntry[]>([]);
	
	useEffect(() => {
		const loadFiles = async () => {
		  try {
			if (ipfs) {
			  const files = await ipfs.files.ls("/");
			  const fileList: MFSEntry[] = [];
			  for await (const file of files) {
				fileList.push({
				  name: file.name,
				  type: file.type,
				  cid: file.cid,
				  size: file.size,
				  mode: file.mode,
				  mtime: file.mtime,	
				});
			  }
			  setFileList(fileList);
			}
		  } catch (err: unknown) {
			console.error("Failed to load files:", err);
		  }
		};
	  
		loadFiles();
	  }, [ipfs]);
*/
	return (
		<Container component="div" maxWidth="lg" sx={{ mb: 4 }}>
			<Paper variant="outlined" sx={{ my: { xs: 3, md: 6 }, p: { xs: 2, md: 3 } }}>

			</Paper>
		</Container>
	)
}


export default App;
