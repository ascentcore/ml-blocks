import React from 'react';
import addIcon from './add-icon.png';
import { useStyles } from './Style.styles';
import { Button } from '@mui/material';

export function MUIAddButton({ property, onChange }) {
    const classes = useStyles();
    return (
        <Button onClick={onChange} style={{ backgroundColor: 'transparent' }}>
            < img
                className={classes.addButton}
                src={addIcon}
                alt='add icon'
            />
        </Button>
    )
}