import React from 'react';
import { Checkbox, Grid } from '@mui/material';
import { useStyles } from './Style.styles';

export function MUICheckbox({ property }) {
    const classes = useStyles();
    return (
        <Grid container className={classes.grid}>
            <div style={{ marginTop: 12 }}>{property.title}</div>
            <Checkbox color="secondary" />
        </Grid>
    )
}