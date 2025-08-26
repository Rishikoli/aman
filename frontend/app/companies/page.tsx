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

export default function CompaniesPage() {
  return (
    <Layout>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" sx={{ fontWeight: 600, mb: 1, color: 'text.primary' }}>
          Company Database
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Comprehensive database of target companies and market intelligence
        </Typography>
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Card>
            <CardContent sx={{ p: 4, textAlign: 'center' }}>
              <Typography variant="h6" gutterBottom>
                Company Intelligence Platform
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                This page will contain detailed company profiles and market analysis
              </Typography>
              <Chip label="Coming Soon" color="primary" />
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Layout>
  );
}