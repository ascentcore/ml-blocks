import React from 'react';
import { Grid, TextField } from '@mui/material';
import { useStyles } from './Style.styles';

export function MUITextField({ property, value, onChange }) {
    const classes = useStyles();

    const handleChange = (event) => {
        if (property.title == 'Phone number') {
            const re = /[0-9]+/g;
            if (event.target.value === '' || re.test(event.target.value)) {
                onChange(event.target.value)
            }
        }
        else onChange(event.target.value)
    }
    return (
        <Grid container className={classes.grid}>
            <TextField
                value={value || ''}
                onChange={handleChange}
                error={!!property.error}
                label={property.title}
                required={property.isRequired}
                className={classes.input}
            />
        </Grid>
    )
}