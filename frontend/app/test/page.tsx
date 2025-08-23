import Layout from '../../components/Layout/Layout';
import { Typography, Box, Card, CardContent } from '@mui/material';

export default function TestPage() {
  return (
    <Layout>
      <Box sx={{ mb: 3 }}>
        <Typography variant="h4" sx={{ fontWeight: 600, mb: 1 }}>
          Test Page
        </Typography>
        <Typography variant="body1" color="text.secondary">
          This page demonstrates the new navbar and compact sidebar layout
        </Typography>
      </Box>

      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Layout Features
          </Typography>
          <Typography variant="body2" color="text.secondary">
            • Horizontal navbar with main navigation tabs
            <br />
            • Compact sidebar (80px wide) with quick access icons
            <br />
            • Responsive design with Material-UI components
            <br />
            • Integrated search and user controls in navbar
          </Typography>
        </CardContent>
      </Card>
    </Layout>
  );
}