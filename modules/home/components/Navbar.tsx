import { useTranslations } from "next-intl";
import { Link } from "@/i18n/routing";

export function Navbar() {
  const t = useTranslations("nav");
  return (
    <header className="border-b border-black/10 dark:border-white/10">
      <nav className="mx-auto flex max-w-3xl items-center justify-between px-4 py-4">
        <Link href="/" className="font-bold">
          damta
        </Link>
        <ul className="flex gap-6 text-sm">
          <li>
            <Link href="/">{t("home")}</Link>
          </li>
          <li>
            <Link href="/blog">{t("blog")}</Link>
          </li>
        </ul>
      </nav>
    </header>
  );
}
