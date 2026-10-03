'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Plus, BarChart2, Clock, CheckCircle, AlertCircle, Search, TrendingUp, FileText, GitCompare } from 'lucide-react';
import { cn, formatRelativeTime } from '@/lib/utils';

const mockBrands = [
  { id: '1', name: 'Nike', domain: 'nike.com', industry: 'Apparel', analysesCount: 12, lastAnalyzed: '2024-01-15T10:00:00Z' },
  { id: '2', name: 'Adidas', domain: 'adidas.com', industry: 'Apparel', analysesCount: 8, lastAnalyzed: '2024-01-10T14:30:00Z' },
  { id: '3', name: 'Puma', domain: 'puma.com', industry: 'Apparel', analysesCount: 5, lastAnalyzed: '2024-01-05T09:15:00Z' },
];

const mockAnalyses = [
  { id: '1', brandName: 'Nike', type: 'COMPETITOR_COMPARISON', status: 'COMPLETED', progress: 100, createdAt: '2024-01-15T10:00:00Z', completedAt: '2024-01-15T10:03:00Z' },
  { id: '2', brandName: 'Adidas', type: 'DEEP_DIVE', status: 'COMPLETED', progress: 100, createdAt: '2024-01-10T14:30:00Z', completedAt: '2024-01-10T14:32:00Z' },
  { id: '3', brandName: 'Puma', type: 'MARKET_LANDSCAPE', status: 'RUNNING', progress: 65, createdAt: '2024-01-15T15:00:00Z', completedAt: null },
  { id: '4', brandName: 'Nike', type: 'CAMPAIGN_TRACKING', status: 'PENDING', progress: 0, createdAt: '2024-01-15T16:00:00Z', completedAt: null },
];

const mockUsage = { used: 7, limit: 20, resetDate: '2024-02-01' };

export default function DashboardPage() {
  const [activeTab, setActiveTab] = useState<'brands' | 'analyses'>('brands');

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold">Dashboard</h1>
          <p className="text-muted-foreground">Track your brands and monitor competitive intelligence</p>
        </div>
        <Link href="/dashboard/analyze/new" className="btn btn-primary">
          <Plus className="mr-2 h-4 w-4" />
          New Analysis
        </Link>
      </div>

      {/* Usage Bar */}
      <div className="card">
        <div className="card-header">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="card-title">Monthly Usage</h3>
              <p className="card-description">{mockUsage.used} of {mockUsage.limit} analyses used</p>
            </div>
            <span className="badge badge-primary">Resets {formatRelativeTime(mockUsage.resetDate)}</span>
          </div>
        </div>
        <div className="card-content">
          <div className="h-2 bg-secondary rounded-full overflow-hidden">
            <div
              className="h-full bg-primary transition-all duration-300"
              style={{ width: `${(mockUsage.used / mockUsage.limit) * 100}%` }}
            />
          </div>
          <div className="flex justify-between text-xs text-muted-foreground mt-1">
            <span>{mockUsage.used} used</span>
            <span>{mockUsage.limit - mockUsage.used} remaining</span>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="card">
        <div className="card-header">
          <div className="flex items-center gap-4 border-b border-border">
            {[
              { id: 'brands', label: 'Tracked Brands', count: mockBrands.length, icon: BarChart2 },
              { id: 'analyses', label: 'Recent Analyses', count: mockAnalyses.length, icon: FileText },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as 'brands' | 'analyses')}
                className={cn(
                  'flex items-center gap-2 px-4 py-2 border-b-2 font-medium text-sm transition-colors',
                  activeTab === tab.id
                    ? 'border-primary text-primary'
                    : 'border-transparent text-muted-foreground hover:text-foreground'
                )}
              >
                <tab.icon className="h-4 w-4" />
                {tab.label}
                <span className="badge badge-outline">{tab.count}</span>
              </button>
            ))}
          </div>
        </div>

        <div className="card-content p-0">
          {activeTab === 'brands' ? (
            <div className="divide-y divide-border">
              {mockBrands.map((brand) => (
                <Link
                  key={brand.id}
                  href={`/dashboard/brands/${brand.id}`}
                  className="flex items-center justify-between p-4 hover:bg-accent/50 transition-colors"
                >
                  <div className="flex items-center gap-4">
                    <div className="h-10 w-10 rounded-lg bg-primary/10 flex items-center justify-center">
                      <span className="text-primary font-bold">{brand.name[0]}</span>
                    </div>
                    <div>
                      <p className="font-medium">{brand.name}</p>
                      <p className="text-sm text-muted-foreground">{brand.industry} • {brand.domain}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-medium">{brand.analysesCount} analyses</p>
                    <p className="text-xs text-muted-foreground">Last: {formatRelativeTime(brand.lastAnalyzed)}</p>
                  </div>
                </Link>
              ))}
            </div>
          ) : (
            <div className="divide-y divide-border">
              {mockAnalyses.map((analysis) => (
                <Link
                  key={analysis.id}
                  href={`/dashboard/analyze/${analysis.id}`}
                  className="flex items-center justify-between p-4 hover:bg-accent/50 transition-colors"
                >
                  <div className="flex items-center gap-4">
                    <div className={cn(
                      'h-10 w-10 rounded-lg flex items-center justify-center',
                      analysis.status === 'COMPLETED' && 'bg-green-100 text-green-700',
                      analysis.status === 'RUNNING' && 'bg-blue-100 text-blue-700',
                      analysis.status === 'PENDING' && 'bg-yellow-100 text-yellow-700',
                      analysis.status === 'FAILED' && 'bg-red-100 text-red-700',
                    )}>
                      {analysis.status === 'COMPLETED' && <CheckCircle className="h-5 w-5" />}
                      {analysis.status === 'RUNNING' && <TrendingUp className="h-5 w-5 animate-pulse" />}
                      {analysis.status === 'PENDING' && <Clock className="h-5 w-5" />}
                      {analysis.status === 'FAILED' && <AlertCircle className="h-5 w-5" />}
                    </div>
                    <div>
                      <p className="font-medium">{analysis.brandName}</p>
                      <p className="text-sm text-muted-foreground capitalize">{analysis.type.toLowerCase().replace('_', ' ')}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    {analysis.status === 'RUNNING' && (
                      <div className="w-32 h-2 bg-secondary rounded-full overflow-hidden">
                        <div
                          className="h-full bg-primary transition-all"
                          style={{ width: `${analysis.progress}%` }}
                        />
                      </div>
                    )}
                    <p className={cn(
                      'text-sm font-medium mt-1',
                      analysis.status === 'COMPLETED' && 'text-green-700',
                      analysis.status === 'RUNNING' && 'text-blue-700',
                      analysis.status === 'PENDING' && 'text-yellow-700',
                      analysis.status === 'FAILED' && 'text-red-700',
                    )}>
                      {analysis.status === 'RUNNING' ? `${analysis.progress}%` : analysis.status}
                    </p>
                    <p className="text-xs text-muted-foreground">{formatRelativeTime(analysis.createdAt)}</p>
                  </div>
                </Link>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid sm:grid-cols-3 gap-4">
        {[
          { title: 'Quick Analysis', desc: 'Analyze a single brand in 2 minutes', icon: Search, href: '/dashboard/analyze/new?type=deep_dive' },
          { title: 'Compare Rivals', desc: 'Side-by-side competitor comparison', icon: GitCompare, href: '/dashboard/analyze/new?type=comparison' },
          { title: 'Market Overview', desc: 'Full landscape analysis for your category', icon: TrendingUp, href: '/dashboard/analyze/new?type=landscape' },
        ].map((action, i) => (
          <Link key={i} href={action.href} className="card p-6 hover:shadow-md transition-shadow">
            <div className="flex items-center gap-4">
              <div className="h-12 w-12 rounded-lg bg-primary/10 text-primary flex items-center justify-center">
                <action.icon className="h-6 w-6" />
              </div>
              <div>
                <h3 className="font-semibold">{action.title}</h3>
                <p className="text-sm text-muted-foreground">{action.desc}</p>
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}