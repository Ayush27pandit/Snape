'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Menu, X, Zap } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/Button';

const navLinks = [
  { href: '#features', label: 'Features' },
  { href: '#workflow', label: 'How it works' },
  { href: '#use-cases', label: 'Use cases' },
  { href: '#pricing', label: 'Pricing' },
  { href: '/docs', label: 'Docs' },
];

export function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => setIsScrolled(window.scrollY > 20);
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <header className={cn(
      'fixed top-0 left-0 right-0 z-50 transition-all duration-200',
      isScrolled ? 'bg-background/95 backdrop-blur-sm border-b border-border' : 'bg-transparent'
    )}>
      <nav className="container-custom" aria-label="Main navigation">
        <div className="flex items-center justify-between h-18 md:h-20">
          <Link href="/" className="flex items-center gap-2" aria-label="Snape home">
            <span className="w-9 h-9 rounded-xl bg-ink flex items-center justify-center text-white font-display text-xl">
              S
            </span>
            <span className="font-display text-xl md:text-2xl font-medium hidden sm:block">Snape</span>
          </Link>

          <div className="hidden md:flex items-center gap-10">
            {navLinks.map((link) => (
              <Link key={link.href} href={link.href} className="nav-link">
                {link.label}
              </Link>
            ))}
          </div>

          <div className="hidden md:flex items-center gap-4">
            <Link href="/sign-in" className="btn btn-ghost text-sm">Sign in</Link>
            <Link href="/sign-up">
              <Button size="default">Get started free</Button>
            </Link>
          </div>

          <button
            className="md:hidden p-2 rounded-lg text-secondary hover:text-ink hover:bg-surface transition-colors"
            onClick={() => setIsOpen(!isOpen)}
            aria-expanded={isOpen}
            aria-controls="mobile-menu"
            aria-label={isOpen ? 'Close menu' : 'Open menu'}
          >
            {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </button>
        </div>

        <div id="mobile-menu" className={cn('md:hidden overflow-hidden transition-all duration-300 ease-out', isOpen ? 'max-h-96 opacity-100 pb-6' : 'max-h-0 opacity-0')}>
          <div className="flex flex-col gap-2 pt-4">
            {navLinks.map((link) => (
              <Link key={link.href} href={link.href} className="nav-link py-3 px-2" onClick={() => setIsOpen(false)}>
                {link.label}
              </Link>
            ))}
            <div className="flex flex-col gap-3 pt-4 border-t border-border">
              <Link href="/sign-in" className="btn btn-ghost w-full justify-center" onClick={() => setIsOpen(false)}>Sign in</Link>
              <Link href="/sign-up" className="btn btn-primary w-full justify-center" onClick={() => setIsOpen(false)}>Get started free</Link>
            </div>
          </div>
        </div>
      </nav>
    </header>
  );
}