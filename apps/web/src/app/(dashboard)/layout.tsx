'use client';

import { usePathname } from 'next/navigation';
import Link from 'next/link';
import { useAuth } from '@clerk/nextjs';
import { LayoutDashboard, Search, BarChart2, GitCompare, Settings, LogOut, User, Bell } from 'lucide-react';
import { cn } from '@/lib/utils';

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
  { name: 'New Analysis', href: '/dashboard/analyze/new', icon: Search },
  { name: 'Brands', href: '/dashboard/brands', icon: BarChart2 },
  { name: 'Comparisons', href: '/dashboard/comparisons', icon: GitCompare },
  { name: 'Settings', href: '/dashboard/settings', icon: Settings },
];

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const { userId, signOut } = useAuth();

  return (
    <div className="min-h-screen bg-dark-50 dark:bg-dark-950">
      <aside className="fixed inset-y-0 left-0 z-50 w-64 bg-background border-r border-border hidden lg:block">
        <div className="flex h-16 items-center justify-between px-6 border-b border-border">
          <Link href="/dashboard" className="flex items-center gap-2">
            <div className="h-8 w-8 rounded-lg bg-primary flex items-center justify-center">
              <span className="text-primary-foreground font-bold text-lg">S</span>
            </div>
            <span className="text-xl font-bold">Snape</span>
          </Link>
        </div>
        <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
          {navigation.map((item) => (
            <Link
              key={item.name}
              href={item.href}
              className={cn(
                'flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors',
                pathname === item.href
                  ? 'bg-primary text-primary-foreground'
                  : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground'
              )}
            >
              <item.icon className="h-5 w-5" />
              {item.name}
            </Link>
          ))}
        </nav>
        <div className="p-4 border-t border-border">
          <div className="flex items-center gap-3 px-3 py-2">
            <div className="h-8 w-8 rounded-full bg-primary/10 flex items-center justify-center">
              <User className="h-4 w-4 text-primary" />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium truncate">{userId}</p>
              <p className="text-xs text-muted-foreground truncate">Pro Plan</p>
            </div>
          </div>
        </div>
      </aside>

      <div className="lg:pl-64">
        <header className="sticky top-0 z-40 h-16 bg-background/80 backdrop-blur-sm border-b border-border">
          <div className="flex h-full items-center justify-between px-6">
            <h1 className="text-xl font-semibold">
              {navigation.find((n) => n.href === pathname)?.name || 'Dashboard'}
            </h1>
            <div className="flex items-center gap-4">
              <button className="relative p-2 rounded-lg hover:bg-accent transition-colors">
                <Bell className="h-5 w-5" />
                <span className="absolute top-1 right-1 h-2 w-2 rounded-full bg-red-500" />
              </button>
              <button
                onClick={() => signOut()}
                className="p-2 rounded-lg hover:bg-accent transition-colors"
              >
                <LogOut className="h-5 w-5" />
              </button>
            </div>
          </div>
        </header>
        <main className="p-6">{children}</main>
      </div>
    </div>
  );
}