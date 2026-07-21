"use client";

import { useCallback, useEffect, useRef, useState } from "react";

/**
 * React wrapper around the browser Web Speech API (SpeechRecognition).
 *
 * Voice is the only input for this system, so recognition runs in `continuous`
 * mode and automatically restarts when the engine ends a segment (for example
 * after a pause) as long as the user has not pressed stop.
 */
export interface UseSpeechRecognitionOptions {
  /** BCP-47 language tag, for example "id-ID" or "en-US". */
  lang?: string;
  /** Called with each finalized (non-interim) transcript. */
  onFinal?: (transcript: string) => void;
}

export interface SpeechRecognitionState {
  supported: boolean;
  listening: boolean;
  interim: string;
  error: string | null;
  start: () => void;
  stop: () => void;
}

export function useSpeechRecognition(
  options: UseSpeechRecognitionOptions = {},
): SpeechRecognitionState {
  const { lang = "id-ID", onFinal } = options;

  const [supported, setSupported] = useState(false);
  const [listening, setListening] = useState(false);
  const [interim, setInterim] = useState("");
  const [error, setError] = useState<string | null>(null);

  const recognitionRef = useRef<SpeechRecognition | null>(null);
  const wantListeningRef = useRef(false);
  const onFinalRef = useRef(onFinal);
  onFinalRef.current = onFinal;

  useEffect(() => {
    if (typeof window === "undefined") return;

    const Ctor = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!Ctor) {
      setSupported(false);
      return;
    }
    setSupported(true);

    const recognition = new Ctor();
    recognition.lang = lang;
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.maxAlternatives = 1;

    recognition.onresult = (event) => {
      let interimText = "";
      for (let i = event.resultIndex; i < event.results.length; i += 1) {
        const result = event.results[i];
        const text = result[0].transcript;
        if (result.isFinal) {
          const final = text.trim();
          if (final) onFinalRef.current?.(final);
        } else {
          interimText += text;
        }
      }
      setInterim(interimText);
    };

    recognition.onerror = (event) => {
      // "no-speech" and "aborted" are routine; surface everything else.
      if (event.error !== "no-speech" && event.error !== "aborted") {
        setError(event.error);
      }
    };

    recognition.onend = () => {
      // Auto-restart to keep a hands-free, voice-only experience.
      if (wantListeningRef.current) {
        try {
          recognition.start();
        } catch {
          setListening(false);
        }
      } else {
        setListening(false);
      }
    };

    recognitionRef.current = recognition;

    return () => {
      wantListeningRef.current = false;
      recognition.onresult = null;
      recognition.onerror = null;
      recognition.onend = null;
      try {
        recognition.abort();
      } catch {
        /* ignore */
      }
    };
  }, [lang]);

  const start = useCallback(() => {
    setError(null);
    wantListeningRef.current = true;
    try {
      recognitionRef.current?.start();
      setListening(true);
    } catch {
      // start() throws if already started; ignore.
    }
  }, []);

  const stop = useCallback(() => {
    wantListeningRef.current = false;
    setInterim("");
    try {
      recognitionRef.current?.stop();
    } catch {
      /* ignore */
    }
    setListening(false);
  }, []);

  return { supported, listening, interim, error, start, stop };
}
