import React from 'react';
import { Grid } from '@mui/material';

const MUIWrapper = ({ children }) => {
    return (
        <Grid container direction="row" >
            <main>
                {children}
            </main>
        </Grid >
    );
}

export default MUIWrapper;