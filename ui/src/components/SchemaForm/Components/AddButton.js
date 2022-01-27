import React from 'react';
import addIcon from './add-icon.png';
import { useStyles } from './Style.styles';
import { Grid } from '@mui/material';

export function MUIAddButton({ property, onChange }) {
    const classes = useStyles();
    return (
        <Grid item>
            <div className={classes.title}>{property.title}</div>
            < img
                className={classes.addButton}
                onClick={onChange}
                src={addIcon}
                alt='add icon'
            />
        </Grid>
    )
}