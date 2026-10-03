'use client';

import { Users, Briefcase, Image, BookOpen, ArrowRight } from 'lucide-react';
import { SectionHeading } from '@/components/ui/SectionHeading';
import { cn } from '@/lib/utils';

const useCases = [
  {
    role: 'Founders',
    tagline: 'Track competitors, identify opportunities, and make strategic decisions.',
    description: 'Monitor rival launches, pricing changes, and market shifts. Get early warnings on competitive threats and whitespace opportunities.',
    icon: <Users className="h-6 w-6" />,
    metrics: ['Competitor tracking', 'Market entry analysis', 'Strategic planning'],
  },
  {
    role: 'Marketers',
    tagline: 'Monitor brand sentiment, track campaigns, and benchmark against competitors.',
    description: 'Measure campaign impact in real-time. Understand audience perception. Benchmark share of voice and sentiment against category leaders.',
    icon: <Briefcase className="h-6 w-6" />,
    metrics: ['Campaign tracking', 'Sentiment monitoring', 'Competitive benchmarking'],
  },
  {
    role: 'Creators',
    tagline: 'Understand brand perception and identify collaboration opportunities.',
    description: 'Analyze your personal brand positioning. Find aligned partners. Track audience sentiment and content performance.',
    icon: <Image className="h-6 w-6" />,
    metrics: ['Personal brand analysis', 'Partnership scouting', 'Audience insights'],
  },
  {
    role: 'Researchers',
    tagline: 'Compare markets, explore category trends, and collect source-backed insights.',
    description: 'Build comprehensive market maps. Track category evolution. Export citation-ready findings for reports and presentations.',
    icon: <BookOpen className="h-6 w-6" />,
    metrics: ['Market landscaping', 'Trend analysis', 'Citation-ready exports'],
  },
];

export function UseCases() {
  return (
    <section id="use-cases" className="section-py bg-surface" aria-labelledby="usecases-heading">
      <div className="container-custom">
        <SectionHeading
          id="usecases-heading"
          eyebrow="BUILT FOR DIFFERENT TEAMS"
          title="Where insights create impact."
          subtitle="Different roles, same need: clear competitive intelligence to act on."
        />

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mt-12">
          {useCases.map((uc, i) => (
            <article key={uc.role} className="card p-6 md:p-8 card-interactive animate-fade-up" style={{ animationDelay: `${i * 100}ms` }}>
              <div className="feature-icon mb-5">{uc.icon}</div>
              <h3 className="font-sans text-xl font-semibold text-ink mb-2">{uc.role}</h3>
              <p className="body-sm text-secondary mb-5">{uc.tagline}</p>
              <p className="body-sm text-muted mb-6 line-clamp-3">{uc.description}</p>
              <ul className="space-y-2 mb-6">
                {uc.metrics.map((metric, j) => (
                  <li key={j} className="flex items-center gap-2 font-sans text-sm text-secondary">
                    <span className="w-1.5 h-1.5 rounded-full bg-accent" aria-hidden="true" />
                    {metric}
                  </li>
                ))}
              </ul>
              <a href={`/use-cases/${uc.role.toLowerCase()}`} className="inline-flex items-center gap-1.5 font-sans text-sm font-medium text-accent hover:text-accent/80 transition-colors">
                Explore for {uc.role}
                <ArrowRight className="h-4 w-4" />
              </a>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}