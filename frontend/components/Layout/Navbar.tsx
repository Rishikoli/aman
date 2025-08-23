import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Box,
  Button,
  IconButton,
  Avatar,
  TextField,
  InputAdornment,
  Tabs,
  Tab,
} from '@mui/material';
import {
  Search,
  Add,
  Assessment,
  Notifications,
  Settings,
  Dashboard,
  Business,
  SmartToy,
  BarChart,
} from '@mui/icons-material';

const navItems = [
  { text: 'Dashboard', icon: <Dashboard />, href: '/' },
  { text: 'Deals', icon: <Business />, href: '/deals' },
  { text: 'Companies', icon: <Assessment />, href: '/companies' },
  { text: 'Agents', icon: <SmartToy />, href: '/agents' },
  { text: 'Reports', icon: <BarChart />, href: '/reports' },
  { text: 'AI Demo', icon: <SmartToy />, href: '/ai-demo' },
];

const Navbar: React.FC = () => {
  const [value, setValue] = React.useState(0);

  const handleChange = (_event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };

  return (
    <AppBar
      position="static"
      elevation={0}
      sx={{
        backgroundColor: '#f6f5fa',
        borderBottom: 'none',
        boxShadow: 'none',
        '&.MuiAppBar-root': {
          boxShadow: 'none',
        }
      }}
    >
      <Toolbar sx={{ justifyContent: 'space-between', py: 1 }}>
        {/* Left section - Logo and Navigation */}
        <Box sx={{ display: 'flex', alignItems: 'center', flex: 1 }}>
          <Box sx={{ mr: 4 }}>
            <Typography variant="h6" component="div" sx={{ fontWeight: 600 }}>
              AMAN
            </Typography>
            <Typography variant="caption" color="text.secondary" sx={{ lineHeight: 1 }}>
              M&A Navigator
            </Typography>
          </Box>

          <Tabs
            value={value}
            onChange={handleChange}
            sx={{
              '& .MuiTab-root': {
                minHeight: 48,
                textTransform: 'none',
                fontSize: '0.875rem',
                fontWeight: 500,
              }
            }}
          >
            {navItems.map((item) => (
              <Tab
                key={item.text}
                icon={item.icon}
                iconPosition="start"
                label={item.text}
                sx={{
                  '& .MuiTab-iconWrapper': {
                    marginRight: 1,
                    marginBottom: 0,
                  }
                }}
              />
            ))}
          </Tabs>
        </Box>

        {/* Center section - Search */}
        <Box sx={{ display: 'flex', alignItems: 'center', flex: 1, justifyContent: 'center' }}>
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

export default Navbar;