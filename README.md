<div align="center">

# Sistem Otomasi Suara

A voice controlled automation system. Speak a command, and the system runs it.
No dashboard, no forms, just your voice.

[![Next.js](https://img.shields.io/badge/Next.js-14-black?logo=next.js)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-strict-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3-38BDF8?logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![Web Speech API](https://img.shields.io/badge/Web_Speech_API-voice-orange)](https://developer.mozilla.org/docs/Web/API/Web_Speech_API)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>

## Overview

Sistem Otomasi Suara turns spoken words into actions. It listens through the
microphone, recognizes what you said, matches it to a command, runs the action,
and speaks a short confirmation back. Everything runs in the browser using the
Web Speech API, so there is no server call for the voice itself.

The interface is deliberately minimal. There is one microphone button and a log
of what you said. Voice is the only input.

## How it works

```
microphone  ->  useSpeechRecognition  ->  parseIntent  ->  executeIntent  ->  spoken reply
   (voice)        (Web Speech API)         (intent.ts)      (automation.ts)     (speech)
```

1. **Listen**: `useSpeechRecognition` wraps the browser SpeechRecognition engine
   and streams your speech as text.
2. **Understand**: `parseIntent` matches the transcript against a command table.
3. **Act**: `executeIntent` performs the action in the browser.
4. **Reply**: the system speaks a confirmation with SpeechSynthesis.

## Voice commands

Works in Indonesian and English. A few examples:

| Say (ID)                | Say (EN)              | Action                          |
| :---------------------- | :-------------------- | :------------------------------ |
| `buka youtube`          | `open youtube`        | Open a known site or a website  |
| `cari resep nasi goreng`| `search cake recipe`  | Search the web                  |
| `jam berapa`            | `what time`           | Speak the current time          |
| `tanggal berapa`        | `what date`           | Speak today's date              |
| `mode gelap`            | `dark mode`           | Toggle dark and light theme     |
| `gulir bawah`           | `scroll down`         | Scroll the page                 |
| `muat ulang`            | `reload`              | Reload the page                 |
| `bantuan`               | `help`                | List available commands         |

Adding a command is a two step change: add a keyword row in
`common/constants/commands.ts` and a case in `services/automation.ts`.

## Getting started

Requirements: Node 18 or newer. A Chromium based browser (Chrome or Edge) is
recommended because it has the best Web Speech API support.

```sh
npm install
npm run dev        # http://localhost:3000
```

Open the site, press the microphone, allow microphone access, and start talking.

### Scripts

| Command         | What it does               |
| :-------------- | :------------------------- |
| `npm run dev`   | Start the dev server       |
| `npm run build` | Create a production build  |
| `npm run start` | Serve the production build |
| `npm run lint`  | Run ESLint                 |

## Project structure

```
app/                    Next.js App Router
  [locale]/             locale segmented routes (id, en)
    layout.tsx          minimal shell, builds metadata
    page.tsx            the voice page
  layout.tsx            root layout
  globals.css
common/
  constants/
    metadata.ts         site metadata
    commands.ts         voice command vocabulary
  libs/
    intent.ts           transcript to intent parser
    tts.ts              text to speech helper
hooks/
  useSpeechRecognition.ts  Web Speech API hook
i18n/                   next-intl routing and request config
messages/               id.json and en.json
modules/
  voice/components/     VoiceControl and TranscriptLog
services/
  automation.ts         runs the recognized action
speech-recognition.d.ts ambient types for the Web Speech API
middleware.ts           next-intl locale middleware
```

## Notes and limits

- The Web Speech API is a browser feature. Support is best on Chrome and Edge,
  and it needs an internet connection in some browsers.
- Popup blockers may stop `open` and `search` from opening a new tab until you
  allow popups for the site.
- Actions are limited to what a web page can safely do, such as opening sites,
  searching, scrolling, and switching theme.

## License

Released under the MIT License. See [LICENSE](LICENSE).

## Author

**Damta Noviyan Muhamad Faiz**
GitHub: [@damta8827773](https://github.com/damta8827773)
