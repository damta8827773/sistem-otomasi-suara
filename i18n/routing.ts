import { defineRouting } from "next-intl/routing";
import { createNavigation } from "next-intl/navigation";

/**
 * Locale routing config. `id` (Bahasa Indonesia) is the default and is not
 * prefixed in the URL; `en` is served under /en.
 */
export const routing = defineRouting({
  locales: ["id", "en"],
  defaultLocale: "id",
  localePrefix: "as-needed",
});

export type Locale = (typeof routing.locales)[number];

// Locale-aware navigation helpers — import these instead of next/link &
// next/navigation so links keep the active locale automatically.
export const { Link, redirect, usePathname, useRouter, getPathname } =
  createNavigation(routing);
