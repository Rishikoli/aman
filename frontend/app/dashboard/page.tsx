'use client';

import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  IconButton,
  Chip,
  LinearProgress,
} from '@mui/material';
import {
  MoreVert,
  FilterList,
} from '@mui/icons-material';
import Layout from '../../components/Layout/Layout';

export default function DashboardPage() {
  return (
    <Layout>
      <Box sx={{ mb: 3 }}>
        <Typography variant="h4" sx={{ fontWeight: 600, mb: 1 }}>
          M&A Navigator Dashboard
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Monitor your M&A deals, financial analysis, and AI agent performance
        </Typography>
      </Box>

      <Grid container spacing={3}>
            {/* Deal Pipeline Card */}
            <Grid item xs={12} md={4}>
              <Card sx={{ height: 320, position: 'relative', overflow: 'hidden' }}>
                <CardContent sx={{ p: 3 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                    <Typography variant="h6" fontWeight={600}>
                      Deal Pipeline
                    </Typography>
                    <IconButton size="small">
                      <MoreVert />
                    </IconButton>
                  </Box>

                  {/* M&A Visualization */}
                  <Box sx={{
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                    height: 120,
                    mb: 2,
                    background: 'linear-gradient(135deg, #1e40af 0%, #3b82f6 100%)',
                    borderRadius: 2,
                    position: 'relative'
                  }}>
                    <Box sx={{
                      width: 60,
                      height: 60,
                      background: 'linear-gradient(45deg, #06b6d4 0%, #0891b2 100%)',
                      borderRadius: '50%',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      color: 'white',
                      fontWeight: 'bold',
                      fontSize: '1.2rem'
                    }}>
                      M&A
                    </Box>
                  </Box>

                  <Typography variant="h6" fontWeight={600} gutterBottom>
                    Active Deals
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                    Current M&A transactions in progress
                  </Typography>

                  <Chip
                    label="12 Active"
                    size="small"
                    sx={{ bgcolor: '#dbeafe', color: '#1e40af', mb: 2 }}
                  />

                  {/* Progress Chart */}
                  <Box sx={{ mt: 2 }}>
                    <LinearProgress
                      variant="determinate"
                      value={75}
                      sx={{
                        height: 6,
                        borderRadius: 3,
                        bgcolor: 'rgba(255,255,255,0.3)',
                        '& .MuiLinearProgress-bar': {
                          bgcolor: '#10b981'
                        }
                      }}
                    />
                    <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
                      Pipeline completion rate: 75%
                    </Typography>
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            {/* Financial Analysis */}
            <Grid item xs={12} md={4}>
              <Card sx={{ height: 320 }}>
                <CardContent sx={{ p: 3 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
                    <Typography variant="h6" fontWeight={600}>
                      Financial Analysis
                    </Typography>
                    <Box sx={{ display: 'flex', gap: 1 }}>
                      <IconButton size="small">
                        <FilterList />
                      </IconButton>
                      <IconButton size="small">
                        <MoreVert />
                      </IconButton>
                    </Box>
                  </Box>

                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    Total Deal Value
                  </Typography>
                  <Box sx={{ display: 'flex', alignItems: 'baseline', gap: 1, mb: 1 }}>
                    <Typography variant="h3" fontWeight={600}>
                      $2.4B
                    </Typography>
                  </Box>
                  <Chip
                    label="+18.5%"
                    size="small"
                    sx={{ bgcolor: '#dcfce7', color: '#166534', mb: 3 }}
                  />

                  {/* Financial Chart */}
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'end', height: 80, mb: 2 }}>
                    {['Q1', 'Q2', 'Q3', 'Q4'].map((quarter, index) => (
                      <Box key={quarter} sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 1 }}>
                        <Box
                          sx={{
                            width: 12,
                            height: [30, 45, 60, 55][index],
                            bgcolor: index === 2 ? '#3b82f6' : '#e5e7eb',
                            borderRadius: 1
                          }}
                        />
                        <Typography variant="caption" color="text.secondary">
                          {quarter}
                        </Typography>
                      </Box>
                    ))}
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            {/* Risk Assessment */}
            <Grid item xs={12} md={4}>
              <Card sx={{ height: 320 }}>
                <CardContent sx={{ p: 3 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
                    <Typography variant="h6" fontWeight={600}>
                      Risk Assessment
                    </Typography>
                    <IconButton size="small">
                      <MoreVert />
                    </IconButton>
                  </Box>

                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    Overall Risk Score
                  </Typography>
                  <Typography variant="h4" fontWeight={600} gutterBottom>
                    Medium
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                    Risk Level: 4.2/10
                  </Typography>

                  {/* Risk Indicator */}
                  <Box sx={{
                    background: 'linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%)',
                    borderRadius: 3,
                    p: 2,
                    color: 'white',
                    position: 'relative',
                    mb: 2
                  }}>
                    <Typography variant="h6" fontWeight={600}>
                      Risk Factors
                    </Typography>
                    <Typography variant="body2" sx={{ mt: 1 }}>
                      Market volatility, regulatory changes
                    </Typography>
                  </Box>

                  <Box sx={{ display: 'flex', gap: 2 }}>
                    <Box>
                      <Typography variant="body2" color="text.secondary">
                        High Risk
                      </Typography>
                      <Typography variant="h6" fontWeight={600}>
                        15%
                      </Typography>
                    </Box>
                    <Box>
                      <Typography variant="body2" color="text.secondary">
                        Low Risk
                      </Typography>
                      <Typography variant="h6" fontWeight={600}>
                        85%
                      </Typography>
                    </Box>
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            {/* Agent Performance */}
            <Grid item xs={12} md={6}>
              <Card sx={{ height: 200 }}>
                <CardContent sx={{ p: 3 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                    <Typography variant="h6" fontWeight={600}>
                      AI Agent Performance
                    </Typography>
                    <Box sx={{ display: 'flex', gap: 1 }}>
                      <IconButton size="small">
                        <FilterList />
                      </IconButton>
                      <IconButton size="small">
                        <MoreVert />
                      </IconButton>
                    </Box>
                  </Box>

                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    Active Agents
                  </Typography>
                  <Box sx={{ display: 'flex', alignItems: 'baseline', gap: 1, mb: 2 }}>
                    <Typography variant="h3" fontWeight={600}>
                      5
                    </Typography>
                    <Chip
                      label="All Online"
                      size="small"
                      sx={{ bgcolor: '#dcfce7', color: '#166534' }}
                    />
                  </Box>

                  {/* Agent Stats */}
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'end', height: 60 }}>
                    {[
                      { label: 'Due Diligence', value: '3' },
                      { label: 'Financial Analysis', value: '2' }
                    ].map((item, index) => (
                      <Box key={index} sx={{ textAlign: 'center' }}>
                        <Typography variant="h6" fontWeight={600}>
                          {item.value}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          {item.label}
                        </Typography>
                      </Box>
                    ))}
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            {/* Market Intelligence */}
            <Grid item xs={12} md={6}>
              <Card sx={{ height: 200 }}>
                <CardContent sx={{ p: 3 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                    <Typography variant="h6" fontWeight={600}>
                      Market Intelligence
                    </Typography>
                    <IconButton size="small">
                      <MoreVert />
                    </IconButton>
                  </Box>

                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 3 }}>
                    {/* Market Sentiment Gauge */}
                    <Box sx={{ position: 'relative', width: 100, height: 100 }}>
                      <Box sx={{
                        width: 100,
                        height: 100,
                        borderRadius: '50%',
                        background: `conic-gradient(#10b981 0deg 252deg, #e2e8f0 252deg 360deg)`,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center'
                      }}>
                        <Box sx={{
                          width: 60,
                          height: 60,
                          borderRadius: '50%',
                          bgcolor: 'white',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          flexDirection: 'column'
                        }}>
                          <Typography variant="h6" fontWeight={600}>
                            70%
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            Positive
                          </Typography>
                        </Box>
                      </Box>
                    </Box>

                    <Box sx={{ display: 'flex', gap: 4 }}>
                      {[
                        { label: 'Opportunities', value: '24' },
                        { label: 'Threats', value: '8' },
                        { label: 'Trends', value: '12' }
                      ].map((item) => (
                        <Box key={item.label} sx={{ textAlign: 'center' }}>
                          <Typography variant="h5" fontWeight={600}>
                            {item.value}
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            {item.label}
                          </Typography>
                        </Box>
                      ))}
                    </Box>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
      </Grid>
    </Layout>
  );
}