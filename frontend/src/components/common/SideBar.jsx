import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import Drawer from '@mui/material/Drawer';
import Stack from '@mui/material/Stack';
import IconButton from '@mui/material/IconButton';
import List from '@mui/material/List';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import DisplaySettingsOutlinedIcon from '@mui/icons-material/DisplaySettingsOutlined';
import CloseIcon from '@mui/icons-material/MenuOpen';
import DeleteIcon from '@mui/icons-material/Delete';
import ExitToAppOutlinedIcon from '@mui/icons-material/ExitToAppOutlined';
import AddBoxOutlinedIcon from '@mui/icons-material/AddBoxOutlined';
import { Box, Divider, Paper, Typography } from '@mui/material';
import QuestionAnswerOutlinedIcon from '@mui/icons-material/QuestionAnswerOutlined';
import { NAV_DRAWER_WIDTH, RoutePaths } from '../../configs';
import NavItem from './NavItem';
import { deleteConversation, getConversations } from '../../api/Bot';
import useToastr from '../../hooks/useToastr';

const SideBar = ({ open, onClose }) => {
  const { showErrorToastr, showSuccessToastr } = useToastr();

  const [conversations, setConversations] = useState([]);

  const handleGetConversations = async () => {
    const response = await getConversations();

    if (response.success) {
      setConversations(response?.data?.conversations || []);
    } else {
      showErrorToastr(response.message);
    }
  };
  const handleDeleteConversation = async (conversationId) => {
    const response = await deleteConversation(conversationId);

    if (response.success) {
      showSuccessToastr('Conversation deleted successfully.');
      setTimeout(() => {
        window.location.assign(RoutePaths.HOME);
      }, 300);
    } else {
      showErrorToastr(response.message);
    }
  };

  useEffect(() => {
    handleGetConversations();
  }, []);

  return (
    <Drawer
      open={open}
      variant="persistent"
      anchor="left"
      onClose={onClose}
      sx={{
        width: NAV_DRAWER_WIDTH,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          minWidth: NAV_DRAWER_WIDTH,
          bgcolor: 'background.paper',
        },
      }}
    >
      <Stack
        direction="row"
        alignItems="center"
        sx={{
          height: 80,
          flexShrink: 0,
          px: 0.5,
          position: 'sticky',
          top: 0,
          zIndex: 'appBar',
          backgroundColor: 'inherit',
          backgroundImage: 'inherit',
        }}
      >
        <IconButton aria-label="Close navigation drawer" onClick={onClose} size="large">
          <CloseIcon />
        </IconButton>
      </Stack>

      <nav>
        <List disablePadding>
          <li>
            <NavItem to={RoutePaths.HOME}>
              <ListItemIcon>
                <DisplaySettingsOutlinedIcon />
              </ListItemIcon>
              <ListItemText primary="Project Details" />
            </NavItem>
          </li>

          <Box sx={{ my: 1 }}>
            <Divider />
            <li>
              <NavItem sx={{ mt: 2 }} to={RoutePaths.CHAT.replace(':conversationId', 'new')}>
                <ListItemIcon>
                  <AddBoxOutlinedIcon />
                </ListItemIcon>
                <ListItemText primary={'New Conversation'.toUpperCase()} />
              </NavItem>
            </li>

            {conversations.length === 0 && (
              <Box component={Paper} sx={{ p: 2, m: 2 }}>
                <Typography variant="body">No Conversations Found.</Typography>
              </Box>
            )}

            {conversations.map((conversation) => (
              <li key={conversation.conversation_id}>
                <NavItem
                  to={`${RoutePaths.CHAT.replace(':conversationId', conversation.conversation_id)}`}
                >
                  <ListItemIcon>
                    <QuestionAnswerOutlinedIcon />
                  </ListItemIcon>
                  <ListItemText primary={conversation.title} />
                  <ListItemIcon>
                    <IconButton
                      size="small"
                      onClick={() => {
                        handleDeleteConversation(conversation.conversation_id);
                      }}
                    >
                      <DeleteIcon />
                    </IconButton>
                  </ListItemIcon>
                </NavItem>
              </li>
            ))}
          </Box>
          <Divider />
          <li>
            <NavItem to={RoutePaths.LOGOUT}>
              <ListItemIcon>
                <ExitToAppOutlinedIcon />
              </ListItemIcon>
              <ListItemText primary="Logout" />
            </NavItem>
          </li>
        </List>
      </nav>
    </Drawer>
  );
};

SideBar.propTypes = {
  open: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
};

export default SideBar;
