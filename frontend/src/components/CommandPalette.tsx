import { useQuery } from "@tanstack/react-query";
import { clsx } from "clsx";
import { CornerDownLeft, LayoutDashboard, Moon, Plus, Search, Ticket, UserCircle, UserRoundCheck, Users } from "lucide-react";
import { useEffect, useMemo, useRef, useState, type KeyboardEvent, type ReactNode } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { setTheme } from "@/lib/theme";
import type { TicketPage } from "@/lib/types";
import { PriorityIcon, StatusIcon } from "./ui";

interface Item {
  id: string;
  group: string;
  label: string;
  icon: ReactNode;
  hint?: ReactNode;
  run: () => void;
}

export function CommandPalette({ open, onClose, onNewTicket }: { open: boolean; onClose: () => void; onNewTicket: () => void }) {
  const [query, setQuery] = useState("");
  const [debounced, setDebounced] = useState("");
  const [active, setActive] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);
  const listRef = useRef<HTMLDivElement>(null);
  const navigate = useNavigate();
  const { isStaff, isAdmin } = useAuth();

  useEffect(() => {
    if (open) {
      setQuery("");
      setDebounced("");
      setActive(0);
      setTimeout(() => inputRef.current?.focus(), 0);
    }
  }, [open]);

  useEffect(() => {
    const id = setTimeout(() => setDebounced(query.trim()), 180);
    return () => clearTimeout(id);
  }, [query]);

  const { data, isFetching } = useQuery({
    queryKey: ["tickets", "palette", debounced],
    queryFn: () => api<TicketPage>("/api/tickets", { query: { q: debounced || undefined, page_size: 6, sort: "updated" } }),
    enabled: open,
  });

  const go = (to: string) => () => { onClose(); navigate(to); };
  const toggleTheme = () => {
    setTheme(!document.documentElement.classList.contains("dark"));
    onClose();
  };

  const items = useMemo<Item[]>(() => {
    const q = query.trim().toLowerCase();
    const actions: Item[] = [
      { id: "new", group: "Actions", label: "Créer un ticket", icon: <Plus className="size-4" />, run: onNewTicket },
      { id: "dash", group: "Navigation", label: "Tableau de bord", icon: <LayoutDashboard className="size-4" />, run: go("/") },
      { id: "tickets", group: "Navigation", label: isStaff ? "Tous les tickets" : "Mes demandes", icon: <Ticket className="size-4" />, run: go("/tickets") },
      ...(isStaff ? [{ id: "mine", group: "Navigation", label: "Assignés à moi", icon: <UserRoundCheck className="size-4" />, run: go("/tickets?assignee=me") }] : []),
      ...(isAdmin ? [{ id: "users", group: "Navigation", label: "Utilisateurs", icon: <Users className="size-4" />, run: go("/users") }] : []),
      { id: "profile", group: "Navigation", label: "Mon profil", icon: <UserCircle className="size-4" />, run: go("/profile") },
      { id: "theme", group: "Actions", label: "Basculer le thème clair / sombre", icon: <Moon className="size-4" />, run: toggleTheme },
    ].filter((a) => !q || a.label.toLowerCase().includes(q));
    const tickets: Item[] = (data?.items ?? []).map((t) => ({
      id: `t${t.id}`,
      group: debounced ? "Tickets" : "Tickets récents",
      label: t.title,
      icon: <StatusIcon status={t.status} />,
      hint: (
        <span className="flex items-center gap-2">
          <PriorityIcon priority={t.priority} />
          <span className="font-mono text-[11px] text-faint">#{t.id}</span>
        </span>
      ),
      run: go(`/tickets/${t.id}`),
    }));
    return q ? [...tickets, ...actions] : [...actions.filter((a) => a.group === "Actions"), ...tickets, ...actions.filter((a) => a.group === "Navigation")];
  }, [query, debounced, data, isStaff, isAdmin]);

  useEffect(() => setActive(0), [query]);
  useEffect(() => {
    listRef.current?.querySelector(`[data-index="${active}"]`)?.scrollIntoView({ block: "nearest" });
  }, [active]);

  if (!open) return null;

  const onKeyDown = (e: KeyboardEvent) => {
    if (e.key === "Escape") onClose();
    else if (e.key === "ArrowDown") { e.preventDefault(); setActive((a) => Math.min(items.length - 1, a + 1)); }
    else if (e.key === "ArrowUp") { e.preventDefault(); setActive((a) => Math.max(0, a - 1)); }
    else if (e.key === "Enter") { e.preventDefault(); items[active]?.run(); }
  };

  let lastGroup = "";
  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center p-4 pt-[12vh]" role="dialog" aria-modal="true" aria-label="Palette de commandes">
      <div className="animate-fade-in absolute inset-0 bg-slate-950/40 backdrop-blur-[2px]" onClick={onClose} />
      <div className="animate-pop-in relative w-full max-w-xl overflow-hidden rounded-2xl border border-line bg-surface shadow-pop" onKeyDown={onKeyDown}>
        <div className="flex items-center gap-3 border-b border-line px-4">
          <Search className={clsx("size-4 shrink-0", isFetching ? "animate-pulse text-brand-500" : "text-faint")} />
          <input
            ref={inputRef}
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Rechercher un ticket, une page, une action…"
            className="h-12 flex-1 bg-transparent text-[15px] outline-none placeholder:text-faint"
          />
          <span className="kbd">Échap</span>
        </div>
        <div ref={listRef} className="max-h-[50vh] overflow-y-auto p-1.5">
          {items.length === 0 && <p className="px-3 py-10 text-center text-sm text-muted">Aucun résultat pour « {query} »</p>}
          {items.map((item, index) => {
            const header = item.group !== lastGroup ? item.group : null;
            lastGroup = item.group;
            return (
              <div key={item.id}>
                {header && <p className="px-2.5 pb-1 pt-2.5 text-[11px] font-medium uppercase tracking-wider text-faint">{header}</p>}
                <button
                  data-index={index}
                  onMouseMove={() => setActive(index)}
                  onClick={item.run}
                  className={clsx("flex w-full items-center gap-3 rounded-lg px-2.5 py-2 text-left text-sm", index === active ? "bg-hover text-ink" : "text-ink-2")}
                >
                  <span className="text-muted">{item.icon}</span>
                  <span className="flex-1 truncate">{item.label}</span>
                  {item.hint}
                  {index === active && <CornerDownLeft className="size-3.5 text-faint" />}
                </button>
              </div>
            );
          })}
        </div>
        <div className="flex items-center gap-4 border-t border-line bg-surface-2 px-4 py-2 text-[11px] text-faint">
          <span className="flex items-center gap-1"><span className="kbd">↑</span><span className="kbd">↓</span> naviguer</span>
          <span className="flex items-center gap-1"><span className="kbd">↵</span> ouvrir</span>
        </div>
      </div>
    </div>
  );
}
