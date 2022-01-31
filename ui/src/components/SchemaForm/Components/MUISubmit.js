import React from 'react';
import { Button, Checkbox, Grid } from '@mui/material';
import { useStyles } from './Style.styles';

export function MUISubmit({ property, onChange }) {
    const classes = useStyles();
    return (
        <Grid container className={classes.grid}>
            <Button variant="outlined" onClick={onChange}>Submit</Button>
        </Grid>
    )
}