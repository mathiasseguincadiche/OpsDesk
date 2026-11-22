import { createContext, useCallback, useContext, useEffect, useMemo, useState, type ReactNode } from "react";
import { useQueryClient } from "@tanstack/react-query";
import { api, setUnauthorizedHandler } from "./api";
import type { BrowserSessionResponse, User } from "./types";

interface AuthValue {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (full_name: string, email: string, password: string) => Promise<void>;
  logout: () => void;
  isStaff: boolean;
  isAdmin: boolean;
}

const AuthContext = createContext<AuthValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const queryClient = useQueryClient();

  const logout = useCallback(() => {
    // Le serveur efface les cookies HttpOnly même si la session a expiré.
    void api<void>("/api/auth/browser/logout", { method: "POST" }).catch(() => undefined);
    setUser(null);
    queryClient.clear();
  }, [queryClient]);

  useEffect(() => {
    setUnauthorizedHandler(logout);
    api<User>("/api/auth/me")
      .then(setUser)
      .catch(() => setUser(null))
      .finally(() => setLoading(false));
  }, [logout]);

  const accept = (data: BrowserSessionResponse) => {
    queryClient.clear();
    setUser(data.user);
  };

  const value = useMemo<AuthValue>(
    () => ({
      user,
      loading,
      logout,
      login: async (email, password) => accept(await api<BrowserSessionResponse>("/api/auth/browser/login", { method: "POST", body: { email, password } })),
      register: async (full_name, email, password) =>
        accept(await api<BrowserSessionResponse>("/api/auth/browser/register", { method: "POST", body: { full_name, email, password } })),
      isStaff: user?.role === "agent" || user?.role === "admin",
      isAdmin: user?.role === "admin",
    }),
    [user, loading, logout],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used inside AuthProvider");
  return context;
}
