import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { clsx } from "clsx";
import { ArrowLeft, ArrowRightLeft, CheckCircle2, Copy, Pencil, PlayCircle, RotateCcw, Send, Tag, Trash2, UserPlus, XCircle } from "lucide-react";
import { useState, type FormEvent, type ReactNode } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { toast } from "sonner";
import { Avatar, Button, CategoryTag, ErrorBox, Field, IconButton, Modal, PriorityBadge, PriorityIcon, RoleBadge, Select, Skeleton, StatusBadge, StatusIcon } from "@/components/ui";
import { ApiError, api } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { fromNow, fullDate } from "@/lib/format";
import { CATEGORY, PRIORITY, STATUS, TRANSITION_LABEL, categories, priorities } from "@/lib/labels";
import type { Category, Priority, Status, TicketDetail, TicketEvent, UserBrief } from "@/lib/types";

const transitionStyle: Record<Status, { variant: "primary" | "secondary" | "success"; icon: ReactNode }> = {
  in_progress: { variant: "primary", icon: <PlayCircle className="size-4" /> },
  resolved: { variant: "success", icon: <CheckCircle2 className="size-4" /> },
  closed: { variant: "secondary", icon: <XCircle className="size-4" /> },
  open: { variant: "secondary", icon: <RotateCcw className="size-4" /> },
};

function eventText(e: TicketEvent): ReactNode {
  const st = (v: string | null) => (v && v in STATUS ? <span className="inline-flex items-center gap-1 font-medium text-ink"><StatusIcon status={v as Status} className="size-3" />{STATUS[v as Status].label}</span> : v);
  switch (e.kind) {
    case "status_changed": return <>a changé le statut de {st(e.from_value)} à {st(e.to_value)}</>;
    case "assigned": return e.to_value ? <>a assigné le ticket à <b className="font-medium text-ink">{e.to_value}</b></> : "a retiré le responsable";
    case "priority_changed": return <>a changé la priorité de <b className="font-medium text-ink">{PRIORITY[e.from_value as Priority]?.label}</b> à <b className="font-medium text-ink">{PRIORITY[e.to_value as Priority]?.label}</b></>;
    case "category_changed": return <>a reclassé le ticket en <b className="font-medium text-ink">{CATEGORY[e.to_value as Category]?.label}</b></>;
    case "edited": return "a modifié le sujet ou la description";
    default: return e.kind;
  }
}

function eventIcon(kind: string) {
  if (kind === "status_changed") return <ArrowRightLeft className="size-3" />;
  if (kind === "assigned") return <UserPlus className="size-3" />;
  if (kind === "edited") return <Pencil className="size-3" />;
  return <Tag className="size-3" />;
}

function Property({ label, children }: { label: string; children: ReactNode }) {
  return (
    <div className="grid grid-cols-[96px_1fr] items-center gap-2 py-1">
      <dt className="text-[13px] text-muted">{label}</dt>
      <dd className="min-w-0 text-[13px]">{children}</dd>
    </div>
  );
}

function DetailSkeleton() {
  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_320px]">
      <div className="space-y-4">
        <Skeleton className="h-5 w-40" /><Skeleton className="h-8 w-3/4" /><Skeleton className="h-24" /><Skeleton className="h-64 rounded-xl" />
      </div>
      <Skeleton className="h-80 rounded-xl" />
    </div>
  );
}

export function TicketDetailPage() {
  const { id } = useParams();
  const { user, isStaff, isAdmin } = useAuth();
  const queryClient = useQueryClient();
  const navigate = useNavigate();
  const [comment, setComment] = useState("");
  const [editing, setEditing] = useState(false);
  const [confirmDelete, setConfirmDelete] = useState(false);

  const key = ["tickets", "detail", id];
  const { data: t, isLoading, error } = useQuery({ queryKey: key, queryFn: () => api<TicketDetail>(`/api/tickets/${id}`) });
  const agents = useQuery({ queryKey: ["agents"], queryFn: () => api<UserBrief[]>("/api/users/agents"), enabled: isStaff });

  const refresh = (data: TicketDetail) => {
    queryClient.setQueryData(key, data);
    queryClient.invalidateQueries({ queryKey: ["tickets"], refetchType: "none" });
    queryClient.invalidateQueries({ queryKey: ["stats"] });
  };
  const onError = (err: Error) => toast.error(err.message);

  const transition = useMutation({
    mutationFn: (status: Status) => api<TicketDetail>(`/api/tickets/${id}/status`, { method: "POST", body: { status } }),
    onSuccess: (data) => { refresh(data); toast.success(`Ticket ${STATUS[data.status].label.toLowerCase()}`); },
    onError,
  });
  const patch = useMutation({
    mutationFn: (body: Record<string, unknown>) => api<TicketDetail>(`/api/tickets/${id}`, { method: "PATCH", body }),
    onSuccess: (data) => { refresh(data); toast.success("Modifications enregistrées"); setEditing(false); },
    onError,
  });
  const addComment = useMutation({
    mutationFn: () => api(`/api/tickets/${id}/comments`, { method: "POST", body: { body: comment } }),
    onSuccess: () => { setComment(""); queryClient.invalidateQueries({ queryKey: key }); },
    onError,
  });
  const remove = useMutation({
    mutationFn: () => api(`/api/tickets/${id}`, { method: "DELETE" }),
    onSuccess: () => { toast.success("Ticket supprimé"); queryClient.invalidateQueries({ queryKey: ["tickets"] }); queryClient.invalidateQueries({ queryKey: ["stats"] }); navigate("/tickets"); },
    onError,
  });

  if (isLoading) return <DetailSkeleton />;
  if (error) {
    const notFound = error instanceof ApiError && error.status === 404;
    return (
      <div className="flex flex-col items-center py-24 text-center">
        <p className="font-mono text-sm font-medium text-brand-600 dark:text-brand-400">{notFound ? "404" : "Erreur"}</p>
        <h1 className="mt-2 text-xl font-semibold">{notFound ? "Ticket introuvable" : "Impossible de charger ce ticket"}</h1>
        <p className="mt-2 text-sm text-muted">{notFound ? "Il a peut-être été supprimé, ou vous n'y avez pas accès." : error.message}</p>
        <Link to="/tickets" className="mt-6 text-sm font-medium text-brand-600 hover:underline dark:text-brand-400">← Retour aux tickets</Link>
      </div>
    );
  }
  if (!t) return null;

  const timeline = [
    ...t.comments.map((c) => ({ type: "comment" as const, at: c.created_at, item: c })),
    ...t.events.filter((e) => e.kind !== "created").map((e) => ({ type: "event" as const, at: e.created_at, item: e })),
  ].sort((a, b) => a.at.localeCompare(b.at));

  const submitComment = (e: FormEvent) => {
    e.preventDefault();
    if (comment.trim()) addComment.mutate();
  };

  const transitionLabel = (s: Status) => {
    if (!isStaff && t.status === "resolved" && s === "in_progress") return "Le problème persiste";
    if (!isStaff && t.status === "resolved" && s === "closed") return "Confirmer la résolution";
    if (!isStaff && s === "closed") return "Annuler ma demande";
    return TRANSITION_LABEL[s];
  };
  const isMine = t.assignee?.id === user!.id;

  return (
    <>
      <Link to="/tickets" className="mb-5 inline-flex items-center gap-1.5 text-[13px] text-muted transition hover:text-ink lg:hidden">
        <ArrowLeft className="size-4" /> Tickets
      </Link>

      <div className="grid gap-6 lg:grid-cols-[minmax(0,1fr)_320px]">
        {/* Main column */}
        <div className="min-w-0 space-y-6">
          <div>
            <div className="flex flex-wrap items-center gap-2 text-[13px] text-muted">
              <span className="font-mono">#{t.id}</span>
              <span className="text-faint">·</span>
              <StatusBadge status={t.status} />
              <PriorityBadge priority={t.priority} />
              <CategoryTag category={t.category} />
              <div className="ml-auto flex items-center gap-0.5">
                <IconButton label="Copier le lien" onClick={() => { navigator.clipboard?.writeText(window.location.href); toast.success("Lien copié"); }}>
                  <Copy className="size-4" />
                </IconButton>
                {t.can_edit && (
                  <IconButton label="Modifier" onClick={() => setEditing(true)}>
                    <Pencil className="size-4" />
                  </IconButton>
                )}
              </div>
            </div>
            <h1 className="mt-3 text-2xl font-semibold leading-tight tracking-tight">{t.title}</h1>
            <p className="mt-2 flex items-center gap-2 text-[13px] text-muted">
              <Avatar name={t.requester.full_name} size="xs" />
              <span><span className="font-medium text-ink-2">{t.requester.full_name}</span> a ouvert ce ticket {fromNow(t.created_at)}</span>
            </p>
          </div>

          <div className="card p-5">
            <div className="whitespace-pre-wrap break-words text-[15px] leading-relaxed text-ink-2">
              {t.description || <span className="italic text-faint">Aucune description fournie.</span>}
            </div>
            {t.allowed_transitions.length > 0 && (
              <div className="mt-5 flex flex-wrap items-center gap-2 border-t border-line pt-4">
                {[...t.allowed_transitions].sort((a, b) => (transitionStyle[a].variant === "secondary" ? 1 : 0) - (transitionStyle[b].variant === "secondary" ? 1 : 0)).map((s) => (
                  <Button key={s} size="sm" variant={transitionStyle[s].variant} loading={transition.isPending && transition.variables === s} onClick={() => transition.mutate(s)}>
                    {!(transition.isPending && transition.variables === s) && transitionStyle[s].icon}
                    {transitionLabel(s)}
                  </Button>
                ))}
                {isStaff && !isMine && t.status !== "closed" && (
                  <Button size="sm" variant="ghost" className="ml-auto" loading={patch.isPending} onClick={() => patch.mutate({ assignee_id: user!.id })}>
                    <UserPlus className="size-4" /> M'assigner
                  </Button>
                )}
              </div>
            )}
          </div>

          {/* Activity */}
          <section>
            <h2 className="mb-4 flex items-center gap-2 text-[13px] font-semibold">
              Activité <span className="num rounded-md bg-hover px-1.5 text-[11px] font-medium text-muted">{t.comments.length + t.events.length}</span>
            </h2>
            <ol className="relative space-y-4 before:absolute before:bottom-0 before:left-[15px] before:top-2 before:w-px before:bg-line">
              <li className="relative flex items-center gap-3">
                <span className="z-10 flex size-8 items-center justify-center rounded-full border border-line bg-surface"><StatusIcon status="open" /></span>
                <p className="text-[13px] text-muted"><b className="font-medium text-ink">{t.requester.full_name}</b> a créé le ticket <span className="text-faint" title={fullDate(t.created_at)}>· {fromNow(t.created_at)}</span></p>
              </li>
              {timeline.map((entry) =>
                entry.type === "comment" ? (
                  <li key={`c${entry.item.id}`} className="relative flex gap-3">
                    <Avatar name={entry.item.author.full_name} className="z-10" />
                    <div className="card min-w-0 flex-1">
                      <div className="flex flex-wrap items-center gap-2 border-b border-line px-4 py-2 text-[13px]">
                        <b className="font-medium">{entry.item.author.full_name}</b>
                        {entry.item.author.role !== "user" && <RoleBadge role={entry.item.author.role} />}
                        <span className="text-xs text-faint" title={fullDate(entry.at)}>{fromNow(entry.at)}</span>
                      </div>
                      <p className="whitespace-pre-wrap break-words px-4 py-3 text-sm leading-relaxed text-ink-2">{entry.item.body}</p>
                    </div>
                  </li>
                ) : (
                  <li key={`e${entry.item.id}`} className="relative flex items-center gap-3">
                    <span className="z-10 ml-2 flex size-4 items-center justify-center rounded-full bg-canvas text-faint ring-4 ring-canvas">{eventIcon(entry.item.kind)}</span>
                    <p className="ml-2 text-[13px] text-muted">
                      <b className="font-medium text-ink">{entry.item.actor.full_name}</b> {eventText(entry.item)} <span className="text-faint" title={fullDate(entry.at)}>· {fromNow(entry.at)}</span>
                    </p>
                  </li>
                ),
              )}
              <li className="relative flex gap-3">
                <Avatar name={user!.full_name} className="z-10" />
                <form onSubmit={submitComment} className="card min-w-0 flex-1 overflow-hidden focus-within:border-brand-500 focus-within:ring-4 focus-within:ring-(--ring)">
                  <textarea
                    className="block min-h-24 w-full resize-y bg-transparent px-4 py-3 text-sm outline-none placeholder:text-faint"
                    placeholder={isStaff ? "Répondre au demandeur ou ajouter une note…" : "Ajouter une précision ou répondre au support…"}
                    value={comment}
                    onChange={(e) => setComment(e.target.value)}
                    maxLength={5000}
                    onKeyDown={(e) => { if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) submitComment(e); }}
                  />
                  <div className="flex items-center justify-between border-t border-line bg-surface-2 px-3 py-2">
                    <span className="hidden items-center gap-1 text-[11px] text-faint sm:flex"><span className="kbd">Ctrl</span><span className="kbd">↵</span> pour envoyer</span>
                    <Button type="submit" size="sm" className="ml-auto" loading={addComment.isPending} disabled={!comment.trim()}>
                      <Send className="size-3.5" /> Commenter
                    </Button>
                  </div>
                </form>
              </li>
            </ol>
          </section>
        </div>

        {/* Sidebar */}
        <aside className="space-y-4 lg:sticky lg:top-20 lg:self-start">
          <div className="card p-4">
            <h3 className="mb-2 text-[11px] font-medium uppercase tracking-wider text-faint">Propriétés</h3>
            <dl>
              <Property label="Statut"><span className="px-2"><StatusBadge status={t.status} /></span></Property>
              <Property label="Priorité">
                {isStaff ? (
                  <Select variant="ghost" value={t.priority} disabled={patch.isPending} onChange={(v) => patch.mutate({ priority: v })}
                    options={priorities.map((p) => ({ value: p, label: PRIORITY[p].label, icon: <PriorityIcon priority={p} /> }))} />
                ) : <span className="px-2"><PriorityBadge priority={t.priority} /></span>}
              </Property>
              <Property label="Catégorie">
                {isStaff ? (
                  <Select variant="ghost" value={t.category} disabled={patch.isPending} onChange={(v) => patch.mutate({ category: v })}
                    options={categories.map((c) => ({ value: c, label: CATEGORY[c].label, icon: <span className="size-2 rounded-full" style={{ background: CATEGORY[c].color }} /> }))} />
                ) : <span className="px-2"><CategoryTag category={t.category} /></span>}
              </Property>
              <Property label="Responsable">
                {isStaff ? (
                  <Select<number>
                    variant="ghost"
                    value={t.assignee?.id ?? 0}
                    disabled={patch.isPending}
                    onChange={(v) => patch.mutate({ assignee_id: v })}
                    options={[
                      { value: 0, label: "Non assigné", icon: <span className="size-5 rounded-full border border-dashed border-line-strong" /> },
                      ...(agents.data ?? []).map((a) => ({ value: a.id, label: a.full_name, hint: a.id === user!.id ? "moi" : undefined, icon: <Avatar name={a.full_name} size="xs" /> })),
                    ]}
                  />
                ) : t.assignee ? (
                  <span className="flex items-center gap-2 px-2"><Avatar name={t.assignee.full_name} size="xs" />{t.assignee.full_name}</span>
                ) : (
                  <span className="px-2 text-faint">En attente d'attribution</span>
                )}
              </Property>
              <Property label="Demandeur">
                <span className="flex items-center gap-2 px-2"><Avatar name={t.requester.full_name} size="xs" /><span className="truncate">{t.requester.full_name}</span></span>
              </Property>
            </dl>
          </div>

          <div className="card p-4">
            <h3 className="mb-2 text-[11px] font-medium uppercase tracking-wider text-faint">Chronologie</h3>
            <dl>
              <Property label="Créé"><span className="px-2" title={fullDate(t.created_at)}>{fullDate(t.created_at)}</span></Property>
              <Property label="Mis à jour"><span className="px-2" title={fullDate(t.updated_at)}>{fromNow(t.updated_at)}</span></Property>
              {t.resolved_at && <Property label="Résolu"><span className="px-2">{fullDate(t.resolved_at)}</span></Property>}
              {t.closed_at && <Property label="Clôturé"><span className="px-2">{fullDate(t.closed_at)}</span></Property>}
            </dl>
          </div>

          {isAdmin && (
            <Button variant="outline-danger" size="sm" className="w-full" onClick={() => setConfirmDelete(true)}>
              <Trash2 className="size-3.5" /> Supprimer le ticket
            </Button>
          )}
        </aside>
      </div>

      {editing && <EditModal onClose={() => setEditing(false)} ticket={t} loading={patch.isPending} error={patch.error} onSave={(body) => patch.mutate(body)} />}
      <Modal open={confirmDelete} onClose={() => setConfirmDelete(false)} title="Supprimer ce ticket ?" description="Cette action est définitive.">
        <p className="text-sm text-ink-2">Le ticket <b>#{t.id}</b>, ses {t.comments.length} commentaire(s) et son historique seront supprimés.</p>
        <div className="mt-6 flex justify-end gap-2">
          <Button variant="secondary" onClick={() => setConfirmDelete(false)}>Annuler</Button>
          <Button variant="danger" loading={remove.isPending} onClick={() => remove.mutate()}>Supprimer définitivement</Button>
        </div>
      </Modal>
    </>
  );
}

function EditModal({ onClose, ticket, onSave, loading, error }: { onClose: () => void; ticket: TicketDetail; onSave: (b: Record<string, unknown>) => void; loading: boolean; error: unknown }) {
  const [title, setTitle] = useState(ticket.title);
  const [description, setDescription] = useState(ticket.description);
  return (
    <Modal open onClose={onClose} title={`Modifier le ticket #${ticket.id}`} wide>
      <form className="space-y-4" onSubmit={(e) => { e.preventDefault(); onSave({ title, description }); }}>
        <Field label="Sujet" htmlFor="ed-title">
          <input id="ed-title" className="input" required minLength={3} maxLength={120} value={title} onChange={(e) => setTitle(e.target.value)} />
        </Field>
        <Field label="Description" htmlFor="ed-desc">
          <textarea id="ed-desc" className="input min-h-40 resize-y" maxLength={5000} value={description} onChange={(e) => setDescription(e.target.value)} />
        </Field>
        <ErrorBox error={error} />
        <div className={clsx("flex justify-end gap-2 pt-1")}>
          <Button type="button" variant="secondary" onClick={onClose}>Annuler</Button>
          <Button type="submit" loading={loading}>Enregistrer</Button>
        </div>
      </form>
    </Modal>
  );
}
