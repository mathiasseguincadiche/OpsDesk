import { format, formatDistanceToNowStrict } from "date-fns";
import { fr } from "date-fns/locale";

export const fromNow = (iso: string) => formatDistanceToNowStrict(new Date(iso), { addSuffix: true, locale: fr });
export const fullDate = (iso: string) => format(new Date(iso), "d MMM yyyy 'à' HH:mm", { locale: fr });
export const shortDay = (iso: string) => format(new Date(iso), "d MMM", { locale: fr });

export const initials = (name: string) =>
  name.split(/\s+/).filter(Boolean).slice(0, 2).map((p) => p[0]!.toUpperCase()).join("");

export function hours(value: number | null) {
  if (value === null) return "—";
  if (value < 1) return `${Math.round(value * 60)} min`;
  if (value < 48) return `${value.toFixed(1).replace(".", ",")} h`;
  return `${(value / 24).toFixed(1).replace(".", ",")} j`;
}
