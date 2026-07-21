/**
 * Site metadata — single source of truth for identity & Open Graph data.
 * Consumed by app/[locale]/layout.tsx to build the Next.js Metadata object.
 */
export const METADATA = {
  creator: "Damta Noviyan Muhamad Faiz",
  description: "Personal website, portfolio, blog",
  keyword: "damta, damta noviyan muhamad faiz",
  authors: {
    name: "Damta Noviyan Muhamad Faiz",
    url: process.env.DOMAIN,
  },
  openGraph: {
    url: process.env.DOMAIN,
    siteName: "Damta Noviyan Muhamad Faiz",
    locale: "id-ID",
  },
  exTitle: "| Damta Noviyan Muhamad Faiz",
  profile: "/images/damta.jpg",
} as const;
