import Link from 'next/link';
import { ArrowRight, Zap, Shield, BarChart2, Users, Clock } from 'lucide-react';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-primary-50 to-white dark:from-dark-900 dark:to-dark-950">
      {/* Navigation */}
      <nav className="border-b border-border/50 bg-background/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 h-16 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2">
            <Zap className="h-8 w-8 text-primary" />
            <span className="text-xl font-bold">Snape</span>
          </Link>
          <div className="flex items-center gap-6">
            <Link href="#features" className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors">
              Features
            </Link>
            <Link href="#pricing" className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors">
              Pricing
            </Link>
            <Link href="/sign-in" className="btn btn-ghost">
              Sign In
            </Link>
            <Link href="/sign-up" className="btn btn-primary">
              Get Started
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20 lg:py-32">
        <div className="max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 text-primary text-sm font-medium mb-8">
            <Zap className="h-4 w-4" />
            <span>AI-Powered Competitive Intelligence</span>
          </div>
          <h1 className="text-4xl lg:text-6xl font-bold tracking-tight text-foreground mb-6">
            Know Your Market.<br />
            <span className="text-primary">Outsmart Your Rivals.</span>
          </h1>
          <p className="text-lg lg:text-xl text-muted-foreground mb-10 max-w-2xl mx-auto">
            Enter a brand name. Snape searches the entire web, analyzes sentiment, tracks competitors,
            and delivers actionable insights — all in minutes, not weeks.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16">
            <Link href="/sign-up" className="btn btn-primary btn-lg w-full sm:w-auto">
              Start Free Analysis
              <ArrowRight className="ml-2 h-4 w-4" />
            </Link>
            <Link href="#demo" className="btn btn-outline btn-lg w-full sm:w-auto">
              View Demo
            </Link>
          </div>
          <div className="flex items-center justify-center gap-8 text-sm text-muted-foreground">
            <span className="flex items-center gap-1">
              <Shield className="h-4 w-4" />
              No credit card required
            </span>
            <span className="flex items-center gap-1">
              <Clock className="h-4 w-4" />
              2 min setup
            </span>
            <span className="flex items-center gap-1">
              <BarChart2 className="h-4 w-4" />
              Cancel anytime
            </span>
          </div>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="container mx-auto px-4 py-20">
        <div className="text-center mb-16">
          <h2 className="text-3xl lg:text-4xl font-bold mb-4">Everything You Need to Win</h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Comprehensive competitive intelligence powered by AI agents that search, analyze, and synthesize
            insights from across the web.
          </p>
        </div>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[
            {
              icon: BarChart2,
              title: 'Brand Deep Dive',
              desc: 'Sentiment analysis, news monitoring, review aggregation, and public opinion tracking for any brand.',
            },
            {
              icon: Users,
              title: 'Competitor Comparison',
              desc: 'Side-by-side analysis of 1-5 rivals across pricing, positioning, features, marketing channels, and audience overlap.',
            },
            {
              icon: Zap,
              title: 'Market Landscape',
              desc: 'Category-wide view of top 10-20 players with positioning maps, trend detection, and opportunity identification.',
            },
            {
              icon: Clock,
              title: 'Campaign Tracking',
              desc: 'Monitor specific launches, campaigns, or events with real-time mention tracking and impact measurement.',
            },
            {
              icon: Shield,
              title: 'Crisis Detection',
              desc: 'Early warning system for reputation events, negative sentiment spikes, and competitor counter-moves.',
            },
            {
              icon: BarChart2,
              title: 'Automated Reports',
              desc: 'Weekly/monthly email digests with executive summaries, key changes, and prioritized recommendations.',
            },
          ].map((feature, i) => (
            <div key={i} className="card p-6 hover:shadow-md transition-shadow">
              <div className="w-12 h-12 rounded-lg bg-primary/10 text-primary flex items-center justify-center mb-4">
                <feature.icon className="h-6 w-6" />
              </div>
              <h3 className="text-lg font-semibold mb-2">{feature.title}</h3>
              <p className="text-muted-foreground">{feature.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* How It Works */}
      <section className="bg-dark-50 dark:bg-dark-900 py-20">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl lg:text-4xl font-bold mb-4">How Snape Works</h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Four AI agents collaborate to deliver comprehensive intelligence in minutes.
            </p>
          </div>
          <div className="grid md:grid-cols-4 gap-6">
            {[
              { step: '01', title: 'Plan', desc: 'AI planner breaks down your request into targeted search strategies', icon: '🎯' },
              { step: '02', title: 'Search', desc: 'Multi-source search across web, news, social, reviews, and e-commerce', icon: '🔍' },
              { step: '03', title: 'Analyze', desc: 'Specialized agents extract insights, metrics, and sentiment from content', icon: '🧠' },
              { step: '04', title: 'Synthesize', desc: 'Final report with comparisons, citations, and actionable recommendations', icon: '📊' },
            ].map((step, i) => (
              <div key={i} className="relative text-center">
                <div className="w-16 h-16 rounded-full bg-primary/10 text-primary flex items-center justify-center mx-auto mb-4 text-2xl font-bold">
                  {step.step}
                </div>
                <div className="text-3xl font-bold mb-2">{step.icon}</div>
                <h3 className="font-semibold mb-1">{step.title}</h3>
                <p className="text-sm text-muted-foreground">{step.desc}</p>
                {i < 3 && (
                  <div className="absolute top-8 right-0 w-full h-0.5 bg-gradient-to-r from-primary to-transparent hidden md:block" />
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Data Sources */}
      <section className="container mx-auto px-4 py-20">
        <div className="text-center mb-16">
          <h2 className="text-3xl lg:text-4xl font-bold mb-4">Comprehensive Data Coverage</h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            We search and monitor 5+ source categories to give you the complete picture.
          </p>
        </div>
        <div className="grid md:grid-cols-5 gap-4">
          {[
            { name: 'Web Search', desc: 'Articles, blogs, forums', icon: '🌐' },
            { name: 'News & Press', desc: 'Major outlets, PR wires', icon: '📰' },
            { name: 'Social Media', desc: 'X, LinkedIn, Reddit', icon: '💬' },
            { name: 'Reviews', desc: 'Trustpilot, G2, App Store', icon: '⭐' },
            { name: 'E-commerce', desc: 'Amazon, Shopify stores', icon: '🛒' },
          ].map((source, i) => (
            <div key={i} className="card p-6 text-center">
              <div className="text-4xl mb-3">{source.icon}</div>
              <h3 className="font-semibold mb-1">{source.name}</h3>
              <p className="text-sm text-muted-foreground">{source.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Pricing */}
      <section id="pricing" className="bg-dark-50 dark:bg-dark-900 py-20">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl lg:text-4xl font-bold mb-4">Simple, Transparent Pricing</h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Start free. Upgrade when you need more. No hidden fees.
            </p>
          </div>
          <div className="grid md:grid-cols-2 gap-6 max-w-4xl mx-auto">
            {/* Free Tier */}
            <div className="card p-6">
              <div className="text-center mb-6">
                <h3 className="text-xl font-semibold">Free</h3>
                <div className="mt-2">
                  <span className="text-4xl font-bold">$0</span>
                  <span className="text-muted-foreground">/month</span>
                </div>
              </div>
              <ul className="space-y-3 mb-6">
                {[
                  '2 analyses per month',
                  '1 brand tracking',
                  'Basic metrics only',
                  'Interactive dashboard',
                  'Email support',
                ].map((feature, i) => (
                  <li key={i} className="flex items-center gap-2 text-sm">
                    <span className="h-5 w-5 rounded-full bg-green-100 text-green-700 flex items-center justify-center text-xs">✓</span>
                    {feature}
                  </li>
                ))}
              </ul>
              <Link href="/sign-up" className="btn btn-outline w-full">
                Start Free
              </Link>
            </div>

            {/* Pro Tier */}
            <div className="card p-6 border-primary relative">
              <div className="absolute -top-3 left-1/2 -translate-x-1/2 px-3 py-1 bg-primary text-primary-foreground text-xs font-semibold rounded-full">
                Most Popular
              </div>
              <div className="text-center mb-6">
                <h3 className="text-xl font-semibold">Pro</h3>
                <div className="mt-2">
                  <span className="text-4xl font-bold">$25</span>
                  <span className="text-muted-foreground">/month</span>
                </div>
              </div>
              <ul className="space-y-3 mb-6">
                {[
                  '20 analyses per month',
                  '5 brands tracking',
                  'All competitive metrics',
                  'Automated email digests',
                  'Priority processing queue',
                  'Export reports (coming soon)',
                  'API access (coming soon)',
                ].map((feature, i) => (
                  <li key={i} className="flex items-center gap-2 text-sm">
                    <span className="h-5 w-5 rounded-full bg-green-100 text-green-700 flex items-center justify-center text-xs">✓</span>
                    {feature}
                  </li>
                ))}
              </ul>
              <Link href="/sign-up" className="btn btn-primary w-full">
                Upgrade to Pro
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="container mx-auto px-4 py-20">
        <div className="max-w-3xl mx-auto text-center">
          <h2 className="text-3xl lg:text-4xl font-bold mb-4">Ready to Outsmart Your Competition?</h2>
          <p className="text-lg text-muted-foreground mb-8">
            Join founders, marketers, and creators using Snape to stay ahead.
          </p>
          <Link href="/sign-up" className="btn btn-primary btn-lg">
            Start Your First Analysis Free
            <ArrowRight className="ml-2 h-4 w-4" />
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border/50 py-12">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <Link href="/" className="flex items-center gap-2 mb-4">
                <Zap className="h-8 w-8 text-primary" />
                <span className="text-xl font-bold">Snape</span>
              </Link>
              <p className="text-sm text-muted-foreground">
                AI-powered competitive intelligence for modern teams.
              </p>
            </div>
            <div>
              <h4 className="font-semibold mb-3">Product</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><Link href="#features" className="hover:text-foreground">Features</Link></li>
                <li><Link href="#pricing" className="hover:text-foreground">Pricing</Link></li>
                <li><Link href="#" className="hover:text-foreground">API Docs</Link></li>
                <li><Link href="#" className="hover:text-foreground">Changelog</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-3">Company</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><Link href="#" className="hover:text-foreground">About</Link></li>
                <li><Link href="#" className="hover:text-foreground">Blog</Link></li>
                <li><Link href="#" className="hover:text-foreground">Careers</Link></li>
                <li><Link href="#" className="hover:text-foreground">Contact</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-3">Legal</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><Link href="#" className="hover:text-foreground">Privacy</Link></li>
                <li><Link href="#" className="hover:text-foreground">Terms</Link></li>
                <li><Link href="#" className="hover:text-foreground">Security</Link></li>
              </ul>
            </div>
          </div>
          <div className="mt-8 pt-8 border-t border-border/50 text-center text-sm text-muted-foreground">
            © 2024 Snape. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
}