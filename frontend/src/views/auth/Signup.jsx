import React, { useRef, useState } from 'react';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Paper from '@mui/material/Paper';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import CircularProgress from '@mui/material/CircularProgress';
import { Controller, useForm } from 'react-hook-form';
import { Link } from '@mui/material';
import PublicWrapper from '../../components/layouts/Public';
import Validations from '../../utils/Validations';
import { registerUser } from '../../api/Auth';
import useToastr from '../../hooks/useToastr';
import RoutePaths from '../../configs/Routes';

const Register = () => {
  const { control, handleSubmit, watch } = useForm();
  const { showSuccessToastr, showErrorToastr } = useToastr();

  const [processing, setProcessing] = useState(false);

  const password = useRef({});
  password.current = watch('password', '');

  const onSubmit = async (data) => {
    setProcessing(true);
    try {
      if (data.password !== data.confirmPassword) {
        showErrorToastr('Passwords does not match.');
        return;
      }
      const userData = {
        first_name: data.firstName,
        last_name: data.lastName,
        email: data.email,
        password: data.password,
        confirm_password: data.confirmPassword,
      };

      const response = await registerUser(userData);

      if (response.success) {
        showSuccessToastr('Registered and logged in successfully');
        window.localStorage.setItem('isLoggedIn', true);
        window.location.assign(RoutePaths.HOME);
      } else {
        showErrorToastr(response.message);
      }
    } catch (error) {
      showErrorToastr(error?.message || 'Something went wrong.');
      setProcessing(false);
    }
  };

  return (
    <PublicWrapper>
      <Box
        style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}
      >
        <Container component="main" maxWidth="sm" sx={{ mb: 4 }}>
          <Paper variant="outlined" sx={{ my: { xs: 3, md: 6 }, p: { xs: 2, md: 3 } }}>
            <Typography variant="h6" gutterBottom>
              Register
            </Typography>
            <form onSubmit={handleSubmit(onSubmit)}>
              <Grid container spacing={3}>
                <Grid item xs={12}>
                  <Controller
                    control={control}
                    id="firstName"
                    name="firstName"
                    rules={{ ...Validations.REQUIRED }}
                    render={({ field: { onChange, value }, fieldState: { error } }) => (
                      <TextField
                        required
                        id="firstName"
                        name="firstName"
                        label="First Name"
                        fullWidth
                        variant="standard"
                        type="text"
                        value={value}
                        onChange={onChange}
                        error={!!error}
                        helperText={error ? error?.message : null}
                      />
                    )}
                  />
                </Grid>
                <Grid item xs={12}>
                  <Controller
                    control={control}
                    id="lastName"
                    name="lastName"
                    rules={{ ...Validations.REQUIRED }}
                    render={({ field: { onChange, value }, fieldState: { error } }) => (
                      <TextField
                        required
                        id="lastName"
                        name="lastName"
                        label="Last Name"
                        fullWidth
                        variant="standard"
                        type="text"
                        value={value}
                        onChange={onChange}
                        error={!!error}
                        helperText={error ? error?.message : null}
                      />
                    )}
                  />
                </Grid>
                <Grid item xs={12}>
                  <Controller
                    control={control}
                    id="email"
                    name="email"
                    rules={{ ...Validations.EMAIL_REQUIRED }}
                    render={({ field: { onChange, value } }) => (
                      <TextField
                        required
                        id="email"
                        name="email"
                        label="Email"
                        fullWidth
                        variant="standard"
                        type="email"
                        value={value}
                        onChange={onChange}
                      />
                    )}
                  />
                </Grid>
                <Grid item xs={12}>
                  <Controller
                    control={control}
                    id="password"
                    name="password"
                    rules={{
                      ...Validations.REQUIRED,
                      ...{
                        minLength: {
                          value: 8,
                          message: `Password must be 8 characters long.`,
                        },
                      },
                    }}
                    render={({ field: { onChange, value }, fieldState: { error } }) => (
                      <TextField
                        required
                        id="password"
                        name="password"
                        label="Password"
                        fullWidth
                        variant="standard"
                        type="password"
                        value={value}
                        onChange={onChange}
                        error={!!error}
                        helperText={error ? error?.message : null}
                      />
                    )}
                  />
                </Grid>
                <Grid item xs={12}>
                  <Controller
                    control={control}
                    id="confirmPassword"
                    name="confirmPassword"
                    rules={{
                      ...Validations.REQUIRED,

                      ...{
                        minLength: {
                          value: 8,
                          message: `Password must be 8 characters long.`,
                        },
                      },

                      validate: (value) =>
                        value === password.current || 'Provided passwords does not match',
                    }}
                    render={({ field: { onChange, value }, fieldState: { error } }) => (
                      <TextField
                        required
                        id="confirmPassword"
                        name="confirmPassword"
                        label="Confirm Password"
                        fullWidth
                        variant="standard"
                        type="password"
                        value={value}
                        onChange={onChange}
                        error={!!error}
                        helperText={error ? error?.message : null}
                      />
                    )}
                  />
                </Grid>
                <Grid item xs={12}>
                  <Typography color="textSecondary" variant="body2">
                    Have an account?{' '}
                    <Link href="/login" underline="hover">
                      Sign In
                    </Link>
                  </Typography>
                </Grid>
                <Grid item xs={12}>
                  <Button
                    variant="contained"
                    fullWidth
                    type="submit"
                    endIcon={processing && <CircularProgress color="secondary" size={18} />}
                    disabled={processing}
                  >
                    {processing ? 'Registering' : 'Register'}
                  </Button>
                </Grid>
              </Grid>
            </form>
          </Paper>
        </Container>
      </Box>
    </PublicWrapper>
  );
};

export default Register;
