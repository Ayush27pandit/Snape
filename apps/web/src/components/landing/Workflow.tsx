'use client';

import { Search, Zap, Brain, TrendingUp, ArrowRight } from 'lucide-react';
import { SectionHeading } from '@/components/ui/SectionHeading';
import { cn } from '@/lib/utils';

const steps = [
  { number: '01', title: 'Enter a brand', desc: 'Choose a brand or category to analyze. Type a name or pick from suggestions.', icon: <Search className="h-6 w-6" /> },
  { number: '02', title: 'AI agents research', desc: 'Multi-agent system searches, collects, and organizes relevant public information across 5+ source types.', icon: <Zap className="h-6 w-6" /> },
  { number: '03', title: 'Get comprehensive analysis', desc: 'Review charts, competitor comparisons, source-backed findings, and sentiment trends.', icon: <Brain className="h-6 w-6" /> },
  { number: '04', title: 'Make better decisions', desc: 'Use the findings to guide positioning, campaigns, and research with confidence.', icon: <TrendingUp className="h-6 w-6" /> },
];

export function Workflow() {
  return (
    <section id="workflow" className="section-py bg-background" aria-labelledby="workflow-heading">
      <div className="container-custom">
        <SectionHeading
          id="workflow-heading"
          eyebrow="SIMPLE PROCESS"
          title="Get insights in minutes."
          subtitle="Four steps from question to actionable intelligence. No manual research, no scattered tools."
        />

        <div className="relative mt-16">
          <div className="hidden lg:block absolute top-1/2 left-10 right-10 -translate-y-1/2 h-px bg-gradient-to-r from-transparent via-border to-transparent -z-10" aria-hidden="true" />

          <div className="grid grid-cols-1 lg:grid-cols-4 gap-8 relative z-10">
            {steps.map((step, i) => (
              <article key={step.number} className="relative animate-fade-up" style={{ animationDelay: `${i * 150}ms` }}>
                <div className="flex items-start gap-4">
                  <div className="flex-shrink-0 w-14 h-14 rounded-2xl flex items-center justify-center text-2xl font-bold text-ink bg-surface border border-border">
                    {step.number}
                  </div>
                  <div>
                    <div className="feature-icon mb-4">{step.icon}</div>
                    <h3 className="font-sans text-lg font-semibold text-ink mb-2">{step.title}</h3>
                    <p className="body-sm text-secondary">{step.desc}</p>
                  </div>
                </div>
                {i < steps.length - 1 && (
                  <div className="absolute left-[70px] top-14 bottom-0 w-px bg-gradient-to-b from-border to-transparent -z-10 lg:hidden" aria-hidden="true" />
                )}
              </article>
            ))}
          </div>
        </div>

        <div className="mt-16 text-center animate-fade-up-delay-4">
          <p className="body-lead mb-6">Ready to see it in action?</p>
          <a href="/dashboard/analyze/new" className="btn btn-primary btn-lg inline-flex items-center gap-2">
            Try it now
            <ArrowRight className="h-5 w-5" />
          </a>
        </div>
      </div>
    </section>
  );
}