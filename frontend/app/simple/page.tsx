'use client';

import { Typography, Box } from '@mui/material';

export default function SimplePage() {
  return (
    <Box sx={{ p: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Simple Test Page
      </Typography>
      <Typography variant="body1">
        This is a simple page to test if MUI components work correctly.
      </Typography>
    </Box>
  );
}