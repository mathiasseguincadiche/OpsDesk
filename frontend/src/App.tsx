import { lazy } from "react";
import { Link, Navigate, Route, Routes } from "react-router-dom";
import { Layout } from "@/components/Layout";
import { Spinner } from "@/components/ui";
import { useAuth } from "@/lib/auth";
import { LoginPage } from "@/pages/Login";

const DashboardPage = lazy(() => import("@/pages/Dashboard").then((m) => ({ default: m.DashboardPage })));
const TicketsPage = lazy(() => import("@/pages/Tickets").then((m) => ({ default: m.TicketsPage })));
const TicketDetailPage = lazy(() => import("@/pages/TicketDetail").then((m) => ({ default: m.TicketDetailPage })));
const ProfilePage = lazy(() => import("@/pages/Profile").then((m) => ({ default: m.ProfilePage })));
const UsersPage = lazy(() => import("@/pages/Users").then((m) => ({ default: m.UsersPage })));

function NotFound() {
  return (
    <div className="flex flex-col items-center py-24 text-center">
      <p className="font-mono text-sm font-medium text-brand-600 dark:text-brand-400">Erreur 404</p>
      <h1 className="mt-2 text-2xl font-semibold tracking-tight">Page introuvable</h1>
      <p className="mt-2 text-sm text-muted">Le lien est peut-être erroné ou la page a été déplacée.</p>
      <Link to="/" className="mt-6 text-sm font-medium text-brand-600 hover:underline dark:text-brand-400">← Retour au tableau de bord</Link>
    </div>
  );
}

export default function App() {
  const { user, loading, isAdmin } = useAuth();
  if (loading) return <div className="flex min-h-screen items-center justify-center"><Spinner /></div>;
  if (!user) {
    return (
      <Routes>
        <Route path="*" element={<LoginPage />} />
      </Routes>
    );
  }
  return (
    <Routes>
      <Route path="/login" element={<Navigate to="/" replace />} />
      <Route element={<Layout />}>
        <Route index element={<DashboardPage />} />
        <Route path="tickets" element={<TicketsPage />} />
        <Route path="tickets/:id" element={<TicketDetailPage />} />
        <Route path="profile" element={<ProfilePage />} />
        {isAdmin && <Route path="users" element={<UsersPage />} />}
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  );
}
