import { AppBar, Container, Grid, Link, Toolbar, Typography } from '@mui/material';
import React from 'react';
import { makeStyles } from '@mui/styles';

export const useStyles = makeStyles((theme) => ({
    appbar: {
        flexGrow: 1,
        background: '#6b5b95',
    },
    link: {
        color: '#FFF',
        marginRight: '10px',
        marginLeft: '50px'
    }
}))

function Header() {
    const classes = useStyles();
    return (
        <div style={{ flexGrow: 1 }}>
            <AppBar position='static' className={classes.appbar}>
                <Container maxWidth="lg">
                    <Toolbar>
                        <Link href="/upload" className={classes.link} underline='none'>Upload</Link>
                        <Link href="/" className={classes.link} underline='none'>Home</Link>
                    </Toolbar>
                </Container>
            </AppBar>
        </div>
    )
};

export default Header;