# Project: damtaweb.com

Personal website, portfolio, and blog for **Damta Noviyan Muhamad Faiz**.

> NOTE: An earlier version of this file (written by another assistant) badly
> misread the folder names below and invented a "voice-controlled OS" in
> Rust/Go/C++ — even prohibiting TypeScript. That was wrong. The folder names
> (`app`, `common/constants`, `common/libs`, `hooks`, `i18n`, `messages`,
> `modules`, `services`, `middleware`) are a standard **Next.js App Router**
> layout. This file now describes the real project.

## Stack

- **Framework:** Next.js (App Router)
- **Language:** TypeScript (strict)
- **Runtime / package manager:** Bun (`bun.lockb`)
- **Styling:** Tailwind CSS
- **Content:** MDX for blog posts / writing (`contents/`)
- **i18n:** `next-intl` — default locale `id-ID`, plus `en`
- **Lint:** ESLint (`.eslintrc.json`)

Explicitly a **web** project: HTML/CSS/TS/JSX are expected and required (the
opposite of the previous erroneous spec).

## Directory structure

```
damtaweb/
├── app/                      # Next.js App Router (routing + layouts)
│   ├── [locale]/             # locale-segmented routes (id, en)
│   │   ├── layout.tsx        # main layout, injects metadata
│   │   ├── page.tsx          # home
│   │   └── blog/             # blog list + [slug] post pages
│   ├── layout.tsx            # root layout (html/body)
│   └── globals.css
├── common/                   # shared, cross-feature code
│   ├── constants/
│   │   └── metadata.ts       # site metadata (creator, openGraph, etc.)
│   └── libs/
│       └── mdx.ts            # MDX loading/parsing helpers
├── contents/                 # MDX content (blog posts, writing)
├── hooks/                    # shared React hooks
│   └── useNotif.ts           # notification/toast hook
├── i18n/                     # next-intl configuration
│   ├── routing.ts            # locales + defaultLocale
│   └── request.ts            # per-request message loading
├── messages/                 # i18n translation catalogs
│   ├── id.json
│   └── en.json
├── modules/                  # feature modules (React components by feature)
│   ├── home/
│   ├── blog/
│   └── comment/              # comment system (Tanya/komentar)
├── public/                   # static assets (images: /images/damta.jpg)
├── services/                 # data/API service layer
├── .eslintrc.json
├── .gitignore
├── middleware.ts             # next-intl locale middleware
├── next.config.mjs           # Next + MDX + next-intl plugins
├── next-env.d.ts
├── package.json
├── tailwind.config.ts
└── tsconfig.json
```

## Conventions

- **Routing** lives only in `app/`; feature UI lives in `modules/<feature>` and
  is imported into the route files. Keep route files thin.
- **`services/`** holds data access (fetching posts, comments, etc.) — no React
  in this layer.
- **`common/`** is for genuinely shared things (metadata, MDX libs, utilities);
  don't put feature-specific code here.
- **i18n:** never hardcode UI strings — add keys to `messages/{id,en}.json` and
  read them via `next-intl`.
- **Content:** blog posts are `.mdx` files in `contents/`, loaded through
  `common/libs/mdx.ts`.

## Site metadata (source of truth)

`common/constants/metadata.ts`:

```ts
export const METADATA = {
  creator: "Damta Noviyan Muhamad Faiz",
  description: "Personal website, portfolio, blog",
  keyword: "damta, damta noviyan muhamad faiz",
  authors: { name: "Damta Noviyan Muhamad Faiz", url: process.env.DOMAIN },
  openGraph: {
    url: process.env.DOMAIN,
    siteName: "Damta Noviyan Muhamad Faiz",
    locale: "id-ID",
  },
  exTitle: "| Damta Noviyan Muhamad Faiz",
  profile: "/images/damta.jpg",
};
```

## Commands

```sh
bun install
bun run dev        # local development
bun run build      # production build
bun run start      # serve production build
bun run lint       # eslint
```
