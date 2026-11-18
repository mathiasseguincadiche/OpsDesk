import { useSyncExternalStore } from "react";

/** Single source of truth: the `dark` class on <html>, observed by every component. */
const isDark = () => document.documentElement.classList.contains("dark");

function subscribe(callback: () => void) {
  const observer = new MutationObserver(callback);
  observer.observe(document.documentElement, { attributes: true, attributeFilter: ["class"] });
  return () => observer.disconnect();
}

export function setTheme(dark: boolean) {
  document.documentElement.classList.toggle("dark", dark);
  try { localStorage.setItem("opsdesk-theme", dark ? "dark" : "light"); } catch { /* storage unavailable */ }
}

export function useTheme() {
  const dark = useSyncExternalStore(subscribe, isDark);
  return { dark, toggle: () => setTheme(!isDark()) };
}
