import React from 'react';
import {
  Box,
  Typography,
  LinearProgress,
  Chip,
  useTheme,
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  TrendingFlat,
  CheckCircle,
  Warning,
  Error,
  Info,
} from '@mui/icons-material';

interface StatusIndicatorProps {
  label: string;
  value: number;
  maxValue?: number;
  status?: 'success' | 'warning' | 'error' | 'info';
  trend?: 'up' | 'down' | 'flat';
  trendValue?: string;
  showProgress?: boolean;
  variant?: 'default' | 'compact' | 'detailed';
}

const StatusIndicator: React.FC<StatusIndicatorProps> = ({
  label,
  value,
  maxValue = 100,
  status = 'info',
  trend,
  trendValue,
  showProgress = true,
  variant = 'default',
}) => {
  const theme = useTheme();

  const getStatusColor = () => {
    switch (status) {
      case 'success':
        return theme.palette.success.main;
      case 'warning':
        return theme.palette.warning.main;
      case 'error':
        return theme.palette.error.main;
      default:
        return theme.palette.info.main;
    }
  };

  const getStatusIcon = () => {
    switch (status) {
      case 'success':
        return <CheckCircle sx={{ fontSize: 16, color: 'success.main' }} />;
      case 'warning':
        return <Warning sx={{ fontSize: 16, color: 'warning.main' }} />;
      case 'error':
        return <Error sx={{ fontSize: 16, color: 'error.main' }} />;
      default:
        return <Info sx={{ fontSize: 16, color: 'info.main' }} />;
    }
  };

  const getTrendIcon = () => {
    switch (trend) {
      case 'up':
        return <TrendingUp sx={{ fontSize: 16, color: 'success.main' }} />;
      case 'down':
        return <TrendingDown sx={{ fontSize: 16, color: 'error.main' }} />;
      case 'flat':
        return <TrendingFlat sx={{ fontSize: 16, color: 'text.secondary' }} />;
      default:
        return undefined;
    }
  };

  const getTrendColor = () => {
    switch (trend) {
      case 'up':
        return 'success.main';
      case 'down':
        return 'error.main';
      default:
        return 'text.secondary';
    }
  };

  const percentage = (value / maxValue) * 100;

  if (variant === 'compact') {
    return (
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        {getStatusIcon()}
        <Typography variant="body2" fontWeight={600}>
          {value}
        </Typography>
        <Typography variant="caption" color="text.secondary">
          {label}
        </Typography>
        {trend && trendValue && (
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
            {getTrendIcon()}
            <Typography variant="caption" color={getTrendColor()}>
              {trendValue}
            </Typography>
          </Box>
        )}
      </Box>
    );
  }

  if (variant === 'detailed') {
    return (
      <Box>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            {getStatusIcon()}
            <Typography variant="body2" color="text.secondary">
              {label}
            </Typography>
          </Box>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Typography variant="h6" fontWeight={600}>
              {value}
            </Typography>
            {maxValue !== 100 && (
              <Typography variant="body2" color="text.secondary">
                / {maxValue}
              </Typography>
            )}
          </Box>
        </Box>
        
        {showProgress && (
          <LinearProgress
            variant="determinate"
            value={percentage}
            sx={{
              height: 8,
              borderRadius: 4,
              bgcolor: 'grey.200',
              '& .MuiLinearProgress-bar': {
                bgcolor: getStatusColor(),
                borderRadius: 4,
              },
            }}
          />
        )}
        
        {trend && trendValue && (
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 1 }}>
            {getTrendIcon()}
            <Typography variant="caption" color={getTrendColor()}>
              {trendValue} vs last period
            </Typography>
          </Box>
        )}
      </Box>
    );
  }

  // Default variant
  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
        <Typography variant="body2" color="text.secondary">
          {label}
        </Typography>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Typography variant="h6" fontWeight={600}>
            {value}
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
      </Box>
      
      {showProgress && (
        <LinearProgress
          variant="determinate"
          value={percentage}
          sx={{
            height: 6,
            borderRadius: 3,
            bgcolor: 'grey.200',
            '& .MuiLinearProgress-bar': {
              bgcolor: getStatusColor(),
              borderRadius: 3,
            },
          }}
        />
      )}
    </Box>
  );
};

export default StatusIndicator;