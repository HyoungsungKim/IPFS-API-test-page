import React, { useEffect, useState } from "react";
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Typography from '@mui/material/Typography';
import Chip from '@mui/material/Chip';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';

import { FileLoaderButton, FileUploaderButton } from "./utils";

import type { IPFSHTTPClient } from "ipfs-http-client";

interface TabPanelProps {
    children?: React.ReactNode;
    index: number;
    value: number;
}

interface ipfsProps {
    ipfs: IPFSHTTPClient | undefined
}

function TabPanel(props: TabPanelProps) {
    const { children, value, index, ...other } = props;

    return (
        <div
            role="tabpanel"
            hidden={value !== index}
            id={`simple-tabpanel-${index}`}
            aria-labelledby={`simple-tab-${index}`}
            {...other}
        >
            {value === index && (
                <Box sx={{ p: 3 }}>
                    {typeof children === "string" ? (
                        <Typography>{children}</Typography>
                    ) : (
                        <>{children}</>
                    )}
                </Box>
            )}
        </div>
    );
}

function a11yProps(index: number) {
    return {
        id: `simple-tab-${index}`,
        'aria-controls': `simple-tabpanel-${index}`,
    };
}

export function CreateTabPanel(props: ipfsProps): JSX.Element {
    const { ipfs } = props
    const [value, setValue] = useState(0);


    const [contentFile, setContentFile] = useState<Blob | undefined>()
    const [cid, setCid] = useState<string | undefined>()



    const handleChange = (event: React.SyntheticEvent, newValue: number) => {
        setValue(newValue);
    };

    return (
        <Box sx={{ width: '100%' }}>
            <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
                <Tabs value={value} onChange={handleChange} aria-label="basic tabs example">
                    <Tab label="Upload PNG/JPEG" {...a11yProps(0)} />
                    <Tab label="Item Two" {...a11yProps(1)} />
                    <Tab label="Item Three" {...a11yProps(2)} />
                </Tabs>
            </Box>


            <TabPanel value={value} index={0}>
                <Grid container spacing={2} alignItems="center">
                    <Grid item xs={12} sm={6}>
                        <FileLoaderButton setFile={setContentFile} fullWidth />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                        {contentFile && ipfs ? (
                            <FileUploaderButton ipfs={ipfs} fileBlob={contentFile} setCid={setCid} fullWidth />
                        ) :
                            <Button disabled fullWidth>Upload to IPFS</Button>
                        }
                    </Grid>
                </Grid>
            </TabPanel>

            <TabPanel value={value} index={1}>
                Item Two
            </TabPanel>
            <TabPanel value={value} index={2}>
                Item Three
            </TabPanel>
        </Box>
    );
}