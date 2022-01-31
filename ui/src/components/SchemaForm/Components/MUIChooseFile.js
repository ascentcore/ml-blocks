import React from 'react';
import { Grid, Button } from '@mui/material';
import { useStyles } from './Style.styles';

export function MUIChooseFile({ property, onChange }) {
    const classes = useStyles();
    return (
        <Grid container className={classes.grid}>

            <Button
                variant="text"
                className={classes.chooseFile}
                onClick={onChange}
            >
                <input
                    type="file"
                    accept="image/*"
                />
            </Button>
        </Grid>
    )
}