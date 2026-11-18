import { useQuery } from "@tanstack/react-query";
import { ArrowRight, Moon, Sun } from "lucide-react";
import { useState, type FormEvent } from "react";
import { Navigate } from "react-router-dom";
import { Logo } from "@/components/Layout";
import { Avatar, Button, ErrorBox, Field, IconButton, PriorityIcon, StatusIcon } from "@/components/ui";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { useTheme } from "@/lib/theme";
import type { Priority, Status } from "@/lib/types";

const DEMO = [
  { label: "Équipe support", who: "Sophie Martin", email: "sophie.martin@opsdesk.local", password: "Demo1234!" },
  { label: "Collaborateur", who: "Julie Durand", email: "julie.durand@opsdesk.local", password: "Demo1234!" },
];

const PREVIEW: { id: number; title: string; status: Status; priority: Priority; who: string }[] = [
  { id: 128, title: "Serveur de fichiers très lent", status: "in_progress", priority: "critical", who: "Karim Benali" },
  { id: 127, title: "Accès VPN impossible depuis le domicile", status: "open", priority: "high", who: "Sophie Martin" },
  { id: 125, title: "Certificat TLS de l'intranet expiré", status: "resolved", priority: "high", who: "Karim Benali" },
  { id: 121, title: "Création d'un compte nouvel arrivant", status: "closed", priority: "normal", who: "Sophie Martin" },
];

/** Decorative, static mock of the product shown on the sign-in page. */
function ProductPreview() {
  return (
    <div className="relative w-full max-w-lg">
      <div className="absolute -inset-10 rounded-[40px] bg-brand-500/20 blur-3xl" />
      <div className="relative overflow-hidden rounded-2xl border border-white/10 bg-[#12151c]/90 shadow-2xl backdrop-blur" aria-hidden>
        <div className="flex items-center gap-1.5 border-b border-white/10 px-4 py-3">
          <span className="size-2.5 rounded-full bg-white/15" /><span className="size-2.5 rounded-full bg-white/15" /><span className="size-2.5 rounded-full bg-white/15" />
          <span className="ml-3 text-xs text-white/40">opsdesk / tickets actifs</span>
        </div>
        <div className="grid grid-cols-3 gap-3 p-4">
          {[["Actifs", "24", "+12 %"], ["Résolus · 14 j", "61", "+18 %"], ["Délai moyen", "6,4 h", "−9 %"]].map(([l, v, d]) => (
            <div key={l} className="rounded-xl border border-white/10 bg-white/[0.03] p-3">
              <p className="text-[10px] text-white/45">{l}</p>
              <p className="num mt-1 text-lg font-semibold text-white">{v}</p>
              <p className="text-[10px] text-emerald-400">{d}</p>
            </div>
          ))}
        </div>
        <ul className="divide-y divide-white/5 border-t border-white/10">
          {PREVIEW.map((t) => (
            <li key={t.id} className="flex items-center gap-3 px-4 py-2.5 text-xs">
              <PriorityIcon priority={t.priority} />
              <span className="font-mono text-white/35">#{t.id}</span>
              <span className="flex-1 truncate text-white/85">{t.title}</span>
              <StatusIcon status={t.status} />
              <Avatar name={t.who} size="xs" className="ring-[#12151c]" />
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export function LoginPage() {
  const { user, login, register } = useAuth();
  const { dark, toggle } = useTheme();
  const [mode, setMode] = useState<"login" | "register">("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [error, setError] = useState<unknown>(null);
  const [busy, setBusy] = useState(false);
  const { data: config } = useQuery({
    queryKey: ["auth-config"],
    queryFn: () => api<{ allow_registration: boolean; demo_mode: boolean }>("/api/auth/config"),
  });

  if (user) return <Navigate to="/" replace />;

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    setBusy(true);
    setError(null);
    try {
      if (mode === "login") await login(email, password);
      else await register(name, email, password);
    } catch (err) {
      setError(err);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="grid min-h-screen bg-surface lg:grid-cols-[minmax(0,1fr)_minmax(0,1.1fr)]">
      {/* Form side */}
      <div className="relative flex flex-col px-6 py-8 sm:px-12">
        <div className="flex items-center justify-between">
          <Logo />
          <IconButton label="Changer de thème" onClick={toggle}>{dark ? <Sun className="size-4" /> : <Moon className="size-4" />}</IconButton>
        </div>

        <div className="flex flex-1 items-center justify-center py-12">
          <div className="animate-fade-in w-full max-w-[360px]">
            <h1 className="text-2xl font-semibold tracking-tight">{mode === "login" ? "Connexion à votre espace" : "Créer votre compte"}</h1>
            <p className="mt-2 text-sm text-muted">
              {mode === "login" ? "Suivez vos demandes et échangez avec le support IT." : "Déclarez vos incidents et suivez leur résolution."}
            </p>

            <form onSubmit={submit} className="mt-8 space-y-4">
              {mode === "register" && (
                <Field label="Nom complet" htmlFor="name">
                  <input id="name" className="input h-10" required minLength={2} value={name} onChange={(e) => setName(e.target.value)} autoComplete="name" placeholder="Camille Dupont" />
                </Field>
              )}
              <Field label="Adresse e-mail professionnelle" htmlFor="email">
                <input id="email" type="email" className="input h-10" required value={email} onChange={(e) => setEmail(e.target.value)} autoComplete="email" placeholder="prenom.nom@entreprise.fr" />
              </Field>
              <Field label="Mot de passe" htmlFor="password" hint={mode === "register" ? "8 caractères minimum." : undefined}>
                <input id="password" type="password" className="input h-10" required minLength={mode === "register" ? 8 : 1} value={password} onChange={(e) => setPassword(e.target.value)} autoComplete={mode === "login" ? "current-password" : "new-password"} placeholder="••••••••" />
              </Field>
              <ErrorBox error={error} />
              <Button type="submit" className="h-10 w-full" loading={busy}>
                {mode === "login" ? "Se connecter" : "Créer mon compte"}
                {!busy && <ArrowRight className="size-4" />}
              </Button>
            </form>

            {config?.allow_registration && (
              <p className="mt-6 text-center text-[13px] text-muted">
                {mode === "login" ? "Pas encore de compte ? " : "Déjà inscrit ? "}
                <button className="font-medium text-brand-600 hover:underline dark:text-brand-400" onClick={() => { setMode(mode === "login" ? "register" : "login"); setError(null); }}>
                  {mode === "login" ? "Créer un compte" : "Se connecter"}
                </button>
              </p>
            )}

            {mode === "login" && config?.demo_mode && (
              <div className="mt-10">
                <div className="flex items-center gap-3 text-[11px] font-medium uppercase tracking-wider text-faint">
                  <span className="h-px flex-1 bg-line" />Accès de démonstration<span className="h-px flex-1 bg-line" />
                </div>
                <div className="mt-4 grid grid-cols-2 gap-2">
                  {DEMO.map((d) => (
                    <button
                      key={d.label}
                      type="button"
                      onClick={() => { setEmail(d.email); setPassword(d.password); setError(null); }}
                      className="flex items-center gap-2.5 rounded-lg border border-line bg-surface p-2.5 text-left transition hover:border-line-strong hover:bg-hover"
                    >
                      <Avatar name={d.who} size="sm" />
                      <span className="min-w-0">
                        <span className="block truncate text-[13px] font-medium">{d.label}</span>
                        <span className="block truncate text-[11px] text-muted">{d.who}</span>
                      </span>
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>

        <p className="text-xs text-faint">© {new Date().getFullYear()} OpsDesk · Support IT</p>
      </div>

      {/* Showcase side */}
      <div className="dot-grid relative hidden overflow-hidden bg-[#0b0d12] lg:flex lg:flex-col lg:items-center lg:justify-center lg:px-12">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top_right,rgba(99,102,241,0.25),transparent_60%)]" />
        <div className="relative w-full max-w-lg">
          <p className="text-sm font-medium text-brand-300">Helpdesk IT</p>
          <h2 className="mt-3 text-[32px] font-semibold leading-tight tracking-tight text-white">
            Chaque demande suivie,<br />de l'ouverture à la résolution.
          </h2>
          <p className="mt-4 max-w-md text-[15px] leading-relaxed text-white/55">
            Priorisation, assignation, historique complet et indicateurs en temps réel pour piloter votre support.
          </p>
          <div className="mt-12">
            <ProductPreview />
          </div>
        </div>
      </div>
    </div>
  );
}
