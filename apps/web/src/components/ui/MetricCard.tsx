import { ReactNode, CSSProperties } from 'react';
import { cn } from '@/lib/utils';

export interface MetricCardProps {
  label: string;
  value: string | number;
  change?: string;
  changeType?: 'positive' | 'negative' | 'neutral';
  icon?: ReactNode;
  className?: string;
  style?: CSSProperties;
}

export function MetricCard({ label, value, change, changeType = 'neutral', icon, className, style }: MetricCardProps) {
  return (
    <div className={cn('card p-6', className)} style={style}>
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1 min-w-0">
          <p className="metric-label mb-2">{label}</p>
          <p className="metric-value font-mono tabular-nums">{value}</p>
        </div>
        {icon && (
          <div className="flex-shrink-0 w-10 h-10 rounded-xl bg-surface flex items-center justify-center text-secondary">
            {icon}
          </div>
        )}
      </div>
      {change && (
        <div className="mt-4 flex items-center gap-2">
          <span className={cn(
            'badge font-mono text-xs',
            changeType === 'positive' && 'badge-positive',
            changeType === 'negative' && 'badge-negative',
            changeType === 'neutral' && 'badge'
          )}>
            {change}
          </span>
        </div>
      )}
    </div>
  );
}