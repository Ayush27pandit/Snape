'use client';

import { Check, HelpCircle } from 'lucide-react';
import { SectionHeading } from '@/components/ui/SectionHeading';
import { Button } from '@/components/ui/Button';
import { cn } from '@/lib/utils';

const plans = [
  {
    name: 'Free',
    price: 0,
    period: 'month',
    description: 'Perfect for trying Snape and occasional analysis',
    features: [
      '2 analyses per month',
      '1 brand tracking',
      'Basic metrics (sentiment, mentions)',
      'Interactive dashboard',
      'Email support',
    ],
    cta: 'Get started free',
    variant: 'outline' as const,
    popular: false,
  },
  {
    name: 'Pro',
    price: 25,
    period: 'month',
    description: 'For professionals who need regular competitive intelligence',
    features: [
      '20 analyses per month',
      '5 brands tracking',
      'All competitive metrics & AI insights',
      'Automated email digests',
      'Priority processing queue',
      'Export reports (coming soon)',
      'API access (coming soon)',
    ],
    cta: 'Get started with Pro',
    variant: 'primary' as const,
    popular: true,
  },
];

const featuresDetail = [
  { category: 'Analysis', free: '2/month', pro: '20/month' },
  { category: 'Brands tracked', free: '1', pro: '5' },
  { category: 'Analysis types', free: 'Deep Dive only', pro: 'All 4 types' },
  { category: 'Competitor comparison', free: '—', pro: 'Up to 5 rivals' },
  { category: 'Metrics', free: 'Basic only', pro: 'All 7 metrics' },
  { category: 'AI insights', free: '—', pro: 'Full (descriptive → prescriptive)' },
  { category: 'Email digests', free: '—', pro: 'Weekly/monthly' },
  { category: 'Queue priority', free: 'Standard', pro: 'Priority' },
  { category: 'Export', free: '—', pro: 'Coming soon' },
  { category: 'API access', free: '—', pro: 'Coming soon' },
  { category: 'Support', free: 'Email', pro: 'Priority email' },
];

export function Pricing() {
  return (
    <section id="pricing" className="section-py bg-background" aria-labelledby="pricing-heading">
      <div className="container-custom">
        <SectionHeading
          id="pricing-heading"
          eyebrow="SIMPLE PRICING"
          title="Start free, scale as you grow."
          subtitle="No hidden fees. Cancel anytime. All plans include access to the full Snape platform."
        />

        <div className="grid md:grid-cols-2 gap-6 md:gap-8 mt-12 max-w-4xl mx-auto">
          {plans.map((plan, i) => (
            <article
              key={plan.name}
              className={cn(
                'card p-6 md:p-8 relative',
                plan.popular && 'border-accent shadow-elevated',
                !plan.popular && 'border-border'
              )}
            >
              {plan.popular && (
                <div className="absolute -top-3 left-1/2 -translate-x-1/2">
                  <span className="badge badge-primary">Most Popular</span>
                </div>
              )}
              <div className="text-center mb-6">
                <h3 className="font-sans text-lg font-semibold text-ink mb-2">{plan.name}</h3>
                <div className="flex items-baseline justify-center gap-1">
                  <span className="font-display font-bold text-ink" style={{ fontSize: 'clamp(3rem, 5vw, 4rem)' }}>
                    ${plan.price}
                  </span>
                  <span className="font-sans text-secondary self-end pb-1">/{plan.period}</span>
                </div>
                <p className="body-sm text-secondary mt-3">{plan.description}</p>
              </div>
              <Button
                className="w-full mb-8"
                variant={plan.variant}
                size="lg"
                onClick={() => window.location.href = '/sign-up'}
              >
                {plan.cta}
              </Button>
              <ul className="space-y-3 mb-8" role="list">
                {plan.features.map((feature, j) => (
                  <li key={j} className="flex items-start gap-3 font-sans text-sm text-secondary">
                    <Check className="h-5 w-5 flex-shrink-0 text-positive mt-0.5" aria-hidden="true" />
                    <span>{feature}</span>
                  </li>
                ))}
              </ul>
            </article>
          ))}
        </div>

        <div className="mt-16 animate-fade-up">
          <h3 className="font-sans text-lg font-semibold text-center text-ink mb-6">Detailed comparison</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-left" role="table">
              <thead>
                <tr className="border-b border-border">
                  <th className="pb-3 font-sans text-sm font-medium text-secondary">Category</th>
                  <th className="pb-3 font-sans text-sm font-medium text-secondary text-center">Free</th>
                  <th className="pb-3 font-sans text-sm font-medium text-secondary text-center">Pro</th>
                </tr>
              </thead>
              <tbody>
                {featuresDetail.map((row, i) => (
                  <tr key={row.category} className={cn('border-b border-border/50', i === featuresDetail.length - 1 && 'border-0')}>
                    <td className="py-4 font-sans text-sm text-secondary">{row.category}</td>
                    <td className="py-4 font-mono text-sm text-muted text-center">{row.free}</td>
                    <td className="py-4 font-mono text-sm font-medium text-ink text-center">{row.pro}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="mt-12 text-center animate-fade-up">
          <p className="body-sm text-muted mb-4">Have questions?</p>
          <a href="/faq" className="btn btn-ghost inline-flex items-center gap-2">
            <HelpCircle className="h-4 w-4" />
            View FAQ
          </a>
        </div>
      </div>
    </section>
  );
}