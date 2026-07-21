/**
 * Text-to-speech helper using the browser SpeechSynthesis API. The system
 * speaks its response so it can be used entirely hands-free.
 */
export function speak(text: string, lang = "id-ID"): void {
  if (typeof window === "undefined" || !("speechSynthesis" in window)) return;

  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = lang;
  utterance.rate = 1;

  // Cancel any in-flight speech so responses do not overlap.
  window.speechSynthesis.cancel();
  window.speechSynthesis.speak(utterance);
}
