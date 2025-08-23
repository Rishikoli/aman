'use client';

import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Button,
  TextField,
  Grid,
  Chip,
  Alert,
  CircularProgress,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Divider,
} from '@mui/material';
import {
  ExpandMore,
  Psychology,
  Business,
  TrendingUp,
  Assessment,
} from '@mui/icons-material';
import Layout from '../../components/Layout/Layout';
import useGemini from '../../src/hooks/useGemini';

export default function AIDemoPage() {
  const {
    loading,
    error,
    status,
    getStatus,
    analyzeDeal,
    researchCompany,
    generateMarketIntelligence,
    generateText,
    clearError,
    isAvailable,
  } = useGemini();

  const [dealData, setDealData] = useState({
    targetCompany: 'TechCorp Inc.',
    acquiringCompany: 'MegaCorp Ltd.',
    dealValue: '$500M',
    industry: 'Technology',
    dealType: 'Acquisition',
  });

  const [companyName, setCompanyName] = useState('Apple Inc.');
  const [industry, setIndustry] = useState('Technology');
  const [prompt, setPrompt] = useState('Explain the key factors to consider in M&A due diligence.');

  const [results, setResults] = useState<{
    dealAnalysis?: Record<string, unknown>;
    companyResearch?: Record<string, unknown>;
    marketIntelligence?: Record<string, unknown>;
    generatedText?: string;
  }>({});

  useEffect(() => {
    getStatus();
  }, [getStatus]);

  const handleAnalyzeDeal = async () => {
    try {
      const analysis = await analyzeDeal(dealData);
      setResults(prev => ({ ...prev, dealAnalysis: analysis }));
    } catch (err) {
      console.error('Deal analysis failed:', err);
    }
  };

  const handleResearchCompany = async () => {
    try {
      const research = await researchCompany(companyName, { industry });
      setResults(prev => ({ ...prev, companyResearch: research }));
    } catch (err) {
      console.error('Company research failed:', err);
    }
  };

  const handleMarketIntelligence = async () => {
    try {
      const intelligence = await generateMarketIntelligence(industry);
      setResults(prev => ({ ...prev, marketIntelligence: intelligence }));
    } catch (err) {
      console.error('Market intelligence failed:', err);
    }
  };

  const handleGenerateText = async () => {
    try {
      const text = await generateText(prompt);
      setResults(prev => ({ ...prev, generatedText: text }));
    } catch (err) {
      console.error('Text generation failed:', err);
    }
  };

  return (
    <Layout>
      <Box sx={{ mb: 3 }}>
        <Typography variant="h4" sx={{ fontWeight: 600, mb: 1 }}>
          Gemini 2.0 Flash AI Demo
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Test the AI-powered features using Google&apos;s Gemini 2.0 Flash model
        </Typography>
      </Box>

      {/* Status Card */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
            <Psychology color="primary" />
            <Typography variant="h6">AI Service Status</Typography>
          </Box>
          
          {status && (
            <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
              <Chip 
                label={`Service: ${status.service}`} 
                color="primary" 
                variant="outlined" 
              />
              <Chip 
                label={`Model: ${status.model}`} 
                color="secondary" 
                variant="outlined" 
              />
              <Chip 
                label={isAvailable ? 'Available' : 'Unavailable'} 
                color={isAvailable ? 'success' : 'error'} 
              />
              <Chip 
                label={status.configured ? 'Configured' : 'Not Configured'} 
                color={status.configured ? 'success' : 'warning'} 
              />
            </Box>
          )}
          
          <Button 
            onClick={getStatus} 
            disabled={loading} 
            sx={{ mt: 2 }}
            startIcon={loading ? <CircularProgress size={16} /> : null}
          >
            Refresh Status
          </Button>
        </CardContent>
      </Card>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }} onClose={clearError}>
          {error}
        </Alert>
      )}

      {!isAvailable && (
        <Alert severity="warning" sx={{ mb: 3 }}>
          AI service is not available. Please configure the Gemini API key in the backend environment.
        </Alert>
      )}

      <Grid container spacing={3}>
        {/* Deal Analysis */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
                <Business color="primary" />
                <Typography variant="h6">Deal Analysis</Typography>
              </Box>
              
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mb: 2 }}>
                <TextField
                  label="Target Company"
                  value={dealData.targetCompany}
                  onChange={(e) => setDealData(prev => ({ ...prev, targetCompany: e.target.value }))}
                  size="small"
                />
                <TextField
                  label="Acquiring Company"
                  value={dealData.acquiringCompany}
                  onChange={(e) => setDealData(prev => ({ ...prev, acquiringCompany: e.target.value }))}
                  size="small"
                />
                <TextField
                  label="Deal Value"
                  value={dealData.dealValue}
                  onChange={(e) => setDealData(prev => ({ ...prev, dealValue: e.target.value }))}
                  size="small"
                />
                <TextField
                  label="Industry"
                  value={dealData.industry}
                  onChange={(e) => setDealData(prev => ({ ...prev, industry: e.target.value }))}
                  size="small"
                />
              </Box>
              
              <Button
                onClick={handleAnalyzeDeal}
                disabled={loading || !isAvailable}
                variant="contained"
                fullWidth
                startIcon={loading ? <CircularProgress size={16} /> : null}
              >
                Analyze Deal
              </Button>
              
              {results.dealAnalysis && (
                <Box sx={{ mt: 2 }}>
                  <Accordion>
                    <AccordionSummary expandIcon={<ExpandMore />}>
                      <Typography variant="subtitle2">Analysis Results</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                      <Typography variant="body2" component="pre" sx={{ whiteSpace: 'pre-wrap' }}>
                        {JSON.stringify(results.dealAnalysis, null, 2)}
                      </Typography>
                    </AccordionDetails>
                  </Accordion>
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Company Research */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
                <Assessment color="primary" />
                <Typography variant="h6">Company Research</Typography>
              </Box>
              
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mb: 2 }}>
                <TextField
                  label="Company Name"
                  value={companyName}
                  onChange={(e) => setCompanyName(e.target.value)}
                  size="small"
                />
                <TextField
                  label="Industry"
                  value={industry}
                  onChange={(e) => setIndustry(e.target.value)}
                  size="small"
                />
              </Box>
              
              <Button
                onClick={handleResearchCompany}
                disabled={loading || !isAvailable}
                variant="contained"
                fullWidth
                startIcon={loading ? <CircularProgress size={16} /> : null}
              >
                Research Company
              </Button>
              
              {results.companyResearch && (
                <Box sx={{ mt: 2 }}>
                  <Accordion>
                    <AccordionSummary expandIcon={<ExpandMore />}>
                      <Typography variant="subtitle2">Research Results</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                      <Typography variant="body2" component="pre" sx={{ whiteSpace: 'pre-wrap' }}>
                        {JSON.stringify(results.companyResearch, null, 2)}
                      </Typography>
                    </AccordionDetails>
                  </Accordion>
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Market Intelligence */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
                <TrendingUp color="primary" />
                <Typography variant="h6">Market Intelligence</Typography>
              </Box>
              
              <TextField
                label="Industry"
                value={industry}
                onChange={(e) => setIndustry(e.target.value)}
                size="small"
                fullWidth
                sx={{ mb: 2 }}
              />
              
              <Button
                onClick={handleMarketIntelligence}
                disabled={loading || !isAvailable}
                variant="contained"
                fullWidth
                startIcon={loading ? <CircularProgress size={16} /> : null}
              >
                Generate Market Intelligence
              </Button>
              
              {results.marketIntelligence && (
                <Box sx={{ mt: 2 }}>
                  <Accordion>
                    <AccordionSummary expandIcon={<ExpandMore />}>
                      <Typography variant="subtitle2">Intelligence Report</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                      <Typography variant="body2" component="pre" sx={{ whiteSpace: 'pre-wrap' }}>
                        {JSON.stringify(results.marketIntelligence, null, 2)}
                      </Typography>
                    </AccordionDetails>
                  </Accordion>
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Text Generation */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
                <Psychology color="primary" />
                <Typography variant="h6">Text Generation</Typography>
              </Box>
              
              <TextField
                label="Prompt"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                multiline
                rows={3}
                fullWidth
                sx={{ mb: 2 }}
              />
              
              <Button
                onClick={handleGenerateText}
                disabled={loading || !isAvailable}
                variant="contained"
                fullWidth
                startIcon={loading ? <CircularProgress size={16} /> : null}
              >
                Generate Text
              </Button>
              
              {results.generatedText && (
                <Box sx={{ mt: 2 }}>
                  <Divider sx={{ mb: 2 }} />
                  <Typography variant="subtitle2" gutterBottom>
                    Generated Response:
                  </Typography>
                  <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap' }}>
                    {results.generatedText}
                  </Typography>
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Layout>
  );
}