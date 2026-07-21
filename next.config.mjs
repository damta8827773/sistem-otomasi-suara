import createMDX from "@next/mdx";
import createNextIntlPlugin from "next-intl/plugin";

// next-intl reads its config from i18n/request.ts.
const withNextIntl = createNextIntlPlugin("./i18n/request.ts");

// MDX support so .mdx files can be used both as content and as routes.
const withMDX = createMDX({
  options: {
    remarkPlugins: [],
    rehypePlugins: [],
  },
});

/** @type {import('next').NextConfig} */
const nextConfig = {
  pageExtensions: ["ts", "tsx", "mdx"],
  reactStrictMode: true,
  images: {
    remotePatterns: [],
  },
};

export default withNextIntl(withMDX(nextConfig));
