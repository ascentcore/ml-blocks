import React from 'react';
import { makeStyles } from '@mui/styles';

export const useStyles = makeStyles((theme) => ({
    root: {
        position: 'absolute',
        bottom: 0,
        width: '100%',
    }
}))

function Footer() {
    const classes = useStyles();

    return (
        <>
            <h3 className={classes.root}>Footer</h3>
        </>
    )
};

export default Footer;