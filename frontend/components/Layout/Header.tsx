import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Box,
  IconButton,
  Avatar,
  AvatarGroup,
  Button,
  Breadcrumbs,
  Link,
  TextField,
  InputAdornment,
} from '@mui/material';
import {
  Search,
  Add,
  Assessment,
  Notifications,
  Settings,
} from '@mui/icons-material';

const Header: React.FC = () => {
  return (
    <AppBar position="static" color="default" elevation={1}>
      <Toolbar sx={{ justifyContent: 'space-between', py: 1 }}>
        {/* Left section - Breadcrumbs */}
        <Box sx={{ display: 'flex', alignItems: 'center', flex: 1 }}>
          <Breadcrumbs aria-label="breadcrumb" sx={{ mr: 3 }}>
            <Link underline="hover" color="inherit" href="/">
              Dashboard
            </Link>
            <Typography color="text.primary">Overview</Typography>
          </Breadcrumbs>
        </Box>

        {/* Center section - Search */}
        <Box sx={{ display: 'flex', alignItems: 'center', flex: 2, justifyContent: 'center' }}>
          <TextField
            size="small"
            placeholder="Search deals, companies, or reports..."
            sx={{ minWidth: 300 }}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <Search />
                </InputAdornment>
              ),
            }}
          />
        </Box>

        {/* Right section - Actions and User */}
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, flex: 1, justifyContent: 'flex-end' }}>
          <Button
            variant="contained"
            startIcon={<Add />}
            size="small"
            sx={{ mr: 1 }}
          >
            Add Deal
          </Button>
          
          <Button
            variant="outlined"
            startIcon={<Assessment />}
            size="small"
            sx={{ mr: 2 }}
          >
            Create Report
          </Button>

          <AvatarGroup max={3} sx={{ mr: 2 }}>
            <Avatar sx={{ width: 32, height: 32, bgcolor: 'primary.main' }}>A</Avatar>
            <Avatar sx={{ width: 32, height: 32, bgcolor: 'secondary.main' }}>B</Avatar>
            <Avatar sx={{ width: 32, height: 32, bgcolor: 'success.main' }}>C</Avatar>
          </AvatarGroup>

          <IconButton size="small">
            <Notifications />
          </IconButton>
          
          <IconButton size="small">
            <Settings />
          </IconButton>

          <Avatar sx={{ width: 32, height: 32, bgcolor: 'primary.main' }}>
            U
          </Avatar>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header;