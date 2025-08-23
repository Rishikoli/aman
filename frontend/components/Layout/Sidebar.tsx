import React from 'react';
import {
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  Box,
  Divider,
  Tooltip,
} from '@mui/material';
import {
  Bookmark,
  History,
  Star,
  Folder,
  Settings,
  Help,
} from '@mui/icons-material';

const drawerWidth = 80;

const quickAccessItems = [
  { text: 'Bookmarks', icon: <Bookmark />, href: '/bookmarks' },
  { text: 'Recent', icon: <History />, href: '/recent' },
  { text: 'Favorites', icon: <Star />, href: '/favorites' },
  { text: 'Files', icon: <Folder />, href: '/files' },
];

const bottomMenuItems = [
  { text: 'Settings', icon: <Settings />, href: '/settings' },
  { text: 'Help', icon: <Help />, href: '/help' },
];

const Sidebar: React.FC = () => {
  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: drawerWidth,
          boxSizing: 'border-box',
          borderRight: 'none',
          backgroundColor: '#f6f5fa',
        },
      }}
    >
      <Box sx={{ height: 64 }} /> {/* Spacer for navbar height */}
      
      <List sx={{ flexGrow: 1, pt: 2 }}>
        {quickAccessItems.map((item) => (
          <ListItem key={item.text} disablePadding>
            <Tooltip title={item.text} placement="right">
              <ListItemButton
                sx={{
                  mx: 1,
                  mb: 1,
                  borderRadius: 1,
                  minHeight: 48,
                  justifyContent: 'center',
                  '&:hover': {
                    backgroundColor: 'action.hover',
                  },
                }}
              >
                <ListItemIcon sx={{ minWidth: 'auto', justifyContent: 'center' }}>
                  {item.icon}
                </ListItemIcon>
              </ListItemButton>
            </Tooltip>
          </ListItem>
        ))}
      </List>

      <Divider />
      
      <List sx={{ pb: 2 }}>
        {bottomMenuItems.map((item) => (
          <ListItem key={item.text} disablePadding>
            <Tooltip title={item.text} placement="right">
              <ListItemButton
                sx={{
                  mx: 1,
                  mb: 1,
                  borderRadius: 1,
                  minHeight: 48,
                  justifyContent: 'center',
                  '&:hover': {
                    backgroundColor: 'action.hover',
                  },
                }}
              >
                <ListItemIcon sx={{ minWidth: 'auto', justifyContent: 'center' }}>
                  {item.icon}
                </ListItemIcon>
              </ListItemButton>
            </Tooltip>
          </ListItem>
        ))}
      </List>
    </Drawer>
  );
};

export default Sidebar;