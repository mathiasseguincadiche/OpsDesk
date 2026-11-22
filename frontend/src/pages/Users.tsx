import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { clsx } from "clsx";
import { KeyRound, Search, ShieldCheck, UserPlus, Users as UsersIcon, Wrench } from "lucide-react";
import { useState, type FormEvent, type ReactNode } from "react";
import { toast } from "sonner";
import { Avatar, Button, ErrorBox, Field, IconButton, Modal, PageHeader, RoleBadge, Select, Skeleton } from "@/components/ui";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { fromNow } from "@/lib/format";
import { ROLE } from "@/lib/labels";
import type { Role, User } from "@/lib/types";

const roles = Object.keys(ROLE) as Role[];
const roleOptions = roles.map((r) => ({ value: r, label: ROLE[r].label }));

function Stat({ icon, label, value }: { icon: ReactNode; label: string; value: number }) {
  return (
    <div className="card flex items-center gap-3 p-4">
      <span className="flex size-9 items-center justify-center rounded-lg border border-line bg-surface-2 text-muted">{icon}</span>
      <div>
        <p className="num text-lg font-semibold leading-none">{value}</p>
        <p className="mt-1 text-xs text-muted">{label}</p>
      </div>
    </div>
  );
}

export function UsersPage() {
  const { user: me } = useAuth();
  const queryClient = useQueryClient();
  const [creating, setCreating] = useState(false);
  const [resetting, setResetting] = useState<User | null>(null);
  const [filter, setFilter] = useState("");
  const { data, isLoading, error } = useQuery({ queryKey: ["users"], queryFn: () => api<User[]>("/api/users") });

  const update = useMutation({
    mutationFn: ({ id, body }: { id: number; body: Partial<User> }) => api<User>(`/api/users/${id}`, { method: "PATCH", body }),
    onSuccess: (u) => {
      queryClient.invalidateQueries({ queryKey: ["users"] });
      queryClient.invalidateQueries({ queryKey: ["agents"] });
      toast.success(`${u.full_name} mis à jour`);
    },
    onError: (e: Error) => toast.error(e.message),
  });

  if (error) return <ErrorBox error={error} />;
  const users = data ?? [];
  const term = filter.trim().toLowerCase();
  const shown = users.filter((u) => !term || u.full_name.toLowerCase().includes(term) || u.email.includes(term));
  const count = (r: Role) => users.filter((u) => u.role === r && u.is_active).length;

  return (
    <>
      <PageHeader
        title="Utilisateurs"
        subtitle="Gérez les comptes, les rôles et les accès à OpsDesk."
        actions={<Button onClick={() => setCreating(true)}><UserPlus className="size-4" /> Créer un compte utilisateur</Button>}
      />

      <div className="mb-4 grid gap-4 sm:grid-cols-3">
        <Stat icon={<UsersIcon className="size-4" />} label="Collaborateurs actifs" value={count("user")} />
        <Stat icon={<Wrench className="size-4" />} label="Membres du support" value={count("agent")} />
        <Stat icon={<ShieldCheck className="size-4" />} label="Administrateurs" value={count("admin")} />
      </div>

      <div className="card overflow-visible">
        <div className="flex items-center gap-3 border-b border-line p-3">
          <div className="relative flex-1 sm:max-w-xs">
            <Search className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-faint" />
            <input className="input pl-9" placeholder="Rechercher un nom ou un e-mail…" value={filter} onChange={(e) => setFilter(e.target.value)} />
          </div>
          <span className="num ml-auto text-[13px] text-muted">{shown.length} compte{shown.length > 1 ? "s" : ""}</span>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full min-w-[760px] text-[13px]">
            <thead>
              <tr className="border-b border-line bg-surface-2 text-left text-[11px] font-medium uppercase tracking-wider text-faint">
                <th className="py-2.5 pl-5">Utilisateur</th>
                <th className="py-2.5">Rôle</th>
                <th className="py-2.5">Dernière connexion</th>
                <th className="py-2.5">Statut</th>
                <th className="py-2.5 pr-5 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-line">
              {isLoading
                ? Array.from({ length: 5 }).map((_, i) => (
                    <tr key={i}><td colSpan={5} className="px-5 py-3"><Skeleton className="h-8" /></td></tr>
                  ))
                : shown.map((u) => {
                    const self = u.id === me!.id;
                    return (
                      <tr key={u.id} className={clsx("transition-colors hover:bg-hover/50", !u.is_active && "opacity-55")}>
                        <td className="py-2.5 pl-5">
                          <div className="flex items-center gap-3">
                            <Avatar name={u.full_name} />
                            <div className="min-w-0">
                              <p className="font-medium text-ink">{u.full_name}{self && <span className="ml-1.5 text-xs font-normal text-faint">(vous)</span>}</p>
                              <p className="truncate text-xs text-muted">{u.email}</p>
                            </div>
                          </div>
                        </td>
                        <td className="py-2.5">
                          {self ? (
                            <RoleBadge role={u.role} />
                          ) : (
                            <Select variant="ghost" className="w-40" value={u.role} onChange={(role) => update.mutate({ id: u.id, body: { role } })} options={roleOptions} label={`Rôle de ${u.full_name}`} />
                          )}
                        </td>
                        <td className="py-2.5 text-muted">{u.last_login_at ? fromNow(u.last_login_at) : <span className="text-faint">Jamais connecté</span>}</td>
                        <td className="py-2.5">
                          <span className={clsx("inline-flex items-center gap-1.5 rounded-md px-2 py-0.5 text-xs font-medium ring-1 ring-inset", u.is_active ? "text-emerald-700 ring-emerald-600/20 dark:text-emerald-400 dark:ring-emerald-400/20" : "text-muted ring-line-strong")}>
                            <span className={clsx("size-1.5 rounded-full", u.is_active ? "bg-emerald-500" : "bg-faint")} />
                            {u.is_active ? "Actif" : "Désactivé"}
                          </span>
                        </td>
                        <td className="py-2.5 pr-5">
                          <div className="flex items-center justify-end gap-1">
                            <IconButton label="Réinitialiser le mot de passe" onClick={() => setResetting(u)}><KeyRound className="size-4" /></IconButton>
                            {!self && (
                              <Button size="xs" variant="secondary" onClick={() => update.mutate({ id: u.id, body: { is_active: !u.is_active } })}>
                                {u.is_active ? "Désactiver" : "Réactiver"}
                              </Button>
                            )}
                          </div>
                        </td>
                      </tr>
                    );
                  })}
            </tbody>
          </table>
        </div>
      </div>

      {creating && <CreateUserModal onClose={() => setCreating(false)} />}
      {resetting && <ResetPasswordModal user={resetting} onClose={() => setResetting(null)} />}
    </>
  );
}

function CreateUserModal({ onClose }: { onClose: () => void }) {
  const queryClient = useQueryClient();
  const [form, setForm] = useState({ full_name: "", email: "", password: "", role: "user" as Role });
  const create = useMutation({
    mutationFn: () => api<User>("/api/users", { method: "POST", body: form }),
    onSuccess: (u) => {
      queryClient.invalidateQueries({ queryKey: ["users"] });
      queryClient.invalidateQueries({ queryKey: ["agents"] });
      toast.success(`${u.full_name} a été ajouté`);
      onClose();
    },
  });
  const submit = (e: FormEvent) => { e.preventDefault(); create.mutate(); };
  return (
    <Modal open onClose={onClose} title="Créer un compte utilisateur" description="Le compte est actif immédiatement avec le mot de passe initial.">
      <form onSubmit={submit} className="space-y-4">
        <Field label="Nom complet" htmlFor="cu-name"><input id="cu-name" className="input" required minLength={2} value={form.full_name} onChange={(e) => setForm({ ...form, full_name: e.target.value })} autoFocus /></Field>
        <Field label="E-mail" htmlFor="cu-email"><input id="cu-email" type="email" className="input" required value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} /></Field>
        <div className="grid gap-4 sm:grid-cols-2">
          <Field label="Mot de passe initial" htmlFor="cu-pass" hint="8 caractères minimum."><input id="cu-pass" type="password" className="input" required minLength={8} value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} autoComplete="new-password" /></Field>
          <div><span className="label">Rôle</span><Select label="Rôle" value={form.role} onChange={(role) => setForm({ ...form, role })} options={roleOptions} /></div>
        </div>
        <ErrorBox error={create.error} />
        <div className="-mx-6 -mb-6 mt-2 flex justify-end gap-2 border-t border-line bg-surface-2 px-6 py-3">
          <Button type="button" variant="secondary" onClick={onClose}>Annuler</Button>
          <Button type="submit" loading={create.isPending}>Créer le compte</Button>
        </div>
      </form>
    </Modal>
  );
}

function ResetPasswordModal({ user, onClose }: { user: User; onClose: () => void }) {
  const [password, setPassword] = useState("");
  const reset = useMutation({
    mutationFn: () => api(`/api/users/${user.id}`, { method: "PATCH", body: { password } }),
    onSuccess: () => { toast.success("Mot de passe réinitialisé"); onClose(); },
  });
  return (
    <Modal open onClose={onClose} title="Réinitialiser le mot de passe" description={`Nouveau mot de passe pour ${user.full_name}.`}>
      <form onSubmit={(e) => { e.preventDefault(); reset.mutate(); }} className="space-y-4">
        <Field label="Nouveau mot de passe" htmlFor="rp" hint="Communiquez-le à l'utilisateur par un canal sûr."><input id="rp" type="password" className="input" required minLength={8} value={password} onChange={(e) => setPassword(e.target.value)} autoComplete="new-password" autoFocus /></Field>
        <ErrorBox error={reset.error} />
        <div className="flex justify-end gap-2">
          <Button type="button" variant="secondary" onClick={onClose}>Annuler</Button>
          <Button type="submit" loading={reset.isPending}>Réinitialiser</Button>
        </div>
      </form>
    </Modal>
  );
}
