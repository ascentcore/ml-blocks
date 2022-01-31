import { Grid } from '@mui/material';
import React from 'react';
import { makeStyles } from '@mui/styles';
import Upload from '../components/SchemaForm/Upload';

export const useStyles = makeStyles((theme) => ({
    grid: {
        marginTop: '60px'
    }
}))

const UploadScreen = () => {
    const classes = useStyles();
    return (
        <Grid container justifyContent="center" alignItems="baseline" className={classes.grid}>
            <Upload />
        </Grid>
    )
}

export default UploadScreen;