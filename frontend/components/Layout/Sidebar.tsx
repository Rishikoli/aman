'use client';

import React, { useState } from 'react';
import {
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  Box,
  Tooltip,
  Typography,
} from '@mui/material';
import {
  Dashboard,
  Business,
  Assessment,
  SmartToy,
  BarChart,
} from '@mui/icons-material';
import { usePathname } from 'next/navigation';
import Link from 'next/link';

const drawerWidth = 80;

// Navigation items matching reference design requirements
const navigationItems = [
  { text: 'Dashboard', icon: <Dashboard />, href: '/dashboard', id: 'dashboard' },
  { text: 'Deals', icon: <Business />, href: '/deals', id: 'deals' },
  { text: 'Companies', icon: <Assessment />, href: '/companies', id: 'companies' },
  { text: 'Agents', icon: <SmartToy />, href: '/agents', id: 'agents' },
  { text: 'Reports', icon: <BarChart />, href: '/reports', id: 'reports' },
];

const Sidebar: React.FC = () => {
  const pathname = usePathname();
  const [activeItem, setActiveItem] = useState('dashboard');

  const isActive = (href: string) => {
    if (!pathname) return false;
    return pathname === href || pathname.startsWith(href + '/');
  };

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: drawerWidth,
          boxSizing: 'border-box',
          borderRight: '1px solid #e2e8f0',
          backgroundColor: '#ffffff',
          boxShadow: '2px 0 8px rgba(0, 0, 0, 0.04)',
        },
      }}
    >
      {/* Logo/Brand Section */}
      <Box sx={{
        height: 80,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        borderBottom: '1px solid #e2e8f0'
      }}>
        <Box sx={{
          width: 40,
          height: 40,
          bgcolor: 'primary.main',
          borderRadius: 2,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: 'white',
          fontWeight: 'bold',
          fontSize: '1.2rem'
        }}>
          A
        </Box>
      </Box>

      {/* Navigation Items */}
      <List sx={{ flexGrow: 1, pt: 3, px: 1 }}>
        {navigationItems.map((item) => (
          <ListItem key={item.id} disablePadding sx={{ mb: 1 }}>
            <Tooltip title={item.text} placement="right" arrow>
              <ListItemButton
                component={Link}
                href={item.href}
                onClick={() => setActiveItem(item.id)}
                sx={{
                  borderRadius: 2,
                  minHeight: 56,
                  justifyContent: 'center',
                  backgroundColor: isActive(item.href) ? 'primary.main' : 'transparent',
                  color: isActive(item.href) ? 'white' : 'text.secondary',
                  transition: 'all 0.2s ease-in-out',
                  '&:hover': {
                    backgroundColor: isActive(item.href) ? 'primary.dark' : 'action.hover',
                    transform: 'translateX(2px)',
                  },
                }}
              >
                <ListItemIcon sx={{
                  minWidth: 'auto',
                  justifyContent: 'center',
                  color: 'inherit'
                }}>
                  {item.icon}
                </ListItemIcon>
              </ListItemButton>
            </Tooltip>
          </ListItem>
        ))}
      </List>

      {/* Bottom section with subtle branding */}
      <Box sx={{
        p: 2,
        borderTop: '1px solid #e2e8f0',
        display: 'flex',
        justifyContent: 'center'
      }}>
        <Typography variant="caption" color="text.disabled" sx={{
          transform: 'rotate(-90deg)',
          whiteSpace: 'nowrap',
          fontSize: '0.7rem'
        }}>
          AMAN
        </Typography>
      </Box>
    </Drawer>
  );
};

export default Sidebar;