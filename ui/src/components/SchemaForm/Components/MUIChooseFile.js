import React from 'react';
import { Button, Checkbox, Grid, Input } from '@mui/material';
import { useStyles } from './Style.styles';

export function MUIChooseFile({ property, onChange }) {
    const classes = useStyles();
    return (
        <Grid container className={classes.grid}>
            <Input
                type='file'
                disableUnderline="true"
                onChange={onChange}
            />
        </Grid>
    )
}