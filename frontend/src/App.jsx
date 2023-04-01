import React, { useEffect } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import CssBaseline from '@mui/material/CssBaseline';
import { StyledEngineProvider } from '@mui/material/styles';

import { RoutePaths } from './configs';
import {
  LoginPage,
  ForgotPasswordPage,
  NotFoundPage,
  LogoutPage,
  HomePage,
  ResetPasswordPage,
  SignupPage,
} from './views';
import { ToastrProvider } from './contexts/ToastrContext';
import './assets/styles/fonts.css';
import AppThemeProvider from './contexts/ThemeContext';
import './App.css';

const App = () => {
  useEffect(async () => {
    try {
      // DO SOMETHING
    } catch {
      // DO SOMETHING
    }
  }, []);

  return (
    <StyledEngineProvider injectFirst>
      <AppThemeProvider>
        <CssBaseline />
        <ToastrProvider>
          <Router>
            <Switch>
              <Route exact path={RoutePaths.HOME} component={HomePage} />
              <Route exact path={RoutePaths.SIGN_UP} component={SignupPage} />
              <Route exact path={RoutePaths.LOGIN} component={LoginPage} />
              <Route exact path={RoutePaths.FORGOT_PASSWORD} component={ForgotPasswordPage} />
              <Route exact path={RoutePaths.RESET_PASSWORD} component={ResetPasswordPage} />
              <Route exact path={RoutePaths.LOGOUT} component={LogoutPage} />
              <Route component={NotFoundPage} />
            </Switch>
          </Router>
        </ToastrProvider>
      </AppThemeProvider>
    </StyledEngineProvider>
  );
};

export default App;
