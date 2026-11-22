import { useMutation, useQueryClient } from "@tanstack/react-query";
import { clsx } from "clsx";
import { useState, type FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "sonner";
import { api } from "@/lib/api";
import { CATEGORY, PRIORITY, categories, priorities } from "@/lib/labels";
import type { Category, Priority, TicketDetail } from "@/lib/types";
import { Button, ErrorBox, Field, Modal, PriorityIcon, Select } from "./ui";

const PRIORITY_HINT: Record<Priority, string> = {
  low: "Gêne mineure, pas d'urgence",
  normal: "Impact sur mon travail, contournement possible",
  high: "Je suis bloqué(e) dans mon travail",
  critical: "Plusieurs personnes ou un service entier bloqués",
};

export function NewTicketModal({ open, onClose }: { open: boolean; onClose: () => void }) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [priority, setPriority] = useState<Priority>("normal");
  const [category, setCategory] = useState<Category>("other");
  const queryClient = useQueryClient();
  const navigate = useNavigate();

  const mutation = useMutation({
    mutationFn: () => api<TicketDetail>("/api/tickets", { method: "POST", body: { title, description, priority, category } }),
    onSuccess: (ticket) => {
      queryClient.invalidateQueries({ queryKey: ["tickets"] });
      queryClient.invalidateQueries({ queryKey: ["stats"] });
      toast.success(`Ticket #${ticket.id} créé`, { description: "Le ticket est enregistré et visible par l'équipe support." });
      setTitle(""); setDescription(""); setPriority("normal"); setCategory("other");
      mutation.reset();
      onClose();
      navigate(`/tickets/${ticket.id}`);
    },
  });

  const submit = (e: FormEvent) => {
    e.preventDefault();
    mutation.mutate();
  };

  return (
    <Modal open={open} onClose={onClose} title="Nouveau ticket" description="Décrivez votre besoin : le support vous répond au plus vite." wide>
      <form onSubmit={submit} className="space-y-4">
        <Field label="Sujet" htmlFor="nt-title">
          <input id="nt-title" className="input" required minLength={3} maxLength={120} autoFocus value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Ex. Impossible de me connecter au VPN" />
        </Field>
        <Field label="Description" htmlFor="nt-desc" hint="Précisez le contexte, le message d'erreur éventuel et ce que vous avez déjà essayé.">
          <textarea id="nt-desc" className="input min-h-32 resize-y" maxLength={5000} value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Depuis ce matin, le client VPN affiche…" />
        </Field>
        <div className="grid gap-4 sm:grid-cols-[1fr_200px]">
          <div>
            <span className="label">Priorité</span>
            <div role="radiogroup" aria-label="Priorité" className="grid grid-cols-4 gap-1 rounded-lg border border-line bg-surface-2 p-1">
              {priorities.map((p) => (
                <button
                  type="button"
                  role="radio"
                  aria-checked={priority === p}
                  key={p}
                  onClick={() => setPriority(p)}
                  className={clsx(
                    "flex items-center justify-center gap-1.5 rounded-md px-2 py-1.5 text-xs font-medium transition",
                    priority === p ? "bg-surface text-ink shadow-card ring-1 ring-line" : "text-muted hover:text-ink",
                  )}
                >
                  <PriorityIcon priority={p} />
                  {PRIORITY[p].label}
                </button>
              ))}
            </div>
            <p className="mt-1.5 text-xs text-faint">{PRIORITY_HINT[priority]}</p>
          </div>
          <div>
            <span className="label">Catégorie</span>
            <Select
              label="Catégorie"
              value={category}
              onChange={setCategory}
              options={categories.map((c) => ({ value: c, label: CATEGORY[c].label, icon: <span className="size-2 rounded-full" style={{ background: CATEGORY[c].color }} /> }))}
            />
          </div>
        </div>
        <ErrorBox error={mutation.error} />
        <div className="-mx-6 -mb-6 mt-2 flex items-center justify-end gap-2 border-t border-line bg-surface-2 px-6 py-3">
          <Button type="button" variant="secondary" onClick={onClose}>Annuler</Button>
          <Button type="submit" loading={mutation.isPending}>Créer le ticket</Button>
        </div>
      </form>
    </Modal>
  );
}
