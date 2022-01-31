import React, { useState } from 'react';
import { Grid, Select, MenuItem, TextField } from '@mui/material';
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
                MenuProps={{
                    anchorOrigin: {
                        vertical: "bottom",
                        horizontal: "center"
                    },
                    transformOrigin: {
                        vertical: "center",
                        horizontal: "center"
                    },
                    getContentAnchorEl: null
                }}
            >
                {property.enum.map((item, index) => {
                    return (
                        <MenuItem key={index} value={item}>
                            {item}
                        </MenuItem>
                    )
                })}
            </Select>
        </Grid >
    )
}