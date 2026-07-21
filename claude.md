# Project: Sistem Otomasi Suara

A voice controlled automation system. The user speaks a command, the system
recognizes it, runs the action in the browser, and speaks a confirmation back.
Voice is the only input. There is no dashboard.

> HISTORY: An earlier spec (from another assistant) built this as a native
> Rust/Go/C++ "voice OS" and prohibited TypeScript. A later attempt misread a
> reference screenshot and built a personal portfolio blog. Both were wrong.
> The real project is this: a voice automation system using the Next.js App
> Router folder structure with TypeScript.

## Stack

- **Framework:** Next.js (App Router)
- **Language:** TypeScript (strict)
- **Voice input:** Web Speech API (SpeechRecognition), client side
- **Voice output:** SpeechSynthesis (text to speech)
- **Styling:** Tailwind CSS (class based dark mode)
- **i18n:** next-intl, locales `id` (default) and `en`

## Directory structure

```
app/                    Next.js App Router
  [locale]/             locale segmented routes (id, en)
    layout.tsx          minimal shell, builds metadata, language switch
    page.tsx            the single voice page
  layout.tsx            root layout
  globals.css
common/
  constants/
    metadata.ts         site metadata (source of truth)
    commands.ts         voice command vocabulary (keywords -> action)
  libs/
    intent.ts           transcript -> Intent parser
    tts.ts              speak() helper (SpeechSynthesis)
hooks/
  useSpeechRecognition.ts  Web Speech API hook (continuous, auto restart)
i18n/                   next-intl routing + request config
messages/               id.json, en.json
modules/
  voice/components/     VoiceControl (mic UI), TranscriptLog
services/
  automation.ts         executeIntent: runs the action, speaks a reply
speech-recognition.d.ts ambient types for the Web Speech API
middleware.ts           next-intl locale middleware
```

## Data flow

```
mic -> useSpeechRecognition -> parseIntent -> executeIntent -> speak reply
```

## Conventions

- **Voice only.** The UI is a microphone button plus a command log. Do not add a
  dashboard or forms.
- **Adding a command** is two edits: a keyword row in
  `common/constants/commands.ts` and a `case` in `services/automation.ts`.
- **No hardcoded UI strings.** Add keys to `messages/{id,en}.json` and read them
  with next-intl.
- **`services/`** holds the action logic and has no React.
- **Actions must be browser safe** (open site, search, scroll, theme, reload).

## Commands

```sh
npm install
npm run dev        # local development
npm run build      # production build
npm run start      # serve production build
npm run lint       # eslint
```

Note: Bun is not installed on the current machine, so use npm. A Chromium based
browser (Chrome or Edge) is recommended for Web Speech API support.
