import { useMutation, useQuery } from "@tanstack/react-query";
import { clsx } from "clsx";
import { Monitor, Moon, Sun } from "lucide-react";
import { useState, type FormEvent, type ReactNode } from "react";
import { toast } from "sonner";
import { Avatar, Button, ErrorBox, Field, PageHeader, RoleBadge } from "@/components/ui";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { fullDate } from "@/lib/format";
import { useTheme } from "@/lib/theme";
import type { Stats } from "@/lib/types";

function Section({ title, description, children }: { title: string; description: string; children: ReactNode }) {
  return (
    <section className="grid gap-6 border-b border-line py-8 first:pt-0 last:border-0 lg:grid-cols-[280px_1fr]">
      <div>
        <h2 className="text-sm font-semibold">{title}</h2>
        <p className="mt-1 text-[13px] text-muted">{description}</p>
      </div>
      <div className="min-w-0">{children}</div>
    </section>
  );
}

export function ProfilePage() {
  const { user, isStaff, logout } = useAuth();
  const { dark, toggle } = useTheme();
  const [current, setCurrent] = useState("");
  const [next, setNext] = useState("");
  const [confirm, setConfirm] = useState("");
  const { data: stats } = useQuery({ queryKey: ["stats"], queryFn: () => api<Stats>("/api/stats") });
  const change = useMutation({
    mutationFn: () => api("/api/auth/me/password", { method: "PUT", body: { current_password: current, new_password: next } }),
    onSuccess: () => { toast.success("Mot de passe modifié. Reconnectez-vous."); setCurrent(""); setNext(""); setConfirm(""); logout(); },
  });
  const mismatch = confirm.length > 0 && confirm !== next;
  const submit = (e: FormEvent) => { e.preventDefault(); if (!mismatch) change.mutate(); };

  const strength = Math.min(4, [next.length >= 8, next.length >= 12, /[A-Z]/.test(next) && /[a-z]/.test(next), /\d/.test(next) && /[^A-Za-z0-9]/.test(next)].filter(Boolean).length);
  const strengthLabel = ["Trop court", "Faible", "Moyen", "Bon", "Excellent"][strength];

  return (
    <div className="max-w-5xl">
      <PageHeader title="Mon profil" subtitle="Vos informations personnelles et vos préférences." />

      <div className="card mb-8 flex flex-col gap-5 p-6 sm:flex-row sm:items-center">
        <Avatar name={user!.full_name} size="xl" />
        <div className="min-w-0 flex-1">
          <div className="flex flex-wrap items-center gap-2">
            <h2 className="text-lg font-semibold">{user!.full_name}</h2>
            <RoleBadge role={user!.role} />
          </div>
          <p className="mt-0.5 text-sm text-muted">{user!.email}</p>
          <p className="mt-2 text-xs text-faint">Membre depuis le {fullDate(user!.created_at)}</p>
        </div>
        {stats && (
          <div className="flex gap-8 border-t border-line pt-4 sm:border-l sm:border-t-0 sm:pl-8 sm:pt-0">
            <div><p className="num text-2xl font-semibold">{isStaff ? stats.assigned_to_me : stats.mine_active}</p><p className="text-xs text-muted">{isStaff ? "Assignés à moi" : "Demandes actives"}</p></div>
            <div><p className="num text-2xl font-semibold">{stats.total}</p><p className="text-xs text-muted">{isStaff ? "Tickets au total" : "Demandes au total"}</p></div>
          </div>
        )}
      </div>

      <Section title="Apparence" description="Choisissez le thème de l'interface sur cet appareil.">
        <div className="grid max-w-md grid-cols-2 gap-3">
          {[
            { key: false, label: "Clair", icon: <Sun className="size-4" /> },
            { key: true, label: "Sombre", icon: <Moon className="size-4" /> },
          ].map((opt) => (
            <button
              key={opt.label}
              onClick={() => dark !== opt.key && toggle()}
              className={clsx(
                "overflow-hidden rounded-xl border text-left transition",
                dark === opt.key ? "border-brand-500 ring-4 ring-(--ring)" : "border-line hover:border-line-strong",
              )}
            >
              <div className={clsx("flex h-20 gap-1.5 p-2.5", opt.key ? "bg-[#0b0d12]" : "bg-[#f7f8fa]")}>
                <div className={clsx("w-1/4 rounded", opt.key ? "bg-[#161a22]" : "bg-white")} />
                <div className="flex flex-1 flex-col gap-1.5">
                  <div className={clsx("h-3 w-2/3 rounded", opt.key ? "bg-[#232835]" : "bg-[#e7e9ee]")} />
                  <div className={clsx("flex-1 rounded", opt.key ? "bg-[#12151c]" : "bg-white")} />
                </div>
              </div>
              <div className="flex items-center gap-2 border-t border-line px-3 py-2 text-[13px] font-medium">{opt.icon}{opt.label}</div>
            </button>
          ))}
        </div>
        <p className="mt-3 flex items-center gap-1.5 text-xs text-faint"><Monitor className="size-3.5" />Par défaut, OpsDesk suit le thème de votre système.</p>
      </Section>

      <Section title="Mot de passe" description="Utilisez un mot de passe long et unique, que vous n'utilisez nulle part ailleurs.">
        <form onSubmit={submit} className="max-w-md space-y-4">
          <Field label="Mot de passe actuel" htmlFor="pw-cur"><input id="pw-cur" type="password" className="input" required value={current} onChange={(e) => setCurrent(e.target.value)} autoComplete="current-password" /></Field>
          <Field label="Nouveau mot de passe" htmlFor="pw-new">
            <input id="pw-new" type="password" className="input" required minLength={8} value={next} onChange={(e) => setNext(e.target.value)} autoComplete="new-password" />
            {next && (
              <div className="mt-2 flex items-center gap-2">
                <div className="flex flex-1 gap-1">
                  {[1, 2, 3, 4].map((i) => (
                    <span key={i} className={clsx("h-1 flex-1 rounded-full transition-colors", i <= strength ? ["bg-rose-500", "bg-amber-500", "bg-sky-500", "bg-emerald-500"][strength - 1] : "bg-hover")} />
                  ))}
                </div>
                <span className="w-16 text-right text-xs text-muted">{strengthLabel}</span>
              </div>
            )}
          </Field>
          <Field label="Confirmation" htmlFor="pw-conf">
            <input id="pw-conf" type="password" className={clsx("input", mismatch && "border-rose-400 focus:border-rose-500")} required value={confirm} onChange={(e) => setConfirm(e.target.value)} autoComplete="new-password" />
            {mismatch && <p className="mt-1.5 text-xs text-rose-600 dark:text-rose-400">Les mots de passe ne correspondent pas.</p>}
          </Field>
          <ErrorBox error={change.error} />
          <Button type="submit" loading={change.isPending} disabled={mismatch || !current || next.length < 8}>Mettre à jour le mot de passe</Button>
        </form>
      </Section>
    </div>
  );
}
