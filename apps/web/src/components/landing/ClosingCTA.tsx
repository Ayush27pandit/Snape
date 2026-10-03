'use client';

import { ArrowRight, Zap } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { cn } from '@/lib/utils';

export function ClosingCTA() {
  return (
    <section className="section-py relative overflow-hidden" aria-labelledby="cta-heading" style={{ backgroundColor: 'var(--color-dark-surface)' }}>
      <div className="absolute inset-0 -z-10 opacity-20" aria-hidden="true">
        <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-[600px] h-[600px] rounded-full bg-accent/20 blur-3xl" />
      </div>
      <div className="container-custom relative z-10">
        <div className="max-w-3xl mx-auto text-center">
          <span className="eyebrow text-accent/80 mb-5">STAY AHEAD OF THE COMPETITION</span>
          <h2 id="cta-heading" className="font-display text-white mb-6" style={{ fontSize: 'clamp(2.5rem, 4vw, 4rem)' }}>
            Turn information into opportunity.
          </h2>
          <p className="body-lead text-white/70 mb-8">
            Make your next move with a clearer view of the market. Join founders, marketers, and creators using Snape to stay ahead.
          </p>
          <Button size="lg" variant="primary" className="bg-white text-ink hover:bg-white/90" onClick={() => window.location.href = '/sign-up'}>
            Get started free
            <ArrowRight className="h-5 w-5" />
          </Button>
          <p className="mt-4 font-sans text-sm text-white/50">No credit card · 2 min setup · Cancel anytime</p>
        </div>
      </div>
    </section>
  );
}