'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ClerkProvider } from '@clerk/nextjs';
import { Toaster } from 'react-hot-toast';
import { useState } from 'react';

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 60 * 1000,
            refetchOnWindowFocus: false,
          },
        },
      })
  );

  const publishableKey = process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY;

  return (
    <QueryClientProvider client={queryClient}>
      {publishableKey ? (
        <ClerkProvider publishableKey={publishableKey}>
          {children}
        </ClerkProvider>
      ) : (
        children
      )}
      <Toaster position="bottom-right" />
    </QueryClientProvider>
  );
}