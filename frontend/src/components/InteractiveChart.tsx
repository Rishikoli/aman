import React, { useState } from 'react';
import {
  Box,
  Typography,
  Chip,
  IconButton,
  Menu,
  MenuItem,
  Tooltip,
} from '@mui/material';
import {
  FilterList,
  Timeline,
  BarChart as BarChartIcon,
  PieChart as PieChartIcon,
} from '@mui/icons-material';
import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as RechartsTooltip,
  Legend,
  LineChart,
  Line,
  AreaChart,
  Area,
} from 'recharts';

interface InteractiveChartProps {
  data: any[];
  type: 'pie' | 'bar' | 'line' | 'area';
  title?: string;
  height?: number;
  colors?: string[];
  onDataPointClick?: (data: any) => void;
  showFilters?: boolean;
  showChartTypeSelector?: boolean;
  animated?: boolean;
  interactive?: boolean;
  showLegend?: boolean;
  showTooltip?: boolean;
  gradient?: boolean;
}

const InteractiveChart: React.FC<InteractiveChartProps> = ({
  data,
  type: initialType,
  title,
  height = 200,
  colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'],
  onDataPointClick,
  showFilters = false,
  showChartTypeSelector = false,
  animated = true,
  interactive = true,
  showLegend = true,
  showTooltip = true,
  gradient = false,
}) => {
  const [chartType, setChartType] = useState(initialType);
  const [filterAnchor, setFilterAnchor] = useState<null | HTMLElement>(null);
  const [chartTypeAnchor, setChartTypeAnchor] = useState<null | HTMLElement>(null);
  const [hoveredData, setHoveredData] = useState<any>(null);
  const [selectedData, setSelectedData] = useState<any>(null);

  const handleFilterClick = (event: React.MouseEvent<HTMLElement>) => {
    setFilterAnchor(event.currentTarget);
  };

  const handleChartTypeClick = (event: React.MouseEvent<HTMLElement>) => {
    setChartTypeAnchor(event.currentTarget);
  };

  const handleClose = () => {
    setFilterAnchor(null);
    setChartTypeAnchor(null);
  };

  const handleChartTypeChange = (newType: 'pie' | 'bar' | 'line' | 'area') => {
    setChartType(newType);
    handleClose();
  };

  const handleDataPointHover = (data: any) => {
    if (interactive) {
      setHoveredData(data);
    }
  };

  const handleDataPointClick = (data: any) => {
    if (interactive) {
      setSelectedData(data);
      if (onDataPointClick) {
        onDataPointClick(data);
      }
    }
  };

  const getGradientId = (index: number) => `gradient-${index}`;

  const renderGradientDefs = () => (
    <defs>
      {colors.map((color, index) => (
        <linearGradient key={index} id={getGradientId(index)} x1="0" y1="0" x2="0" y2="1">
          <stop offset="5%" stopColor={color} stopOpacity={0.8} />
          <stop offset="95%" stopColor={color} stopOpacity={0.1} />
        </linearGradient>
      ))}
    </defs>
  );

  const renderChart = () => {
    const commonProps = {
      data,
      onClick: handleDataPointClick,
      onMouseEnter: handleDataPointHover,
    };

    switch (chartType) {
      case 'pie':
        return (
          <PieChart {...commonProps}>
            {gradient && renderGradientDefs()}
            <Pie
              dataKey="value"
              cx="50%"
              cy="50%"
              outerRadius={height / 3}
              paddingAngle={2}
              animationBegin={0}
              animationDuration={animated ? 800 : 0}
              style={{ cursor: interactive ? 'pointer' : 'default' }}
            >
              {data.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={gradient ? `url(#${getGradientId(index)})` : colors[index % colors.length]}
                  stroke={selectedData === entry ? '#000' : 'none'}
                  strokeWidth={selectedData === entry ? 2 : 0}
                />
              ))}
            </Pie>
            {showTooltip && <RechartsTooltip />}
            {showLegend && <Legend />}
          </PieChart>
        );

      case 'bar':
        return (
          <BarChart {...commonProps}>
            {gradient && renderGradientDefs()}
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis dataKey="name" />
            <YAxis />
            {showTooltip && <RechartsTooltip />}
            <Bar
              dataKey="value"
              fill={gradient ? `url(#${getGradientId(0)})` : colors[0]}
              radius={[4, 4, 0, 0]}
              animationDuration={animated ? 800 : 0}
              style={{ cursor: interactive ? 'pointer' : 'default' }}
            />
          </BarChart>
        );

      case 'line':
        return (
          <LineChart {...commonProps}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis dataKey="name" />
            <YAxis />
            {showTooltip && <RechartsTooltip />}
            <Line
              type="monotone"
              dataKey="value"
              stroke={colors[0]}
              strokeWidth={3}
              dot={{ fill: colors[0], strokeWidth: 2, r: 4 }}
              activeDot={{
                r: 8,
                stroke: colors[0],
                strokeWidth: 2,
                style: { cursor: interactive ? 'pointer' : 'default' }
              }}
              animationDuration={animated ? 1000 : 0}
            />
          </LineChart>
        );

      case 'area':
        return (
          <AreaChart {...commonProps}>
            {gradient && renderGradientDefs()}
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis dataKey="name" />
            <YAxis />
            {showTooltip && <RechartsTooltip />}
            <Area
              type="monotone"
              dataKey="value"
              stroke={colors[0]}
              fill={gradient ? `url(#${getGradientId(0)})` : colors[0]}
              fillOpacity={gradient ? 1 : 0.3}
              strokeWidth={2}
              animationDuration={animated ? 1000 : 0}
              style={{ cursor: interactive ? 'pointer' : 'default' }}
            />
          </AreaChart>
        );

      default:
        return (
          <BarChart {...commonProps}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis dataKey="name" />
            <YAxis />
            {showTooltip && <RechartsTooltip />}
            <Bar
              dataKey="value"
              fill={colors[0]}
              radius={[4, 4, 0, 0]}
              animationDuration={animated ? 800 : 0}
              style={{ cursor: interactive ? 'pointer' : 'default' }}
            />
          </BarChart>
        );
    }
  };

  return (
    <Box>
      {/* Chart Header */}
      {(title || showFilters || showChartTypeSelector) && (
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          {title && (
            <Typography variant="h6" fontWeight={600}>
              {title}
            </Typography>
          )}
          <Box sx={{ display: 'flex', gap: 1 }}>
            {showFilters && (
              <Tooltip title="Filter data">
                <IconButton size="small" onClick={handleFilterClick}>
                  <FilterList />
                </IconButton>
              </Tooltip>
            )}
            {showChartTypeSelector && (
              <Tooltip title="Change chart type">
                <IconButton size="small" onClick={handleChartTypeClick}>
                  {chartType === 'pie' && <PieChartIcon />}
                  {chartType === 'bar' && <BarChartIcon />}
                  {(chartType === 'line' || chartType === 'area') && <Timeline />}
                </IconButton>
              </Tooltip>
            )}
          </Box>
        </Box>
      )}

      {/* Chart */}
      <ResponsiveContainer width="100%" height={height}>
        {renderChart()}
      </ResponsiveContainer>

      {/* Filter Menu */}
      <Menu
        anchorEl={filterAnchor}
        open={Boolean(filterAnchor)}
        onClose={handleClose}
      >
        <MenuItem onClick={handleClose}>Last 7 days</MenuItem>
        <MenuItem onClick={handleClose}>Last 30 days</MenuItem>
        <MenuItem onClick={handleClose}>Last 90 days</MenuItem>
        <MenuItem onClick={handleClose}>Custom range</MenuItem>
      </Menu>

      {/* Chart Type Menu */}
      <Menu
        anchorEl={chartTypeAnchor}
        open={Boolean(chartTypeAnchor)}
        onClose={handleClose}
      >
        <MenuItem onClick={() => handleChartTypeChange('pie')}>Pie Chart</MenuItem>
        <MenuItem onClick={() => handleChartTypeChange('bar')}>Bar Chart</MenuItem>
        <MenuItem onClick={() => handleChartTypeChange('line')}>Line Chart</MenuItem>
        <MenuItem onClick={() => handleChartTypeChange('area')}>Area Chart</MenuItem>
      </Menu>
    </Box>
  );
};

export default InteractiveChart;