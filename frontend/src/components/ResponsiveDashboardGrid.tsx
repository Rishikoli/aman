import React from 'react';
import { Grid, useTheme, useMediaQuery, Box } from '@mui/material';

interface ResponsiveDashboardGridProps {
  children: React.ReactNode;
  spacing?: number;
  priority?: 'performance' | 'balanced' | 'dense';
  adaptiveHeight?: boolean;
}

const ResponsiveDashboardGrid: React.FC<ResponsiveDashboardGridProps> = ({
  children,
  spacing = 3,
  priority = 'balanced',
  adaptiveHeight = true,
}) => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const isTablet = useMediaQuery(theme.breakpoints.between('sm', 'lg'));
  const isDesktop = useMediaQuery(theme.breakpoints.up('lg'));
  const isXLarge = useMediaQuery(theme.breakpoints.up('xl'));

  // Advanced responsive grid configuration based on priority
  const getGridProps = (childIndex: number) => {
    const childCount = React.Children.count(children);
    
    if (priority === 'performance') {
      // Prioritize important cards (first 3) with larger sizes
      if (childIndex < 3) {
        if (isMobile) return { xs: 12 };
        if (isTablet) return { xs: 12, sm: 6 };
        return { xs: 12, sm: 6, lg: 6 }; // Larger cards for important content
      }
    }
    
    if (priority === 'dense') {
      // More cards per row for dense layouts
      if (isMobile) return { xs: 12 };
      if (isTablet) return { xs: 6, sm: 4 };
      if (isXLarge) return { xs: 12, sm: 6, lg: 3 }; // 4 columns on XL screens
      return { xs: 12, sm: 6, lg: 4 };
    }
    
    // Balanced layout (default)
    if (isMobile) return { xs: 12 };
    if (isTablet) return { xs: 12, sm: 6 };
    if (isXLarge) return { xs: 12, sm: 6, lg: 4, xl: 3 }; // 4 columns on XL
    return { xs: 12, sm: 6, lg: 4 };
  };

  const getSpacing = () => {
    if (isMobile) return Math.max(1, spacing - 1);
    if (isTablet) return spacing;
    return spacing;
  };

  return (
    <Box sx={{ 
      width: '100%',
      transition: 'all 0.3s ease-in-out',
    }}>
      <Grid 
        container 
        spacing={getSpacing()}
        sx={{
          '& .MuiGrid-item': {
            transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
          },
          ...(adaptiveHeight && {
            '& .MuiGrid-item': {
              display: 'flex',
              '& > *': {
                width: '100%',
              },
            },
          }),
        }}
      >
        {React.Children.map(children, (child, index) => {
          const gridProps = getGridProps(index);
          
          return (
            <Grid 
              item 
              {...gridProps} 
              key={index}
              sx={{
                minHeight: adaptiveHeight ? 'auto' : undefined,
                '&:hover': {
                  zIndex: 1,
                },
              }}
            >
              {child}
            </Grid>
          );
        })}
      </Grid>
    </Box>
  );
};

export default ResponsiveDashboardGrid;