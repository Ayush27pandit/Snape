# Snape Landing Page Design Specification

**Document type:** Implementation brief for an AI coding agent\
**Product:** Snape, an AI-powered competitive intelligence platform\
**Primary goal:** Build a polished, responsive marketing landing page
that communicates Snape's value quickly and converts visitors into free
users.

------------------------------------------------------------------------

## 1. Product overview

Snape helps founders, marketers, and creators understand brands and
markets without manually searching dozens of websites.

Users can enter a brand name and receive: - Brand deep dives covering
news, reviews, sentiment, and public opinion - Side-by-side comparisons
against 1--5 competitors - Market landscape analysis across 10--20
players - Campaign tracking for launches, announcements, and events -
Actionable insights grounded in collected sources

The landing page should communicate one central idea: **turn scattered
public data into clear competitive decisions.**

### Primary audience

-   Founders evaluating competitors and market opportunities
-   Marketers tracking brand perception, share of voice, and campaigns
-   Creators understanding their brand and audience positioning
-   Researchers exploring market and category trends

### Primary conversion

Get started free.

### Secondary conversion

Try a brand analysis by entering a company name in the hero search
field.

------------------------------------------------------------------------

## 2. Design direction

### Visual concept

Use a premium, editorial SaaS aesthetic inspired by the restraint and
clarity of high-end product websites, especially Apple's use of
whitespace, typography, and large product imagery. Treat this as
inspiration, not a pixel-for-pixel recreation of any existing website.

The design should feel: - Precise and considered - Calm rather than
loud - Data-rich but not visually cluttered - Premium without looking
like a luxury fashion site - Modern, with real product UI as the main
visual asset

### Avoid

-   Purple or violet gradients
-   Generic startup gradients
-   Huge glowing blobs behind every section
-   Excessive glassmorphism
-   Repeated identical card grids without hierarchy
-   Generic geometric sans-serif typography for every text element
-   Emoji used as interface icons
-   Fake logos, fabricated customer quotes, or unsupported trust claims
-   Decorative animation that competes with the content

### Design principles

1.  **Product first:** Show the Snape dashboard prominently. The product
    UI should be the hero's visual anchor.
2.  **Editorial typography:** Use a distinctive serif display face for
    major headings and a highly readable sans-serif for interface and
    body copy.
3.  **Restrained color:** Mostly off-white, black, slate gray, and
    subtle blue. Reserve green for positive metrics and status.
4.  **Real hierarchy:** Large headlines, short supporting copy,
    deliberate section spacing, and clear calls to action.
5.  **Progressive detail:** Explain the value first, then reveal
    features, workflow, use cases, and pricing.
6.  **Responsive by design:** The page must work on mobile, not merely
    shrink the desktop layout.

------------------------------------------------------------------------

## 3. Color system

Use CSS variables or Tailwind theme tokens. Do not scatter raw hex
values throughout components.

  --------------------------------------------------------------------------
  Token                      Value                   Usage
  -------------------------- ----------------------- -----------------------
  `--color-ink`              `#0B0F14`               Primary text, dark CTA

  `--color-text-secondary`   `#68707C`               Supporting copy

  `--color-text-muted`       `#8A919B`               Captions, helper labels

  `--color-background`       `#FFFFFF`               Main page background

  `--color-surface`          `#F7F8FA`               Alternate sections and
                                                     soft panels

  `--color-surface-raised`   `#FFFFFF`               Cards and dashboard
                                                     panels

  `--color-border`           `#E5E8EC`               Borders and dividers

  `--color-accent`           `#2563EB`               Links, focus rings,
                                                     selected states

  `--color-accent-soft`      `#EFF6FF`               Selected tabs and
                                                     subtle blue surfaces

  `--color-positive`         `#16A34A`               Positive sentiment and
                                                     metric changes

  `--color-warning`          `#D97706`               Cautions and
                                                     medium-impact insights

  `--color-negative`         `#DC2626`               Negative sentiment and
                                                     alerts

  `--color-dark-surface`     `#111820`               Dark CTA banner and
                                                     selected dark panels
  --------------------------------------------------------------------------

### Color usage rules

-   The overall page should remain predominantly white and neutral.
-   Blue is an accent, not a full-page background.
-   Use semantic colors only when they communicate meaning, especially
    in analytics.
-   Do not use color alone to convey sentiment. Include labels, icons,
    or values.
-   Keep text contrast accessible. Target WCAG AA contrast for body text
    and controls.
-   Use gradients only as subtle atmospheric lighting behind the hero
    product mockup or closing CTA.

------------------------------------------------------------------------

## 4. Typography

### Recommended font pairing

Use a refined editorial serif for display headings and a modern
sans-serif for body text and UI.

Suggested pairing: - **Display:** `DM Serif Display` or
`Instrument Serif` - **Body/UI:** `Inter` or `Geist Sans` - **Optional
data labels:** use the body font with tabular numerals

Choose one display font and one sans-serif. Do not load every suggested
family.

### Type scale

  -----------------------------------------------------------------------------------------------
  Element                                  Desktop                         Mobile Notes
  --------------- -------------------------------- ------------------------------ ---------------
  Hero heading      `clamp(3.5rem, 6.2vw, 6.5rem)`   `clamp(3rem, 13vw, 4.25rem)` Tight leading,
                                                                                  editorial

  Section heading       `clamp(2.5rem, 4vw, 4rem)`              `2.25rem–2.75rem` Serif

  Card heading                  `1.125rem–1.25rem`                     `1.125rem` Sans-serif,
                                                                                  medium weight

  Body lead                     `1.125rem–1.25rem`                `1rem–1.125rem` Comfortable
                                                                                  line height

  Body                                      `1rem`               `0.9375rem–1rem` Line height
                                                                                  1.5--1.7

  Eyebrow                      `0.6875rem–0.75rem`                    `0.6875rem` Uppercase,
                                                                                  letter spacing

  UI labels                     `0.75rem–0.875rem`             `0.75rem–0.875rem` Clear at small
                                                                                  sizes
  -----------------------------------------------------------------------------------------------

### Typography rules

-   Use the serif face for hero and major section headlines, not for
    every card title.
-   Use sentence case for navigation, buttons, and most headings.
-   Avoid ultra-light weights for body text.
-   Keep headline line lengths intentional. Use explicit line breaks
    only where they improve composition.
-   Use tabular numerals for dashboard metrics to prevent values from
    shifting.
-   Ensure the font files load locally or through a reliable font
    provider with appropriate fallbacks.

------------------------------------------------------------------------

## 5. Layout and spacing

### Global layout

-   Maximum content width: `1200px–1320px`
-   Main horizontal page padding: `clamp(20px, 5vw, 80px)`
-   Desktop section spacing: `96px–160px`
-   Tablet section spacing: `80px–112px`
-   Mobile section spacing: `64px–88px`
-   Standard card radius: `16px–24px`
-   Search/input radius: pill-shaped or `999px`
-   Small UI control radius: `8px–12px`
-   Border thickness: `1px`
-   Shadows: soft and low-opacity; avoid heavy black shadows

Use a consistent spacing scale based on 4px or 8px increments.

### Grid

-   Desktop: 12-column grid
-   Feature grids: 2 columns where copy and supporting visuals need room
-   Use-case cards: 4 columns on wide desktop, 2 on tablet, 1 on narrow
    mobile
-   Pricing: 2 columns on desktop, stacked on mobile
-   Dashboard mockup: wide enough to read key metrics on desktop;
    simplified or horizontally cropped with a deliberate frame on mobile

### Background treatments

Alternate between white and very light neutral surfaces to create
section rhythm. Avoid putting every section inside a rounded container.
Use full-width background changes sparingly.

------------------------------------------------------------------------

## 6. Page structure and section requirements

Build the page in the following order. Keep sections modular so they can
be reordered or revised independently.

### 6.1 Navigation

**Layout** - Snape mark and wordmark on the left - Product, Use cases,
Pricing, Blog, Docs in the middle on desktop - Sign in and Get started
free on the right - Mobile menu button on small screens

**Visual treatment** - White or near-white background - Compact height,
generous horizontal spacing - Sticky navigation is optional; if used,
keep it subtle and avoid a large shadow - Dark pill-shaped primary CTA -
Minimal outline or text treatment for secondary navigation

**Behavior** - Navigation links scroll to relevant sections or route to
existing pages. - Mobile menu opens and closes accessibly. - CTA uses
the real app route if one exists. Do not invent an authentication route
without checking the project.

### 6.2 Hero section

**Suggested copy** - Eyebrow:
`COMPETITIVE INTELLIGENCE, POWERED BY AI` - Headline:
`See the bigger picture. Stay ahead.` - Supporting copy:
`Turn scattered data into clear competitive intelligence. Track sentiment, compare competitors, and uncover opportunities in minutes, not weeks.` -
Primary action: `Analyze brand` - Supporting examples: `Zomato`,
`Swiggy`, `Nike`, `Apple`, `Tesla`

**Layout** - Desktop: editorial copy on the left, large Snape dashboard
mockup on the right - Tablet: two-column layout may remain if readable;
otherwise stack - Mobile: copy and input first, dashboard preview
below - Keep enough whitespace around the heading to make the hero feel
composed rather than crowded

**Dashboard mockup** Create a high-fidelity product preview that
includes: - Sidebar navigation - Brand header for Zomato - Sentiment
score - Share of voice - Mention volume - Average rating - Market
position - Sentiment trend line chart - Share-of-voice donut chart - Top
insight cards

Use illustrative sample values and clearly treat them as demo data. Do
not imply that the values are live or verified unless the backend
actually supplies them.

**Hero background** Use a very subtle architectural, abstract, or softly
lit neutral image behind the dashboard. It must not reduce text
contrast. The dashboard should remain the visual focus.

**Hero interaction** - Brand input accepts a brand name. - Enter and
button click submit the same action. - Suggested brands populate the
input. - If analysis is not wired to the backend yet, show a clear demo
state or route to an existing demo. Do not show a fake loading state
that never resolves.

### 6.3 Trust strip

Show a restrained row of brand logos or customer marks below the hero.

Potential examples shown in the concept: Zomato, Swiggy, Razorpay,
Paytm, CRED, Zepto, PhonePe, Uber Eats.

**Important:** Use these only as examples of recognizable brands in an
analysis UI, not as customer endorsements. Do not imply that these
companies use Snape. If no verified customer logos exist, label the
strip `Brands you can analyze` or use supported data-source logos
instead.

### 6.4 Feature overview

**Eyebrow:** `EVERYTHING YOU NEED`\
**Heading:** `From data to decisions.`

Use four feature cards: 1. **Brand Deep Dive**\
Analyze sentiment, news, reviews, and public opinion for any brand. 2.
**Competitor Comparison**\
Compare 1--5 competitors side by side across key metrics. 3. **Market
Landscape**\
Explore a category of 10--20 players and identify opportunities. 4.
**Campaign Tracking**\
Measure public response to launches, announcements, and events.

Each card should include: - Small line icon - Title and short
description - A distinct, lightweight visual such as a chart, comparison
bars, or market map - A subtle hover state

Do not make the entire card a link unless it leads somewhere meaningful.

### 6.5 Data sources / real-time intelligence

**Eyebrow:** `REAL-TIME INSIGHTS`\
**Heading:** `Analyze across the entire web.`

Explain that Snape combines multiple public sources to create a fuller
view of a brand.

Source groups: - News and press outlets - Social media, including X,
LinkedIn, and Reddit where accessible - Review platforms such as
Trustpilot, G2, and App Store reviews - E-commerce and product pages -
Blogs, forums, and industry publications

**Visual** Build a layered evidence collage: source snippets, a news
card, a social post, a review card, and a small analytics panel. Use a
consistent card system and avoid a chaotic pile of floating windows.

**Data honesty** Only claim a source is connected when it is supported
by the product implementation and terms of access. If the landing page
is describing planned integrations, label them accordingly.

### 6.6 Workflow section

**Eyebrow:** `SIMPLE PROCESS`\
**Heading:** `Get insights in minutes.`

Four steps: 1. **Enter a brand**\
Choose a brand or category to analyze. 2. **AI agents research**\
Search, collect, and organize relevant public information. 3. **Get
comprehensive analysis**\
Review charts, competitor comparisons, source-backed findings, and
sentiment trends. 4. **Make better decisions**\
Use the findings to guide positioning, campaigns, and research.

**Visual** A horizontal sequence with numbered steps, outline icons, and
thin connector lines on desktop. Stack vertically on mobile.

**Animation** Reveal steps in sequence when the section enters the
viewport, with a reduced-motion fallback.

### 6.7 Use cases

**Eyebrow:** `BUILT FOR DIFFERENT TEAMS`\
**Heading:** `Where insights create impact.`

Four cards: - **Founders:** Track competitors, identify opportunities,
and make strategic decisions. - **Marketers:** Monitor brand sentiment,
track campaigns, and benchmark against competitors. - **Creators:**
Understand brand perception and identify collaboration opportunities. -
**Researchers:** Compare markets, explore category trends, and collect
source-backed insights.

Use relevant, consistent photography or restrained editorial
illustrations. If using photos, keep crops, color treatment, and
lighting consistent. Avoid generic AI-generated business people where a
product visual would be more relevant.

### 6.8 Testimonials / proof

**Eyebrow:** `LOVED BY EARLY USERS`\
**Heading:** `Trusted by people who look closer.`

Use real customer testimonials only, with permission and accurate names,
roles, and organizations.

If verified testimonials are not available: - Replace this section with
a product-benefits section, or - Use clearly labeled sample quotes in
development only, and remove them before production.

Do not publish fabricated user counts, ratings, or claims such as
`Trusted by 3,000+ users` without evidence.

### 6.9 Pricing

**Eyebrow:** `SIMPLE PRICING`\
**Heading:** `Start free, scale as you grow.`

Use two pricing cards based on the current MVP pricing:

#### Free

-   Price: `$0/month`
-   2 analyses per month
-   1 brand
-   Basic metrics
-   CTA: `Get started free`

#### Pro

-   Price: `$25/month`
-   20 analyses per month
-   5 brands
-   All metrics and AI insights
-   Email digests
-   CTA: `Get started with Pro`

Show the Pro plan with slightly stronger visual emphasis, but do not
make the free plan hard to find.

**Pricing behavior** - If monthly/yearly billing is offered, implement a
real toggle and show accurate prices. - Do not show a yearly discount
until a real yearly price has been decided. - Pricing buttons must route
to the actual sign-up or checkout flow. - Make plan limits and renewal
terms easy to understand.

### 6.10 Closing CTA

**Visual** A wide, dark, cinematic banner with a subdued mountain or
abstract horizon image. Keep the image dark enough for legible white
text. Avoid purple hues and strong neon effects.

**Suggested copy** - Eyebrow: `STAY AHEAD OF THE COMPETITION` - Heading:
`Turn information into opportunity.` - Supporting copy:
`Make your next move with a clearer view of the market.` - CTA:
`Get started free`

The banner should feel like a deliberate visual pause before the footer.

### 6.11 Footer

Include: - Snape logo and a short product description - Product links -
Use cases - Pricing - Blog and docs, if those pages exist - Privacy and
terms links, when available - Social links only for active, official
accounts - Current copyright year generated dynamically

Do not render dead links or placeholder `#` links in production.

------------------------------------------------------------------------

## 7. Asset requirements

Create an organized asset folder and use descriptive names. Prefer local
assets for predictable performance.

Suggested structure:

``` text
public/
  images/
    hero/
      snape-hero-background.webp
      snape-dashboard-preview.webp
    sources/
      news-source-card.webp
      social-source-card.webp
      review-source-card.webp
    use-cases/
      founders.webp
      marketers.webp
      creators.webp
      researchers.webp
    cta/
      closing-landscape.webp
  logos/
    snape-mark.svg
    snape-wordmark.svg
    sources/
  icons/
```

This is a suggested structure. Adapt it to the repository's existing
conventions instead of duplicating existing assets.

### Asset sourcing rules

1.  Inspect the repository before creating new assets.
2.  Reuse the existing Snape logo if one exists.
3.  Use custom SVGs or a consistent icon library for interface icons.
4.  Use WebP or AVIF for raster imagery where supported.
5.  Avoid large background images when CSS gradients or simple shapes
    are sufficient.
6.  Never hotlink random images from search results.
7.  Use assets with suitable licenses and record their source where
    appropriate.
8.  Do not use third-party logos in a way that implies endorsement.
9.  For the dashboard, prefer real frontend components over a flat
    screenshot when the result can be implemented accurately.
10. If using a static screenshot, provide appropriate alt text and
    ensure mobile readability.

### Image treatment

-   Natural, neutral color grading
-   Soft daylight or restrained cinematic lighting
-   Minimal visual noise
-   Consistent aspect ratios within each card group
-   Rounded corners matching the UI
-   No purple overlays

### Image loading

-   Use `next/image` for Next.js image assets.
-   Set dimensions or aspect ratios to prevent layout shift.
-   Prioritize the hero's primary visual.
-   Lazy-load below-the-fold images.
-   Provide useful alt text for meaningful images; use empty alt text
    for purely decorative images.

------------------------------------------------------------------------

## 8. Dashboard and chart design

The dashboard is the most important visual proof that Snape is a real
product.

### Dashboard visual language

-   White and pale-gray panels
-   Thin neutral borders
-   Small, legible sans-serif labels
-   Restrained shadows
-   Compact, consistent spacing
-   Blue for active navigation and selected elements
-   Green/red/orange for semantic metric changes
-   No purple chart palette

### Suggested sample metrics

Use only as explicitly illustrative demo data: - Sentiment score:
`+64` - Share of voice: `28.4%` - Mentions: `124.2k` - Average rating:
`4.2/5` - Market position: `#2`

Keep the date range visible when charts imply a timeline. Add labels and
legends to charts so that meaning does not rely on color alone.

### Charts

-   Sentiment trend: line chart with clear axis labels
-   Share of voice: donut chart with labeled segments and percentages
-   Mentions: small bar chart or sparkline
-   Top insights: compact cards with impact labels and short
    explanations

Use the chart library already installed in the project. If none exists,
choose a lightweight accessible library rather than adding multiple
charting dependencies.

------------------------------------------------------------------------

## 9. Motion and animation guidelines

Motion should make the interface feel responsive and help visitors
understand relationships. Keep it subtle, short, and purposeful.

### Recommended motion

  -----------------------------------------------------------------------
  Element                 Animation               Timing
  ----------------------- ----------------------- -----------------------
  Hero copy               Fade in and move upward 500--700ms
                          by 12--18px             

  Dashboard mockup        Fade in with slight     700--900ms
                          upward movement         

  Dashboard floating      Very subtle vertical    5--8s loop
  effect                  movement                

  Feature cards           Fade/translate into     400--600ms
                          view as section appears 

  Workflow steps          Staggered reveal        100--150ms stagger

  Chart lines             Draw or animate from    700--1000ms
                          baseline on first       
                          reveal                  

  Metric values           Count up once when      500--800ms
                          visible                 

  Buttons                 Small color/shadow      150--220ms
                          change on hover         

  Cards                   Move up 2--4px on hover 180--250ms

  Navigation              Subtle background or    150--200ms
                          border change           
  -----------------------------------------------------------------------

Timing values are starting points, not rigid requirements. Prioritize
smoothness and responsiveness.

### Motion rules

-   Prefer CSS transitions for simple hover and focus effects.
-   Use the animation library already present in the repository. If none
    exists, CSS and the Intersection Observer API may be enough; avoid
    adding a large library for a few reveals.
-   Do not animate every element.
-   Avoid large parallax movement, scroll hijacking, cursor-following
    effects, and looping attention-grabbing animations.
-   Start animations only when useful, not on every re-render.
-   Avoid layout shifts during entrance animations.
-   Keep transform and opacity as the primary animated properties.
-   Stop or simplify continuous motion when the component is offscreen.
-   Respect `prefers-reduced-motion: reduce`. Remove floating motion and
    scroll-triggered movement for users who request reduced motion.
-   Ensure interactions work without animation.

### Interaction states

Every interactive element needs: - Default - Hover, where applicable -
Keyboard focus-visible - Active/pressed - Disabled, when applicable -
Loading and error states for async actions

Use a clear focus ring. Never remove outlines without providing a
visible replacement.

------------------------------------------------------------------------

## 10. Responsive behavior

### Desktop: 1200px and above

-   Two-column hero with dashboard preview on the right
-   Full navigation
-   Four-column use-case grid where content allows
-   Two-column pricing cards
-   Horizontal workflow

### Tablet: 768px--1199px

-   Reduce hero headline size and dashboard scale
-   Allow hero content to stack if the dashboard becomes too narrow
-   Use two-column feature and use-case grids
-   Preserve readable card widths and generous spacing

### Mobile: below 768px

-   Single-column layout
-   Compact navigation with accessible menu
-   Hero headline around 48--68px depending on viewport width
-   Search input and CTA fit the available width
-   Dashboard preview below the main CTA; simplify its visible contents
    if necessary
-   Feature and use-case cards stack vertically or use a carefully
    tested horizontal scroller
-   Workflow becomes vertical
-   Pricing cards stack, with price and CTA visible without awkward
    overflow
-   Reduce decorative imagery and disable parallax
-   No horizontal page overflow
-   Touch targets should generally be at least 44px high

Test at 320px, 375px, 390px, 768px, 1024px, 1280px, and 1440px widths.

------------------------------------------------------------------------

## 11. Accessibility

-   Use semantic landmarks: `header`, `nav`, `main`, section headings,
    and `footer`.
-   Maintain a logical heading hierarchy with one primary `h1`.
-   Ensure all controls work with a keyboard.
-   Use accessible names for icon-only buttons.
-   Associate labels and error messages with form fields.
-   Do not rely on color alone for chart or status meaning.
-   Maintain readable contrast for text and UI controls.
-   Provide useful image alt text.
-   Make mobile navigation keyboard accessible and announce its expanded
    state.
-   Respect reduced-motion preferences.
-   Use `aria-live` or an equivalent accessible status region for
    analysis submission results where appropriate.

------------------------------------------------------------------------

## 12. Performance requirements

-   Keep the initial hero fast and avoid unnecessary client-side
    JavaScript.
-   Prefer Server Components in Next.js where possible; use Client
    Components only for interactive areas.
-   Use optimized images and font loading.
-   Avoid loading all below-the-fold imagery eagerly.
-   Avoid heavy background videos.
-   Lazy-load nonessential charts or complex visualizations below the
    fold.
-   Prevent cumulative layout shift by defining image dimensions and
    stable component heights.
-   Use CSS for simple visual effects rather than JavaScript when
    practical.
-   Avoid adding dependencies without a clear benefit.

### Suggested quality targets

Aim for strong Core Web Vitals and a Lighthouse score of 90+ where
practical for Performance, Accessibility, Best Practices, and SEO. Treat
these as targets to measure, not guarantees.

------------------------------------------------------------------------

## 13. SEO and metadata

Implement: - Page title: `Snape | AI-Powered Competitive Intelligence` -
Description:
`Analyze brands, compare competitors, track sentiment, and turn public data into actionable market insights with Snape.` -
Canonical URL once the production domain is known - Open Graph title,
description, and image - Twitter/X card metadata where relevant -
Favicon and app icons using the Snape mark - Appropriate heading
structure - Descriptive link text - Structured data only where it
accurately represents the product

Do not invent a production domain or social account URL.

------------------------------------------------------------------------

## 14. Suggested component architecture

Adapt to the existing codebase; do not restructure the repository
unnecessarily.

``` text
apps/web/src/
  app/
    page.tsx
    layout.tsx
    globals.css
  components/
    landing/
      Navbar.tsx
      HeroSection.tsx
      BrandSearch.tsx
      DashboardPreview.tsx
      TrustStrip.tsx
      FeatureOverview.tsx
      DataSourcesSection.tsx
      WorkflowSection.tsx
      UseCasesSection.tsx
      TestimonialsSection.tsx
      PricingSection.tsx
      ClosingCta.tsx
      Footer.tsx
    ui/
      Button.tsx
      SectionHeading.tsx
      FeatureCard.tsx
      MetricCard.tsx
```

Use existing components and conventions when they already cover these
responsibilities. Keep the landing page components small, typed, and
easy to adjust.

### Implementation notes

-   Use TypeScript types for reusable component props.
-   Keep repeated content in typed data arrays where appropriate.
-   Use semantic HTML and avoid unnecessary wrapper elements.
-   Keep all color and typography tokens centralized.
-   Avoid turning the entire landing page into one large component.
-   Keep the visual dashboard separate from actual analysis data unless
    the backend is wired to it.
-   Ensure links and CTA buttons have meaningful destinations.

------------------------------------------------------------------------

## 15. Implementation plan for the AI coding agent

Follow these steps in order:

1.  **Inspect the repository**
    -   Read the package manifest, current routes, design tokens, and
        existing UI components.
    -   Identify the installed icon, animation, and chart libraries.
    -   Locate the Snape logo and any existing dashboard components.
    -   Do not overwrite existing working functionality.
2.  **Set the foundation**
    -   Establish color, typography, spacing, radius, shadow, and
        container tokens.
    -   Load the selected fonts.
    -   Define responsive container and section utilities.
3.  **Build the page structure**
    -   Implement navigation, hero, trust strip, features, sources,
        workflow, use cases, proof, pricing, closing CTA, and footer.
    -   Use reusable components and consistent section spacing.
4.  **Build the dashboard preview**
    -   Create a realistic responsive UI with metric cards, charts, and
        insight cards.
    -   Use clearly illustrative data unless real data is available.
    -   Ensure text and chart labels remain legible at intended
        breakpoints.
5.  **Add behavior**
    -   Wire the brand search to the existing analysis route/API if
        available.
    -   Connect navigation and pricing CTAs to valid routes.
    -   Add mobile menu behavior and form validation.
    -   Include loading, error, and success states for real async work.
6.  **Add motion**
    -   Add restrained entrance and hover effects.
    -   Support reduced-motion preferences.
    -   Avoid introducing animation dependencies unless needed.
7.  **Verify**
    -   Run lint, type checks, and available tests.
    -   Test responsive layouts at the specified widths.
    -   Check keyboard navigation, focus visibility, contrast, and
        reduced motion.
    -   Inspect the browser console and network requests.
    -   Confirm no placeholder links, fabricated testimonials, or
        unsupported claims remain.
8.  **Report back**
    -   Summarize the sections implemented.
    -   List any missing assets or decisions.
    -   State which commands and checks were run and their results.
    -   Call out any integrations that remain unwired.

------------------------------------------------------------------------

## 16. Definition of done

The landing page is ready when:

-   [ ] The visual direction matches the premium editorial reference.
-   [ ] Purple is absent from the color system and visual effects.
-   [ ] Serif display typography is paired with readable sans-serif UI
    typography.
-   [ ] All specified sections exist and have consistent spacing.
-   [ ] The hero dashboard looks like a coherent product interface.
-   [ ] Desktop, tablet, and mobile layouts work without horizontal
    overflow.
-   [ ] The brand search behaves correctly or has a clear, intentional
    demo state.
-   [ ] All navigation and CTA links have valid destinations.
-   [ ] Animations are subtle and respect reduced-motion preferences.
-   [ ] Keyboard access, focus states, contrast, and semantic structure
    are checked.
-   [ ] Images are optimized and do not cause layout shifts.
-   [ ] No fake testimonials, customer endorsements, user counts, or
    live-data claims remain.
-   [ ] Linting, type checking, and available tests pass, or any
    failures are documented.

------------------------------------------------------------------------

## 17. Final instruction to the coding agent

Prioritize fidelity, spacing, typography, and the quality of the
dashboard mockup over adding more visual effects. Build a landing page
that feels art-directed and credible, not like a generic template.
Inspect the existing repository first, reuse working code, and make the
smallest set of changes needed to deliver the design.
