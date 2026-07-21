import type { Intent } from "@/common/libs/intent";
import { SITES } from "@/common/constants/commands";
import { speak } from "@/common/libs/tts";
import type { Locale } from "@/i18n/routing";

/**
 * Automation service: executes a parsed Intent in the browser and speaks a
 * short confirmation. This is the layer that actually performs actions, kept
 * free of React so the voice UI stays thin. All actions are browser safe.
 */
export interface ActionResult {
  ok: boolean;
  message: string;
}

export function executeIntent(intent: Intent, locale: Locale): ActionResult {
  const isID = locale === "id";
  const lang = isID ? "id-ID" : "en-US";

  const done = (message: string, ok = true): ActionResult => {
    speak(message, lang);
    return { ok, message };
  };

  const openSearch = (query: string) =>
    window.open(`https://www.google.com/search?q=${encodeURIComponent(query)}`, "_blank");

  switch (intent.action) {
    case "open_site": {
      const key = intent.arg.toLowerCase().replace(/\s+/g, "");
      const url = SITES[key] ?? (key.includes(".") ? `https://${key}` : null);
      if (url) {
        window.open(url, "_blank");
        return done(isID ? `Membuka ${intent.arg}` : `Opening ${intent.arg}`);
      }
      openSearch(intent.arg);
      return done(
        isID ? `Situs tidak dikenal, mencari ${intent.arg}` : `Unknown site, searching ${intent.arg}`,
      );
    }

    case "search": {
      if (!intent.arg) {
        return done(isID ? "Mau cari apa?" : "What should I search for?", false);
      }
      openSearch(intent.arg);
      return done(isID ? `Mencari ${intent.arg}` : `Searching ${intent.arg}`);
    }

    case "time": {
      const now = new Date().toLocaleTimeString(lang, { hour: "2-digit", minute: "2-digit" });
      return done(isID ? `Sekarang pukul ${now}` : `It is ${now}`);
    }

    case "date": {
      const today = new Date().toLocaleDateString(lang, {
        weekday: "long",
        day: "numeric",
        month: "long",
        year: "numeric",
      });
      return done(isID ? `Hari ini ${today}` : `Today is ${today}`);
    }

    case "scroll_down": {
      window.scrollBy({ top: window.innerHeight * 0.8, behavior: "smooth" });
      return done(isID ? "Menggulir ke bawah" : "Scrolling down");
    }

    case "scroll_up": {
      window.scrollBy({ top: -window.innerHeight * 0.8, behavior: "smooth" });
      return done(isID ? "Menggulir ke atas" : "Scrolling up");
    }

    case "toggle_theme": {
      const root = document.documentElement;
      root.classList.toggle("dark");
      const dark = root.classList.contains("dark");
      if (isID) return done(dark ? "Mode gelap aktif" : "Mode terang aktif");
      return done(dark ? "Dark mode on" : "Light mode on");
    }

    case "reload": {
      const message = isID ? "Memuat ulang" : "Reloading";
      speak(message, lang);
      window.setTimeout(() => window.location.reload(), 500);
      return { ok: true, message };
    }

    case "back": {
      const message = isID ? "Kembali" : "Going back";
      speak(message, lang);
      window.history.back();
      return { ok: true, message };
    }

    case "help": {
      return done(
        isID
          ? "Coba ucapkan: buka youtube, cari resep nasi goreng, jam berapa, mode gelap, gulir bawah."
          : "Try saying: open youtube, search cake recipe, what time, dark mode, scroll down.",
      );
    }

    default:
      return done(
        isID ? `Perintah tidak dikenali: ${intent.raw}` : `Command not recognized: ${intent.raw}`,
        false,
      );
  }
}
