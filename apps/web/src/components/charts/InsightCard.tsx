'use client';

import { TrendingUp, BarChart2, Zap } from 'lucide-react';

interface InsightCardProps {
  title: string;
  desc: string;
  type: 'positive' | 'negative' | 'warning';
}

export function InsightCard({ title, desc, type }: InsightCardProps) {
  const icons = {
    positive: <TrendingUp className="h-4 w-4" />,
    negative: <BarChart2 className="h-4 w-4" />,
    warning: <Zap className="h-4 w-4" />,
  };
  const colors = {
    positive: 'var(--color-positive)',
    negative: 'var(--color-negative)',
    warning: 'var(--color-warning)',
  };

  return (
    <div className="p-3 rounded-lg bg-surface border border-border">
      <div className="flex items-start gap-2">
        <span className="flex-shrink-0 mt-0.5 text-xs" style={{ color: colors[type] }}>{icons[type]}</span>
        <div className="flex-1 min-w-0">
          <p className="font-sans text-xs font-medium text-ink">{title}</p>
          <p className="font-sans text-xs text-muted">{desc}</p>
        </div>
      </div>
    </div>
  );
}