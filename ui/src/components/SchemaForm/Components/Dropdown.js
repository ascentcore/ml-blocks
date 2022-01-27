import React, { useState } from 'react';
import { Grid, Select, MenuItem } from '@mui/material';
import { useStyles } from './Style.styles';

export function MUISelectElement({ property, value, onChange }) {
    const classes = useStyles();

    const handleChange = (event) => {
        onChange(event.target.value);
    };
    return (
        <Grid container direction="row" className={classes.grid}>
            {property.title}
            <Select
                value={value}
                onChange={handleChange}
                className={classes.selector}
            >
                <MenuItem value={property.enum[0]}>{property.enum[0]}</MenuItem>
                <MenuItem value={property.enum[1]}>{property.enum[1]}</MenuItem>
            </Select>
        </Grid>
    )
}