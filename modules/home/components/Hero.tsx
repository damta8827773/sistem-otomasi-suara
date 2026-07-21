import { useTranslations } from "next-intl";
import { Link } from "@/i18n/routing";

export function Hero() {
  const t = useTranslations("home");
  return (
    <section className="py-12">
      <h1 className="text-4xl font-bold tracking-tight">{t("greeting")}</h1>
      <p className="mt-4 text-lg text-black/70 dark:text-white/70">{t("tagline")}</p>
      <Link
        href="/blog"
        className="mt-8 inline-block rounded-md border border-black/20 px-4 py-2 text-sm font-medium hover:bg-black/5 dark:border-white/20 dark:hover:bg-white/5"
      >
        {t("readBlog")} →
      </Link>
    </section>
  );
}
