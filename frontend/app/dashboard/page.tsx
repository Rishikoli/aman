'use client';

import React from 'react';
import {
  Box,
  Typography,
  Grid,
  IconButton,
  Chip,
  LinearProgress,
  Avatar,
  AvatarGroup,
} from '@mui/material';
import {
  MoreVert,
  FilterList,
  TrendingUp,
  Assessment,
  SmartToy,
  Security,
  Analytics,
  Business,
  Refresh,
} from '@mui/icons-material';
import Layout from '../../components/Layout/Layout';
import DashboardCard from '../../src/components/DashboardCard';
import InteractiveChart from '../../src/components/InteractiveChart';
import StatusIndicator from '../../src/components/StatusIndicator';
import ResponsiveDashboardGrid from '../../src/components/ResponsiveDashboardGrid';
import LoadingAnimation from '../../src/components/LoadingAnimation';
import MetricHighlight from '../../src/components/MetricHighlight';

// Sample data for charts
const dealAnalysisData = [
  { name: 'Due Diligence', value: 35, color: '#3b82f6' },
  { name: 'Negotiation', value: 25, color: '#10b981' },
  { name: 'Legal Review', value: 20, color: '#f59e0b' },
  { name: 'Closing', value: 20, color: '#ef4444' },
];

const activityData = [
  { name: 'Mon', value: 12 },
  { name: 'Tue', value: 19 },
  { name: 'Wed', value: 15 },
  { name: 'Thu', value: 25 },
  { name: 'Fri', value: 22 },
  { name: 'Sat', value: 8 },
  { name: 'Sun', value: 5 },
];

const agentPerformanceData = [
  { name: 'Due Diligence', value: 85, color: '#3b82f6' },
  { name: 'Financial', value: 92, color: '#10b981' },
  { name: 'Legal', value: 78, color: '#f59e0b' },
  { name: 'Risk', value: 88, color: '#ef4444' },
  { name: 'Market Intel', value: 95, color: '#8b5cf6' },
];

export default function DashboardPage() {
  const [loading, setLoading] = React.useState(false);
  const [refreshing, setRefreshing] = React.useState(false);

  const handleRefresh = async () => {
    setRefreshing(true);
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000));
    setRefreshing(false);
  };

  const handleDrillDown = (cardType: string) => {
    console.log(`Drilling down into ${cardType}`);
    // Navigate to detailed view
  };

  const handleDownload = (cardType: string) => {
    console.log(`Downloading ${cardType} data`);
    // Download functionality
  };

  const handleShare = (cardType: string) => {
    console.log(`Sharing ${cardType}`);
    // Share functionality
  };

  if (loading) {
    return (
      <Layout>
        <LoadingAnimation variant="dashboard" showProgress />
      </Layout>
    );
  }

  return (
    <Layout>
      <Box sx={{ mb: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
          <Box>
            <Typography variant="h4" sx={{ fontWeight: 600, mb: 1, color: 'text.primary' }}>
              M&A Navigator Dashboard
            </Typography>
            <Typography variant="body1" color="text.secondary">
              Monitor your M&A deals, financial analysis, and AI agent performance in real-time
            </Typography>
          </Box>
          <Box sx={{ display: 'flex', gap: 2 }}>
            <IconButton 
              onClick={handleRefresh} 
              disabled={refreshing}
              sx={{ 
                bgcolor: 'background.paper',
                boxShadow: 1,
                '&:hover': { bgcolor: 'primary.50' },
              }}
            >
              <Refresh sx={{ 
                animation: refreshing ? 'spin 1s linear infinite' : 'none',
                '@keyframes spin': {
                  '0%': { transform: 'rotate(0deg)' },
                  '100%': { transform: 'rotate(360deg)' },
                },
              }} />
            </IconButton>
          </Box>
        </Box>
      </Box>

      {/* Enhanced Responsive Grid Layout */}
      <ResponsiveDashboardGrid spacing={3} priority="balanced" adaptiveHeight>
        {/* Deal Analysis Card - 3D Visualization */}
        <DashboardCard 
          height={380} 
          expandable 
          priority="high"
          onRefresh={() => handleRefresh()}
          onDrillDown={() => handleDrillDown('deal-analysis')}
          onDownload={() => handleDownload('deal-analysis')}
          onShare={() => handleShare('deal-analysis')}
          expandedContent={
            <Box>
              <MetricHighlight
                title="Pipeline Conversion Rate"
                value="68%"
                trend="up"
                trendValue="+12%"
                progress={68}
                color="success"
                variant="large"
              />
              <Box sx={{ mt: 3 }}>
                <InteractiveChart
                  data={dealAnalysisData}
                  type="bar"
                  height={150}
                  colors={['#3b82f6', '#10b981', '#f59e0b', '#ef4444']}
                  animated
                  gradient
                  showChartTypeSelector
                />
              </Box>
            </Box>
          }
        >
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 3 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <Box sx={{
                  width: 48,
                  height: 48,
                  bgcolor: 'primary.main',
                  borderRadius: 2,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'white'
                }}>
                  <Business />
                </Box>
                <Box>
                  <Typography variant="h6" fontWeight={600}>
                    Deal Analysis
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Pipeline & Progress
                  </Typography>
                </Box>
              </Box>
            </Box>

            {/* 3D-style Deal Pipeline Visualization */}
            <Box sx={{
              height: 160,
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              borderRadius: 3,
              position: 'relative',
              mb: 3,
              overflow: 'hidden',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}>
              <Box sx={{
                width: 80,
                height: 80,
                background: 'linear-gradient(45deg, #06b6d4 0%, #0891b2 100%)',
                borderRadius: '50%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: 'white',
                fontWeight: 'bold',
                fontSize: '1.5rem',
                boxShadow: '0 8px 32px rgba(0,0,0,0.3)',
                transform: 'perspective(1000px) rotateX(15deg)',
              }}>
                12
              </Box>
              <Box sx={{
                position: 'absolute',
                bottom: 16,
                left: 16,
                color: 'white',
                opacity: 0.9
              }}>
                <Typography variant="body2" fontWeight={600}>
                  Active Deals
                </Typography>
                <Typography variant="caption">
                  $2.4B Total Value
                </Typography>
              </Box>
            </Box>

            <InteractiveChart
              data={dealAnalysisData}
              type="pie"
              height={120}
              colors={['#3b82f6', '#10b981', '#f59e0b', '#ef4444']}
              animated
              interactive
              gradient
              onDataPointClick={(data) => console.log('Clicked:', data)}
            />
        </DashboardCard>

        {/* Activity Feed Card */}
        <DashboardCard 
          height={380}
          priority="medium"
          onRefresh={() => handleRefresh()}
          onDrillDown={() => handleDrillDown('activity-feed')}
          onDownload={() => handleDownload('activity-feed')}
          expandable
          expandedContent={
            <Box>
              <Typography variant="h6" gutterBottom>Recent Activities</Typography>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                <StatusIndicator
                  label="Document Reviews"
                  value={23}
                  status="success"
                  trend="up"
                  trendValue="+15%"
                  variant="detailed"
                />
                <StatusIndicator
                  label="Financial Analysis"
                  value={8}
                  status="warning"
                  trend="down"
                  trendValue="-5%"
                  variant="detailed"
                />
                <StatusIndicator
                  label="Legal Reviews"
                  value={12}
                  status="info"
                  trend="up"
                  trendValue="+8%"
                  variant="detailed"
                />
              </Box>
            </Box>
          }
        >
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 3 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <Box sx={{
                  width: 48,
                  height: 48,
                  bgcolor: 'success.main',
                  borderRadius: 2,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'white'
                }}>
                  <TrendingUp />
                </Box>
                <Box>
                  <Typography variant="h6" fontWeight={600}>
                    Activity Feed
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Weekly Overview
                  </Typography>
                </Box>
              </Box>
            </Box>

            <Box sx={{ mb: 3 }}>
              <Typography variant="h3" fontWeight={600} gutterBottom>
                127
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                Total Activities This Week
              </Typography>
              <Chip
                label="+23.5%"
                size="small"
                sx={{ bgcolor: 'success.50', color: 'success.main', fontWeight: 600 }}
              />
            </Box>

            <InteractiveChart
              data={activityData}
              type="bar"
              height={140}
              colors={['#10b981']}
              animated
              interactive
              gradient
              showChartTypeSelector
            />

            <Box sx={{ mt: 2, display: 'flex', justifyContent: 'space-between' }}>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h6" fontWeight={600}>
                  45
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  Documents
                </Typography>
              </Box>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h6" fontWeight={600}>
                  28
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  Meetings
                </Typography>
              </Box>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h6" fontWeight={600}>
                  54
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  Tasks
                </Typography>
              </Box>
            </Box>
        </DashboardCard>

        {/* Financial Metrics Card */}
        <DashboardCard 
          height={380}
          priority="high"
          onRefresh={() => handleRefresh()}
          onDrillDown={() => handleDrillDown('financial-metrics')}
          onDownload={() => handleDownload('financial-metrics')}
          expandable
          expandedContent={
            <Box>
              <Typography variant="h6" gutterBottom>Detailed Financial Breakdown</Typography>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                <MetricHighlight
                  title="EBITDA Margin"
                  value="24.5%"
                  trend="up"
                  trendValue="+3.2%"
                  color="success"
                  variant="compact"
                />
                <MetricHighlight
                  title="Debt-to-Equity"
                  value="0.45"
                  trend="down"
                  trendValue="-0.08"
                  color="warning"
                  variant="compact"
                />
                <MetricHighlight
                  title="ROI"
                  value="18.7%"
                  trend="up"
                  trendValue="+2.1%"
                  color="success"
                  variant="compact"
                />
              </Box>
            </Box>
          }
        >
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 3 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <Box sx={{
                  width: 48,
                  height: 48,
                  bgcolor: 'warning.main',
                  borderRadius: 2,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'white'
                }}>
                  <Analytics />
                </Box>
                <Box>
                  <Typography variant="h6" fontWeight={600}>
                    Financial Metrics
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Key Performance
                  </Typography>
                </Box>
              </Box>
            </Box>

            {/* Large Number Display */}
            <Box sx={{ textAlign: 'center', mb: 3 }}>
              <Typography variant="h2" fontWeight={700} sx={{ 
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                backgroundClip: 'text',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                mb: 1
              }}>
                $2.4B
              </Typography>
              <Typography variant="body1" color="text.secondary" gutterBottom>
                Total Deal Value
              </Typography>
              <Box sx={{ display: 'flex', justifyContent: 'center', gap: 2, mb: 2 }}>
                <Chip
                  icon={<TrendingUp />}
                  label="+18.5%"
                  size="small"
                  sx={{ bgcolor: 'success.50', color: 'success.main', fontWeight: 600 }}
                />
                <Chip
                  label="YoY Growth"
                  size="small"
                  variant="outlined"
                />
              </Box>
            </Box>

            {/* Trend Indicators */}
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h5" fontWeight={600} color="success.main">
                  $890M
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  Completed
                </Typography>
              </Box>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h5" fontWeight={600} color="primary.main">
                  $1.2B
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  In Progress
                </Typography>
              </Box>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h5" fontWeight={600} color="warning.main">
                  $310M
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  Pipeline
                </Typography>
              </Box>
            </Box>

            <LinearProgress
              variant="determinate"
              value={72}
              sx={{
                height: 8,
                borderRadius: 4,
                bgcolor: 'grey.200',
                '& .MuiLinearProgress-bar': {
                  bgcolor: 'primary.main',
                  borderRadius: 4,
                },
              }}
            />
            <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
              72% of annual target achieved
            </Typography>
        </DashboardCard>

        {/* Risk Assessment Card */}
        <DashboardCard 
          height={380}
          priority="high"
          onRefresh={() => handleRefresh()}
          onDrillDown={() => handleDrillDown('risk-assessment')}
          onDownload={() => handleDownload('risk-assessment')}
          expandable
          expandedContent={
            <Box>
              <Typography variant="h6" gutterBottom>Risk Analysis Details</Typography>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                <StatusIndicator
                  label="Liquidity Risk"
                  value={15}
                  status="success"
                  trend="down"
                  trendValue="-10%"
                  variant="detailed"
                  showProgress
                />
                <StatusIndicator
                  label="Currency Risk"
                  value={35}
                  status="warning"
                  trend="up"
                  trendValue="+5%"
                  variant="detailed"
                  showProgress
                />
                <StatusIndicator
                  label="Political Risk"
                  value={20}
                  status="info"
                  trend="flat"
                  trendValue="0%"
                  variant="detailed"
                  showProgress
                />
              </Box>
            </Box>
          }
        >
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 3 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <Box sx={{
                  width: 48,
                  height: 48,
                  bgcolor: 'error.main',
                  borderRadius: 2,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'white'
                }}>
                  <Security />
                </Box>
                <Box>
                  <Typography variant="h6" fontWeight={600}>
                    Risk Assessment
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Portfolio Analysis
                  </Typography>
                </Box>
              </Box>
            </Box>

            {/* Risk Score Visualization */}
            <Box sx={{ textAlign: 'center', mb: 3 }}>
              <Box sx={{ position: 'relative', display: 'inline-flex', mb: 2 }}>
                <Box sx={{
                  width: 120,
                  height: 120,
                  borderRadius: '50%',
                  background: `conic-gradient(#f59e0b 0deg 151deg, #e2e8f0 151deg 360deg)`,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center'
                }}>
                  <Box sx={{
                    width: 80,
                    height: 80,
                    borderRadius: '50%',
                    bgcolor: 'white',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    flexDirection: 'column',
                    boxShadow: '0 4px 12px rgba(0,0,0,0.1)'
                  }}>
                    <Typography variant="h5" fontWeight={700} color="warning.main">
                      4.2
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      /10
                    </Typography>
                  </Box>
                </Box>
              </Box>
              <Typography variant="h6" fontWeight={600} gutterBottom>
                Medium Risk
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Overall portfolio risk level
              </Typography>
            </Box>

            {/* Color-coded Risk Indicators */}
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
              <StatusIndicator
                label="Market Risk"
                value={65}
                status="warning"
                trend="up"
                trendValue="+5%"
                variant="compact"
              />
              <StatusIndicator
                label="Credit Risk"
                value={35}
                status="success"
                trend="down"
                trendValue="-8%"
                variant="compact"
              />
              <StatusIndicator
                label="Operational Risk"
                value={45}
                status="info"
                trend="flat"
                trendValue="0%"
                variant="compact"
              />
              <StatusIndicator
                label="Regulatory Risk"
                value={25}
                status="success"
                trend="down"
                trendValue="-12%"
                variant="compact"
              />
            </Box>
        </DashboardCard>

        {/* Agent Status Card */}
        <DashboardCard 
          height={380}
          priority="medium"
          onRefresh={() => handleRefresh()}
          onDrillDown={() => handleDrillDown('agent-status')}
          onDownload={() => handleDownload('agent-status')}
          expandable
          expandedContent={
            <Box>
              <Typography variant="h6" gutterBottom>Agent Performance Details</Typography>
              <InteractiveChart
                data={agentPerformanceData}
                type="bar"
                height={200}
                colors={['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']}
                animated
                interactive
                gradient
                showChartTypeSelector
                title="Performance by Agent"
              />
            </Box>
          }
        >
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 3 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <Box sx={{
                  width: 48,
                  height: 48,
                  bgcolor: 'secondary.main',
                  borderRadius: 2,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'white'
                }}>
                  <SmartToy />
                </Box>
                <Box>
                  <Typography variant="h6" fontWeight={600}>
                    Agent Status
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    AI Performance
                  </Typography>
                </Box>
              </Box>
            </Box>

            <Box sx={{ display: 'flex', alignItems: 'center', gap: 3, mb: 3 }}>
              {/* Donut Chart for Agent Performance */}
              <Box sx={{ position: 'relative', width: 120, height: 120 }}>
                <Box sx={{
                  width: 120,
                  height: 120,
                  borderRadius: '50%',
                  background: `conic-gradient(#10b981 0deg 306deg, #e2e8f0 306deg 360deg)`,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center'
                }}>
                  <Box sx={{
                    width: 70,
                    height: 70,
                    borderRadius: '50%',
                    bgcolor: 'white',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    flexDirection: 'column',
                    boxShadow: '0 4px 12px rgba(0,0,0,0.1)'
                  }}>
                    <Typography variant="h5" fontWeight={700} color="success.main">
                      85%
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      Avg
                    </Typography>
                  </Box>
                </Box>
              </Box>

              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                <Chip
                  label="5 Active"
                  size="small"
                  sx={{ bgcolor: 'success.50', color: 'success.main', fontWeight: 600 }}
                />
                <Chip
                  label="All Online"
                  size="small"
                  sx={{ bgcolor: 'info.50', color: 'info.main', fontWeight: 600 }}
                />
                <Chip
                  label="High Performance"
                  size="small"
                  sx={{ bgcolor: 'primary.50', color: 'primary.main', fontWeight: 600 }}
                />
              </Box>
            </Box>

            {/* Agent Performance Breakdown */}
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
              {agentPerformanceData.map((agent, index) => (
                <Box key={agent.name} sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Box sx={{
                      width: 8,
                      height: 8,
                      borderRadius: '50%',
                      bgcolor: agent.color
                    }} />
                    <Typography variant="body2" color="text.secondary">
                      {agent.name}
                    </Typography>
                  </Box>
                  <Typography variant="body2" fontWeight={600}>
                    {agent.value}%
                  </Typography>
                </Box>
              ))}
            </Box>
        </DashboardCard>

        {/* Market Intelligence Card */}
        <DashboardCard 
          height={380}
          priority="medium"
          onRefresh={() => handleRefresh()}
          onDrillDown={() => handleDrillDown('market-intelligence')}
          onDownload={() => handleDownload('market-intelligence')}
          expandable
          expandedContent={
            <Box>
              <Typography variant="h6" gutterBottom>Market Trends Analysis</Typography>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                <MetricHighlight
                  title="Market Volatility"
                  value="12.3%"
                  trend="down"
                  trendValue="-2.1%"
                  color="success"
                  variant="compact"
                />
                <MetricHighlight
                  title="Sector Growth"
                  value="8.7%"
                  trend="up"
                  trendValue="+1.5%"
                  color="info"
                  variant="compact"
                />
                <MetricHighlight
                  title="Competition Index"
                  value="74"
                  trend="up"
                  trendValue="+3"
                  color="warning"
                  variant="compact"
                />
              </Box>
            </Box>
          }
        >
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 3 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <Box sx={{
                  width: 48,
                  height: 48,
                  bgcolor: 'info.main',
                  borderRadius: 2,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'white'
                }}>
                  <Assessment />
                </Box>
                <Box>
                  <Typography variant="h6" fontWeight={600}>
                    Market Intelligence
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Real-time Insights
                  </Typography>
                </Box>
              </Box>
            </Box>

            <Box sx={{ display: 'flex', alignItems: 'center', gap: 3, mb: 3 }}>
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
                    flexDirection: 'column',
                    boxShadow: '0 4px 12px rgba(0,0,0,0.1)'
                  }}>
                    <Typography variant="h6" fontWeight={600} color="success.main">
                      70%
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      Positive
                    </Typography>
                  </Box>
                </Box>
              </Box>

              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                <Box sx={{ textAlign: 'center' }}>
                  <Typography variant="h5" fontWeight={600} color="success.main">
                    24
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    Opportunities
                  </Typography>
                </Box>
                <Box sx={{ textAlign: 'center' }}>
                  <Typography variant="h5" fontWeight={600} color="error.main">
                    8
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    Threats
                  </Typography>
                </Box>
              </Box>
            </Box>

            {/* Market Trends */}
            <Box sx={{ mb: 2 }}>
              <Typography variant="body2" fontWeight={600} gutterBottom>
                Key Market Trends
              </Typography>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Typography variant="body2" color="text.secondary">
                    Tech Sector M&A
                  </Typography>
                  <Chip
                    label="+15%"
                    size="small"
                    sx={{ bgcolor: 'success.50', color: 'success.main', fontWeight: 600 }}
                  />
                </Box>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Typography variant="body2" color="text.secondary">
                    Healthcare Deals
                  </Typography>
                  <Chip
                    label="+8%"
                    size="small"
                    sx={{ bgcolor: 'success.50', color: 'success.main', fontWeight: 600 }}
                  />
                </Box>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Typography variant="body2" color="text.secondary">
                    Energy Sector
                  </Typography>
                  <Chip
                    label="-3%"
                    size="small"
                    sx={{ bgcolor: 'error.50', color: 'error.main', fontWeight: 600 }}
                  />
                </Box>
              </Box>
            </Box>

            {/* Team Collaboration */}
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', pt: 2, borderTop: '1px solid', borderColor: 'divider' }}>
              <Typography variant="body2" color="text.secondary">
                Analyst Team
              </Typography>
              <AvatarGroup max={4} sx={{ '& .MuiAvatar-root': { width: 28, height: 28, fontSize: '0.75rem' } }}>
                <Avatar sx={{ bgcolor: 'primary.main' }}>JD</Avatar>
                <Avatar sx={{ bgcolor: 'success.main' }}>SM</Avatar>
                <Avatar sx={{ bgcolor: 'warning.main' }}>AR</Avatar>
                <Avatar sx={{ bgcolor: 'error.main' }}>+3</Avatar>
              </AvatarGroup>
            </Box>
        </DashboardCard>
      </ResponsiveDashboardGrid>
    </Layout>
  );
}