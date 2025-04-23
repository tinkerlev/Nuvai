import '@testing-library/jest-dom';
import { render, screen } from '@testing-library/react';
import App from '../src/App';
import { describe, it, expect } from 'vitest';

describe('App component', () => {
  it('renders without crashing', () => {
    render(<App />);
    expect(screen.getByText(/Click/i)).toBeInTheDocument(); 
  });
});
