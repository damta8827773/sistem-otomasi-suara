<div align="center">

# damtaweb.com

Personal website, portfolio, and blog of **Damta Noviyan Muhamad Faiz**.

[![Next.js](https://img.shields.io/badge/Next.js-14-black?logo=next.js)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-strict-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3-38BDF8?logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![next-intl](https://img.shields.io/badge/i18n-next--intl-orange)](https://next-intl.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>

## Overview

A fast, modern personal site built on the Next.js App Router. It ships with a
bilingual interface (Indonesian and English), an MDX powered blog, and a
lightweight comment system. The codebase is organized by feature so it stays
easy to read, extend, and reuse.

Use it as a starting point for your own portfolio, or explore the structure to
see one clean way to wire up i18n, MDX, and a service layer in Next.js.

## Features

- **App Router** with locale segmented routes (`/`, `/en`, `/blog/...`).
- **Bilingual** out of the box with next-intl (default `id`, plus `en`).
- **MDX blog** with frontmatter, loaded through a small server side helper.
- **Comment system** with a client component, a toast hook, and an API route.
- **TypeScript strict** across the whole project.
- **Tailwind CSS** with light and dark mode support.
- **Feature first structure**: thin routes, UI in `modules`, data in `services`.

## Tech stack

| Area           | Choice                     |
| :------------- | :------------------------- |
| Framework      | Next.js 14 (App Router)    |
| Language       | TypeScript (strict)        |
| Styling        | Tailwind CSS               |
| Content        | MDX + gray-matter          |
| i18n           | next-intl                  |
| Package manager| Bun (npm also works)       |

## Getting started

Requirements: Node 18 or newer. Bun is recommended but optional.

```sh
# 1. Install dependencies
bun install          # or: npm install

# 2. Configure environment
cp .env.example .env  # then set DOMAIN

# 3. Run the dev server
bun run dev          # or: npm run dev
```

Open http://localhost:3000 in your browser.

### Scripts

| Command         | What it does           |
| :-------------- | :--------------------- |
| `bun run dev`   | Start the dev server   |
| `bun run build` | Create a production build |
| `bun run start` | Serve the production build |
| `bun run lint`  | Run ESLint             |

## Project structure

```
app/                    Next.js App Router
  [locale]/             locale segmented routes (id, en)
    layout.tsx          main layout, builds metadata
    page.tsx            home
    blog/               blog list and [slug] post pages
  api/comments/         comment API route
  layout.tsx            root layout
  globals.css
common/
  constants/metadata.ts site metadata, the single source of truth
  libs/mdx.ts           MDX loader with frontmatter parsing
contents/blog/          .mdx blog posts
hooks/useNotif.ts       toast and notification hook
i18n/                   next-intl routing and request config
messages/               id.json and en.json translation catalogs
modules/                feature UI (home, blog, comment)
public/                 static assets, for example images/damta.jpg
services/               data access layer (comment.ts)
middleware.ts           next-intl locale middleware
```

## Writing a blog post

Create a new `.mdx` file inside `contents/blog` with frontmatter:

```mdx
---
title: "My first post"
date: "2026-07-21"
summary: "A short description shown in the blog list."
lang: "id"
tags: ["personal"]
---

Write your content here in Markdown or MDX.
```

The post appears automatically on the blog page, sorted by date.

## Internationalization

UI strings live in `messages/id.json` and `messages/en.json`. Never hardcode
text in components. Add a key to both catalogs and read it with the `next-intl`
hooks. The active locale is detected by the middleware and reflected in the URL.

## Deployment

The project deploys cleanly to any platform that supports Next.js. The fastest
path is Vercel:

1. Push this repository to GitHub.
2. Import it on Vercel.
3. Set the `DOMAIN` environment variable.
4. Deploy.

## Notes

- The comment store in `app/api/comments/route.ts` is in memory for local
  development. Connect a real database before going to production.
- Add your photo at `public/images/damta.jpg`, referenced by `metadata.profile`.

## License

Released under the MIT License. See [LICENSE](LICENSE) for details.

## Author

**Damta Noviyan Muhamad Faiz**
GitHub: [@damta8827773](https://github.com/damta8827773)
