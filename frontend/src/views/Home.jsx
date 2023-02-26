import React from 'react';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';

import Box from '@mui/material/Box';
import Container from '@mui/material/Container';

import { PrivateWrapper } from '../components/layouts';

// 404 Page
const Home = () => {
  const pageName = 'home';

  return (
    <PrivateWrapper>
      <Grid
        container
        spacing={0}
        height="100vh"
        alignItems="center"
        justifyContent="center"
        direction="row"
      >
        <Box
          maxWidth="xs"
          alignItems="center"
          justifyContent="center"
          display="flex"
          flexDirection="column"
        >
          <Container component="div">
            <Typography component="h1" variant="h1" align="center">
              {pageName}
            </Typography>
          </Container>
        </Box>
      </Grid>
    </PrivateWrapper>
  );
};

export default Home;
