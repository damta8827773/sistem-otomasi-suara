import { getTranslations, setRequestLocale } from "next-intl/server";
import { VoiceControl } from "@/modules/voice/components/VoiceControl";

export default async function HomePage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  setRequestLocale(locale);
  const t = await getTranslations("home");

  return (
    <section className="flex flex-col items-center gap-4 py-8 text-center">
      <h1 className="text-3xl font-bold tracking-tight">{t("title")}</h1>
      <p className="max-w-md text-black/60 dark:text-white/60">{t("subtitle")}</p>
      <div className="mt-6 w-full">
        <VoiceControl />
      </div>
    </section>
  );
}
