import { useTranslations } from "next-intl";
import { METADATA } from "@/common/constants/metadata";

export function Footer() {
  const t = useTranslations("footer");
  const year = new Date().getFullYear();
  return (
    <footer className="border-t border-black/10 dark:border-white/10">
      <div className="mx-auto max-w-3xl px-4 py-6 text-sm text-black/60 dark:text-white/60">
        © {year} {METADATA.creator}. {t("rights")}
      </div>
    </footer>
  );
}
