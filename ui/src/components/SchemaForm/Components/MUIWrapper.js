import React from 'react';
import { Grid } from '@mui/material';
import { useStyles } from './Style.styles';

const MUIWrapper = ({ children, property }) => {
    const classes = useStyles();
    return (
        <Grid container direction="column" >
            <main>
                {children}
            </main>
            {property.error && (<span className={classes.error}>{typeof property.error !== 'boolean' && property.error[0].message}</span>)}
        </Grid >
    );
}

export default MUIWrapper;