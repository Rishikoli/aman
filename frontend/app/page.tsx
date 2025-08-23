'use client';

import {
  Container,
  Typography,
  Box,
  Card,
  CardContent,
  Grid,
  Button,
  Chip,
  Stack
} from '@mui/material';
import {
  Dashboard,
  TrendingUp,
  Security,
  Assessment,
  SmartToy,
  ArrowForward,
  Analytics,
  AutoAwesome
} from '@mui/icons-material';
import Link from 'next/link';

export default function HomePage() {
  const features = [
    {
      title: 'Deal Dashboard',
      description: 'Comprehensive overview of all M&A deals and their progress with real-time analytics',
      icon: <Dashboard sx={{ fontSize: 48, color: 'primary.main' }} />,
      stats: '12 Active Deals',
      color: 'primary.main',
      href: '/dashboard'
    },
    {
      title: 'ML Financial Analysis',
      description: 'Advanced ML-powered financial analysis with AI insights, anomaly detection, and forecasting',
      icon: <TrendingUp sx={{ fontSize: 48, color: 'success.main' }} />,
      stats: '$2.4B Analyzed',
      color: 'success.main',
      href: '/ml-analysis'
    },
    {
      title: 'Legal & Compliance',
      description: 'Contract analysis and regulatory compliance checking with intelligent insights',
      icon: <Security sx={{ fontSize: 48, color: 'warning.main' }} />,
      stats: '98% Accuracy',
      color: 'warning.main',
      href: '/legal'
    },
    {
      title: 'Risk Assessment',
      description: 'Comprehensive risk analysis and mitigation strategies using advanced algorithms',
      icon: <Assessment sx={{ fontSize: 48, color: 'error.main' }} />,
      stats: 'Medium Risk',
      color: 'error.main',
      href: '/risk'
    },
    {
      title: 'AI Agents',
      description: 'Autonomous agents handling due diligence tasks with machine learning capabilities',
      icon: <SmartToy sx={{ fontSize: 48, color: 'secondary.main' }} />,
      stats: '5 Active Agents',
      color: 'secondary.main',
      href: '/agents'
    },
    {
      title: 'Market Intelligence',
      description: 'Real-time market data and sentiment analysis for informed decision making',
      icon: <Analytics sx={{ fontSize: 48, color: 'info.main' }} />,
      stats: '70% Positive',
      color: 'info.main',
      href: '/market'
    },
  ];

  return (
    <Box sx={{ minHeight: '100vh', bgcolor: '#fafafa' }}>
      {/* Hero Section */}
      <Box sx={{
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        color: 'white',
        py: 8
      }}>
        <Container maxWidth="lg">
          <Box sx={{ textAlign: 'center', mb: 6 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 2, mb: 3 }}>
              <Box sx={{
                width: 48,
                height: 48,
                bgcolor: 'white',
                borderRadius: 2,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: '#667eea',
                fontWeight: 'bold',
                fontSize: '1.5rem'
              }}>
                {/* Logo placeholder */}
                A
              </Box>
              <Typography variant="h3" component="h1" fontWeight={700}>
                AMAN
              </Typography>
            </Box>

            <Typography variant="h2" component="h1" gutterBottom fontWeight={600}>
              Autonomous M&A Navigator
            </Typography>
            <Typography variant="h5" sx={{ mb: 4, opacity: 0.9 }}>
              AI-powered due diligence platform for mergers and acquisitions
            </Typography>

            <Stack direction="row" spacing={2} justifyContent="center">
              <Button
                variant="contained"
                size="large"
                sx={{
                  bgcolor: 'white',
                  color: '#667eea',
                  '&:hover': { bgcolor: 'rgba(255,255,255,0.9)' }
                }}
                endIcon={<ArrowForward />}
                component={Link}
                href="/dashboard"
              >
                Go to Dashboard
              </Button>
              <Button
                variant="outlined"
                size="large"
                sx={{
                  borderColor: 'white',
                  color: 'white',
                  '&:hover': { borderColor: 'white', bgcolor: 'rgba(255,255,255,0.1)' }
                }}
              >
                Learn More
              </Button>
            </Stack>
          </Box>

          {/* Stats */}
          <Grid container spacing={4} sx={{ mt: 4 }}>
            <Grid item xs={12} md={3}>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h3" fontWeight={600}>
                  $2.4B
                </Typography>
                <Typography variant="body1" sx={{ opacity: 0.8 }}>
                  Total Deal Value
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={12} md={3}>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h3" fontWeight={600}>
                  12
                </Typography>
                <Typography variant="body1" sx={{ opacity: 0.8 }}>
                  Active Deals
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={12} md={3}>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h3" fontWeight={600}>
                  5
                </Typography>
                <Typography variant="body1" sx={{ opacity: 0.8 }}>
                  AI Agents
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={12} md={3}>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h3" fontWeight={600}>
                  98%
                </Typography>
                <Typography variant="body1" sx={{ opacity: 0.8 }}>
                  Accuracy Rate
                </Typography>
              </Box>
            </Grid>
          </Grid>
        </Container>
      </Box>

      {/* Features Section */}
      <Container maxWidth="lg" sx={{ py: 8 }}>
        <Box sx={{ textAlign: 'center', mb: 6 }}>
          <Typography variant="h3" component="h2" gutterBottom fontWeight={600}>
            Comprehensive M&A Platform
          </Typography>
          <Typography variant="h6" color="text.secondary" sx={{ maxWidth: 600, mx: 'auto' }}>
            Streamline your mergers and acquisitions process with AI-powered automation,
            intelligent analysis, and comprehensive due diligence tools.
          </Typography>
        </Box>

        <Grid container spacing={4}>
          {features.map((feature, index) => (
            <Grid item xs={12} md={6} lg={4} key={index}>
              <Card
                className="card-hover"
                sx={{
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  transition: 'all 0.3s ease-in-out',
                  cursor: 'pointer',
                  '&:hover': {
                    transform: 'translateY(-8px)',
                    boxShadow: '0 12px 40px rgba(0,0,0,0.15)',
                  },
                }}
                component={Link}
                href={feature.href}
                style={{ textDecoration: 'none' }}
              >
                <CardContent sx={{ flexGrow: 1, p: 4 }}>
                  <Box sx={{ display: 'flex', alignItems: 'flex-start', mb: 3 }}>
                    <Box sx={{ mr: 3 }}>
                      {feature.icon}
                    </Box>
                    <Box sx={{ flexGrow: 1 }}>
                      <Typography variant="h5" component="h3" gutterBottom fontWeight={600}>
                        {feature.title}
                      </Typography>
                      <Typography variant="body1" color="text.secondary" sx={{ mb: 3, lineHeight: 1.6 }}>
                        {feature.description}
                      </Typography>
                    </Box>
                  </Box>

                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Chip
                      label={feature.stats}
                      sx={{
                        bgcolor: `${feature.color}15`,
                        color: feature.color,
                        fontWeight: 600
                      }}
                    />
                    <ArrowForward sx={{ color: feature.color }} />
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Container>

      {/* CTA Section */}
      <Box sx={{
        bgcolor: '#f8fafc',
        py: 8,
        borderTop: '1px solid #e2e8f0'
      }}>
        <Container maxWidth="lg">
          <Box sx={{ textAlign: 'center' }}>
            <AutoAwesome sx={{ fontSize: 64, color: 'primary.main', mb: 2 }} />
            <Typography variant="h4" component="h2" gutterBottom fontWeight={600}>
              Ready to Transform Your M&A Process?
            </Typography>
            <Typography variant="h6" color="text.secondary" sx={{ mb: 4, maxWidth: 600, mx: 'auto' }}>
              Join leading investment firms and corporations who trust AMAN for their
              most critical merger and acquisition decisions.
            </Typography>

            <Stack direction="row" spacing={2} justifyContent="center">
              <Button
                variant="contained"
                size="large"
                endIcon={<ArrowForward />}
                component={Link}
                href="/dashboard"
              >
                Start Your Analysis
              </Button>
              <Button
                variant="outlined"
                size="large"
              >
                Schedule Demo
              </Button>
            </Stack>
          </Box>
        </Container>
      </Box>

      {/* Footer */}
      <Box sx={{
        bgcolor: '#1a202c',
        color: 'white',
        py: 6
      }}>
        <Container maxWidth="lg">
          <Grid container spacing={4}>
            <Grid item xs={12} md={6}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
                <Box sx={{
                  width: 32,
                  height: 32,
                  bgcolor: 'white',
                  borderRadius: 1,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: '#1a202c',
                  fontWeight: 'bold'
                }}>
                  {/* Logo placeholder */}
                  A
                </Box>
                <Typography variant="h6" fontWeight={600}>
                  AMAN
                </Typography>
              </Box>
              <Typography variant="body2" sx={{ opacity: 0.8, maxWidth: 400 }}>
                Autonomous M&A Navigator - Revolutionizing due diligence with
                artificial intelligence and advanced analytics.
              </Typography>
            </Grid>
            <Grid item xs={12} md={6}>
              <Box sx={{ textAlign: { xs: 'left', md: 'right' } }}>
                <Typography variant="body2" sx={{ opacity: 0.8 }}>
                  © 2024 AMAN. All rights reserved.
                </Typography>
                <Typography variant="body2" sx={{ opacity: 0.6, mt: 1 }}>
                  Powered by AI agents for comprehensive due diligence automation
                </Typography>
              </Box>
            </Grid>
          </Grid>
        </Container>
      </Box>
    </Box>
  );
}