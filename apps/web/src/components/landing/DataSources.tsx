'use client';

import { Newspaper, MessageSquare, Star, ShoppingBag, FileText, Globe } from 'lucide-react';
import { SectionHeading } from '@/components/ui/SectionHeading';
import { cn } from '@/lib/utils';

const sourceGroups = [
  { name: 'News & Press', desc: 'Major outlets, industry publications, PR wires', icon: <Newspaper className="h-6 w-6" />, count: '500+ sources' },
  { name: 'Social Media', desc: 'X, LinkedIn, Reddit, and accessible platforms', icon: <MessageSquare className="h-6 w-6" />, count: 'Real-time' },
  { name: 'Reviews', desc: 'Trustpilot, G2, App Store, Google Reviews', icon: <Star className="h-6 w-6" />, count: 'Structured data' },
  { name: 'E-commerce', desc: 'Amazon, Shopify stores, product pages', icon: <ShoppingBag className="h-6 w-6" />, count: 'Pricing & features' },
  { name: 'Blogs & Forums', desc: 'Industry blogs, communities, discussions', icon: <FileText className="h-6 w-6" />, count: 'Long-form insights' },
  { name: 'Web Search', desc: 'General web, articles, editorial content', icon: <Globe className="h-6 w-6" />, count: 'Broad coverage' },
];

const evidenceItems = [
  { type: 'news', title: 'TechCrunch', excerpt: 'Zomato\'s Q4 results beat estimates as food delivery margins improve...', time: '2h ago', sentiment: 'positive' as const },
  { type: 'social', title: '@foodie_reviews', excerpt: 'Just tried the new Zomato Pro membership. The delivery speed is actually insane now 🚀', time: '4h ago', sentiment: 'positive' as const },
  { type: 'review', title: 'App Store Review', excerpt: '⭐⭐⭐⭐⭐ Best food delivery app in India. Customer support is responsive.', time: '1d ago', sentiment: 'positive' as const },
  { type: 'pricing', title: 'Amazon Fresh', excerpt: 'Zomato grocery delivery now available in 12 cities. Competitive pricing vs BigBasket.', time: '3h ago', sentiment: 'neutral' as const },
  { type: 'news', title: 'Competitor Alert', excerpt: 'Swiggy launches loyalty program targeting Zomato users...', time: '1h ago', sentiment: 'negative' as const },
];

export function DataSources() {
  return (
    <section id="sources" className="section-py bg-surface" aria-labelledby="sources-heading">
      <div className="container-custom">
        <SectionHeading
          id="sources-heading"
          eyebrow="REAL-TIME INSIGHTS"
          title="Analyze across the entire web."
          subtitle="Snape combines multiple public sources to create a fuller view of any brand. Each source type adds a different lens — together they reveal the complete picture."
        />

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mt-12">
          {sourceGroups.map((source, i) => (
            <article key={source.name} className="card p-6 animate-fade-up" style={{ animationDelay: `${i * 100}ms` }}>
              <div className="feature-icon mb-4">{source.icon}</div>
              <h3 className="font-sans text-lg font-semibold text-ink mb-2">{source.name}</h3>
              <p className="body-sm text-secondary mb-3">{source.desc}</p>
              <span className="badge badge-primary">{source.count}</span>
            </article>
          ))}
        </div>

        <div className="mt-16">
          <h3 className="font-sans text-lg font-semibold text-ink mb-6">Evidence collage — how sources appear in analysis</h3>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
            {evidenceItems.map((item, i) => (
              <article key={item.type} className="card p-4 animate-fade-up" style={{ animationDelay: `${(i + 6) * 100}ms` }}>
                <div className="flex items-start gap-3">
                  <div className={cn(
                    'flex-shrink-0 w-10 h-10 rounded-xl flex items-center justify-center',
                    item.type === 'news' && 'bg-blue-100 text-blue-600',
                    item.type === 'social' && 'bg-purple-100 text-purple-600',
                    item.type === 'review' && 'bg-amber-100 text-amber-600',
                    item.type === 'pricing' && 'bg-green-100 text-green-600',
                  )}>
                    {item.type === 'news' && <Newspaper className="h-5 w-5" />}
                    {item.type === 'social' && <MessageSquare className="h-5 w-5" />}
                    {item.type === 'review' && <Star className="h-5 w-5" />}
                    {item.type === 'pricing' && <ShoppingBag className="h-5 w-5" />}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="font-sans text-xs font-medium text-secondary uppercase tracking-wide">{item.type}</p>
                    <p className="font-sans text-sm font-medium text-ink mt-1 line-clamp-2">{item.title}</p>
                    <p className="font-sans text-xs text-muted mt-1 line-clamp-2">{item.excerpt}</p>
                    <div className="flex items-center gap-2 mt-2">
                      <span className="font-sans text-xs text-muted">{item.time}</span>
                      <span className={cn(
                        'badge font-mono text-[10px]',
                        item.sentiment === 'positive' && 'badge-positive',
                        item.sentiment === 'negative' && 'badge-negative',
                        item.sentiment === 'neutral' && 'badge',
                      )}>
                        {item.sentiment}
                      </span>
                    </div>
                  </div>
                </div>
              </article>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}