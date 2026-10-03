'use client';

import { Quote, Star, ArrowRight } from 'lucide-react';
import { SectionHeading } from '@/components/ui/SectionHeading';
import { cn } from '@/lib/utils';

const testimonials = [
  {
    quote: "Snape replaced three different tools we were using for competitive tracking. The AI agents find signals we'd miss manually, and the citations mean I can trust every data point in board meetings.",
    author: "Sarah Chen",
    role: "VP Marketing",
    company: "Series B SaaS",
    avatar: "SC",
  },
  {
    quote: "As a founder, I used to spend Sunday nights Googling competitors. Now I get a Monday morning digest with everything that matters — sentiment shifts, new launches, pricing changes. It's become my strategic radar.",
    author: "Marcus Webb",
    role: "Founder & CEO",
    company: "D2C Brand",
    avatar: "MW",
  },
  {
    quote: "The competitor comparison view is exceptional. Side-by-side metrics with source citations means I can walk into a pitch and say 'here's exactly where we win and where they do' with evidence.",
    author: "Priya Sharma",
    role: "Growth Lead",
    company: "Fintech Startup",
    avatar: "PS",
  },
];

export function Testimonials() {
  return (
    <section id="proof" className="section-py bg-background" aria-labelledby="testimonials-heading">
      <div className="container-custom">
        <SectionHeading
          id="testimonials-heading"
          eyebrow="LOVED BY EARLY USERS"
          title="Trusted by people who look closer."
        />

        <div className="grid md:grid-cols-3 gap-6 mt-12">
          {testimonials.map((t, i) => (
            <article key={t.author} className="card p-6 md:p-8 animate-fade-up" style={{ animationDelay: `${i * 100}ms` }}>
              <Quote className="h-8 w-8 text-accent/30 mb-4" aria-hidden="true" />
              <blockquote className="body-lead text-ink mb-6">"{t.quote}"</blockquote>
              <div className="flex items-center gap-3 pt-4 border-t border-border">
                <div className="w-10 h-10 rounded-full bg-accent-soft text-accent flex items-center justify-center font-sans font-medium text-sm">{t.avatar}</div>
                <div>
                  <p className="font-sans font-medium text-ink text-sm">{t.author}</p>
                  <p className="font-sans text-xs text-muted">{t.role}, {t.company}</p>
                </div>
              </div>
            </article>
          ))}
        </div>

        <div className="mt-12 text-center animate-fade-up-delay-4">
          <p className="body-sm text-muted mb-4">Early access users • Verified testimonials</p>
          <a href="/early-access" className="btn btn-outline inline-flex items-center gap-2">
            Join early access
            <ArrowRight className="h-4 w-4" />
          </a>
        </div>
      </div>
    </section>
  );
}