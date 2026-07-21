import type { ReactNode } from "react";

// Root layout is intentionally minimal: the real <html>/<body> and providers
// live in app/[locale]/layout.tsx so they can be locale-aware. This wrapper
// exists only to satisfy the App Router's root-layout requirement.
export default function RootLayout({ children }: { children: ReactNode }) {
  return children;
}
