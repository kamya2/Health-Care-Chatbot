/* eslint-disable react/prop-types */
import React from 'react';
import { Grid, Card, CardHeader, CardContent, Typography, Paper, Box } from '@mui/material';
import { Info, CheckCircle, Warning } from '@mui/icons-material';
import { PrivateWrapper } from '../components/layouts';

const ExampleCard = ({ title, icon }) => (
  <Card sx={{ height: '100%' }}>
    <CardHeader
      avatar={icon}
      title={title}
      sx={{ backgroundColor: 'primary.main', color: 'primary.contrastText' }}
    />
    <CardContent>
      <Box component={Paper} p={2} m={1}>
        <Typography variant="body1">What are the symptoms of a cold?</Typography>
      </Box>
      <Box component={Paper} p={2} m={1}>
        <Typography variant="body1">How can I prevent hair loss?</Typography>
      </Box>
      <Box component={Paper} p={2} m={1}>
        <Typography variant="body1">What is the cure for pneumonia?</Typography>
      </Box>
      <Box component={Paper} p={2} m={1}>
        <Typography variant="body1">reason for headache?</Typography>
      </Box>
    </CardContent>
  </Card>
);

const CapabilityCard = ({ title, icon }) => (
  <Card sx={{ height: '100%' }}>
    <CardHeader
      avatar={icon}
      title={title}
      sx={{ backgroundColor: 'success.main', color: 'success.contrastText' }}
    />
    <CardContent>
      <Box display="flex" flexDirection="column" justifyContent="space-between">
        <Typography variant="body1" py={2}>
          Fast and convenient: No need to wait on hold or schedule an appointment - MediCare is
          quick and easy to use.
        </Typography>
        <Typography variant="body1" py={2}>
          Answer queries: Our chatbot is here to answer any questions you may have about your health
          or well-being.
        </Typography>
        <Typography variant="body1" py={2}>
          Give information: Our chatbot can provide you with detailed information about various
          medical conditions, their symptoms, causes, and treatment options.
        </Typography>
      </Box>
    </CardContent>
  </Card>
);

const LimitationCard = ({ title, icon }) => (
  <Card sx={{ height: '100%' }}>
    <CardHeader
      avatar={icon}
      title={title}
      sx={{ backgroundColor: 'warning.main', color: 'warning.contrastText' }}
    />
    <CardContent>
      <Typography variant="body1" py={2}>
        MediCare Bot is not a substitute for a doctor: While MediCare Bot can provide helpful
        information, it is not a replacement for medical advice from a licensed physician.
      </Typography>
      <Typography variant="body1" py={2}>
        Limited scope: MediCare Bot is designed to provide general medical information and advice,
        but it may not be able to answer every question or address every concern.
      </Typography>
    </CardContent>
  </Card>
);
// Main Home Page
const Home = () => (
  <PrivateWrapper pageName="MediCare Bot">
    <Grid minHeight="90vh" container alignItems="center" justifyContent="center">
      <Grid container spacing={2}>
        <Grid item xs={12} md={4}>
          <ExampleCard title="Examples" icon={<Info />} />
        </Grid>
        <Grid item xs={12} md={4}>
          <CapabilityCard title="Capabilities" icon={<CheckCircle />} />
        </Grid>
        <Grid item xs={12} md={4}>
          <LimitationCard title="Limitations" icon={<Warning />} />
        </Grid>
      </Grid>
    </Grid>
  </PrivateWrapper>
);

export default Home;
