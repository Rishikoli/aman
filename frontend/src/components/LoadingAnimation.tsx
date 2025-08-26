import React from 'react';
import {
  Box,
  Skeleton,
  Card,
  CardContent,
  Grid,
  keyframes,
} from '@mui/material';

// Advanced loading animations
const shimmer = keyframes`
  0% {
    background-position: -200px 0;
  }
  100% {
    background-position: calc(200px + 100%) 0;
  }
`;

const pulse = keyframes`
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
`;

const slideIn = keyframes`
  0% {
    transform: translateY(20px);
    opacity: 0;
  }
  100% {
    transform: translateY(0);
    opacity: 1;
  }
`;

const wave = keyframes`
  0%, 60%, 100% {
    transform: initial;
  }
  30% {
    transform: translateY(-15px);
  }
`;

interface LoadingAnimationProps {
  variant?: 'card' | 'dashboard' | 'list' | 'chart' | 'metric' | 'detailed';
  count?: number;
  delay?: number;
  showProgress?: boolean;
}

const LoadingAnimation: React.FC<LoadingAnimationProps> = ({
  variant = 'card',
  count = 1,
  delay = 0,
  showProgress = false,
}) => {
  const renderCardSkeleton = (index: number = 0) => (
    <Card 
      sx={{ 
        height: 380, 
        position: 'relative',
        animation: `${slideIn} 0.6s ease-out ${delay + index * 0.1}s both`,
      }}
    >
      <CardContent sx={{ p: 3, height: '100%' }}>
        {/* Header */}
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 3 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Skeleton 
              variant="rectangular" 
              width={48} 
              height={48} 
              sx={{ 
                borderRadius: 2,
                animation: `${shimmer} 2s infinite linear, ${pulse} 2s infinite ease-in-out`,
                background: 'linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%)',
                backgroundSize: '200px 100%',
              }} 
            />
            <Box>
              <Skeleton 
                variant="text" 
                width={120} 
                height={24} 
                sx={{ 
                  mb: 1,
                  animation: `${wave} 2s infinite ease-in-out ${index * 0.1}s`,
                }} 
              />
              <Skeleton 
                variant="text" 
                width={80} 
                height={16}
                sx={{ 
                  animation: `${wave} 2s infinite ease-in-out ${index * 0.1 + 0.2}s`,
                }} 
              />
            </Box>
          </Box>
          <Skeleton 
            variant="circular" 
            width={24} 
            height={24}
            sx={{ 
              animation: `${pulse} 1.5s infinite ease-in-out ${index * 0.1}s`,
            }} 
          />
        </Box>

        {/* Main Content */}
        <Skeleton 
          variant="rectangular" 
          width="100%" 
          height={160} 
          sx={{ 
            borderRadius: 2, 
            mb: 3,
            animation: `${shimmer} 2s infinite linear ${index * 0.2}s`,
            background: 'linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%)',
            backgroundSize: '200px 100%',
          }} 
        />

        {/* Chart Area */}
        <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
          {[...Array(4)].map((_, i) => (
            <Skeleton 
              key={i}
              variant="rectangular" 
              width="25%" 
              height={60 + Math.random() * 40} 
              sx={{ 
                borderRadius: 1,
                animation: `${wave} 2s infinite ease-in-out ${i * 0.1}s`,
              }} 
            />
          ))}
        </Box>

        {/* Footer */}
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Skeleton 
            variant="rectangular" 
            width={100} 
            height={24} 
            sx={{ 
              borderRadius: 1,
              animation: `${pulse} 1.8s infinite ease-in-out`,
            }} 
          />
          <Skeleton 
            variant="text" 
            width={60} 
            height={20}
            sx={{ 
              animation: `${pulse} 1.8s infinite ease-in-out 0.3s`,
            }} 
          />
        </Box>

        {/* Progress indicator */}
        {showProgress && (
          <Box sx={{ mt: 2, pt: 2, borderTop: '1px solid', borderColor: 'divider' }}>
            <Skeleton 
              variant="rectangular" 
              width="100%" 
              height={4} 
              sx={{ 
                borderRadius: 2,
                animation: `${shimmer} 1.5s infinite linear`,
                background: 'linear-gradient(90deg, #e3f2fd 25%, #bbdefb 50%, #e3f2fd 75%)',
                backgroundSize: '200px 100%',
              }} 
            />
          </Box>
        )}
      </CardContent>
    </Card>
  );

  const renderDashboardSkeleton = () => (
    <Grid container spacing={3}>
      {Array.from({ length: 6 }).map((_, index) => (
        <Grid item xs={12} md={6} lg={4} key={index}>
          {renderCardSkeleton(index)}
        </Grid>
      ))}
    </Grid>
  );

  const renderMetricSkeleton = () => (
    <Box sx={{ 
      p: 3,
      animation: `${slideIn} 0.5s ease-out ${delay}s both`,
    }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Skeleton variant="text" width={120} height={20} />
        <Skeleton variant="rectangular" width={60} height={24} sx={{ borderRadius: 1 }} />
      </Box>
      <Skeleton 
        variant="text" 
        width={80} 
        height={48} 
        sx={{ 
          mb: 1,
          animation: `${pulse} 2s infinite ease-in-out`,
        }} 
      />
      <Skeleton 
        variant="rectangular" 
        width="100%" 
        height={8} 
        sx={{ 
          borderRadius: 4,
          animation: `${shimmer} 2s infinite linear`,
          background: 'linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%)',
          backgroundSize: '200px 100%',
        }} 
      />
    </Box>
  );

  const renderDetailedSkeleton = () => (
    <Card sx={{ 
      animation: `${slideIn} 0.6s ease-out ${delay}s both`,
    }}>
      <CardContent sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 3 }}>
          <Box>
            <Skeleton variant="text" width={200} height={28} sx={{ mb: 1 }} />
            <Skeleton variant="text" width={150} height={20} />
          </Box>
          <Box sx={{ display: 'flex', gap: 1 }}>
            <Skeleton variant="circular" width={32} height={32} />
            <Skeleton variant="circular" width={32} height={32} />
          </Box>
        </Box>
        
        <Box sx={{ display: 'flex', gap: 3, mb: 3 }}>
          <Box sx={{ flex: 1 }}>
            <Skeleton variant="text" width={100} height={20} sx={{ mb: 1 }} />
            <Skeleton variant="text" width={60} height={32} />
          </Box>
          <Box sx={{ flex: 1 }}>
            <Skeleton variant="text" width={100} height={20} sx={{ mb: 1 }} />
            <Skeleton variant="text" width={60} height={32} />
          </Box>
        </Box>
        
        <Skeleton variant="rectangular" width="100%" height={200} sx={{ borderRadius: 2, mb: 2 }} />
        
        <Box sx={{ display: 'flex', gap: 2 }}>
          {[...Array(3)].map((_, i) => (
            <Skeleton 
              key={i}
              variant="rectangular" 
              width={80} 
              height={32} 
              sx={{ 
                borderRadius: 1,
                animation: `${wave} 2s infinite ease-in-out ${i * 0.2}s`,
              }} 
            />
          ))}
        </Box>
      </CardContent>
    </Card>
  );

  const renderListSkeleton = () => (
    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
      {Array.from({ length: count }).map((_, index) => (
        <Card key={index}>
          <CardContent sx={{ p: 3 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              <Skeleton variant="circular" width={40} height={40} />
              <Box sx={{ flexGrow: 1 }}>
                <Skeleton variant="text" width="60%" height={20} sx={{ mb: 1 }} />
                <Skeleton variant="text" width="40%" height={16} />
              </Box>
              <Skeleton variant="rectangular" width={80} height={32} sx={{ borderRadius: 1 }} />
            </Box>
          </CardContent>
        </Card>
      ))}
    </Box>
  );

  const renderChartSkeleton = () => (
    <Box sx={{ p: 2 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Skeleton variant="text" width={150} height={24} />
        <Skeleton variant="circular" width={24} height={24} />
      </Box>
      <Skeleton 
        variant="rectangular" 
        width="100%" 
        height={200} 
        sx={{ 
          borderRadius: 2,
          animation: `${shimmer} 2s infinite linear`,
          background: 'linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%)',
          backgroundSize: '200px 100%',
        }} 
      />
    </Box>
  );

  switch (variant) {
    case 'dashboard':
      return renderDashboardSkeleton();
    case 'list':
      return renderListSkeleton();
    case 'chart':
      return renderChartSkeleton();
    case 'metric':
      return renderMetricSkeleton();
    case 'detailed':
      return renderDetailedSkeleton();
    default:
      return renderCardSkeleton();
  }
};

export default LoadingAnimation;