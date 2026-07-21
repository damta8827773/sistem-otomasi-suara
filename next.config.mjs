import createNextIntlPlugin from "next-intl/plugin";

// next-intl reads its config from i18n/request.ts.
const withNextIntl = createNextIntlPlugin("./i18n/request.ts");

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
};

export default withNextIntl(nextConfig);
