import type { Metadata } from "next";
import type { ReactNode } from "react";
import { notFound } from "next/navigation";
import { NextIntlClientProvider } from "next-intl";
import { getMessages, getTranslations, setRequestLocale } from "next-intl/server";
import { routing, Link } from "@/i18n/routing";
import { METADATA } from "@/common/constants/metadata";
import "../globals.css";

// Pre-render both locales at build time.
export function generateStaticParams() {
  return routing.locales.map((locale) => ({ locale }));
}

// Build the Next.js Metadata object from the single source of truth.
export const metadata: Metadata = {
  title: {
    default: METADATA.openGraph.siteName,
    template: `%s ${METADATA.exTitle}`,
  },
  description: METADATA.description,
  keywords: METADATA.keyword,
  creator: METADATA.creator,
  authors: [{ name: METADATA.authors.name, url: METADATA.authors.url }],
  metadataBase: METADATA.openGraph.url ? new URL(METADATA.openGraph.url) : undefined,
  openGraph: {
    url: METADATA.openGraph.url,
    siteName: METADATA.openGraph.siteName,
    locale: METADATA.openGraph.locale,
    type: "website",
  },
};

export default async function LocaleLayout({
  children,
  params,
}: {
  children: ReactNode;
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;

  if (!routing.locales.includes(locale as (typeof routing.locales)[number])) {
    notFound();
  }

  setRequestLocale(locale);
  const messages = await getMessages();
  const t = await getTranslations("app");

  return (
    <html lang={locale}>
      <body className="min-h-screen flex flex-col font-sans antialiased">
        <NextIntlClientProvider messages={messages}>
          <header className="border-b border-black/10 dark:border-white/10">
            <div className="mx-auto flex max-w-2xl items-center justify-between px-4 py-4">
              <span className="text-sm font-semibold">{t("name")}</span>
              <div className="flex gap-3 text-xs text-black/60 dark:text-white/60">
                <Link href="/" locale="id">
                  ID
                </Link>
                <Link href="/" locale="en">
                  EN
                </Link>
              </div>
            </div>
          </header>
          <main className="flex-1 mx-auto w-full max-w-2xl px-4 py-10">{children}</main>
        </NextIntlClientProvider>
      </body>
    </html>
  );
}
