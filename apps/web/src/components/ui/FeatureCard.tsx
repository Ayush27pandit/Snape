import { ReactNode, CSSProperties } from 'react';
import { cn } from '@/lib/utils';

export interface FeatureCardProps {
  icon: ReactNode;
  title: string;
  description: string;
  visual?: ReactNode;
  href?: string;
  className?: string;
  style?: CSSProperties;
}

export function FeatureCard({ icon, title, description, visual, href, className, style }: FeatureCardProps) {
  const content = (
    <article className={cn('card p-6 md:p-8', href && 'card-interactive', className)} style={style}>
      <div className="feature-icon mb-5">
        {icon}
      </div>
      <h3 className="font-sans text-lg font-semibold text-ink mb-3">{title}</h3>
      <p className="body-sm text-secondary mb-5">{description}</p>
      {visual && (
        <div className="mt-6 pt-6 border-t border-border">
          {visual}
        </div>
      )}
    </article>
  );

  if (href) {
    return <a href={href} className="block">{content}</a>;
  }

  return content;
}