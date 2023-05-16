import React, { useState, useEffect } from 'react';
import { AppBar, Box, Button, Container, Chip, Divider, Grid, Stack, TextField, Typography } from '@mui/material';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';
import { Tooltip } from '@mui/material';


import { CreateTabPanel } from './create/createView';
import type { IPFSHTTPClient } from "ipfs-http-client";
import type { IPFSEntry } from "ipfs-core-types/src/root"

import { getIpfsClient } from "./common/connectIPFS";
import { lsCids } from "./common/lsCids"

interface CommonProps {
	ipfs: IPFSHTTPClient | undefined
	setIpfs: React.Dispatch<React.SetStateAction<IPFSHTTPClient | undefined>>
}

interface ControllerProps extends CommonProps {
	setCids: React.Dispatch<React.SetStateAction<string[] | undefined>>
}

interface ViewProps extends CommonProps {
	cids: string[] | undefined
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
	const [cids, setCids] = useState<string[] | undefined>([])

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
					<Controller ipfs={ipfs} setIpfs={setIpfs} setCids={setCids} />
				</Grid>

				<Grid item xs={6}>
					<View ipfs={ipfs} setIpfs={setIpfs} cids={cids} />
				</Grid>
			</Grid>

		</div>
	)
}

function Controller(props: ControllerProps): JSX.Element {
	const { ipfs, setIpfs, setCids } = props
	// Use a server IP instead of a docker ip
	const [ipfsAddress, setIpfsAddress] = useState<string>(process.env.REACT_APP_IPFS_ADDRESS_PORT ? process.env.REACT_APP_IPFS_ADDRESS_PORT : "http://localhost:5001")
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

				<CreateTabPanel ipfs={ipfs} setCids={setCids} />
				<Divider />

			</Paper>
		</Container>
	)
}


function View(props: ViewProps): JSX.Element {
	const { ipfs, setIpfs, cids } = props;

	const [lsCidsResult, setLsCidsResult] = useState<IPFSEntry[]>([]);

	useEffect(() => {
		const fetchResults = async () => {
			if (ipfs && cids) {
				const results = await lsCids(ipfs, cids);
				setLsCidsResult(results);
			}
		};

		fetchResults();
	}, [ipfs, cids]);

	const CidTables = (): JSX.Element => {
		return (
			<TableContainer component={Paper}>
				<Table>
					<TableHead>
						<TableRow>
							<TableCell>Name</TableCell>
							<TableCell>Path</TableCell>
						</TableRow>
					</TableHead>
					<TableBody>
						{lsCidsResult.map((lsCid: IPFSEntry) => (
							<TableRow key={lsCid.path}>
								<TableCell>{lsCid.name}</TableCell>
								<TableCell>
									<Tooltip title={<img src={"https://ipfs.io/ipfs/" + lsCid.path} alt={lsCid.name} />} placement="top">
										<a href={`https://ipfs.io/ipfs/${lsCid.path}`} target="_blank" rel="noopener noreferrer">
											{lsCid.path}
										</a>
									</Tooltip>
								</TableCell>
							</TableRow>
						))}
					</TableBody>
				</Table>
			</TableContainer>
		)
	}


	return (
		<Container component="div" maxWidth="lg" sx={{ mb: 4 }}>
			<Paper variant="outlined" sx={{ my: { xs: 3, md: 6 }, p: { xs: 2, md: 3 } }}>
				<CidTables />
			</Paper>
		</Container>
	);
}



export default App;
