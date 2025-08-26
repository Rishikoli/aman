'use client';

import React, { useState } from 'react';
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
  Chip,
  Menu,
  MenuItem,
} from '@mui/material';
import {
  Search,
  Add,
  Assessment,
  Notifications,
  CalendarToday,
  KeyboardArrowDown,
  NavigateNext,
} from '@mui/icons-material';
import { usePathname } from 'next/navigation';

const Header: React.FC = () => {
  const pathname = usePathname();
  const [dateMenuAnchor, setDateMenuAnchor] = useState<null | HTMLElement>(null);

  const handleDateMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setDateMenuAnchor(event.currentTarget);
  };

  const handleDateMenuClose = () => {
    setDateMenuAnchor(null);
  };

  // Generate breadcrumbs based on current route
  const generateBreadcrumbs = () => {
    const pathSegments = pathname.split('/').filter(segment => segment);
    const breadcrumbs = [
      { label: 'Dashboard', href: '/dashboard' }
    ];

    pathSegments.forEach((segment, index) => {
      if (segment !== 'dashboard') {
        const href = '/' + pathSegments.slice(0, index + 1).join('/');
        const label = segment.charAt(0).toUpperCase() + segment.slice(1);
        breadcrumbs.push({ label, href });
      }
    });

    return breadcrumbs;
  };

  const breadcrumbs = generateBreadcrumbs();

  return (
    <AppBar 
      position="static" 
      color="default" 
      elevation={0}
      sx={{
        backgroundColor: '#ffffff',
        borderBottom: '1px solid #e2e8f0',
        boxShadow: '0 1px 3px rgba(0, 0, 0, 0.04)',
      }}
    >
      <Toolbar sx={{ 
        justifyContent: 'space-between', 
        py: 1.5,
        minHeight: 80,
        px: 3
      }}>
        {/* Left section - Breadcrumbs */}
        <Box sx={{ display: 'flex', alignItems: 'center', flex: 1 }}>
          <Breadcrumbs 
            aria-label="breadcrumb" 
            separator={<NavigateNext fontSize="small" />}
            sx={{ mr: 3 }}
          >
            {breadcrumbs.map((crumb, index) => (
              index === breadcrumbs.length - 1 ? (
                <Typography key={crumb.href} color="text.primary" fontWeight={600}>
                  {crumb.label}
                </Typography>
              ) : (
                <Link 
                  key={crumb.href}
                  underline="hover" 
                  color="text.secondary" 
                  href={crumb.href}
                  sx={{ 
                    '&:hover': { color: 'primary.main' },
                    transition: 'color 0.2s ease'
                  }}
                >
                  {crumb.label}
                </Link>
              )
            ))}
          </Breadcrumbs>
        </Box>

        {/* Center section - Global Search Bar */}
        <Box sx={{ display: 'flex', alignItems: 'center', flex: 2, justifyContent: 'center' }}>
          <TextField
            size="small"
            placeholder="Search deals, companies, agents, or reports..."
            sx={{ 
              minWidth: 400,
              '& .MuiOutlinedInput-root': {
                borderRadius: 2,
                backgroundColor: '#f8fafc',
                '&:hover': {
                  backgroundColor: '#f1f5f9',
                },
                '&.Mui-focused': {
                  backgroundColor: '#ffffff',
                }
              }
            }}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <Search sx={{ color: 'text.secondary' }} />
                </InputAdornment>
              ),
            }}
          />
        </Box>

        {/* Right section - Date Picker, Actions and User Management */}
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, flex: 1, justifyContent: 'flex-end' }}>
          {/* Date Range Picker */}
          <Button
            variant="outlined"
            size="small"
            startIcon={<CalendarToday />}
            endIcon={<KeyboardArrowDown />}
            onClick={handleDateMenuOpen}
            sx={{ 
              borderColor: '#e2e8f0',
              color: 'text.secondary',
              '&:hover': {
                borderColor: 'primary.main',
                backgroundColor: 'primary.50'
              }
            }}
          >
            Last 30 days
          </Button>
          <Menu
            anchorEl={dateMenuAnchor}
            open={Boolean(dateMenuAnchor)}
            onClose={handleDateMenuClose}
          >
            <MenuItem onClick={handleDateMenuClose}>Last 7 days</MenuItem>
            <MenuItem onClick={handleDateMenuClose}>Last 30 days</MenuItem>
            <MenuItem onClick={handleDateMenuClose}>Last 90 days</MenuItem>
            <MenuItem onClick={handleDateMenuClose}>Custom range</MenuItem>
          </Menu>

          {/* Action Buttons */}
          <Button
            variant="contained"
            startIcon={<Add />}
            size="small"
            sx={{ 
              borderRadius: 2,
              textTransform: 'none',
              fontWeight: 600,
              px: 2
            }}
          >
            Add Deal
          </Button>
          
          <Button
            variant="outlined"
            startIcon={<Assessment />}
            size="small"
            sx={{ 
              borderRadius: 2,
              textTransform: 'none',
              fontWeight: 600,
              px: 2,
              borderColor: '#e2e8f0',
              '&:hover': {
                borderColor: 'primary.main',
                backgroundColor: 'primary.50'
              }
            }}
          >
            Create Report
          </Button>

          {/* Team Member Avatars */}
          <AvatarGroup 
            max={4} 
            sx={{ 
              mr: 2,
              '& .MuiAvatar-root': {
                width: 36,
                height: 36,
                fontSize: '0.875rem',
                border: '2px solid #ffffff',
                boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)'
              }
            }}
          >
            <Avatar sx={{ bgcolor: '#3b82f6' }}>JD</Avatar>
            <Avatar sx={{ bgcolor: '#10b981' }}>SM</Avatar>
            <Avatar sx={{ bgcolor: '#f59e0b' }}>AR</Avatar>
            <Avatar sx={{ bgcolor: '#ef4444' }}>MK</Avatar>
            <Avatar sx={{ bgcolor: '#8b5cf6' }}>+2</Avatar>
          </AvatarGroup>

          {/* Notifications */}
          <IconButton 
            size="small"
            sx={{ 
              backgroundColor: '#f8fafc',
              '&:hover': { backgroundColor: '#f1f5f9' }
            }}
          >
            <Notifications />
          </IconButton>

          {/* User Avatar */}
          <Avatar sx={{ 
            width: 40, 
            height: 40, 
            bgcolor: 'primary.main',
            fontWeight: 600,
            cursor: 'pointer',
            '&:hover': {
              boxShadow: '0 4px 8px rgba(0, 0, 0, 0.15)'
            }
          }}>
            U
          </Avatar>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header;