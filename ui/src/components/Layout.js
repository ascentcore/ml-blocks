import React from 'react';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import Header from './Header';
import Footer from './Footer';

const Layout = ({ children }) => {
    return (
        <>
            <Grid container justifyContent="center" direction="column" >
                <Header />
                <Container maxWidth="md">{children}</Container>
            </Grid>
            <Footer />
        </>
    );
}

export default Layout;