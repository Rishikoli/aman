'use client';

import React, { useState } from 'react';
import {
    Box,
    Container,
    Typography,
    Paper,
    Grid,
    TextField,
    Button,
    Card,
    CardContent,
    CardHeader,
    Chip,
    Alert,
    CircularProgress,
    Tabs,
    Tab,
    Accordion,
    AccordionSummary,
    AccordionDetails,
    List,
    ListItem,
    ListItemText,
    ListItemIcon,
    LinearProgress,
} from '@mui/material';
import {
    TrendingUp,
    TrendingDown,
    Warning,
    CheckCircle,
    Analytics,
    Assessment,
    PieChart,
    Timeline,
    ExpandMore,
    Speed,
} from '@mui/icons-material';

interface TabPanelProps {
    children?: React.ReactNode;
    index: number;
    value: number;
}

function TabPanel(props: TabPanelProps) {
    const { children, value, index, ...other } = props;

    return (
        <div
            role="tabpanel"
            hidden={value !== index}
            id={`simple-tabpanel-${index}`}
            aria-labelledby={`simple-tab-${index}`}
            {...other}
        >
            {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
        </div>
    );
}

export default function MLAnalysisPage() {
    const [symbol, setSymbol] = useState('');
    const [loading, setLoading] = useState(false);
    const [analysisData, setAnalysisData] = useState<any>(null);
    const [error, setError] = useState<string | null>(null);
    const [tabValue, setTabValue] = useState(0);

    const handleAnalyze = async () => {
        if (!symbol.trim()) {
            setError('Please enter a stock symbol');
            return;
        }

        setLoading(true);
        setError(null);
        setAnalysisData(null);

        try {
            const response = await fetch(`/api/v1/financial/ml-analysis/${symbol.toUpperCase()}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    period: 'annual',
                    limit: 5,
                    forecast_years: 3,
                    include_narrative_analysis: true,
                }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.message || 'Analysis failed');
            }

            setAnalysisData(data.data);
        } catch (err: any) {
            setError(err.message || 'An error occurred during analysis');
        } finally {
            setLoading(false);
        }
    };

    const handleQuickHealthCheck = async () => {
        if (!symbol.trim()) {
            setError('Please enter a stock symbol');
            return;
        }

        setLoading(true);
        setError(null);

        try {
            const response = await fetch(`/api/v1/financial/health-check/${symbol.toUpperCase()}`);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.message || 'Health check failed');
            }

            setAnalysisData({
                ml_analysis: {
                    data: data.data,
                },
                basic_financial_data: null,
            });
            setTabValue(0);
        } catch (err: any) {
            setError(err.message || 'An error occurred during health check');
        } finally {
            setLoading(false);
        }
    };

    const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
        setTabValue(newValue);
    };

    const getHealthScoreColor = (score: number) => {
        if (score >= 80) return 'success';
        if (score >= 60) return 'warning';
        return 'error';
    };

    const getHealthScoreIcon = (score: number) => {
        if (score >= 80) return <CheckCircle color="success" />;
        if (score >= 60) return <Warning color="warning" />;
        return <Warning color="error" />;
    };

    const getRiskLevelColor = (level: string) => {
        switch (level?.toLowerCase()) {
            case 'low': return 'success';
            case 'medium': return 'warning';
            case 'high': return 'error';
            default: return 'default';
        }
    };

    return (
        <Container maxWidth="xl" sx={{ py: 4 }}>
            <Typography variant="h3" component="h1" gutterBottom sx={{ mb: 4, fontWeight: 'bold' }}>
                🤖 ML-Powered Financial Analysis
            </Typography>

            {/* Input Section */}
            <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
                <Grid container spacing={3} alignItems="center">
                    <Grid item xs={12} md={4}>
                        <TextField
                            fullWidth
                            label="Stock Symbol"
                            value={symbol}
                            onChange={(e) => setSymbol(e.target.value.toUpperCase())}
                            placeholder="e.g., AAPL, MSFT, GOOGL"
                            variant="outlined"
                            disabled={loading}
                        />
                    </Grid>
                    <Grid item xs={12} md={4}>
                        <Button
                            fullWidth
                            variant="contained"
                            size="large"
                            onClick={handleAnalyze}
                            disabled={loading}
                            startIcon={loading ? <CircularProgress size={20} /> : <Analytics />}
                            sx={{ height: 56 }}
                        >
                            {loading ? 'Analyzing...' : 'Full ML Analysis'}
                        </Button>
                    </Grid>
                    <Grid item xs={12} md={4}>
                        <Button
                            fullWidth
                            variant="outlined"
                            size="large"
                            onClick={handleQuickHealthCheck}
                            disabled={loading}
                            startIcon={<Speed />}
                            sx={{ height: 56 }}
                        >
                            Quick Health Check
                        </Button>
                    </Grid>
                </Grid>
            </Paper>

            {/* Error Display */}
            {error && (
                <Alert severity="error" sx={{ mb: 4 }}>
                    {error}
                </Alert>
            )}

            {/* Results Section */}
            {analysisData && (
                <Box>
                    <Tabs value={tabValue} onChange={handleTabChange} sx={{ mb: 3 }}>
                        <Tab label="Overview" icon={<Assessment />} />
                        <Tab label="Financial Ratios" icon={<PieChart />} />
                        <Tab label="Forecasts" icon={<Timeline />} />
                        <Tab label="Risk Analysis" icon={<Warning />} />
                        <Tab label="AI Insights" icon={<Analytics />} />
                    </Tabs>

                    {/* Overview Tab */}
                    <TabPanel value={tabValue} index={0}>
                        <Grid container spacing={3}>
                            {/* Health Score Card */}
                            {analysisData.ml_analysis?.data?.health_score && (
                                <Grid item xs={12} md={4}>
                                    <Card elevation={3}>
                                        <CardHeader
                                            title="Financial Health Score"
                                            avatar={getHealthScoreIcon(analysisData.ml_analysis.data.health_score.overall_score)}
                                        />
                                        <CardContent>
                                            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                                                <Typography variant="h2" component="div" sx={{ mr: 2 }}>
                                                    {analysisData.ml_analysis.data.health_score.overall_score}
                                                </Typography>
                                                <Typography variant="h6" color="text.secondary">
                                                    / 100
                                                </Typography>
                                            </Box>
                                            <Chip
                                                label={`Grade: ${analysisData.ml_analysis.data.health_score.grade}`}
                                                color={getHealthScoreColor(analysisData.ml_analysis.data.health_score.overall_score)}
                                                size="large"
                                            />
                                            <LinearProgress
                                                variant="determinate"
                                                value={analysisData.ml_analysis.data.health_score.overall_score}
                                                sx={{ mt: 2, height: 8, borderRadius: 4 }}
                                                color={getHealthScoreColor(analysisData.ml_analysis.data.health_score.overall_score)}
                                            />
                                        </CardContent>
                                    </Card>
                                </Grid>
                            )}

                            {/* Company Info */}
                            {analysisData.basic_financial_data?.profile && (
                                <Grid item xs={12} md={8}>
                                    <Card elevation={3}>
                                        <CardHeader title="Company Information" />
                                        <CardContent>
                                            <Grid container spacing={2}>
                                                <Grid item xs={12} sm={6}>
                                                    <Typography variant="h6" gutterBottom>
                                                        {analysisData.basic_financial_data.profile.companyName}
                                                    </Typography>
                                                    <Typography color="text.secondary" gutterBottom>
                                                        {analysisData.basic_financial_data.profile.symbol}
                                                    </Typography>
                                                    <Typography variant="body2">
                                                        {analysisData.basic_financial_data.profile.industry} • {analysisData.basic_financial_data.profile.sector}
                                                    </Typography>
                                                </Grid>
                                                <Grid item xs={12} sm={6}>
                                                    <Typography variant="body2" color="text.secondary">
                                                        Market Cap: ${(analysisData.basic_financial_data.profile.marketCap / 1000000000).toFixed(2)}B
                                                    </Typography>
                                                    <Typography variant="body2" color="text.secondary">
                                                        Employees: {analysisData.basic_financial_data.profile.fullTimeEmployees?.toLocaleString()}
                                                    </Typography>
                                                </Grid>
                                            </Grid>
                                        </CardContent>
                                    </Card>
                                </Grid>
                            )}

                            {/* Key Metrics */}
                            {analysisData.ml_analysis?.data?.key_ratios && (
                                <Grid item xs={12}>
                                    <Card elevation={3}>
                                        <CardHeader title="Key Financial Metrics" />
                                        <CardContent>
                                            <Grid container spacing={3}>
                                                {Object.entries(analysisData.ml_analysis.data.key_ratios).map(([key, value]: [string, any]) => (
                                                    <Grid item xs={6} sm={3} key={key}>
                                                        <Box sx={{ textAlign: 'center' }}>
                                                            <Typography variant="h5" component="div">
                                                                {typeof value === 'number' ? value.toFixed(2) : value}
                                                            </Typography>
                                                            <Typography variant="body2" color="text.secondary">
                                                                {key.replace(/_/g, ' ').toUpperCase()}
                                                            </Typography>
                                                        </Box>
                                                    </Grid>
                                                ))}
                                            </Grid>
                                        </CardContent>
                                    </Card>
                                </Grid>
                            )}
                        </Grid>
                    </TabPanel>

                    {/* Financial Ratios Tab */}
                    <TabPanel value={tabValue} index={1}>
                        <Grid container spacing={3}>
                            <Grid item xs={12}>
                                <Card elevation={3}>
                                    <CardHeader title="Financial Ratios Analysis" />
                                    <CardContent>
                                        {analysisData.ml_analysis?.data?.financial_ratios && (
                                            <List>
                                                {Object.entries(analysisData.ml_analysis.data.financial_ratios).map(([category, ratios]: [string, any]) => (
                                                    <Accordion key={category}>
                                                        <AccordionSummary expandIcon={<ExpandMore />}>
                                                            <Typography variant="h6">{category.replace(/_/g, ' ').toUpperCase()}</Typography>
                                                        </AccordionSummary>
                                                        <AccordionDetails>
                                                            {typeof ratios === 'object' && ratios !== null && (
                                                                <List dense>
                                                                    {Object.entries(ratios).map(([ratio, values]: [string, any]) => (
                                                                        <ListItem key={ratio}>
                                                                            <ListItemText
                                                                                primary={ratio.replace(/_/g, ' ').toUpperCase()}
                                                                                secondary={Array.isArray(values) ? `Latest: ${values[0]?.toFixed(2)}` : 'N/A'}
                                                                            />
                                                                        </ListItem>
                                                                    ))}
                                                                </List>
                                                            )}
                                                        </AccordionDetails>
                                                    </Accordion>
                                                ))}
                                            </List>
                                        )}
                                    </CardContent>
                                </Card>
                            </Grid>
                        </Grid>
                    </TabPanel>

                    {/* Forecasts Tab */}
                    <TabPanel value={tabValue} index={2}>
                        <Grid container spacing={3}>
                            {analysisData.ml_analysis?.data?.financial_forecasts?.forecasts && (
                                <Grid item xs={12}>
                                    <Card elevation={3}>
                                        <CardHeader title="3-Year Financial Forecasts" />
                                        <CardContent>
                                            <Grid container spacing={2}>
                                                {Object.entries(analysisData.ml_analysis.data.financial_forecasts.forecasts).map(([metric, data]: [string, any]) => (
                                                    <Grid item xs={12} sm={6} md={4} key={metric}>
                                                        <Paper sx={{ p: 2 }}>
                                                            <Typography variant="h6" gutterBottom>
                                                                {metric.replace(/_/g, ' ').toUpperCase()}
                                                            </Typography>
                                                            {data.values && (
                                                                <Box>
                                                                    <Typography variant="body2" color="text.secondary">
                                                                        Trend: {data.trend}
                                                                    </Typography>
                                                                    <Typography variant="body2" color="text.secondary">
                                                                        Growth Rate: {data.annual_growth_rate?.toFixed(2)}%
                                                                    </Typography>
                                                                    <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                                                                        {data.trend === 'increasing' ?
                                                                            <TrendingUp color="success" /> :
                                                                            <TrendingDown color="error" />
                                                                        }
                                                                        <Typography variant="body2" sx={{ ml: 1 }}>
                                                                            {data.trend === 'increasing' ? 'Positive' : 'Negative'} Outlook
                                                                        </Typography>
                                                                    </Box>
                                                                </Box>
                                                            )}
                                                        </Paper>
                                                    </Grid>
                                                ))}
                                            </Grid>
                                        </CardContent>
                                    </Card>
                                </Grid>
                            )}
                        </Grid>
                    </TabPanel>

                    {/* Risk Analysis Tab */}
                    <TabPanel value={tabValue} index={3}>
                        <Grid container spacing={3}>
                            {analysisData.ml_analysis?.data?.risk_assessment && (
                                <>
                                    <Grid item xs={12} md={4}>
                                        <Card elevation={3}>
                                            <CardHeader title="Risk Level" />
                                            <CardContent sx={{ textAlign: 'center' }}>
                                                <Chip
                                                    label={analysisData.ml_analysis.data.risk_assessment.overall_risk_level}
                                                    color={getRiskLevelColor(analysisData.ml_analysis.data.risk_assessment.overall_risk_level)}
                                                    size="large"
                                                    sx={{ mb: 2 }}
                                                />
                                                <Typography variant="h4">
                                                    {analysisData.ml_analysis.data.risk_assessment.risk_score}/100
                                                </Typography>
                                                <LinearProgress
                                                    variant="determinate"
                                                    value={analysisData.ml_analysis.data.risk_assessment.risk_score}
                                                    sx={{ mt: 2, height: 8, borderRadius: 4 }}
                                                    color={getRiskLevelColor(analysisData.ml_analysis.data.risk_assessment.overall_risk_level)}
                                                />
                                            </CardContent>
                                        </Card>
                                    </Grid>

                                    <Grid item xs={12} md={8}>
                                        <Card elevation={3}>
                                            <CardHeader title="Risk Factors" />
                                            <CardContent>
                                                <List>
                                                    {analysisData.ml_analysis.data.risk_assessment.risk_factors?.map((factor: string, index: number) => (
                                                        <ListItem key={index}>
                                                            <ListItemIcon>
                                                                <Warning color="warning" />
                                                            </ListItemIcon>
                                                            <ListItemText primary={factor} />
                                                        </ListItem>
                                                    ))}
                                                </List>
                                            </CardContent>
                                        </Card>
                                    </Grid>
                                </>
                            )}

                            {/* Anomalies */}
                            {analysisData.ml_analysis?.data?.anomaly_detection?.anomalies && (
                                <Grid item xs={12}>
                                    <Card elevation={3}>
                                        <CardHeader title="Financial Anomalies Detected" />
                                        <CardContent>
                                            {analysisData.ml_analysis.data.anomaly_detection.anomalies.map((anomaly: any, index: number) => (
                                                <Alert key={index} severity="warning" sx={{ mb: 2 }}>
                                                    <Typography variant="subtitle1">
                                                        {anomaly.severity} Anomaly - {anomaly.period}
                                                    </Typography>
                                                    <Typography variant="body2">
                                                        {anomaly.description}
                                                    </Typography>
                                                </Alert>
                                            ))}
                                        </CardContent>
                                    </Card>
                                </Grid>
                            )}
                        </Grid>
                    </TabPanel>

                    {/* AI Insights Tab */}
                    <TabPanel value={tabValue} index={4}>
                        <Grid container spacing={3}>
                            {/* Executive Summary */}
                            {analysisData.ml_analysis?.data?.executive_summary && (
                                <Grid item xs={12}>
                                    <Card elevation={3}>
                                        <CardHeader title="Executive Summary" />
                                        <CardContent>
                                            <Typography variant="h6" gutterBottom>
                                                Overall Assessment: {analysisData.ml_analysis.data.executive_summary.overall_assessment}
                                            </Typography>

                                            <Typography variant="subtitle1" gutterBottom sx={{ mt: 2 }}>
                                                Key Findings:
                                            </Typography>
                                            <List>
                                                {analysisData.ml_analysis.data.executive_summary.key_findings?.map((finding: string, index: number) => (
                                                    <ListItem key={index}>
                                                        <ListItemIcon>
                                                            <CheckCircle color="primary" />
                                                        </ListItemIcon>
                                                        <ListItemText primary={finding} />
                                                    </ListItem>
                                                ))}
                                            </List>

                                            <Typography variant="subtitle1" gutterBottom sx={{ mt: 2 }}>
                                                Recommendations:
                                            </Typography>
                                            <List>
                                                {analysisData.ml_analysis.data.executive_summary.recommendations?.map((rec: string, index: number) => (
                                                    <ListItem key={index}>
                                                        <ListItemIcon>
                                                            <TrendingUp color="success" />
                                                        </ListItemIcon>
                                                        <ListItemText primary={rec} />
                                                    </ListItem>
                                                ))}
                                            </List>
                                        </CardContent>
                                    </Card>
                                </Grid>
                            )}

                            {/* Analysis Metadata */}
                            <Grid item xs={12}>
                                <Card elevation={3}>
                                    <CardHeader title="Analysis Details" />
                                    <CardContent>
                                        <Grid container spacing={2}>
                                            <Grid item xs={12} sm={6}>
                                                <Typography variant="body2" color="text.secondary">
                                                    Analysis Date: {new Date(analysisData.ml_analysis?.data?.analysis_date || Date.now()).toLocaleString()}
                                                </Typography>
                                                <Typography variant="body2" color="text.secondary">
                                                    Data Quality Score: {analysisData.ml_analysis?.data?.metadata?.data_quality_score}
                                                </Typography>
                                            </Grid>
                                            <Grid item xs={12} sm={6}>
                                                <Typography variant="body2" color="text.secondary">
                                                    Confidence Level: {analysisData.ml_analysis?.data?.metadata?.confidence_level}
                                                </Typography>
                                                <Typography variant="body2" color="text.secondary">
                                                    AI Model: Gemini 2.0 Flash + scikit-learn
                                                </Typography>
                                            </Grid>
                                        </Grid>
                                    </CardContent>
                                </Card>
                            </Grid>
                        </Grid>
                    </TabPanel>
                </Box>
            )}
        </Container>
    );
}