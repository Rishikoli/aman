import React from 'react';
import { Box, Container } from '@mui/material';
import Navbar from './Navbar';
import Sidebar from './Sidebar';

interface LayoutProps {
  children: React.ReactNode;
  showSidebar?: boolean;
}

const Layout: React.FC<LayoutProps> = ({ children, showSidebar = true }) => {
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh', backgroundColor: '#f6f5fa' }}>
      <Navbar />
      <Box sx={{ display: 'flex', flexGrow: 1 }}>
        {showSidebar && <Sidebar />}
        <Box component="main" sx={{ flexGrow: 1, p: 3, backgroundColor: '#f6f5fa' }}>
          <Container maxWidth="xl">
            {children}
          </Container>
        </Box>
      </Box>
    </Box>
  );
};

export default Layout;