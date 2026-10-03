'use client';

import { cn } from '@/lib/utils';

const brands = [
  { name: 'Zomato', color: '#E23744' },
  { name: 'Swiggy', color: '#FC8019' },
  { name: 'Razorpay', color: '#02042B' },
  { name: 'Paytm', color: '#00BAF2' },
  { name: 'CRED', color: '#0B0F14' },
  { name: 'Zepto', color: '#5D3FD3' },
  { name: 'PhonePe', color: '#5F259F' },
  { name: 'Uber Eats', color: '#000000' },
];

export function TrustStrip() {
  return (
    <section className="border-y border-border py-12" aria-label="Brands you can analyze">
      <div className="container-custom">
        <p className="eyebrow text-center mb-8">BRANDS YOU CAN ANALYZE</p>
        <div className="flex items-center justify-center gap-8 md:gap-16 flex-wrap opacity-60 hover:opacity-100 transition-opacity duration-300">
          {brands.map((brand) => (
            <span
              key={brand.name}
              className="font-sans font-medium text-sm text-secondary whitespace-nowrap"
              style={{ color: brand.color }}
            >
              {brand.name}
            </span>
          ))}
        </div>
      </div>
    </section>
  );
}