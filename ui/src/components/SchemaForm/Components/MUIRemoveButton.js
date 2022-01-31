import React from 'react';
import { Button, Grid } from '@mui/material';
import { useStyles } from './Style.styles';

export function MUIRemoveButton({ property, onChange }) {
    const classes = useStyles();
    return (
        <Grid container className={classes.grid}>
            <Button variant="outlined" onClick={onChange} className={classes.removeButton}>Remove</Button>
        </Grid>
    )
}