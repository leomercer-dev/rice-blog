# Building a Static Site From Scratch — No Frameworks, No Compromise

Every framework I've used for static sites has felt like putting a suit on a ghost. They generate the right HTML but miss what makes a site feel alive: the spacing between lines, the way color choices shape mood, the feeling of reading something that was written by someone who actually cares about it.

So I built my own. No React, no Next.js, no Tailwind CDN, no analytics scripts, no Google Fonts, no framework bloat. Just HTML, CSS, and JavaScript — the same three technologies the web was built on in 1995.

## Why This Matters

This isn't about Luddism or performance punk aesthetics. It's about **control**. Every dependency I don't install is a potential break point, a security vulnerability, a tracking pixel, a loading cost. When your site is three files and you wrote every line of CSS yourself, you know exactly what it does and why.

## The Stack (Yes, This Is A Stack)

- **HTML** — The content. Semantically structured. No div soup.
- **CSS** — Custom properties for theming, CSS Grid for layout, `clamp()` for responsive typography, custom scrollbar styling. Every animation is a `transition` on an existing property. No keyframe spam.
- **JavaScript** — 200 lines total. Mobile menu toggle, lightbox for image galleries, back-to-top button, theme toggle with localStorage persistence. That's it.
- **Python + Jinja2** — Build system. Templates handle the repeated structure (headers, footers, navigation), data lives in YAML files so I can add new rices without touching HTML.
- **GitHub Pages** — Hosting. Custom domain, free HTTPS via Let's Encrypt, automatic CDN delivery. The infrastructure of a Fortune 500 site for $0/month.

## Design Decisions

### Dark by Default
This is a site about desktop customization. Dark mode isn't an option here — it's the default state. Light mode exists as a toggle (CSS class swap on `<html>`, persisted in localStorage). The entire palette comes from Catppuccin Mocha Mauve because that's what I'm using on my screen right now, and consistency matters more than neutrality.

### No External Dependencies
No Google Fonts (JetBrains Mono is already installed on this machine, the browser falls back to local), no CDN-hosted libraries, no analytics trackers. If it loads from somewhere else, it doesn't exist in my site.

### Performance Targets
- First contentful paint under 0.8s on a typical connection
- Total page weight under 200KB (excluding screenshots)
- Lighthouse score of 95+ on all metrics — not because I care about the badge, but because those numbers correlate with things that actually matter: no render-blocking resources, optimized images, minimal JavaScript

## What's Next

This is version 0.1. The architecture supports adding RSS feeds (client-side XML generation via GitHub Actions), a comment system via Giscus (GitHub Discussions-based, zero server needed), search (Lunr.js client-side indexing), and expanding the rice documentation to include dotfile repositories. But all of that comes after the foundation is solid.

The code for this site lives in `~/.hermes/cache/delegation/rice-blog/`. I'll push it to GitHub when I'm done iterating.

## TL;DR

Static sites don't need static-site generators. They need a designer with taste and someone who knows how HTML works. This is proof of that.
