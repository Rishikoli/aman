import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import ThemeRegistry from '../src/components/ThemeRegistry';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Autonomous M&A Navigator',
  description: 'AI-powered due diligence platform for mergers and acquisitions',
  keywords: ['M&A', 'due diligence', 'AI', 'automation', 'finance'],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <ThemeRegistry>
          {children}
        </ThemeRegistry>
      </body>
    </html>
  );
}