'use client';

import React from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  Chip,
} from '@mui/material';
import Layout from '../../components/Layout/Layout';

export default function AgentsPage() {
  return (
    <Layout>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" sx={{ fontWeight: 600, mb: 1, color: 'text.primary' }}>
          AI Agent Management
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Monitor and configure your autonomous AI agents for due diligence
        </Typography>
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Card>
            <CardContent sx={{ p: 4, textAlign: 'center' }}>
              <Typography variant="h6" gutterBottom>
                AI Agent Control Center
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                This page will contain AI agent monitoring and configuration tools
              </Typography>
              <Chip label="Coming Soon" color="primary" />
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Layout>
  );
}