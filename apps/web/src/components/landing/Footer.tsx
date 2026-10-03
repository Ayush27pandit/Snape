'use client';

import Link from 'next/link';
import { Zap, Twitter, Linkedin, Github, Mail } from 'lucide-react';
import { cn } from '@/lib/utils';

const footerLinks = {
  Product: [
    { label: 'Features', href: '#features' },
    { label: 'Use cases', href: '#use-cases' },
    { label: 'Pricing', href: '#pricing' },
    { label: 'API Docs', href: '/docs' },
    { label: 'Changelog', href: '/changelog' },
  ],
  Company: [
    { label: 'About', href: '/about' },
    { label: 'Blog', href: '/blog' },
    { label: 'Careers', href: '/careers' },
    { label: 'Contact', href: '/contact' },
    { label: 'Press', href: '/press' },
  ],
  Resources: [
    { label: 'Help Center', href: '/help' },
    { label: 'Community', href: '/community' },
    { label: 'Templates', href: '/templates' },
    { label: 'Webinars', href: '/webinars' },
    { label: 'FAQ', href: '/faq' },
  ],
  Legal: [
    { label: 'Privacy', href: '/privacy' },
    { label: 'Terms', href: '/terms' },
    { label: 'Security', href: '/security' },
    { label: 'Cookies', href: '/cookies' },
  ],
};

const socialLinks = [
  { name: 'Twitter', icon: <Twitter className="h-5 w-5" />, href: 'https://twitter.com/snape' },
  { name: 'LinkedIn', icon: <Linkedin className="h-5 w-5" />, href: 'https://linkedin.com/company/snape' },
  { name: 'GitHub', icon: <Github className="h-5 w-5" />, href: 'https://github.com/snape' },
  { name: 'Email', icon: <Mail className="h-5 w-5" />, href: 'mailto:hello@snape.ai' },
];

export function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-surface border-t border-border" role="contentinfo">
      <div className="container-custom py-12 md:py-16">
        <div className="grid grid-cols-2 md:grid-cols-6 gap-8 mb-12">
          <div className="col-span-2 md:col-span-1">
            <Link href="/" className="flex items-center gap-2 mb-4" aria-label="Snape home">
              <span className="w-9 h-9 rounded-xl bg-ink flex items-center justify-center text-white font-display text-xl">S</span>
              <span className="font-display text-xl font-medium">Snape</span>
            </Link>
            <p className="body-sm text-secondary mb-6 max-w-xs">
              AI-powered competitive intelligence for modern teams. Turn scattered data into clear decisions.
            </p>
            <div className="flex gap-4">
              {socialLinks.map((social) => (
                <a
                  key={social.name}
                  href={social.href}
                  className="p-2 rounded-lg text-secondary hover:text-white hover:bg-ink transition-colors"
                  aria-label={social.name}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  {social.icon}
                </a>
              ))}
            </div>
          </div>

          {Object.entries(footerLinks).map(([category, links]) => (
            <nav key={category} aria-label={`${category} links`}>
              <h4 className="font-sans font-semibold text-ink mb-4">{category}</h4>
              <ul className="space-y-3" role="list">
                {links.map((link) => (
                  <li key={link.label}>
                    <Link href={link.href} className="footer-link text-sm">{link.label}</Link>
                  </li>
                ))}
              </ul>
            </nav>
          ))}
        </div>

        <div className="pt-8 border-t border-border">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <p className="font-sans text-sm text-muted">
              © {currentYear} Snape. All rights reserved.
            </p>
            <div className="flex items-center gap-6 font-sans text-sm text-muted">
              <Link href="/privacy" className="footer-link">Privacy</Link>
              <Link href="/terms" className="footer-link">Terms</Link>
              <Link href="/security" className="footer-link">Security</Link>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}