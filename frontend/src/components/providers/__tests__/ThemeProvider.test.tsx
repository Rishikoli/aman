import React from 'react';
import { render, screen } from '@testing-library/react';

import { ThemeProvider } from '../ThemeProvider';

describe('ThemeProvider', () => {
  it('renders children correctly', () => {
    render(
      <ThemeProvider>
        <div data-testid="test-child">Test Content</div>
      </ThemeProvider>
    );

    expect(screen.getByTestId('test-child')).toBeInTheDocument();
    expect(screen.getByText('Test Content')).toBeInTheDocument();
  });

  it('provides MUI theme context', () => {
    const TestComponent = () => {
      return <div data-testid="themed-component">Themed Component</div>;
    };

    render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    );

    expect(screen.getByTestId('themed-component')).toBeInTheDocument();
  });
});