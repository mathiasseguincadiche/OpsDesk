import type { Category, Priority, Role, Status } from "./types";

export const STATUS: Record<Status, { label: string; badge: string; dot: string; color: string }> = {
  open: { label: "Ouvert", badge: "bg-surface text-ink-2 ring-line-strong", dot: "bg-sky-500", color: "#3b82f6" },
  in_progress: { label: "En cours", badge: "bg-surface text-ink-2 ring-line-strong", dot: "bg-amber-500", color: "#f59e0b" },
  resolved: { label: "Résolu", badge: "bg-surface text-ink-2 ring-line-strong", dot: "bg-emerald-500", color: "#10b981" },
  closed: { label: "Clôturé", badge: "bg-surface text-ink-2 ring-line-strong", dot: "bg-slate-400", color: "#8b93a3" },
};

export const PRIORITY: Record<Priority, { label: string; badge: string; color: string; bars: number }> = {
  low: { label: "Basse", badge: "text-slate-500 dark:text-slate-400", color: "#94a3b8", bars: 1 },
  normal: { label: "Normale", badge: "text-sky-600 dark:text-sky-400", color: "#0ea5e9", bars: 2 },
  high: { label: "Haute", badge: "text-orange-600 dark:text-orange-400", color: "#f97316", bars: 3 },
  critical: { label: "Critique", badge: "text-rose-600 dark:text-rose-400", color: "#e11d48", bars: 4 },
};

export const CATEGORY: Record<Category, { label: string; color: string }> = {
  hardware: { label: "Matériel", color: "#6366f1" },
  software: { label: "Logiciel", color: "#8b5cf6" },
  network: { label: "Réseau", color: "#0ea5e9" },
  access: { label: "Accès & comptes", color: "#14b8a6" },
  other: { label: "Autre", color: "#94a3b8" },
};

export const ROLE: Record<Role, { label: string; badge: string }> = {
  user: { label: "Collaborateur", badge: "bg-surface text-ink-2 ring-line-strong" },
  agent: { label: "Support", badge: "bg-brand-50 text-brand-700 dark:bg-brand-500/15 dark:text-brand-300" },
  admin: { label: "Administrateur", badge: "bg-violet-50 text-violet-700 dark:bg-violet-500/15 dark:text-violet-300" },
};

export const TRANSITION_LABEL: Record<Status, string> = {
  open: "Rouvrir",
  in_progress: "Prendre en charge",
  resolved: "Marquer comme résolu",
  closed: "Clôturer",
};

export const statuses = Object.keys(STATUS) as Status[];
export const priorities = Object.keys(PRIORITY) as Priority[];
export const categories = Object.keys(CATEGORY) as Category[];
