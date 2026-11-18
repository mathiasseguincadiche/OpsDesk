import { useQuery } from "@tanstack/react-query";
import { clsx } from "clsx";
import {
  ChevronRight,
  Inbox,
  LayoutDashboard,
  LogOut,
  Menu,
  Moon,
  Plus,
  Search,
  Sun,
  Ticket,
  UserCircle,
  UserRoundCheck,
  Users,
  X,
} from "lucide-react";
import { Suspense, useEffect, useRef, useState, type ReactNode } from "react";
import { Link, NavLink, Outlet, useLocation } from "react-router-dom";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { useTheme } from "@/lib/theme";
import type { Stats } from "@/lib/types";
import { CommandPalette } from "./CommandPalette";
import { NewTicketModal } from "./NewTicketModal";
import { Avatar, Button, IconButton, PageSkeleton, RoleBadge } from "./ui";

export function Logo({ className, compact }: { className?: string; compact?: boolean }) {
  return (
    <div className={clsx("flex items-center gap-2.5", className)}>
      <img src="/favicon.svg" alt="" className="size-7 rounded-lg" />
      {!compact && <span className="text-[15px] font-semibold tracking-tight">OpsDesk</span>}
    </div>
  );
}

function useStats() {
  return useQuery({ queryKey: ["stats"], queryFn: () => api<Stats>("/api/stats"), refetchInterval: 30_000 });
}

function SystemStatus() {
  const { data, isError } = useQuery({
    queryKey: ["health"],
    queryFn: () => api<{ status: string; version: string; database: string }>("/health/ready"),
    refetchInterval: 30_000,
    retry: false,
  });
  const ok = !isError && data?.status === "ready";
  return (
    <div className="flex items-center gap-2 px-2 text-xs text-muted" title={ok ? "API et base de données opérationnelles" : "Service dégradé"}>
      <span className="relative flex size-2">
        {ok && <span className="absolute inline-flex size-full animate-ping rounded-full bg-emerald-400 opacity-60" />}
        <span className={clsx("relative inline-flex size-2 rounded-full", ok ? "bg-emerald-500" : data || isError ? "bg-rose-500" : "bg-faint")} />
      </span>
      <span>{ok ? "Systèmes opérationnels" : data || isError ? "Service dégradé" : "Vérification…"}</span>
      {data?.version && <span className="ml-auto font-mono text-[10px] text-faint">v{data.version}</span>}
    </div>
  );
}

interface NavItem {
  to: string;
  label: string;
  icon: typeof Inbox;
  end?: boolean;
  count?: number;
}

function NavSection({ title, items, onNavigate }: { title?: string; items: NavItem[]; onNavigate: () => void }) {
  const location = useLocation();
  return (
    <div>
      {title && <p className="mb-1 px-2.5 text-[11px] font-medium uppercase tracking-wider text-faint">{title}</p>}
      <div className="space-y-0.5">
        {items.map(({ to, label, icon: Icon, end, count }) => {
          // Links carrying a query string are only active on an exact match.
          const [path, query] = to.split("?");
          const active = query
            ? location.pathname === path && location.search === `?${query}`
            : end
              ? location.pathname === path
              : location.pathname.startsWith(path) && !(path === "/tickets" && location.search.includes("assignee=me"));
          return (
            <NavLink
              key={to}
              to={to}
              onClick={onNavigate}
              className={clsx(
                "group flex h-8 items-center gap-2.5 rounded-md px-2.5 text-[13px] font-medium transition-colors",
                active ? "bg-surface text-ink shadow-card ring-1 ring-line" : "text-muted hover:bg-hover hover:text-ink",
              )}
            >
              <Icon className={clsx("size-4", active ? "text-brand-600 dark:text-brand-400" : "text-faint group-hover:text-muted")} />
              <span className="flex-1">{label}</span>
              {count !== undefined && count > 0 && (
                <span className={clsx("num rounded px-1.5 text-[11px] font-medium", active ? "bg-brand-50 text-brand-700 dark:bg-brand-500/15 dark:text-brand-300" : "text-faint")}>
                  {count}
                </span>
              )}
            </NavLink>
          );
        })}
      </div>
    </div>
  );
}

function UserMenu() {
  const { user, logout } = useAuth();
  const { dark, toggle } = useTheme();
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (!open) return;
    const close = (e: MouseEvent) => !ref.current?.contains(e.target as Node) && setOpen(false);
    const esc = (e: KeyboardEvent) => e.key === "Escape" && setOpen(false);
    document.addEventListener("mousedown", close);
    document.addEventListener("keydown", esc);
    return () => {
      document.removeEventListener("mousedown", close);
      document.removeEventListener("keydown", esc);
    };
  }, [open]);

  return (
    <div ref={ref} className="relative">
      <button onClick={() => setOpen((o) => !o)} className="flex items-center gap-2 rounded-full p-0.5 pr-0.5 transition hover:ring-4 hover:ring-hover" aria-label="Menu du compte" aria-expanded={open}>
        <Avatar name={user!.full_name} size="md" />
      </button>
      {open && (
        <div className="animate-pop-in absolute right-0 z-50 mt-2 w-64 rounded-xl border border-line bg-surface p-1.5 shadow-pop">
          <div className="flex items-center gap-3 px-2.5 py-2.5">
            <Avatar name={user!.full_name} size="lg" />
            <div className="min-w-0">
              <p className="truncate text-sm font-semibold">{user!.full_name}</p>
              <p className="truncate text-xs text-muted">{user!.email}</p>
            </div>
          </div>
          <div className="px-2.5 pb-2"><RoleBadge role={user!.role} /></div>
          <div className="my-1 h-px bg-line" />
          <MenuItem to="/profile" icon={<UserCircle className="size-4" />} onClick={() => setOpen(false)}>Mon profil</MenuItem>
          <MenuItem icon={dark ? <Sun className="size-4" /> : <Moon className="size-4" />} onClick={toggle}>
            {dark ? "Thème clair" : "Thème sombre"}
          </MenuItem>
          <div className="my-1 h-px bg-line" />
          <MenuItem icon={<LogOut className="size-4" />} onClick={logout} danger>Se déconnecter</MenuItem>
        </div>
      )}
    </div>
  );
}

function MenuItem({ to, icon, children, onClick, danger }: { to?: string; icon: ReactNode; children: ReactNode; onClick?: () => void; danger?: boolean }) {
  const cls = clsx(
    "flex w-full items-center gap-2.5 rounded-lg px-2.5 py-2 text-left text-[13px] transition-colors",
    danger ? "text-rose-600 hover:bg-rose-50 dark:text-rose-400 dark:hover:bg-rose-500/10" : "text-ink-2 hover:bg-hover hover:text-ink",
  );
  return to ? <Link to={to} className={cls} onClick={onClick}>{icon}{children}</Link> : <button className={cls} onClick={onClick}>{icon}{children}</button>;
}

const CRUMBS: Record<string, string> = { "": "Tableau de bord", tickets: "Tickets", users: "Utilisateurs", profile: "Mon profil" };

function Breadcrumbs() {
  const { pathname } = useLocation();
  const parts = pathname.split("/").filter(Boolean);
  const items: { label: string; to?: string }[] = [{ label: CRUMBS[parts[0] ?? ""] ?? "Page", to: parts.length > 1 ? `/${parts[0]}` : undefined }];
  if (parts[0] === "tickets" && parts[1]) items.push({ label: `#${parts[1]}` });
  return (
    <nav aria-label="Fil d'Ariane" className="flex min-w-0 items-center gap-1.5 text-[13px]">
      <span className="text-faint">Support IT</span>
      {items.map((item, i) => (
        <span key={i} className="flex min-w-0 items-center gap-1.5">
          <ChevronRight className="size-3.5 shrink-0 text-faint" />
          {item.to ? (
            <Link to={item.to} className="truncate text-muted hover:text-ink">{item.label}</Link>
          ) : (
            <span className="truncate font-medium text-ink">{item.label}</span>
          )}
        </span>
      ))}
    </nav>
  );
}

export function Layout() {
  const { isAdmin, isStaff } = useAuth();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [creating, setCreating] = useState(false);
  const [paletteOpen, setPaletteOpen] = useState(false);
  const location = useLocation();
  const { data: stats } = useStats();

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        setPaletteOpen((o) => !o);
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  useEffect(() => setMobileOpen(false), [location.pathname]);

  const active = stats ? stats.by_status.open + stats.by_status.in_progress : undefined;
  const main: NavItem[] = [
    { to: "/", label: "Tableau de bord", icon: LayoutDashboard, end: true },
    { to: "/tickets", label: isStaff ? "Tous les tickets" : "Mes demandes", icon: Ticket, count: active },
    ...(isStaff ? [{ to: "/tickets?assignee=me", label: "Assignés à moi", icon: UserRoundCheck, count: stats?.assigned_to_me }] : []),
  ];
  const admin: NavItem[] = isAdmin ? [{ to: "/users", label: "Utilisateurs", icon: Users }] : [];

  const sidebar = (
    <div className="flex h-full flex-col">
      <div className="flex h-14 items-center justify-between px-4">
        <Link to="/"><Logo /></Link>
        <IconButton label="Fermer le menu" className="lg:hidden" onClick={() => setMobileOpen(false)}>
          <X className="size-4" />
        </IconButton>
      </div>
      <div className="space-y-2 px-3">
        <Button className="w-full" onClick={() => { setCreating(true); setMobileOpen(false); }}>
          <Plus className="size-4" /> Nouveau ticket
        </Button>
        <button
          onClick={() => { setPaletteOpen(true); setMobileOpen(false); }}
          className="flex h-8 w-full items-center gap-2 rounded-md border border-line bg-surface px-2.5 text-[13px] text-faint shadow-xs transition hover:border-line-strong hover:text-muted"
        >
          <Search className="size-3.5" />
          <span className="flex-1 text-left">Rechercher…</span>
          <span className="kbd">Ctrl</span><span className="kbd">K</span>
        </button>
      </div>
      <nav className="mt-6 flex-1 space-y-6 overflow-y-auto px-3">
        <NavSection items={main} onNavigate={() => setMobileOpen(false)} />
        {admin.length > 0 && <NavSection title="Administration" items={admin} onNavigate={() => setMobileOpen(false)} />}
      </nav>
      <div className="border-t border-line p-3">
        <SystemStatus />
      </div>
    </div>
  );

  return (
    <div className="min-h-screen">
      <aside className="fixed inset-y-0 left-0 z-30 hidden w-60 border-r border-line bg-surface-2 lg:block">{sidebar}</aside>

      {mobileOpen && (
        <div className="fixed inset-0 z-40 lg:hidden">
          <div className="animate-fade-in absolute inset-0 bg-slate-950/40 backdrop-blur-[2px]" onClick={() => setMobileOpen(false)} />
          <aside className="animate-fade-in relative h-full w-72 border-r border-line bg-surface-2 shadow-pop">{sidebar}</aside>
        </div>
      )}

      <div className="lg:pl-60">
        <header className="sticky top-0 z-20 flex h-14 items-center gap-3 border-b border-line bg-canvas/80 px-4 backdrop-blur-md sm:px-6 lg:px-8">
          <IconButton label="Ouvrir le menu" className="lg:hidden" onClick={() => setMobileOpen(true)}>
            <Menu className="size-5" />
          </IconButton>
          <div className="lg:hidden"><Logo compact /></div>
          <div className="hidden min-w-0 flex-1 lg:block"><Breadcrumbs /></div>
          <div className="ml-auto flex items-center gap-1">
            <IconButton label="Rechercher (Ctrl+K)" onClick={() => setPaletteOpen(true)} className="lg:hidden">
              <Search className="size-4" />
            </IconButton>
            <IconButton label="Nouveau ticket" onClick={() => setCreating(true)} className="lg:hidden">
              <Plus className="size-4" />
            </IconButton>
            <UserMenu />
          </div>
        </header>
        <main>
          <div key={location.pathname} className="animate-fade-in mx-auto max-w-[1400px] px-4 py-6 sm:px-6 lg:px-8 lg:py-8">
            <Suspense fallback={<PageSkeleton />}>
              <Outlet />
            </Suspense>
          </div>
        </main>
      </div>

      <NewTicketModal open={creating} onClose={() => setCreating(false)} />
      <CommandPalette
        open={paletteOpen}
        onClose={() => setPaletteOpen(false)}
        onNewTicket={() => { setPaletteOpen(false); setCreating(true); }}
      />
    </div>
  );
}
