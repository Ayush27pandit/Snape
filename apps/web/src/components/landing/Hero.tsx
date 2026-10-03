'use client';

import { useState, useRef, useEffect } from 'react';
import { ArrowRight, Search, Zap, TrendingUp, Users, BarChart2, Star } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/Button';
import { MetricCard } from '@/components/ui/MetricCard';
import { SentimentChart } from '@/components/charts/SentimentChart';
import { ShareOfVoiceChart } from '@/components/charts/ShareOfVoiceChart';
import { InsightCard } from '@/components/charts/InsightCard';

const suggestedBrands = ['Zomato', 'Swiggy', 'Nike', 'Apple', 'Tesla', 'Airbnb', 'Stripe', 'Notion'];

function DashboardPreview() {
  const metrics = [
    { label: 'Sentiment Score', value: '+64', change: '+12% vs last month', changeType: 'positive' as const, icon: <TrendingUp className="h-5 w-5" /> },
    { label: 'Share of Voice', value: '28.4%', change: '+2.1pp', changeType: 'positive' as const, icon: <Users className="h-5 w-5" /> },
    { label: 'Mentions', value: '124.2k', change: '+18%', changeType: 'positive' as const, icon: <BarChart2 className="h-5 w-5" /> },
    { label: 'Avg Rating', value: '4.2/5', change: '+0.1', changeType: 'positive' as const, icon: <Star className="h-5 w-5" /> },
  ];

  return (
    <div className="card relative overflow-hidden bg-surface-raised border-border shadow-elevated">
      <div className="absolute inset-0 bg-gradient-to-br from-accent/5 via-transparent to-positive/5" aria-hidden="true" />
      <div className="relative p-5 md:p-6 space-y-5">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-ink flex items-center justify-center text-white font-display text-lg">S</div>
            <div>
              <p className="font-sans font-medium text-ink">Zomato</p>
              <p className="font-sans text-xs text-muted">Food Delivery · India</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <span className="badge badge-primary">Live</span>
            <button className="p-2 rounded-lg text-muted hover:text-ink hover:bg-surface transition-colors" aria-label="More options">
              <svg className="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="1" /><circle cx="19" cy="12" r="1" /><circle cx="5" cy="12" r="1" /></svg>
            </button>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          {metrics.map((metric, i) => (
            <MetricCard key={metric.label} {...metric} className="animate-count-up" style={{ animationDelay: `${i * 100}ms` }} />
          ))}
        </div>

        <div className="grid grid-cols-2 gap-4 pt-2">
          <div className="chart-container h-40" aria-label="Sentiment trend chart">
            <SentimentChart />
          </div>
          <div className="chart-container h-40" aria-label="Share of voice chart">
            <ShareOfVoiceChart />
          </div>
        </div>

        <div className="grid grid-cols-3 gap-3 pt-2">
          <InsightCard title="Pricing Advantage" desc="23% below category avg" type="positive" />
          <InsightCard title="Sentiment Rising" desc="Strong Q4 campaign" type="positive" />
          <InsightCard title="Competitor Alert" desc="Swiggy launched loyalty" type="warning" />
        </div>
      </div>
    </div>
  );
}

export function Hero() {
  const [query, setQuery] = useState('');
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [focusedIndex, setFocusedIndex] = useState(-1);
  const inputRef = useRef<HTMLInputElement>(null);
  const suggestionsRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (inputRef.current && !inputRef.current.contains(e.target as Node) &&
          suggestionsRef.current && !suggestionsRef.current.contains(e.target as Node)) {
        setShowSuggestions(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      window.location.href = `/dashboard/analyze/new?brand=${encodeURIComponent(query.trim())}`;
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (!showSuggestions) return;
    const filtered = suggestedBrands.filter(b => b.toLowerCase().includes(query.toLowerCase()));
    if (filtered.length === 0) return;

    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setFocusedIndex(prev => Math.min(prev + 1, filtered.length - 1));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setFocusedIndex(prev => Math.max(prev - 1, 0));
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (focusedIndex >= 0 && filtered[focusedIndex]) {
        setQuery(filtered[focusedIndex]);
        handleSubmit(e);
      }
    } else if (e.key === 'Escape') {
      setShowSuggestions(false);
      setFocusedIndex(-1);
    }
  };

  const filteredSuggestions = suggestedBrands.filter(b =>
    b.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <section className="relative section-py overflow-hidden" aria-labelledby="hero-heading">
      <div className="container-custom">
        <div className="grid lg:grid-cols-2 gap-12 lg:gap-16 items-start">
          <div className="max-w-2xl mx-auto lg:mx-0 animate-fade-up">
            <p className="eyebrow mb-5">COMPETITIVE INTELLIGENCE, POWERED BY AI</p>
            <h1 id="hero-heading" className="font-display text-ink mb-6 leading-tight">
              See the bigger picture.<br /><span className="gradient-text">Stay ahead.</span>
            </h1>
            <p className="body-lead mb-8">
              Turn scattered data into clear competitive intelligence. Track sentiment, compare competitors, and uncover opportunities in minutes, not weeks.
            </p>

            <form onSubmit={handleSubmit} className="relative mb-6" role="search">
              <label htmlFor="brand-search" className="sr-only">Enter a brand name to analyze</label>
              <div className="relative">
                <Search className="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-muted" aria-hidden="true" />
                <input
                  ref={inputRef}
                  id="brand-search"
                  type="text"
                  value={query}
                  onChange={(e) => {
                    setQuery(e.target.value);
                    setShowSuggestions(true);
                    setFocusedIndex(-1);
                  }}
                  onFocus={() => setShowSuggestions(query.length > 0)}
                  onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
                  onKeyDown={handleKeyDown}
                  placeholder="Enter a brand name (e.g., Nike, Zomato, Tesla)"
                  className="input pl-12 pr-40 py-4 text-lg"
                  autoComplete="off"
                  aria-autocomplete="list"
                  aria-controls="brand-suggestions"
                  aria-expanded={showSuggestions && filteredSuggestions.length > 0}
                />
                <Button type="submit" className="absolute right-2 top-1/2 -translate-y-1/2" size="default" aria-label="Analyze brand">
                  <ArrowRight className="h-5 w-5" />
                </Button>
              </div>
              {showSuggestions && filteredSuggestions.length > 0 && (
                <div
                  ref={suggestionsRef}
                  id="brand-suggestions"
                  role="listbox"
                  className="absolute top-full left-0 right-0 mt-2 card shadow-elevated overflow-hidden"
                >
                  {filteredSuggestions.map((brand, index) => (
                    <button
                      key={brand}
                      role="option"
                      aria-selected={index === focusedIndex}
                      onClick={() => {
                        setQuery(brand);
                        setShowSuggestions(false);
                        handleSubmit(new Event('submit') as unknown as React.FormEvent);
                      }}
                      onMouseEnter={() => setFocusedIndex(index)}
                      className={cn(
                        'w-full px-4 py-3 text-left font-sans text-base transition-colors',
                        index === focusedIndex ? 'bg-accent-soft text-accent' : 'hover:bg-surface'
                      )}
                    >
                      {brand}
                    </button>
                  ))}
                </div>
              )}
            </form>

            <p className="body-sm text-muted">Try: {suggestedBrands.slice(0, 5).map(b => <code key={b} className="px-1.5 py-0.5 rounded bg-surface font-mono text-xs mx-0.5">{b}</code>)}</p>

            <div className="mt-10 flex flex-wrap items-center gap-6 text-sm text-secondary">
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-positive" aria-hidden="true" />
                <span>No credit card required</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-accent" aria-hidden="true" />
                <span>2 min setup</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-warning" aria-hidden="true" />
                <span>Cancel anytime</span>
              </div>
            </div>
          </div>

          <div className="relative animate-fade-up-delay-1">
            <DashboardPreview />
          </div>
        </div>
      </div>

      <div className="absolute inset-0 -z-10 opacity-30" aria-hidden="true">
        <div className="absolute top-1/4 right-1/4 w-96 h-96 rounded-full bg-accent/20 blur-3xl" />
        <div className="absolute bottom-1/4 left-1/4 w-72 h-72 rounded-full bg-positive/10 blur-3xl" />
      </div>
    </section>
  );
}