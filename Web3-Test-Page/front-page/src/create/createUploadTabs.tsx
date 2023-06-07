import React, { useState } from "react";
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';

import { FileLoaderButton, FileUploaderButton } from "./utils";
import { FileUploadAPI } from "./API-utils"

import type { IPFSHTTPClient } from "ipfs-http-client";

interface TabPanelProps {
    children?: React.ReactNode;
    index: number;
    value: number;
}

interface CreateTabProps {
    ipfs: IPFSHTTPClient | undefined
    setCids: React.Dispatch<React.SetStateAction<string[] | undefined>>
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

export function CreateTabPanel(props: CreateTabProps): JSX.Element {
    const { ipfs, setCids } = props
    const [value, setValue] = useState(0);


    const [file, setFile] = useState<File | null>(null)



    const handleChange = (event: React.SyntheticEvent, newValue: number) => {
        setValue(newValue);
    };

    return (
        <Box sx={{ width: '100%' }}>
            <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
                <Tabs value={value} onChange={handleChange} aria-label="basic tabs example">
                    <Tab label="Upload File" {...a11yProps(0)} />
                    <Tab label="Upload File By API" {...a11yProps(1)} />
                </Tabs>
            </Box>


            <TabPanel value={value} index={0}>
                <Grid container spacing={2} alignItems="center">
                    <Grid item xs={12} sm={6}>
                        <FileLoaderButton setFile={setFile} fullWidth />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                        {file && ipfs ? (
                            <FileUploaderButton ipfs={ipfs} file={file} setCids={setCids} fullWidth />
                        ) :
                            <Button disabled fullWidth>Upload to IPFS</Button>
                        }
                    </Grid>
                </Grid>
            </TabPanel>
            <TabPanel value={value} index={1}>
                <Grid container spacing={2} alignItems="center">
                    <Grid item xs={12} sm={6}>
                        <FileLoaderButton setFile={setFile} fullWidth />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                        {file && ipfs ? (
                            <FileUploadAPI ipfs={ipfs} file={file} setCids={setCids} fullWidth />
                        ) :
                            <Button disabled fullWidth>Upload to IPFS</Button>
                        }
                    </Grid>
                </Grid>
            </TabPanel>
        </Box>
    );
}