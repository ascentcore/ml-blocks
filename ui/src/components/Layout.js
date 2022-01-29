import React from 'react';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import Header from './Header';
import Footer from './Footer';

const Layout = ({ children }) => {
    return (
        <>
            <Grid container direction="column" >
                <Header />
                <main>{children}</main>
            </Grid>
            <Footer />
        </>
    );
}

export default Layout;