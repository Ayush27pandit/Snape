import type { Metadata, Viewport } from 'next';
import { Inter, DM_Serif_Display } from 'next/font/google';
import './globals.css';
import { Providers } from './providers';

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-sans',
  display: 'swap',
  preload: true,
});

const dmSerifDisplay = DM_Serif_Display({
  subsets: ['latin'],
  weight: '400',
  variable: '--font-display',
  display: 'swap',
  preload: true,
});

export const metadata: Metadata = {
  title: 'Snape | AI-Powered Competitive Intelligence',
  description: 'Analyze brands, compare competitors, track sentiment, and turn public data into actionable market insights with Snape.',
  openGraph: {
    title: 'Snape | AI-Powered Competitive Intelligence',
    description: 'Analyze brands, compare competitors, track sentiment, and turn public data into actionable market insights with Snape.',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Snape | AI-Powered Competitive Intelligence',
    description: 'Analyze brands, compare competitors, track sentiment, and turn public data into actionable market insights with Snape.',
  },
  robots: 'index, follow',
};

export const viewport: Viewport = {
  themeColor: '#0B0F14',
  width: 'device-width',
  initialScale: 1,
  maximumScale: 5,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning className={`${inter.variable} ${dmSerifDisplay.variable}`}>
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link rel="dns-prefetch" href="https://fonts.googleapis.com" />
        <link rel="dns-prefetch" href="https://fonts.gstatic.com" />
      </head>
      <body className={`${inter.variable} ${dmSerifDisplay.variable} font-sans antialiased`}>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}