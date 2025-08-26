import React from 'react';
import { Box, Container } from '@mui/material';
import Header from './Header';
import Sidebar from './Sidebar';

interface LayoutProps {
  children: React.ReactNode;
  showSidebar?: boolean;
}

const Layout: React.FC<LayoutProps> = ({ children, showSidebar = true }) => {
  return (
    <Box sx={{ 
      display: 'flex', 
      minHeight: '100vh', 
      backgroundColor: '#fafafa' // Clean white background as per requirements
    }}>
      {/* Left Sidebar Navigation */}
      {showSidebar && <Sidebar />}
      
      {/* Main Content Area */}
      <Box sx={{ 
        flexGrow: 1, 
        display: 'flex', 
        flexDirection: 'column',
        minHeight: '100vh'
      }}>
        {/* Top Header */}
        <Header />
        
        {/* Main Content with proper spacing and card-based layout */}
        <Box 
          component="main" 
          sx={{ 
            flexGrow: 1, 
            p: 3, 
            backgroundColor: '#fafafa',
            overflow: 'auto'
          }}
        >
          <Container maxWidth="xl" sx={{ height: '100%' }}>
            {children}
          </Container>
        </Box>
      </Box>
    </Box>
  );
};

export default Layout;