import { ReactNode } from 'react';
import { cn } from '@/lib/utils';

export interface SectionHeadingProps {
  eyebrow?: string;
  title: string;
  subtitle?: string;
  align?: 'left' | 'center';
  className?: string;
  titleSize?: 'sm' | 'lg';
  id?: string;
}

export function SectionHeading({ eyebrow, title, subtitle, align = 'center', className, titleSize = 'lg', id }: SectionHeadingProps) {
  return (
    <div className={cn('section-heading', align === 'left' ? 'text-left' : 'text-center', className)}>
      {eyebrow && <p className="eyebrow mb-3">{eyebrow}</p>}
      <h2 id={id} className={cn('section-title', titleSize === 'sm' ? 'section-title-sm' : 'section-title-lg')}>
        {title}
      </h2>
      {subtitle && <p className="body-lead mt-4">{subtitle}</p>}
    </div>
  );
}