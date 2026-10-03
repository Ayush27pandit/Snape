'use client';

import { Search, GitCompare, Globe, Calendar, TrendingUp, Shield } from 'lucide-react';
import { FeatureCard } from '@/components/ui/FeatureCard';
import { SectionHeading } from '@/components/ui/SectionHeading';

const features = [
  {
    title: 'Brand Deep Dive',
    description: 'Analyze sentiment, news, reviews, and public opinion for any brand. Get comprehensive insights from across the web in a single report.',
    icon: <Search className="h-6 w-6" />,
    visual: (
      <div className="h-24 bg-surface rounded-lg border border-border flex items-center justify-center">
        <span className="text-muted text-sm">Sentiment trend chart preview</span>
      </div>
    ),
  },
  {
    title: 'Competitor Comparison',
    description: 'Compare 1–5 competitors side by side across key metrics: pricing, positioning, features, marketing channels, and audience overlap.',
    icon: <GitCompare className="h-6 w-6" />,
    visual: (
      <div className="h-24 bg-surface rounded-lg border border-border flex items-center justify-center">
        <span className="text-muted text-sm">Comparison bars preview</span>
      </div>
    ),
  },
  {
    title: 'Market Landscape',
    description: 'Explore a category of 10–20 players and identify opportunities. See positioning maps, trend detection, and whitespace analysis.',
    icon: <Globe className="h-6 w-6" />,
    visual: (
      <div className="h-24 bg-surface rounded-lg border border-border flex items-center justify-center">
        <span className="text-muted text-sm">Market map preview</span>
      </div>
    ),
  },
  {
    title: 'Campaign Tracking',
    description: 'Measure public response to launches, announcements, and events. Track mention volume, sentiment shifts, and competitor reactions.',
    icon: <Calendar className="h-6 w-6" />,
    visual: (
      <div className="h-24 bg-surface rounded-lg border border-border flex items-center justify-center">
        <span className="text-muted text-sm">Campaign timeline preview</span>
      </div>
    ),
  },
];

export function FeatureOverview() {
  return (
    <section id="features" className="section-py bg-background" aria-labelledby="features-heading">
      <div className="container-custom">
        <SectionHeading
          id="features-heading"
          eyebrow="EVERYTHING YOU NEED"
          title="From data to decisions."
          subtitle="Four analysis types cover every competitive intelligence need. Each powered by AI agents that search, analyze, and synthesize insights from the live web."
        />
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mt-12">
          {features.map((feature, i) => (
            <FeatureCard key={feature.title} {...feature} className="animate-fade-up" style={{ animationDelay: `${i * 100}ms` }} />
          ))}
        </div>
      </div>
    </section>
  );
}