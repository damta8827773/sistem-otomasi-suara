/**
 * Site metadata, the single source of truth for identity and Open Graph data.
 * Consumed by app/[locale]/layout.tsx to build the Next.js Metadata object.
 */
export const METADATA = {
  creator: "Damta Noviyan Muhamad Faiz",
  description:
    "Sistem otomasi yang dikendalikan sepenuhnya lewat perintah suara, dibangun dengan Next.js dan TypeScript.",
  keyword: "sistem otomasi, kontrol suara, voice command, otomasi suara, damta",
  authors: {
    name: "Damta Noviyan Muhamad Faiz",
    url: process.env.DOMAIN,
  },
  openGraph: {
    url: process.env.DOMAIN,
    siteName: "Sistem Otomasi Suara",
    locale: "id-ID",
  },
  exTitle: "| Sistem Otomasi Suara",
  profile: "/images/damta.jpg",
} as const;
