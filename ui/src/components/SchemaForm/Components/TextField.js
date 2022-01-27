import React from 'react';
import { TextField } from '@mui/material';
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
        <TextField
            value={value || ''}
            onChange={handleChange}
            error={!!property.error}
            label={property.title}
            helperText={property.error ? property.error[0].keyword : ' '}
            required={property.isRequired}
            className={classes.input}
        />
    )
}