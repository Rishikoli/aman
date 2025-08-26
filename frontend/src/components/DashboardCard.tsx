import React, { useState } from 'react';
import {
  Card,
  CardContent,
  Box,
  IconButton,
  Collapse,
  Skeleton,
  Fade,
  useTheme,
  Menu,
  MenuItem,
  Tooltip,
  Zoom,
} from '@mui/material';
import {
  ExpandMore,
  ExpandLess,
  Fullscreen,
  MoreVert,
  Refresh,
  Download,
  Share,
} from '@mui/icons-material';

interface DashboardCardProps {
  children: React.ReactNode;
  expandable?: boolean;
  expandedContent?: React.ReactNode;
  loading?: boolean;
  height?: number | string;
  onExpand?: () => void;
  onDrillDown?: () => void;
  onRefresh?: () => void;
  onDownload?: () => void;
  onShare?: () => void;
  interactive?: boolean;
  priority?: 'high' | 'medium' | 'low';
}

const DashboardCard: React.FC<DashboardCardProps> = ({
  children,
  expandable = false,
  expandedContent,
  loading = false,
  height = 380,
  onExpand,
  onDrillDown,
  onRefresh,
  onDownload,
  onShare,
  interactive = true,
  priority = 'medium',
}) => {
  const [expanded, setExpanded] = useState(false);
  const [menuAnchor, setMenuAnchor] = useState<null | HTMLElement>(null);
  const [isHovered, setIsHovered] = useState(false);
  const theme = useTheme();

  const handleExpandClick = () => {
    setExpanded(!expanded);
    if (onExpand) {
      onExpand();
    }
  };

  const handleDrillDown = () => {
    if (onDrillDown) {
      onDrillDown();
    }
  };

  const handleMenuClick = (event: React.MouseEvent<HTMLElement>) => {
    setMenuAnchor(event.currentTarget);
  };

  const handleMenuClose = () => {
    setMenuAnchor(null);
  };

  const getPriorityColor = () => {
    switch (priority) {
      case 'high':
        return theme.palette.error.main;
      case 'low':
        return theme.palette.success.main;
      default:
        return theme.palette.primary.main;
    }
  };

  const getPriorityGlow = () => {
    switch (priority) {
      case 'high':
        return `0 0 0 2px ${theme.palette.error.main}20`;
      case 'low':
        return `0 0 0 2px ${theme.palette.success.main}20`;
      default:
        return `0 0 0 2px ${theme.palette.primary.main}20`;
    }
  };

  if (loading) {
    return (
      <Card sx={{ height, position: 'relative' }}>
        <CardContent sx={{ p: 3, height: '100%' }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 3 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              <Skeleton variant="rectangular" width={48} height={48} sx={{ borderRadius: 2 }} />
              <Box>
                <Skeleton variant="text" width={120} height={24} />
                <Skeleton variant="text" width={80} height={16} />
              </Box>
            </Box>
            <Skeleton variant="circular" width={24} height={24} />
          </Box>
          <Skeleton variant="rectangular" width="100%" height={200} sx={{ borderRadius: 2, mb: 2 }} />
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Skeleton variant="rectangular" width={100} height={24} sx={{ borderRadius: 1 }} />
            <Skeleton variant="text" width={60} height={20} />
          </Box>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      sx={{
        height: expanded ? 'auto' : height,
        position: 'relative',
        transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
        borderLeft: `4px solid ${getPriorityColor()}`,
        cursor: interactive ? 'pointer' : 'default',
        '&:hover': {
          transform: interactive ? 'translateY(-4px)' : 'none',
          boxShadow: interactive ? `${theme.shadows[8]}, ${getPriorityGlow()}` : theme.shadows[2],
        },
        '&:hover .card-actions': {
          opacity: 1,
          transform: 'translateY(0)',
        },
        '&:active': {
          transform: interactive ? 'translateY(-2px)' : 'none',
        },
      }}
    >
      <CardContent sx={{ p: 3, height: expanded ? 'auto' : '100%', display: 'flex', flexDirection: 'column' }}>
        {/* Card Actions */}
        <Zoom in={isHovered} timeout={200}>
          <Box
            className="card-actions"
            sx={{
              position: 'absolute',
              top: 12,
              right: 12,
              display: 'flex',
              gap: 1,
              opacity: 0,
              transform: 'translateY(-8px)',
              transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
              zIndex: 2,
            }}
          >
            {expandable && (
              <Tooltip title={expanded ? "Collapse" : "Expand"} arrow>
                <IconButton
                  size="small"
                  onClick={handleExpandClick}
                  sx={{
                    bgcolor: 'background.paper',
                    boxShadow: 2,
                    backdropFilter: 'blur(8px)',
                    '&:hover': { 
                      bgcolor: 'primary.50',
                      transform: 'scale(1.1)',
                      boxShadow: 3,
                    },
                    transition: 'all 0.2s ease-in-out',
                  }}
                >
                  {expanded ? <ExpandLess /> : <ExpandMore />}
                </IconButton>
              </Tooltip>
            )}
            <Tooltip title="Drill Down" arrow>
              <IconButton
                size="small"
                onClick={handleDrillDown}
                sx={{
                  bgcolor: 'background.paper',
                  boxShadow: 2,
                  backdropFilter: 'blur(8px)',
                  '&:hover': { 
                    bgcolor: 'info.50',
                    transform: 'scale(1.1)',
                    boxShadow: 3,
                  },
                  transition: 'all 0.2s ease-in-out',
                }}
              >
                <Fullscreen />
              </IconButton>
            </Tooltip>
            <Tooltip title="More Options" arrow>
              <IconButton
                size="small"
                onClick={handleMenuClick}
                sx={{
                  bgcolor: 'background.paper',
                  boxShadow: 2,
                  backdropFilter: 'blur(8px)',
                  '&:hover': { 
                    bgcolor: 'grey.50',
                    transform: 'scale(1.1)',
                    boxShadow: 3,
                  },
                  transition: 'all 0.2s ease-in-out',
                }}
              >
                <MoreVert />
              </IconButton>
            </Tooltip>
          </Box>
        </Zoom>

        {/* Main Content */}
        <Fade in={!loading} timeout={300}>
          <Box sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
            {children}
          </Box>
        </Fade>

        {/* Expanded Content */}
        <Collapse in={expanded} timeout={400}>
          <Box sx={{ 
            mt: 3, 
            pt: 3, 
            borderTop: '2px solid', 
            borderColor: 'divider',
            borderRadius: 1,
            bgcolor: 'grey.50',
            p: 2,
            mx: -1,
          }}>
            {expandedContent || (
              <Box sx={{ textAlign: 'center', py: 2 }}>
                <Skeleton variant="rectangular" width="100%" height={100} sx={{ borderRadius: 2 }} />
              </Box>
            )}
          </Box>
        </Collapse>
      </CardContent>

      {/* Context Menu */}
      <Menu
        anchorEl={menuAnchor}
        open={Boolean(menuAnchor)}
        onClose={handleMenuClose}
        transformOrigin={{ horizontal: 'right', vertical: 'top' }}
        anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
        PaperProps={{
          sx: {
            mt: 1,
            boxShadow: theme.shadows[8],
            borderRadius: 2,
            minWidth: 160,
          }
        }}
      >
        {onRefresh && (
          <MenuItem onClick={() => { onRefresh(); handleMenuClose(); }}>
            <Refresh sx={{ mr: 2, fontSize: 20 }} />
            Refresh Data
          </MenuItem>
        )}
        {onDownload && (
          <MenuItem onClick={() => { onDownload(); handleMenuClose(); }}>
            <Download sx={{ mr: 2, fontSize: 20 }} />
            Download
          </MenuItem>
        )}
        {onShare && (
          <MenuItem onClick={() => { onShare(); handleMenuClose(); }}>
            <Share sx={{ mr: 2, fontSize: 20 }} />
            Share
          </MenuItem>
        )}
      </Menu>
    </Card>
  );
};

export default DashboardCard;