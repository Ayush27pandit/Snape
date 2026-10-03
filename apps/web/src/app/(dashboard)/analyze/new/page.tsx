'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { ArrowRight, Loader2, Zap, Users, Globe, Calendar } from 'lucide-react';
import { cn } from '@/lib/utils';

const analysisTypes = [
  { value: 'DEEP_DIVE', label: 'Brand Deep Dive', desc: 'Comprehensive single brand analysis', icon: Zap },
  { value: 'COMPETITOR_COMPARISON', label: 'Competitor Comparison', desc: 'Side-by-side vs 1-5 rivals', icon: Users },
  { value: 'MARKET_LANDSCAPE', label: 'Market Landscape', desc: 'Category-wide view of top players', icon: Globe },
  { value: 'CAMPAIGN_TRACKING', label: 'Campaign Tracking', desc: 'Monitor specific launch or event', icon: Calendar },
];

const focusAreas = [
  'sentiment',
  'pricing',
  'product',
  'marketing',
  'audience',
  'crisis',
];

const dateRanges = [
  { value: 'LAST_7_DAYS', label: 'Last 7 days' },
  { value: 'LAST_30_DAYS', label: 'Last 30 days' },
  { value: 'LAST_90_DAYS', label: 'Last 90 days' },
  { value: 'LAST_YEAR', label: 'Last year' },
];

const depthOptions = [
  { value: 'quick', label: 'Quick (1-2 min)', desc: 'Top 5 sources, key metrics only' },
  { value: 'deep', label: 'Deep (3-5 min)', desc: 'Top 15 sources, full analysis' },
  { value: 'comprehensive', label: 'Comprehensive (8-10 min)', desc: 'Top 30 sources, exhaustive' },
];

export default function NewAnalysisPage() {
  const router = useRouter();
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    brandId: '',
    brandName: '',
    type: 'COMPETITOR_COMPARISON',
    competitors: [] as string[],
    dateRange: 'LAST_30_DAYS',
    focusAreas: ['sentiment', 'pricing', 'product', 'marketing'],
    depth: 'deep',
  });
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    // TODO: Call API to start analysis
    await new Promise(r => setTimeout(r, 1000));
    router.push('/dashboard/analyze/job-123');
    setIsLoading(false);
  };

  const updateField = (field: string, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const toggleFocusArea = (area: string) => {
    setFormData(prev => ({
      ...prev,
      focusAreas: prev.focusAreas.includes(area)
        ? prev.focusAreas.filter(a => a !== area)
        : [...prev.focusAreas, area]
    }));
  };

  const toggleCompetitor = (comp: string) => {
    setFormData(prev => ({
      ...prev,
      competitors: prev.competitors.includes(comp)
        ? prev.competitors.filter(c => c !== comp)
        : [...prev.competitors, comp]
    }));
  };

  const steps = [
    { num: 1, label: 'Brand' },
    { num: 2, label: 'Type' },
    { num: 3, label: 'Configure' },
    { num: 4, label: 'Review' },
  ];

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      {/* Progress Steps */}
      <div className="flex items-center justify-between">
        {steps.map((s, i) => (
          <div key={s.num} className="flex flex-col items-center">
            <div className={cn(
              'w-10 h-10 rounded-full flex items-center justify-center font-medium transition-colors',
              step >= s.num ? 'bg-primary text-primary-foreground' : 'bg-secondary text-secondary-foreground'
            )}>
              {step > s.num ? <ArrowRight className="h-5 w-5" /> : s.num}
            </div>
            <span className={cn('mt-2 text-xs font-medium', step >= s.num ? 'text-foreground' : 'text-muted-foreground')}>
              {s.label}
            </span>
            {i < steps.length - 1 && (
              <div className={cn(
                'absolute top-5 left-1/2 w-full h-0.5 -ml-px',
                step > s.num ? 'bg-primary' : 'bg-border'
              )} />
            )}
          </div>
        ))}
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Step 1: Brand Selection */}
        {step === 1 && (
          <div className="card p-6 space-y-4 animate-slide-up">
            <div>
              <h2 className="text-xl font-semibold">Select Brand</h2>
              <p className="text-muted-foreground">Choose an existing brand or enter a new one</p>
            </div>

            <div className="space-y-3">
              <label className="flex items-center gap-3 p-4 border rounded-lg cursor-pointer hover:bg-accent/50 transition-colors">
                <input
                  type="radio"
                  name="brandSource"
                  value="existing"
                  checked={!!formData.brandId}
                  onChange={() => updateField('brandId', '1')}
                  className="sr-only peer"
                />
                <div className="w-5 h-5 border rounded-full relative peer-checked:after:content-[''] peer-checked:after:absolute peer-checked:after:top-1 peer-checked:after:left-1 peer-checked:after:w-3 peer-checked:after:h-3 peer-checked:after:rounded-full peer-checked:after:bg-primary"></div>
                <div className="flex-1">
                  <p className="font-medium">Nike</p>
                  <p className="text-sm text-muted-foreground">nike.com • Apparel • 12 analyses</p>
                </div>
              </label>

              <label className="flex items-center gap-3 p-4 border rounded-lg cursor-pointer hover:bg-accent/50 transition-colors">
                <input
                  type="radio"
                  name="brandSource"
                  value="existing"
                  checked={formData.brandId === '2'}
                  onChange={() => updateField('brandId', '2')}
                  className="sr-only peer"
                />
                <div className="w-5 h-5 border rounded-full relative peer-checked:after:content-[''] peer-checked:after:absolute peer-checked:after:top-1 peer-checked:after:left-1 peer-checked:after:w-3 peer-checked:after:h-3 peer-checked:after:rounded-full peer-checked:after:bg-primary"></div>
                <div className="flex-1">
                  <p className="font-medium">Adidas</p>
                  <p className="text-sm text-muted-foreground">adidas.com • Apparel • 8 analyses</p>
                </div>
              </label>

              <div className="border-2 border-dashed border-border rounded-lg p-4 text-center">
                <p className="text-sm text-muted-foreground">Or enter a new brand name</p>
                <input
                  type="text"
                  placeholder="e.g., Tesla, Airbnb, Notion"
                  className="input mt-2 max-w-xs mx-auto"
                  value={formData.brandName}
                  onChange={(e) => updateField('brandName', e.target.value)}
                />
              </div>
            </div>

            <div className="flex justify-end">
              <button type="button" onClick={() => setStep(2)} className="btn btn-primary" disabled={!formData.brandId && !formData.brandName}>
                Next <ArrowRight className="ml-2 h-4 w-4" />
              </button>
            </div>
          </div>
        )}

        {/* Step 2: Analysis Type */}
        {step === 2 && (
          <div className="card p-6 space-y-4 animate-slide-up">
            <div>
              <h2 className="text-xl font-semibold">Choose Analysis Type</h2>
              <p className="text-muted-foreground">What kind of intelligence do you need?</p>
            </div>

            <div className="grid gap-3">
              {analysisTypes.map((type) => (
                <label key={type.value} className={cn(
                  'p-4 border rounded-lg cursor-pointer transition-colors flex items-center gap-4',
                  formData.type === type.value
                    ? 'border-primary bg-primary/5'
                    : 'hover:bg-accent/50'
                )}>
                  <input
                    type="radio"
                    name="analysisType"
                    value={type.value}
                    checked={formData.type === type.value}
                    onChange={() => updateField('type', type.value)}
                    className="sr-only peer"
                  />
                  <div className="h-10 w-10 rounded-lg bg-primary/10 text-primary flex items-center justify-center">
                    <type.icon className="h-5 w-5" />
                  </div>
                  <div>
                    <p className="font-medium">{type.label}</p>
                    <p className="text-sm text-muted-foreground">{type.desc}</p>
                  </div>
                </label>
              ))}
            </div>

            <div className="flex justify-between">
              <button type="button" onClick={() => setStep(1)} className="btn btn-outline">Back</button>
              <button type="button" onClick={() => setStep(3)} className="btn btn-primary">Next <ArrowRight className="ml-2 h-4 w-4" /></button>
            </div>
          </div>
        )}

        {/* Step 3: Configuration */}
        {step === 3 && (
          <div className="card p-6 space-y-6 animate-slide-up">
            <div>
              <h2 className="text-xl font-semibold">Configure Analysis</h2>
              <p className="text-muted-foreground">Fine-tune your analysis parameters</p>
            </div>

            {/* Competitors */}
            {formData.type === 'COMPETITOR_COMPARISON' && (
              <div className="space-y-3">
                <label className="block text-sm font-medium">Competitors to Compare</label>
                <div className="flex flex-wrap gap-2">
                  {['Adidas', 'Puma', 'Under Armour', 'New Balance', 'Reebok'].map((comp) => (
                    <button
                      key={comp}
                      type="button"
                      onClick={() => toggleCompetitor(comp)}
                      className={cn(
                        'px-3 py-1.5 rounded-full text-sm font-medium transition-colors',
                        formData.competitors.includes(comp)
                          ? 'bg-primary text-primary-foreground'
                          : 'bg-secondary text-secondary-foreground hover:bg-secondary/80'
                      )}
                    >
                      {comp}
                    </button>
                  ))}
                </div>
                <p className="text-sm text-muted-foreground">
                  {formData.competitors.length}/5 selected
                </p>
              </div>
            )}

            {/* Date Range */}
            <div className="space-y-3">
              <label className="block text-sm font-medium">Date Range</label>
              <select
                value={formData.dateRange}
                onChange={(e) => updateField('dateRange', e.target.value)}
                className="input max-w-xs"
              >
                {dateRanges.map((dr) => (
                  <option key={dr.value} value={dr.value}>{dr.label}</option>
                ))}
              </select>
            </div>

            {/* Focus Areas */}
            <div className="space-y-3">
              <label className="block text-sm font-medium">Focus Areas</label>
              <div className="flex flex-wrap gap-2">
                {focusAreas.map((area) => (
                  <button
                    key={area}
                    type="button"
                    onClick={() => toggleFocusArea(area)}
                    className={cn(
                      'px-3 py-1.5 rounded-full text-sm font-medium transition-colors',
                      formData.focusAreas.includes(area)
                        ? 'bg-primary text-primary-foreground'
                        : 'bg-secondary text-secondary-foreground hover:bg-secondary/80'
                    )}
                  >
                    {area.charAt(0).toUpperCase() + area.slice(1)}
                  </button>
                ))}
              </div>
            </div>

            {/* Depth */}
            <div className="space-y-3">
              <label className="block text-sm font-medium">Analysis Depth</label>
              <div className="space-y-2">
                {depthOptions.map((opt) => (
                  <label key={opt.value} className={cn(
                    'flex items-center gap-3 p-3 border rounded-lg cursor-pointer transition-colors',
                    formData.depth === opt.value
                      ? 'border-primary bg-primary/5'
                      : 'hover:bg-accent/50'
                  )}>
                    <input
                      type="radio"
                      name="depth"
                      value={opt.value}
                      checked={formData.depth === opt.value}
                      onChange={() => updateField('depth', opt.value)}
                      className="sr-only peer"
                    />
                    <div className="flex-1">
                      <p className="font-medium">{opt.label}</p>
                      <p className="text-sm text-muted-foreground">{opt.desc}</p>
                    </div>
                  </label>
                ))}
              </div>
            </div>

            <div className="flex justify-between">
              <button type="button" onClick={() => setStep(2)} className="btn btn-outline">Back</button>
              <button type="button" onClick={() => setStep(4)} className="btn btn-primary">Next <ArrowRight className="ml-2 h-4 w-4" /></button>
            </div>
          </div>
        )}

        {/* Step 4: Review */}
        {step === 4 && (
          <div className="card p-6 space-y-6 animate-slide-up">
            <div>
              <h2 className="text-xl font-semibold">Review & Start</h2>
              <p className="text-muted-foreground">Confirm your analysis configuration</p>
            </div>

            <div className="space-y-4">
              <div className="p-4 bg-secondary/50 rounded-lg">
                <p className="font-medium">Brand</p>
                <p className="text-lg">{formData.brandName || 'Nike'}</p>
              </div>

              <div className="p-4 bg-secondary/50 rounded-lg">
                <p className="font-medium">Analysis Type</p>
                <p className="text-lg capitalize">{formData.type.toLowerCase().replace('_', ' ')}</p>
              </div>

              {formData.type === 'COMPETITOR_COMPARISON' && formData.competitors.length > 0 && (
                <div className="p-4 bg-secondary/50 rounded-lg">
                  <p className="font-medium">Competitors</p>
                  <div className="flex flex-wrap gap-2 mt-1">
                    {formData.competitors.map((c) => (
                      <span key={c} className="badge badge-outline">{c}</span>
                    ))}
                  </div>
                </div>
              )}

              <div className="p-4 bg-secondary/50 rounded-lg">
                <p className="font-medium">Date Range</p>
                <p className="text-lg capitalize">{dateRanges.find(d => d.value === formData.dateRange)?.label}</p>
              </div>

              <div className="p-4 bg-secondary/50 rounded-lg">
                <p className="font-medium">Focus Areas</p>
                <div className="flex flex-wrap gap-2 mt-1">
                  {formData.focusAreas.map((a) => (
                    <span key={a} className="badge badge-outline">{a}</span>
                  ))}
                </div>
              </div>

              <div className="p-4 bg-secondary/50 rounded-lg">
                <p className="font-medium">Depth</p>
                <p className="text-lg capitalize">{depthOptions.find(d => d.value === formData.depth)?.label}</p>
              </div>
            </div>

            <div className="flex justify-between pt-4 border-t">
              <button type="button" onClick={() => setStep(3)} className="btn btn-outline">Back</button>
              <button type="submit" disabled={isLoading} className="btn btn-primary">
                {isLoading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Starting...
                  </>
                ) : (
                  <>
                    Start Analysis
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </>
                )}
              </button>
            </div>
          </div>
        )}
      </form>
    </div>
  );
}