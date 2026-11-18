import { keepPreviousData, useQuery } from "@tanstack/react-query";
import { clsx } from "clsx";
import { ArrowDownUp, ChevronLeft, ChevronRight, Inbox, MessageSquare, Search, SearchX, X } from "lucide-react";
import { useEffect, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { Avatar, Button, CategoryTag, EmptyState, ErrorBox, PageHeader, PriorityIcon, Select, Skeleton, StatusBadge, type Option } from "@/components/ui";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { fromNow, fullDate } from "@/lib/format";
import { CATEGORY, PRIORITY, STATUS, categories, priorities } from "@/lib/labels";
import type { Stats, TicketPage } from "@/lib/types";

const PAGE_SIZE = 15;
const SORTS: Option<string>[] = [
  { value: "newest", label: "Plus récents" },
  { value: "updated", label: "Dernière activité" },
  { value: "priority", label: "Priorité" },
  { value: "oldest", label: "Plus anciens" },
];

export function TicketsPage() {
  const { isStaff } = useAuth();
  const [params, setParams] = useSearchParams();
  const [search, setSearch] = useState(params.get("q") ?? "");

  const tab = params.get("tab") ?? "active";
  const page = Number(params.get("page") ?? 1);
  const priority = params.get("priority") ?? "";
  const category = params.get("category") ?? "";
  const assignee = params.get("assignee") ?? "";
  const sort = params.get("sort") ?? "newest";
  const q = params.get("q") ?? "";

  const update = (changes: Record<string, string>) => {
    const next = new URLSearchParams(params);
    for (const [k, v] of Object.entries(changes)) {
      if (v) next.set(k, v);
      else next.delete(k);
    }
    if (!("page" in changes)) next.delete("page");
    setParams(next, { replace: true });
  };

  useEffect(() => {
    const id = setTimeout(() => search !== q && update({ q: search }), 300);
    return () => clearTimeout(id);
  }, [search]); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => setSearch(q), [q]);

  const { data: stats } = useQuery({ queryKey: ["stats"], queryFn: () => api<Stats>("/api/stats") });
  const statusFilter = tab === "active" ? ["open", "in_progress"] : tab === "all" ? undefined : [tab];
  const { data, isLoading, isFetching, error } = useQuery({
    queryKey: ["tickets", { tab, page, priority, category, assignee, sort, q }],
    queryFn: () =>
      api<TicketPage>("/api/tickets", {
        query: { status: statusFilter, priority: priority || undefined, category: category || undefined, assignee: assignee || undefined, sort, q, page, page_size: PAGE_SIZE },
      }),
    placeholderData: keepPreviousData,
  });

  const counts = stats?.by_status;
  const tabs = [
    { key: "active", label: "Actifs", count: counts && counts.open + counts.in_progress },
    { key: "open", label: STATUS.open.label, count: counts?.open },
    { key: "in_progress", label: STATUS.in_progress.label, count: counts?.in_progress },
    { key: "resolved", label: STATUS.resolved.label, count: counts?.resolved },
    { key: "closed", label: STATUS.closed.label, count: counts?.closed },
    { key: "all", label: "Tous", count: stats?.total },
  ];

  const chips = [
    priority && { key: "priority", label: `Priorité : ${PRIORITY[priority as keyof typeof PRIORITY].label}` },
    category && { key: "category", label: `Catégorie : ${CATEGORY[category as keyof typeof CATEGORY].label}` },
    assignee && { key: "assignee", label: assignee === "me" ? "Assignés à moi" : assignee === "none" ? "Sans responsable" : "Responsable filtré" },
    q && { key: "q", label: `« ${q} »` },
  ].filter(Boolean) as { key: string; label: string }[];

  const title = assignee === "me" ? "Assignés à moi" : isStaff ? "Tickets" : "Mes demandes";
  const first = data ? (data.page - 1) * data.page_size + 1 : 0;
  const last = data ? Math.min(data.total, data.page * data.page_size) : 0;

  return (
    <>
      <PageHeader
        title={title}
        subtitle={isStaff ? "Suivez, assignez et résolvez les demandes de support." : "Retrouvez toutes les demandes que vous avez ouvertes."}
      />

      <div className="card overflow-visible">
        {/* Tabs */}
        <div className="flex gap-1 overflow-x-auto overflow-y-hidden border-b border-line px-3 [scrollbar-width:none]">
          {tabs.map((t) => {
            const selected = tab === t.key;
            return (
              <button
                key={t.key}
                onClick={() => update({ tab: t.key === "active" ? "" : t.key })}
                className={clsx(
                  "relative flex items-center gap-2 whitespace-nowrap px-2.5 py-3 text-[13px] font-medium transition-colors",
                  selected ? "text-ink" : "text-muted hover:text-ink",
                )}
              >
                {t.label}
                {t.count !== undefined && (
                  <span className={clsx("num rounded-md px-1.5 py-px text-[11px]", selected ? "bg-ink text-surface" : "bg-hover text-muted")}>{t.count}</span>
                )}
                {selected && <span className="absolute inset-x-2 bottom-0 h-0.5 rounded-full bg-brand-600 dark:bg-brand-400" />}
              </button>
            );
          })}
        </div>

        {/* Toolbar */}
        <div className="flex flex-col gap-2 border-b border-line p-3 lg:flex-row lg:items-center">
          <div className="relative flex-1">
            <Search className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-faint" />
            <input className="input pl-9" placeholder="Rechercher par titre, description ou numéro…" value={search} onChange={(e) => setSearch(e.target.value)} />
          </div>
          <div className="grid grid-cols-2 gap-2 sm:flex">
            <Select
              label="Priorité"
              className="sm:w-40"
              value={priority}
              onChange={(v) => update({ priority: v })}
              options={[{ value: "", label: "Toutes priorités" }, ...priorities.map((p) => ({ value: p, label: PRIORITY[p].label, icon: <PriorityIcon priority={p} /> }))]}
            />
            <Select
              label="Catégorie"
              className="sm:w-44"
              value={category}
              onChange={(v) => update({ category: v })}
              options={[{ value: "", label: "Toutes catégories" }, ...categories.map((c) => ({ value: c, label: CATEGORY[c].label, icon: <span className="size-2 rounded-full" style={{ background: CATEGORY[c].color }} /> }))]}
            />
            {isStaff && (
              <Select
                label="Responsable"
                className="sm:w-44"
                value={assignee}
                onChange={(v) => update({ assignee: v })}
                options={[{ value: "", label: "Tous responsables" }, { value: "me", label: "Assignés à moi" }, { value: "none", label: "Sans responsable" }]}
              />
            )}
            <Select
              label="Trier"
              className="sm:w-48"
              align="right"
              value={sort}
              onChange={(v) => update({ sort: v === "newest" ? "" : v })}
              options={SORTS.map((o) => ({ ...o, icon: <ArrowDownUp className="size-3.5 text-faint" /> }))}
            />
          </div>
        </div>

        {chips.length > 0 && (
          <div className="flex flex-wrap items-center gap-2 border-b border-line px-3 py-2">
            {chips.map((c) => (
              <span key={c.key} className="inline-flex items-center gap-1 rounded-md border border-line bg-surface-2 py-0.5 pl-2 pr-1 text-xs text-ink-2">
                {c.label}
                <button onClick={() => (c.key === "q" ? setSearch("") : update({ [c.key]: "" }))} className="rounded p-0.5 text-faint hover:bg-hover hover:text-ink" aria-label={`Retirer le filtre ${c.label}`}>
                  <X className="size-3" />
                </button>
              </span>
            ))}
            <button onClick={() => { setSearch(""); update({ priority: "", category: "", assignee: "", q: "" }); }} className="text-xs font-medium text-muted hover:text-ink">
              Tout effacer
            </button>
          </div>
        )}

        {/* Content */}
        {error ? (
          <div className="p-4"><ErrorBox error={error} /></div>
        ) : isLoading ? (
          <div className="divide-y divide-line">
            {Array.from({ length: 8 }).map((_, i) => (
              <div key={i} className="flex items-center gap-4 px-5 py-3.5">
                <Skeleton className="size-4" /><Skeleton className="h-4 w-10" /><Skeleton className="h-4 flex-1" /><Skeleton className="h-5 w-20" /><Skeleton className="h-6 w-6 rounded-full" />
              </div>
            ))}
          </div>
        ) : data!.items.length === 0 ? (
          chips.length ? (
            <EmptyState icon={<SearchX className="size-5" />} title="Aucun ticket ne correspond" action={<Button variant="secondary" size="sm" onClick={() => { setSearch(""); update({ priority: "", category: "", assignee: "", q: "" }); }}>Effacer les filtres</Button>}>
              Essayez d'élargir votre recherche ou de retirer un filtre.
            </EmptyState>
          ) : (
            <EmptyState icon={<Inbox className="size-5" />} title="Rien à afficher ici">
              Aucun ticket dans cette vue pour le moment.
            </EmptyState>
          )
        ) : (
          <div className={clsx("transition-opacity", isFetching && "opacity-60")}>
            <table className="hidden w-full table-fixed text-[13px] md:table">
              <colgroup>
                <col className="w-10" /><col className="w-16" /><col /><col className="w-32" /><col className="hidden w-40 xl:table-column" /><col className="w-44" /><col className="w-32" />
              </colgroup>
              <thead>
                <tr className="border-b border-line bg-surface-2 text-left text-[11px] font-medium uppercase tracking-wider text-faint">
                  <th className="py-2.5 pl-5" aria-label="Priorité" />
                  <th className="py-2.5">N°</th>
                  <th className="py-2.5 pr-4">Sujet</th>
                  <th className="py-2.5">Statut</th>
                  <th className="hidden py-2.5 xl:table-cell">Catégorie</th>
                  <th className="py-2.5">Responsable</th>
                  <th className="py-2.5 pr-5 text-right">Activité</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-line">
                {data!.items.map((t) => (
                  <tr key={t.id} className="group relative transition-colors hover:bg-hover/60">
                    <td className="py-3 pl-5"><PriorityIcon priority={t.priority} /></td>
                    <td className="num py-3 font-mono text-xs text-faint">#{t.id}</td>
                    <td className="py-3 pr-4">
                      <Link to={`/tickets/${t.id}`} className="block after:absolute after:inset-0">
                        <span className="flex items-center gap-2">
                          <span className="truncate font-medium text-ink">{t.title}</span>
                          {t.comment_count > 0 && <span className="num inline-flex shrink-0 items-center gap-1 text-xs text-faint"><MessageSquare className="size-3" />{t.comment_count}</span>}
                        </span>
                        <span className="mt-0.5 block truncate text-xs text-muted">{t.requester.full_name} · ouvert {fromNow(t.created_at)}</span>
                      </Link>
                    </td>
                    <td className="py-3"><StatusBadge status={t.status} /></td>
                    <td className="hidden py-3 xl:table-cell"><CategoryTag category={t.category} /></td>
                    <td className="py-3">
                      {t.assignee ? (
                        <span className="flex items-center gap-2"><Avatar name={t.assignee.full_name} size="xs" /><span className="truncate text-ink-2">{t.assignee.full_name}</span></span>
                      ) : (
                        <span className="flex items-center gap-2 text-faint"><span className="size-5 rounded-full border border-dashed border-line-strong" />Non assigné</span>
                      )}
                    </td>
                    <td className="py-3 pr-5 text-right text-xs text-muted" title={fullDate(t.updated_at)}>{fromNow(t.updated_at)}</td>
                  </tr>
                ))}
              </tbody>
            </table>

            <ul className="divide-y divide-line md:hidden">
              {data!.items.map((t) => (
                <li key={t.id}>
                  <Link to={`/tickets/${t.id}`} className="block px-4 py-3.5 active:bg-hover">
                    <div className="flex items-center gap-2 text-xs text-faint">
                      <PriorityIcon priority={t.priority} />
                      <span className="font-mono">#{t.id}</span>
                      <span className="ml-auto">{fromNow(t.updated_at)}</span>
                    </div>
                    <p className="mt-1 font-medium leading-snug">{t.title}</p>
                    <div className="mt-2 flex flex-wrap items-center gap-2">
                      <StatusBadge status={t.status} />
                      <CategoryTag category={t.category} />
                      {t.assignee && <Avatar name={t.assignee.full_name} size="xs" className="ml-auto" />}
                    </div>
                  </Link>
                </li>
              ))}
            </ul>

            <div className="flex items-center justify-between border-t border-line px-5 py-3 text-[13px]">
              <span className="num text-muted">
                <span className="font-medium text-ink">{first}–{last}</span> sur {data!.total}
              </span>
              <div className="flex items-center gap-1">
                <Button variant="secondary" size="sm" disabled={page <= 1} onClick={() => update({ page: String(page - 1) })} aria-label="Page précédente">
                  <ChevronLeft className="size-4" />
                </Button>
                <span className="num px-2 text-muted">{data!.page} / {data!.pages}</span>
                <Button variant="secondary" size="sm" disabled={page >= data!.pages} onClick={() => update({ page: String(page + 1) })} aria-label="Page suivante">
                  <ChevronRight className="size-4" />
                </Button>
              </div>
            </div>
          </div>
        )}
      </div>
    </>
  );
}
