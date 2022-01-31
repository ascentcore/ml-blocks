import { Grid } from '@mui/material';
import React from 'react';
import Upload from '../components/SchemaForm/Upload';

const UploadScreen = () => {
    return (
        <Grid container justifyContent="center" alignItems="center">
            <Upload />
        </Grid>
    )
}

export default UploadScreen;