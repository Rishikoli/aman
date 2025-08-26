import React from 'react';
import {
  Box,
  Typography,
  Chip,
  LinearProgress,
  useTheme,
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  TrendingFlat,
} from '@mui/icons-material';

interface MetricHighlightProps {
  title: string;
  value: string | number;
  subtitle?: string;
  trend?: 'up' | 'down' | 'flat';
  trendValue?: string;
  progress?: number;
  color?: 'primary' | 'success' | 'warning' | 'error' | 'info';
  variant?: 'default' | 'compact' | 'large';
}

const MetricHighlight: React.FC<MetricHighlightProps> = ({
  title,
  value,
  subtitle,
  trend,
  trendValue,
  progress,
  color = 'primary',
  variant = 'default',
}) => {
  const theme = useTheme();

  const getTrendIcon = () => {
    switch (trend) {
      case 'up':
        return <TrendingUp sx={{ fontSize: 16 }} />;
      case 'down':
        return <TrendingDown sx={{ fontSize: 16 }} />;
      case 'flat':
        return <TrendingFlat sx={{ fontSize: 16 }} />;
      default:
        return undefined;
    }
  };

  const getTrendColor = () => {
    switch (trend) {
      case 'up':
        return theme.palette.success.main;
      case 'down':
        return theme.palette.error.main;
      default:
        return theme.palette.text.secondary;
    }
  };

  const getColorValue = () => {
    switch (color) {
      case 'success':
        return theme.palette.success.main;
      case 'warning':
        return theme.palette.warning.main;
      case 'error':
        return theme.palette.error.main;
      case 'info':
        return theme.palette.info.main;
      default:
        return theme.palette.primary.main;
    }
  };

  if (variant === 'compact') {
    return (
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
        <Box>
          <Typography variant="h6" fontWeight={600} color={getColorValue()}>
            {value}
          </Typography>
          <Typography variant="caption" color="text.secondary">
            {title}
          </Typography>
        </Box>
        {trend && trendValue && (
          <Chip
            {...(getTrendIcon() && { icon: getTrendIcon() })}
            label={trendValue}
            size="small"
            sx={{
              bgcolor: trend === 'up' ? 'success.50' : trend === 'down' ? 'error.50' : 'grey.100',
              color: getTrendColor(),
              fontWeight: 600,
              '& .MuiChip-icon': {
                color: 'inherit',
              },
            }}
          />
        )}
      </Box>
    );
  }

  if (variant === 'large') {
    return (
      <Box sx={{ textAlign: 'center', p: 2 }}>
        <Typography variant="h2" fontWeight={700} color={getColorValue()} gutterBottom>
          {value}
        </Typography>
        <Typography variant="h6" fontWeight={600} gutterBottom>
          {title}
        </Typography>
        {subtitle && (
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            {subtitle}
          </Typography>
        )}
        {trend && trendValue && (
          <Box sx={{ display: 'flex', justifyContent: 'center', gap: 1, mb: 2 }}>
            <Chip
              {...(getTrendIcon() && { icon: getTrendIcon() })}
              label={trendValue}
              size="small"
              sx={{
                bgcolor: trend === 'up' ? 'success.50' : trend === 'down' ? 'error.50' : 'grey.100',
                color: getTrendColor(),
                fontWeight: 600,
                '& .MuiChip-icon': {
                  color: 'inherit',
                },
              }}
            />
          </Box>
        )}
        {progress !== undefined && (
          <Box sx={{ mt: 2 }}>
            <LinearProgress
              variant="determinate"
              value={progress}
              sx={{
                height: 8,
                borderRadius: 4,
                bgcolor: 'grey.200',
                '& .MuiLinearProgress-bar': {
                  bgcolor: getColorValue(),
                  borderRadius: 4,
                },
              }}
            />
            <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
              {progress}% of target
            </Typography>
          </Box>
        )}
      </Box>
    );
  }

  // Default variant
  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 1 }}>
        <Typography variant="body2" color="text.secondary">
          {title}
        </Typography>
        {trend && trendValue && (
          <Chip
            {...(getTrendIcon() && { icon: getTrendIcon() })}
            label={trendValue}
            size="small"
            sx={{
              bgcolor: trend === 'up' ? 'success.50' : trend === 'down' ? 'error.50' : 'grey.100',
              color: getTrendColor(),
              fontWeight: 600,
              '& .MuiChip-icon': {
                color: 'inherit',
              },
            }}
          />
        )}
      </Box>
      
      <Typography variant="h4" fontWeight={600} color={getColorValue()} gutterBottom>
        {value}
      </Typography>
      
      {subtitle && (
        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
          {subtitle}
        </Typography>
      )}
      
      {progress !== undefined && (
        <Box>
          <LinearProgress
            variant="determinate"
            value={progress}
            sx={{
              height: 6,
              borderRadius: 3,
              bgcolor: 'grey.200',
              '& .MuiLinearProgress-bar': {
                bgcolor: getColorValue(),
                borderRadius: 3,
              },
            }}
          />
          <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
            {progress}% complete
          </Typography>
        </Box>
      )}
    </Box>
  );
};

export default MetricHighlight;