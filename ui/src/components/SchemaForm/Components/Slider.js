import React from 'react';
import { Grid, Slider } from '@mui/material';
import { useStyles } from './Style.styles';

export function MUISlider({ property, value, onChange }) {
    const classes = useStyles();
    const handleChange = (event, newValue) => {
        onChange(newValue)
    }

    return (
        <Grid item className={classes.grid}>
            <div className={classes.title}>{property.title}</div>
            <Slider
                value={value !== undefined ? value : property.minimum ? property.minimum : 0}
                min={property.minimum ? property.minimum : 0}
                onChange={handleChange}
                valueLabelDisplay='auto'
                className={classes.slider}
            />
        </Grid>
    )
}