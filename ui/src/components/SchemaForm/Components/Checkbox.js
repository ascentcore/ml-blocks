import React from 'react';
import { Checkbox } from '@mui/material';

export function MUICheckbox({ property }) {
    return (
        <>
            {property.title}
            <Checkbox />
        </>
    )
}