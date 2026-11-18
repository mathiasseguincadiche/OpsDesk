import { useQuery } from "@tanstack/react-query";
import { clsx } from "clsx";
import { format } from "date-fns";
import { fr } from "date-fns/locale";
import { ArrowDownRight, ArrowRight, ArrowUpRight, CheckCircle2, Inbox, MessageSquare, Minus, Plus, Timer, TriangleAlert } from "lucide-react";
import type { ReactNode } from "react";
import { Link } from "react-router-dom";
import { Area, AreaChart, CartesianGrid, Cell, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { Avatar, ErrorBox, PageHeader, PageSkeleton, PriorityIcon, Skeleton, StatusBadge, StatusIcon } from "@/components/ui";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { fromNow, hours, shortDay } from "@/lib/format";
import { CATEGORY, PRIORITY, STATUS, categories, priorities, statuses } from "@/lib/labels";
import type { Stats, TicketPage } from "@/lib/types";

const PERIOD = 14;

/* ---------- building blocks ---------- */
function Delta({ current, previous, inverse }: { current: number; previous: number; inverse?: boolean }) {
  if (previous === 0 && current === 0) return <span className="text-xs text-faint">—</span>;
  const pct = previous === 0 ? 100 : Math.round(((current - previous) / previous) * 100);
  const up = pct > 0;
  const good = inverse ? !up : up;
  const Icon = pct === 0 ? Minus : up ? ArrowUpRight : ArrowDownRight;
  return (
    <span
      className={clsx(
        "num inline-flex items-center gap-0.5 rounded-md px-1.5 py-0.5 text-[11px] font-medium",
        pct === 0 ? "bg-hover text-muted" : good ? "bg-emerald-50 text-emerald-700 dark:bg-emerald-500/10 dark:text-emerald-400" : "bg-rose-50 text-rose-700 dark:bg-rose-500/10 dark:text-rose-400",
      )}
      title={`${previous} sur les ${PERIOD} jours précédents`}
    >
      <Icon className="size-3" />
      {Math.abs(pct)} %
    </span>
  );
}

function Sparkline({ data, color }: { data: number[]; color: string }) {
  const id = `spark-${color.replace("#", "")}`;
  return (
    <div className="h-10 w-24">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={data.map((v, i) => ({ i, v }))} margin={{ top: 2, bottom: 2, left: 0, right: 0 }}>
          <defs>
            <linearGradient id={id} x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor={color} stopOpacity={0.25} />
              <stop offset="100%" stopColor={color} stopOpacity={0} />
            </linearGradient>
          </defs>
          <Area type="monotone" dataKey="v" stroke={color} strokeWidth={1.75} fill={`url(#${id})`} isAnimationActive={false} />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}

function Kpi({ icon, label, value, footer, spark, sparkColor }: { icon: ReactNode; label: string; value: ReactNode; footer: ReactNode; spark?: number[]; sparkColor?: string }) {
  return (
    <div className="card flex flex-col p-5">
      <div className="flex items-center gap-2 text-[13px] font-medium text-muted">
        <span className="text-faint">{icon}</span>
        {label}
      </div>
      <div className="mt-3 flex items-end justify-between gap-3">
        <p className="num text-[28px] font-semibold leading-none tracking-tight">{value}</p>
        {spark && sparkColor && <Sparkline data={spark} color={sparkColor} />}
      </div>
      <div className="mt-3 flex items-center gap-2 text-xs text-muted">{footer}</div>
    </div>
  );
}

function Panel({ title, action, children, className, bodyClassName }: { title: string; action?: ReactNode; children: ReactNode; className?: string; bodyClassName?: string }) {
  return (
    <section className={clsx("card flex flex-col", className)}>
      <header className="card-header">
        <h2 className="card-title">{title}</h2>
        {action}
      </header>
      <div className={clsx("flex-1", bodyClassName ?? "p-5")}>{children}</div>
    </section>
  );
}

function ChartTooltip({ active, payload, label }: { active?: boolean; payload?: { name: string; value: number; color: string }[]; label?: string }) {
  if (!active || !payload?.length) return null;
  return (
    <div className="rounded-lg border border-line bg-surface px-3 py-2 text-xs shadow-pop">
      <p className="mb-1 font-medium text-ink">{label}</p>
      {payload.map((p) => (
        <p key={p.name} className="flex items-center gap-2 text-muted">
          <span className="size-2 rounded-full" style={{ background: p.color }} />
          {p.name}
          <span className="num ml-auto pl-4 font-medium text-ink">{p.value}</span>
        </p>
      ))}
    </div>
  );
}

function BarList({ rows, total }: { rows: { key: string; label: ReactNode; value: number; color: string }[]; total: number }) {
  return (
    <ul className="space-y-3">
      {rows.map((r) => {
        const pct = total ? (r.value / total) * 100 : 0;
        return (
          <li key={r.key}>
            <div className="mb-1.5 flex items-center justify-between text-[13px]">
              <span className="flex items-center gap-2 text-ink-2">{r.label}</span>
              <span className="num text-muted"><span className="font-medium text-ink">{r.value}</span> · {Math.round(pct)} %</span>
            </div>
            <div className="h-1.5 overflow-hidden rounded-full bg-hover">
              <div className="h-full rounded-full transition-[width] duration-700" style={{ width: `${pct}%`, background: r.color }} />
            </div>
          </li>
        );
      })}
    </ul>
  );
}

const sum = (values: number[]) => values.reduce((a, b) => a + b, 0);

/* ---------- page ---------- */
export function DashboardPage() {
  const { user, isStaff } = useAuth();
  const stats = useQuery({
    queryKey: ["stats", PERIOD * 2],
    queryFn: () => api<Stats>("/api/stats", { query: { days: PERIOD * 2 } }),
    refetchInterval: 30_000,
  });
  const urgent = useQuery({
    queryKey: ["tickets", "urgent"],
    queryFn: () => api<TicketPage>("/api/tickets", { query: { status: ["open", "in_progress"], sort: "priority", page_size: 6 } }),
  });
  const recent = useQuery({
    queryKey: ["tickets", "recent"],
    queryFn: () => api<TicketPage>("/api/tickets", { query: { page_size: 6, sort: "updated" } }),
  });

  if (stats.isLoading) return <PageSkeleton />;
  if (stats.error) return <ErrorBox error={stats.error} />;
  const s = stats.data!;

  const previous = s.timeline.slice(0, PERIOD);
  const current = s.timeline.slice(PERIOD);
  const createdNow = sum(current.map((d) => d.created));
  const createdBefore = sum(previous.map((d) => d.created));
  const resolvedNow = sum(current.map((d) => d.resolved));
  const resolvedBefore = sum(previous.map((d) => d.resolved));
  const active = s.by_status.open + s.by_status.in_progress;
  const timeline = current.map((d) => ({ ...d, label: shortDay(d.date) }));
  const statusData = statuses.map((k) => ({ key: k, name: STATUS[k].label, value: s.by_status[k], color: STATUS[k].color }));
  const hour = new Date().getHours();
  const firstName = user!.full_name.split(" ")[0];

  return (
    <>
      <PageHeader
        eyebrow={<span className="inline-block first-letter:uppercase">{format(new Date(), "EEEE d MMMM yyyy", { locale: fr })}</span>}
        title={`${hour >= 5 && hour < 18 ? "Bonjour" : "Bonsoir"} ${firstName}`}
        subtitle={isStaff ? "Voici l'état du support aujourd'hui." : "Voici où en sont vos demandes."}
        actions={
          <Link to="/tickets" className="inline-flex h-9 items-center gap-1.5 rounded-lg border border-line-strong bg-surface px-3.5 text-sm font-medium text-ink-2 shadow-xs transition hover:bg-hover hover:text-ink">
            Voir les tickets <ArrowRight className="size-4" />
          </Link>
        }
      />

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <Kpi
          icon={<Inbox className="size-4" />}
          label="Tickets actifs"
          value={active}
          footer={isStaff ? <><span className="font-medium text-ink">{s.unassigned_open}</span> sans responsable</> : <><span className="font-medium text-ink">{s.by_status.in_progress}</span> en cours de traitement</>}
        />
        <Kpi
          icon={<Plus className="size-4" />}
          label={`Nouveaux · ${PERIOD} j`}
          value={createdNow}
          spark={current.map((d) => d.created)}
          sparkColor="#3b82f6"
          footer={<><Delta current={createdNow} previous={createdBefore} inverse /> vs {PERIOD} j précédents</>}
        />
        <Kpi
          icon={<CheckCircle2 className="size-4" />}
          label={`Résolus · ${PERIOD} j`}
          value={resolvedNow}
          spark={current.map((d) => d.resolved)}
          sparkColor="#10b981"
          footer={<><Delta current={resolvedNow} previous={resolvedBefore} /> vs {PERIOD} j précédents</>}
        />
        <Kpi
          icon={<Timer className="size-4" />}
          label="Délai moyen de résolution"
          value={hours(s.avg_resolution_hours)}
          footer={
            s.critical_open > 0 ? (
              <span className="inline-flex items-center gap-1 font-medium text-rose-600 dark:text-rose-400"><TriangleAlert className="size-3.5" />{s.critical_open} critique{s.critical_open > 1 ? "s" : ""} en attente</span>
            ) : (
              <span className="inline-flex items-center gap-1 text-emerald-600 dark:text-emerald-400"><CheckCircle2 className="size-3.5" />Aucun incident critique</span>
            )
          }
        />
      </div>

      <div className="mt-4 grid gap-4 xl:grid-cols-3">
        <Panel
          title={`Activité des ${PERIOD} derniers jours`}
          className="xl:col-span-2"
          action={
            <div className="flex items-center gap-4 text-xs text-muted">
              <span className="flex items-center gap-1.5"><span className="h-0.5 w-3 rounded bg-brand-500" />Créés</span>
              <span className="flex items-center gap-1.5"><span className="h-0.5 w-3 rounded bg-emerald-500" />Résolus</span>
            </div>
          }
        >
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={timeline} margin={{ left: -24, right: 4, top: 8, bottom: 0 }}>
                <defs>
                  <linearGradient id="gCreated" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#6366f1" stopOpacity={0.22} />
                    <stop offset="100%" stopColor="#6366f1" stopOpacity={0} />
                  </linearGradient>
                  <linearGradient id="gResolved" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#10b981" stopOpacity={0.18} />
                    <stop offset="100%" stopColor="#10b981" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 4" vertical={false} />
                <XAxis dataKey="label" tick={{ fontSize: 11, fill: "var(--faint)" }} tickLine={false} axisLine={false} interval="preserveStartEnd" minTickGap={24} />
                <YAxis allowDecimals={false} tick={{ fontSize: 11, fill: "var(--faint)" }} tickLine={false} axisLine={false} />
                <Tooltip content={<ChartTooltip />} cursor={{ stroke: "var(--line-strong)", strokeDasharray: "3 3" }} />
                <Area type="monotoneX" dataKey="created" name="Créés" stroke="#6366f1" strokeWidth={2} fill="url(#gCreated)" activeDot={{ r: 4, strokeWidth: 2, stroke: "var(--surface)" }} animationDuration={600} />
                <Area type="monotoneX" dataKey="resolved" name="Résolus" stroke="#10b981" strokeWidth={2} fill="url(#gResolved)" activeDot={{ r: 4, strokeWidth: 2, stroke: "var(--surface)" }} animationDuration={600} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        <Panel title="Répartition par statut">
          <div className="relative mx-auto h-44 w-44">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={s.total ? statusData : [{ key: "none", name: "Aucun", value: 1, color: "var(--line)" }]} dataKey="value" nameKey="name" innerRadius={58} outerRadius={80} paddingAngle={s.total ? 2 : 0} cornerRadius={4} strokeWidth={0} startAngle={90} endAngle={-270} animationDuration={600}>
                  {(s.total ? statusData : [{ key: "none", color: "var(--line)" }]).map((d) => <Cell key={d.key} fill={d.color} />)}
                </Pie>
                {s.total > 0 && <Tooltip content={<ChartTooltip />} />}
              </PieChart>
            </ResponsiveContainer>
            <div className="pointer-events-none absolute inset-0 flex flex-col items-center justify-center">
              <span className="num text-3xl font-semibold tracking-tight">{s.total}</span>
              <span className="text-xs text-muted">tickets</span>
            </div>
          </div>
          <ul className="mt-5 space-y-2">
            {statusData.map((d) => (
              <li key={d.key}>
                <Link to={`/tickets?tab=${d.key}`} className="flex items-center gap-2.5 rounded-md px-2 py-1 text-[13px] transition hover:bg-hover">
                  <span className="size-2 rounded-full" style={{ background: d.color }} />
                  <span className="text-ink-2">{d.name}</span>
                  <span className="num ml-auto font-medium">{d.value}</span>
                  <span className="num w-10 text-right text-xs text-faint">{s.total ? Math.round((d.value / s.total) * 100) : 0} %</span>
                </Link>
              </li>
            ))}
          </ul>
        </Panel>
      </div>

      <div className="mt-4 grid gap-4 xl:grid-cols-3">
        <Panel
          title={isStaff ? "À traiter en priorité" : "Mes demandes en cours"}
          className="xl:col-span-2"
          bodyClassName="p-0"
          action={<Link to="/tickets?sort=priority" className="text-xs font-medium text-brand-600 hover:underline dark:text-brand-400">Tout voir</Link>}
        >
          {urgent.isLoading ? (
            <div className="space-y-3 p-5">{[0, 1, 2, 3].map((i) => <Skeleton key={i} className="h-9" />)}</div>
          ) : urgent.data!.items.length === 0 ? (
            <div className="flex flex-col items-center py-12 text-center">
              <CheckCircle2 className="size-8 text-emerald-500" />
              <p className="mt-3 text-sm font-medium">Tout est sous contrôle</p>
              <p className="text-sm text-muted">Aucun ticket actif pour le moment.</p>
            </div>
          ) : (
            <ul className="divide-y divide-line">
              {urgent.data!.items.map((t) => (
                <li key={t.id}>
                  <Link to={`/tickets/${t.id}`} className="flex items-center gap-3 px-5 py-3 transition hover:bg-hover/60">
                    <PriorityIcon priority={t.priority} />
                    <span className="num w-10 shrink-0 font-mono text-xs text-faint">#{t.id}</span>
                    <span className="min-w-0 flex-1 truncate text-[13px] font-medium">{t.title}</span>
                    <span className="hidden sm:inline-flex"><StatusBadge status={t.status} /></span>
                    {t.assignee ? <Avatar name={t.assignee.full_name} size="sm" /> : <span className="size-6 rounded-full border border-dashed border-line-strong" title="Non assigné" />}
                    <span className="hidden w-24 text-right text-xs text-faint md:block">{fromNow(t.created_at)}</span>
                  </Link>
                </li>
              ))}
            </ul>
          )}
        </Panel>

        {isStaff ? (
          <Panel title="Charge de l'équipe">
            {s.agents.length === 0 ? (
              <p className="py-8 text-center text-sm text-muted">Aucun membre du support</p>
            ) : (
              <ul className="space-y-4">
                {s.agents.map((a) => {
                  const max = Math.max(1, ...s.agents.map((x) => x.open));
                  return (
                    <li key={a.id} className="flex items-center gap-3">
                      <Avatar name={a.full_name} size="sm" />
                      <div className="min-w-0 flex-1">
                        <div className="mb-1 flex justify-between text-[13px]">
                          <span className="truncate text-ink-2">{a.full_name}</span>
                          <span className="num font-medium">{a.open}</span>
                        </div>
                        <div className="h-1.5 overflow-hidden rounded-full bg-hover">
                          <div className="h-full rounded-full bg-brand-500 transition-[width] duration-700" style={{ width: `${(a.open / max) * 100}%` }} />
                        </div>
                      </div>
                    </li>
                  );
                })}
              </ul>
            )}
            {s.unassigned_open > 0 && (
              <Link to="/tickets?assignee=none" className="mt-5 flex items-center gap-2 rounded-lg border border-amber-200 bg-amber-50 px-3 py-2 text-[13px] text-amber-800 transition hover:bg-amber-100 dark:border-amber-500/20 dark:bg-amber-500/10 dark:text-amber-300">
                <TriangleAlert className="size-4" />
                <span className="flex-1">{s.unassigned_open} ticket{s.unassigned_open > 1 ? "s" : ""} sans responsable</span>
                <ArrowRight className="size-3.5" />
              </Link>
            )}
          </Panel>
        ) : (
          <Panel title="Par priorité">
            <BarList total={s.total} rows={priorities.map((p) => ({ key: p, label: <><PriorityIcon priority={p} />{PRIORITY[p].label}</>, value: s.by_priority[p], color: PRIORITY[p].color }))} />
          </Panel>
        )}
      </div>

      <div className="mt-4 grid gap-4 xl:grid-cols-3">
        <Panel title="Par catégorie">
          <BarList total={s.total} rows={categories.map((c) => ({ key: c, label: CATEGORY[c].label, value: s.by_category[c], color: CATEGORY[c].color }))} />
        </Panel>
        {isStaff && (
          <Panel title="Par priorité">
            <BarList total={s.total} rows={priorities.map((p) => ({ key: p, label: <><PriorityIcon priority={p} />{PRIORITY[p].label}</>, value: s.by_priority[p], color: PRIORITY[p].color }))} />
          </Panel>
        )}
        <Panel title="Dernières mises à jour" bodyClassName="p-0" className={isStaff ? "" : "xl:col-span-2"}>
          <ul className="divide-y divide-line">
            {recent.data?.items.slice(0, 5).map((t) => (
              <li key={t.id}>
                <Link to={`/tickets/${t.id}`} className="flex items-start gap-3 px-5 py-3 transition hover:bg-hover/60">
                  <StatusIcon status={t.status} className="mt-0.5" />
                  <span className="min-w-0 flex-1">
                    <span className="block truncate text-[13px] font-medium">{t.title}</span>
                    <span className="mt-0.5 flex items-center gap-2 text-xs text-faint">
                      <span className="font-mono">#{t.id}</span>·<span className="whitespace-nowrap">{fromNow(t.updated_at)}</span>
                      {t.comment_count > 0 && <span className="num flex items-center gap-1"><MessageSquare className="size-3" />{t.comment_count}</span>}
                    </span>
                  </span>
                </Link>
              </li>
            ))}
          </ul>
        </Panel>
      </div>
    </>
  );
}
