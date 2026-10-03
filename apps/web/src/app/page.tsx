import { Navbar } from '@/components/landing/Navbar';
import { Hero } from '@/components/landing/Hero';
import { TrustStrip } from '@/components/landing/TrustStrip';
import { FeatureOverview } from '@/components/landing/FeatureOverview';
import { DataSources } from '@/components/landing/DataSources';
import { Workflow } from '@/components/landing/Workflow';
import { UseCases } from '@/components/landing/UseCases';
import { Testimonials } from '@/components/landing/Testimonials';
import { Pricing } from '@/components/landing/Pricing';
import { ClosingCTA } from '@/components/landing/ClosingCTA';
import { Footer } from '@/components/landing/Footer';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-background text-ink">
      <Navbar />
      <main>
        <Hero />
        <TrustStrip />
        <FeatureOverview />
        <DataSources />
        <Workflow />
        <UseCases />
        <Testimonials />
        <Pricing />
        <ClosingCTA />
        <Footer />
      </main>
    </div>
  );
}