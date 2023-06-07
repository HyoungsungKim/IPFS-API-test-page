import React, { useState, useEffect } from 'react';
import { AppBar, Box, Button, Container, Chip, Divider, Grid, Stack, TextField, Typography, RadioGroup, FormControlLabel, Radio } from '@mui/material';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';
import { Tooltip } from '@mui/material';
import axios from 'axios';
import { ethers } from 'ethers';

import { ConnectWallet } from './common/web3Utils'
import type {Metadata} from './common/web3Utils'
import { CreateTabPanel } from './create/createUploadTabs';
import { MintNFTBox } from './create/createMintNFTBox';
import { ReferNFTIdBox } from './create/createReferNFTCid'

import type { IPFSHTTPClient } from "ipfs-http-client";
import type { IPFSEntry } from "ipfs-core-types/src/root"

import { getIpfsClient } from "./common/connectIPFS";
import { lsCids } from "./common/lsCids"

declare global {
	interface Window {
		ethereum: any
	}
}

interface CommonProps {
	ipfs: IPFSHTTPClient | undefined
	setIpfs: React.Dispatch<React.SetStateAction<IPFSHTTPClient | undefined>>
}

interface ControllerProps extends CommonProps {
	provider: ethers.BrowserProvider | undefined
	cids: string[] | undefined
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
	const [provider, setProvider] = useState<ethers.BrowserProvider | undefined>()

	useEffect(() => {
		if (window.ethereum) {
			const provider = new ethers.BrowserProvider(window.ethereum)
			setProvider(provider)
		}
	}, [window.ethereum])

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
					<Controller ipfs={ipfs} provider={provider} cids={cids} setIpfs={setIpfs} setCids={setCids} />
				</Grid>

				<Grid item xs={6}>
					<View ipfs={ipfs} setIpfs={setIpfs} cids={cids} />
				</Grid>
			</Grid>

		</div>
	)
}

function Controller(props: ControllerProps): JSX.Element {
	const { ipfs, provider, cids, setIpfs, setCids } = props
	// Use a server IP instead of a docker ip
	const [ipfsAddress, setIpfsAddress] = useState<string>(process.env.REACT_APP_IPFS_ADDRESS_PORT ? process.env.REACT_APP_IPFS_ADDRESS_PORT : "http://localhost:5001")
	const [APIserverAddress, setAPIserverAddress] = useState<string>(process.env.REACT_APP_API_SERVER_ADDRESS_PORT ? process.env.REACT_APP_API_SERVER_ADDRESS_PORT : "http://localhost:3005")

	const [ipfsOnline, setIpfsOnline] = useState<boolean>(false)
	const [APIserverOnline, setAPIserverOnline] = useState<boolean>(false)
	const [tokenId, setTokenId] = useState<number | undefined>()
	const [metadata, setMetadata] = useState<Metadata | undefined>()

	const [selectedLanguage, setSelectedLanguage] = useState('kor'); // Default selected language

	const handleTokenIdChange = (event: React.ChangeEvent<HTMLInputElement>) => {
		setTokenId(parseInt(event.target.value, 10));
	};

	const handleLanguageChange = (event: React.ChangeEvent<HTMLInputElement>) => {
		setSelectedLanguage(event.target.value);
	};


	const videoUrlKor = 'https://ipfs.io/ipfs/QmbyzHMbQA97gYddwtqJyub7CzNK2ob8Cz9pFNoBgoEHJ7/Whiplash_trailor_kor.mp4'
	const videoUrlEng = 'https://ipfs.io/ipfs/QmVMQ9fguoXGQKfRdRts9UQQRwHA41w2UZVnUGeZQpgbhT/Whiplash_trailor_eng.mp4'
	const selectedVideoUrl = selectedLanguage === 'kor' ? videoUrlKor : videoUrlEng;


	const checkAPIserverOnline = (): Promise<boolean> => {
		return new Promise(async (resolve) => {
			try {
				const response = await axios.get(`${APIserverAddress}/api/v1/api-server-ping`);
				console.log(response)
				if (response.status !== 200) {
					resolve(false);
				} else {
					resolve(true);
				}
			} catch (err: unknown) {
				console.error(err);
				resolve(false);
			}
		})
	}

	useEffect(() => {
		getIpfsClient(ipfsAddress).then(([client, online]) => {
			setIpfs(client);
			setIpfsOnline(online);
			if (client) {
				setIpfs(client);
			}

			checkAPIserverOnline().then((status) => {
				setAPIserverOnline(status)
			})
		});
	}, [ipfsAddress, APIserverAddress]);

	useEffect(() => {
		if (metadata) {
			setSelectedLanguage(metadata.country)
		}
	}, [metadata])

	return (
		<Container component="div" maxWidth="lg" sx={{ mb: 4 }}>
			<Paper variant="outlined" sx={{ my: { xs: 3, md: 6 }, p: { xs: 2, md: 3 } }}>
				<Box sx={{ borderBottom: 1, borderColor: 'transparent', marginBottom: 2, display: 'flex', justifyContent: 'center', alignItems: 'center', textAlign: 'center' }}>
					<Chip label={ipfsOnline ? "IPFS online" : "IPFS offline"} color={ipfsOnline ? "success" : "error"} />
					<Typography variant="body1" sx={{ marginLeft: 1 }}>
						{ipfsAddress}
					</Typography>
				</Box>

				<Box sx={{ borderBottom: 1, borderColor: 'transparent', marginBottom: 2, display: 'flex', justifyContent: 'center', alignItems: 'center', textAlign: 'center' }}>
					<Chip label={APIserverOnline ? "API server online" : "API server offline"} color={APIserverOnline ? "success" : "error"} />
					<Typography variant="body1" sx={{ marginLeft: 1 }}>
						{APIserverAddress}
					</Typography>
				</Box>


				<Box sx={{ borderBottom: 1, borderColor: 'transparent', marginBottom: 2, display: 'flex', justifyContent: 'center', alignItems: 'center', textAlign: 'center' }}>
					<ConnectWallet web3Provider={provider} />
				</Box>

				<CreateTabPanel ipfs={ipfs} setCids={setCids} />
				<Divider />

				<MintNFTBox web3Provider={provider} cid={cids ? cids[cids.length - 1] : undefined} />

				<Divider />


	
				<ReferNFTIdBox web3Provider={provider} tokenId={tokenId ? tokenId : undefined} setMetadata={setMetadata}/>
				<Grid item xs={12}>
					<TextField
						label="Token Id"
						value={tokenId}
						onChange={handleTokenIdChange}
						fullWidth
					/>
				</Grid>
				<Divider />

				<Box sx={{ borderBottom: 1, borderColor: 'transparent', marginBottom: 0.5, display: 'flex', justifyContent: 'center', alignItems: 'center', textAlign: 'center' }}>
					<RadioGroup sx={{ flexDirection: 'row', alignItems: 'center' }} name="language" value={metadata? metadata.country : selectedLanguage} onChange={handleLanguageChange}>
						<FormControlLabel value="kor" control={<Radio />} label="Korean" disabled />
						<FormControlLabel value="eng" control={<Radio />} label="English" disabled />
					</RadioGroup>
				</Box>

				<Divider />
				<Box sx={{
					width: '100%',
					height: '300px', // Adjust the height as needed
					border: '1px solid #ccc',
					backgroundColor: '#f0f0f0',
					display: 'flex',
					justifyContent: 'center',
					alignItems: 'center',
					textAlign: 'center',
				}}>

					<video src={selectedVideoUrl} controls style={{ width: '100%', height: '100%' }} />
				</Box>

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
