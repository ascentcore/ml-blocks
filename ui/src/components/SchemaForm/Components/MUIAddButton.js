import React from 'react';
import addIcon from './add-icon.png';
import { useStyles } from './Style.styles';
import { Grid } from '@mui/material';

export function MUIAddButton({ property, onChange }) {
    const classes = useStyles();
    return (
        < img
            className={classes.addButton}
            onClick={onChange}
            src={addIcon}
            alt='add icon'
            required={property.isRequired}
        />
    )
}