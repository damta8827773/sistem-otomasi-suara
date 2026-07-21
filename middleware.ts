import createMiddleware from "next-intl/middleware";
import { routing } from "./i18n/routing";

// next-intl locale middleware: detects the locale (URL prefix, cookie, or
// Accept-Language) and rewrites requests to the correct [locale] segment.
export default createMiddleware(routing);

export const config = {
  // Match all pathnames except API routes, Next internals, and static files.
  matcher: ["/((?!api|_next|_vercel|.*\\..*).*)"],
};
