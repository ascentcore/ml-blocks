import React, { useState } from 'react';
import { FormControl, FormControlLabel, Radio, RadioGroup } from '@mui/material';
import { useStyles } from './Style.styles';

export function MUIRadioButtons({ property, value, onChange }) {
    const classes = useStyles();
    const handleChange = (e) => {
        onChange(e.target.value);
    }
    return (
        <FormControl>
            <div className={classes.title}>{property.title}*</div>
            <RadioGroup value={value} onChange={handleChange} className={classes.radioButton}>
                {property.enum.map((item, index) => {
                    return (
                        <FormControlLabel
                            key={index}
                            control={<Radio required={property.isRequired} />}
                            label={item}
                            value={item}
                        />
                    )
                })}
            </RadioGroup>
        </FormControl>
    )
}