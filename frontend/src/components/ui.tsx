import { clsx } from "clsx";
import { Check, ChevronDown, Loader2, X } from "lucide-react";
import { useEffect, useRef, useState, type ButtonHTMLAttributes, type KeyboardEvent as ReactKeyboardEvent, type ReactNode } from "react";
import { CATEGORY, PRIORITY, ROLE, STATUS } from "@/lib/labels";
import { initials } from "@/lib/format";
import type { Category, Priority, Role, Status } from "@/lib/types";

/* ---------------- Button ---------------- */
type Variant = "primary" | "secondary" | "ghost" | "danger" | "success" | "outline-danger";

const variants: Record<Variant, string> = {
  primary:
    "bg-brand-600 text-white shadow-xs shadow-brand-900/20 hover:bg-brand-700 active:bg-brand-800 [box-shadow:inset_0_1px_0_rgb(255_255_255/0.12),0_1px_2px_rgb(30_27_75/0.25)]",
  secondary: "bg-surface text-ink-2 border border-line-strong shadow-xs hover:bg-hover hover:text-ink",
  ghost: "text-muted hover:bg-hover hover:text-ink",
  danger: "bg-rose-600 text-white shadow-xs hover:bg-rose-700",
  success: "bg-emerald-600 text-white shadow-xs hover:bg-emerald-700 [box-shadow:inset_0_1px_0_rgb(255_255_255/0.12),0_1px_2px_rgb(6_78_59/0.25)]",
  "outline-danger": "border border-line-strong bg-surface text-rose-600 hover:border-rose-300 hover:bg-rose-50 dark:text-rose-400 dark:hover:border-rose-500/40 dark:hover:bg-rose-500/10",
};

export function Button({
  variant = "primary",
  size = "md",
  loading,
  className,
  children,
  disabled,
  ...props
}: ButtonHTMLAttributes<HTMLButtonElement> & { variant?: Variant; size?: "xs" | "sm" | "md"; loading?: boolean }) {
  return (
    <button
      {...props}
      disabled={disabled || loading}
      className={clsx(
        "inline-flex select-none items-center justify-center gap-1.5 whitespace-nowrap rounded-lg font-medium transition-colors disabled:pointer-events-none disabled:opacity-50",
        size === "xs" && "h-7 px-2.5 text-xs",
        size === "sm" && "h-8 px-3 text-[13px]",
        size === "md" && "h-9 px-3.5 text-sm",
        variants[variant],
        className,
      )}
    >
      {loading && <Loader2 className="size-3.5 animate-spin" />}
      {children}
    </button>
  );
}

export function IconButton({ label, className, children, ...props }: ButtonHTMLAttributes<HTMLButtonElement> & { label: string }) {
  return (
    <button
      {...props}
      aria-label={label}
      title={label}
      className={clsx("inline-flex size-8 items-center justify-center rounded-lg text-muted transition-colors hover:bg-hover hover:text-ink", className)}
    >
      {children}
    </button>
  );
}

/* ---------------- Badges ---------------- */
export function StatusBadge({ status, size = "sm" }: { status: Status; size?: "sm" | "md" }) {
  const s = STATUS[status];
  return (
    <span
      className={clsx(
        "inline-flex items-center gap-1.5 whitespace-nowrap rounded-md font-medium ring-1 ring-inset",
        size === "sm" ? "px-2 py-0.5 text-xs" : "px-2.5 py-1 text-[13px]",
        s.badge,
      )}
    >
      <StatusIcon status={status} />
      {s.label}
    </span>
  );
}

/** Small circular status glyph, Linear-style: empty → half → full → check. */
export function StatusIcon({ status, className }: { status: Status; className?: string }) {
  const color = STATUS[status].color;
  return (
    <svg viewBox="0 0 14 14" className={clsx("size-3.5 shrink-0", className)} aria-hidden>
      <circle cx="7" cy="7" r="5.5" fill="none" stroke={color} strokeWidth="1.5" strokeDasharray={status === "open" ? "2.2 1.6" : undefined} />
      {status === "in_progress" && <path d="M7 3.5a3.5 3.5 0 0 1 0 7z" fill={color} />}
      {status === "resolved" && (
        <>
          <circle cx="7" cy="7" r="5.5" fill={color} />
          <path d="M4.6 7.1l1.6 1.6 3.2-3.3" fill="none" stroke="white" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
        </>
      )}
      {status === "closed" && (
        <>
          <circle cx="7" cy="7" r="5.5" fill={color} />
          <path d="M5 5l4 4M9 5l-4 4" stroke="white" strokeWidth="1.4" strokeLinecap="round" />
        </>
      )}
    </svg>
  );
}

export function PriorityIcon({ priority, className }: { priority: Priority; className?: string }) {
  const p = PRIORITY[priority];
  if (priority === "critical") {
    return (
      <svg viewBox="0 0 14 14" className={clsx("size-3.5 shrink-0", className)} aria-hidden>
        <rect x="1" y="1" width="12" height="12" rx="3" fill={p.color} />
        <path d="M7 3.8v4" stroke="white" strokeWidth="1.6" strokeLinecap="round" />
        <circle cx="7" cy="10.2" r="0.95" fill="white" />
      </svg>
    );
  }
  return (
    <svg viewBox="0 0 14 14" className={clsx("size-3.5 shrink-0", className)} aria-hidden>
      {[0, 1, 2].map((i) => (
        <rect key={i} x={1.5 + i * 4} y={9 - i * 3} width="3" height={3.5 + i * 3} rx="0.8" fill={i < p.bars ? p.color : "var(--line-strong)"} />
      ))}
    </svg>
  );
}

export function PriorityBadge({ priority, showLabel = true }: { priority: Priority; showLabel?: boolean }) {
  return (
    <span className="inline-flex items-center gap-1.5 whitespace-nowrap text-xs font-medium text-ink-2" title={`Priorité ${PRIORITY[priority].label.toLowerCase()}`}>
      <PriorityIcon priority={priority} />
      {showLabel && PRIORITY[priority].label}
    </span>
  );
}

export function CategoryTag({ category }: { category: Category }) {
  const c = CATEGORY[category];
  return (
    <span className="inline-flex items-center gap-1.5 whitespace-nowrap rounded-md border border-line px-1.5 py-0.5 text-xs text-ink-2">
      <span className="size-1.5 rounded-full" style={{ background: c.color }} />
      {c.label}
    </span>
  );
}

export function RoleBadge({ role }: { role: Role }) {
  return <span className={clsx("inline-flex rounded-md px-1.5 py-0.5 text-[11px] font-medium", ROLE[role].badge)}>{ROLE[role].label}</span>;
}

/* ---------------- Avatar ---------------- */
const avatarColors = [
  "from-indigo-500 to-violet-500",
  "from-sky-500 to-indigo-500",
  "from-teal-500 to-emerald-500",
  "from-rose-500 to-orange-400",
  "from-amber-500 to-orange-500",
  "from-fuchsia-500 to-pink-500",
  "from-cyan-500 to-sky-500",
];

export function Avatar({ name, size = "md", className }: { name: string; size?: "xs" | "sm" | "md" | "lg" | "xl"; className?: string }) {
  const color = avatarColors[[...name].reduce((sum, ch) => sum + ch.charCodeAt(0), 0) % avatarColors.length];
  return (
    <span
      title={name}
      className={clsx(
        "inline-flex shrink-0 select-none items-center justify-center rounded-full bg-gradient-to-br font-semibold text-white ring-2 ring-surface",
        color,
        size === "xs" && "size-5 text-[9px]",
        size === "sm" && "size-6 text-[10px]",
        size === "md" && "size-8 text-[11px]",
        size === "lg" && "size-10 text-sm",
        size === "xl" && "size-16 text-xl",
        className,
      )}
    >
      {initials(name)}
    </span>
  );
}

/* ---------------- Dropdown select ---------------- */
export interface Option<T extends string | number> {
  value: T;
  label: string;
  icon?: ReactNode;
  hint?: string;
}

export function Select<T extends string | number>({
  value,
  options,
  onChange,
  placeholder = "Choisir…",
  disabled,
  className,
  buttonClassName,
  align = "left",
  label,
  variant = "field",
}: {
  value: T | null;
  options: Option<T>[];
  onChange: (value: T) => void;
  placeholder?: string;
  disabled?: boolean;
  className?: string;
  buttonClassName?: string;
  align?: "left" | "right";
  label?: string;
  variant?: "field" | "ghost";
}) {
  const [open, setOpen] = useState(false);
  const [active, setActive] = useState(0);
  const ref = useRef<HTMLDivElement>(null);
  const current = options.find((o) => o.value === value);

  useEffect(() => {
    if (!open) return;
    setActive(Math.max(0, options.findIndex((o) => o.value === value)));
    const onClick = (e: MouseEvent) => !ref.current?.contains(e.target as Node) && setOpen(false);
    document.addEventListener("mousedown", onClick);
    return () => document.removeEventListener("mousedown", onClick);
  }, [open, options, value]);

  const choose = (v: T) => {
    setOpen(false);
    if (v !== value) onChange(v);
  };

  const onKeyDown = (e: ReactKeyboardEvent) => {
    if (!open && (e.key === "ArrowDown" || e.key === "Enter" || e.key === " ")) {
      e.preventDefault();
      setOpen(true);
      return;
    }
    if (!open) return;
    if (e.key === "Escape") { e.preventDefault(); setOpen(false); }
    else if (e.key === "ArrowDown") { e.preventDefault(); setActive((a) => Math.min(options.length - 1, a + 1)); }
    else if (e.key === "ArrowUp") { e.preventDefault(); setActive((a) => Math.max(0, a - 1)); }
    else if (e.key === "Enter") { e.preventDefault(); choose(options[active].value); }
    else if (e.key === "Tab") setOpen(false);
  };

  return (
    <div ref={ref} className={clsx("relative", className)} onKeyDown={onKeyDown}>
      <button
        type="button"
        disabled={disabled}
        aria-haspopup="listbox"
        aria-expanded={open}
        aria-label={label}
        onClick={() => setOpen((o) => !o)}
        className={clsx(
          "flex w-full items-center gap-2 text-left text-sm transition disabled:cursor-not-allowed disabled:opacity-60",
          variant === "field"
            ? "h-9 rounded-lg border border-line-strong bg-surface px-3 shadow-xs hover:border-faint/60 focus-visible:border-brand-500 focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-(--ring)"
            : "h-8 rounded-md px-2 hover:bg-hover",
          open && variant === "field" && "border-brand-500 ring-4 ring-(--ring)",
          buttonClassName,
        )}
      >
        {current?.icon}
        <span className={clsx("flex-1 truncate", !current && "text-faint")}>{current?.label ?? placeholder}</span>
        <ChevronDown className={clsx("size-3.5 shrink-0 text-faint transition-transform", open && "rotate-180")} />
      </button>
      {open && (
        <ul
          role="listbox"
          className={clsx(
            "animate-pop-in absolute z-50 mt-1.5 max-h-72 min-w-full overflow-y-auto rounded-xl border border-line bg-surface p-1 shadow-pop",
            align === "right" ? "right-0" : "left-0",
          )}
        >
          {options.map((o, i) => (
            <li
              key={String(o.value)}
              role="option"
              aria-selected={o.value === value}
              onMouseEnter={() => setActive(i)}
              onMouseDown={(e) => { e.preventDefault(); choose(o.value); }}
              className={clsx(
                "flex cursor-pointer items-center gap-2 whitespace-nowrap rounded-lg px-2.5 py-1.5 text-sm",
                i === active ? "bg-hover text-ink" : "text-ink-2",
              )}
            >
              {o.icon}
              <span className="flex-1">{o.label}</span>
              {o.hint && <span className="text-xs text-faint">{o.hint}</span>}
              <Check className={clsx("size-3.5 text-brand-600 dark:text-brand-400", o.value !== value && "invisible")} />
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

/* ---------------- Feedback ---------------- */
export function Spinner({ className }: { className?: string }) {
  return <Loader2 className={clsx("size-5 animate-spin text-brand-500", className)} />;
}

export function Skeleton({ className }: { className?: string }) {
  return <div className={clsx("skeleton", className)} />;
}

export function PageSkeleton() {
  return (
    <div className="space-y-6" aria-busy="true" aria-label="Chargement">
      <div className="space-y-2">
        <Skeleton className="h-7 w-56" />
        <Skeleton className="h-4 w-80" />
      </div>
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {[0, 1, 2, 3].map((i) => <Skeleton key={i} className="h-28 rounded-xl" />)}
      </div>
      <Skeleton className="h-72 rounded-xl" />
    </div>
  );
}

export function EmptyState({ icon, title, children, action }: { icon: ReactNode; title: string; children?: ReactNode; action?: ReactNode }) {
  return (
    <div className="flex flex-col items-center justify-center px-6 py-16 text-center">
      <div className="relative mb-5">
        <div className="absolute inset-0 -m-3 rounded-full bg-brand-500/10 blur-xl" />
        <div className="relative flex size-12 items-center justify-center rounded-xl border border-line bg-surface text-muted shadow-card">{icon}</div>
      </div>
      <h3 className="text-sm font-semibold">{title}</h3>
      {children && <div className="mt-1 max-w-sm text-sm text-muted">{children}</div>}
      {action && <div className="mt-5">{action}</div>}
    </div>
  );
}

export function Modal({ open, onClose, title, description, children, wide }: { open: boolean; onClose: () => void; title: string; description?: string; children: ReactNode; wide?: boolean }) {
  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", onKey);
    const overflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      window.removeEventListener("keydown", onKey);
      document.body.style.overflow = overflow;
    };
  }, [open, onClose]);
  if (!open) return null;
  return (
    <div className="fixed inset-0 z-50 flex items-end justify-center sm:items-start sm:p-4 sm:pt-[12vh]" role="dialog" aria-modal="true" aria-label={title}>
      <div className="animate-fade-in absolute inset-0 bg-slate-950/40 backdrop-blur-[2px]" onClick={onClose} />
      <div className={clsx("animate-pop-in relative max-h-[90vh] w-full overflow-y-auto rounded-t-2xl border border-line bg-surface shadow-pop sm:rounded-2xl", wide ? "sm:max-w-2xl" : "sm:max-w-md")}>
        <div className="flex items-start justify-between gap-4 px-6 pb-2 pt-5">
          <div>
            <h2 className="text-base font-semibold">{title}</h2>
            {description && <p className="mt-0.5 text-sm text-muted">{description}</p>}
          </div>
          <IconButton label="Fermer" onClick={onClose} className="-mr-2 -mt-1">
            <X className="size-4" />
          </IconButton>
        </div>
        <div className="px-6 pb-6 pt-3">{children}</div>
      </div>
    </div>
  );
}

export function PageHeader({ title, subtitle, actions, eyebrow }: { title: ReactNode; subtitle?: ReactNode; actions?: ReactNode; eyebrow?: ReactNode }) {
  return (
    <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
      <div className="min-w-0">
        {eyebrow && <div className="mb-1 text-xs font-medium text-muted">{eyebrow}</div>}
        <h1 className="text-[22px] font-semibold leading-tight tracking-tight">{title}</h1>
        {subtitle && <p className="mt-1 text-sm text-muted">{subtitle}</p>}
      </div>
      {actions && <div className="flex flex-wrap items-center gap-2">{actions}</div>}
    </div>
  );
}

export function ErrorBox({ error }: { error: unknown }) {
  if (!error) return null;
  return (
    <div role="alert" className="flex items-start gap-2 rounded-lg border border-rose-200 bg-rose-50 px-3 py-2.5 text-[13px] text-rose-700 dark:border-rose-500/25 dark:bg-rose-500/10 dark:text-rose-300">
      <span className="mt-1.5 size-1.5 shrink-0 rounded-full bg-rose-500" />
      {error instanceof Error ? error.message : String(error)}
    </div>
  );
}

export function Field({ label, htmlFor, hint, children }: { label: string; htmlFor?: string; hint?: string; children: ReactNode }) {
  return (
    <div>
      <label className="label" htmlFor={htmlFor}>{label}</label>
      {children}
      {hint && <p className="mt-1.5 text-xs text-faint">{hint}</p>}
    </div>
  );
}
