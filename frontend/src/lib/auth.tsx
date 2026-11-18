import { createContext, useCallback, useContext, useEffect, useMemo, useState, type ReactNode } from "react";
import { useQueryClient } from "@tanstack/react-query";
import { api, setUnauthorizedHandler, tokenStore } from "./api";
import type { TokenResponse, User } from "./types";

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
  const [loading, setLoading] = useState(Boolean(tokenStore.get()));
  const queryClient = useQueryClient();

  const logout = useCallback(() => {
    tokenStore.set(null);
    setUser(null);
    queryClient.clear();
  }, [queryClient]);

  useEffect(() => {
    setUnauthorizedHandler(logout);
    if (!tokenStore.get()) return;
    api<User>("/api/auth/me")
      .then(setUser)
      .catch(() => tokenStore.set(null))
      .finally(() => setLoading(false));
  }, [logout]);

  const accept = (data: TokenResponse) => {
    tokenStore.set(data.access_token);
    queryClient.clear();
    setUser(data.user);
  };

  const value = useMemo<AuthValue>(
    () => ({
      user,
      loading,
      logout,
      login: async (email, password) => accept(await api<TokenResponse>("/api/auth/login", { method: "POST", body: { email, password } })),
      register: async (full_name, email, password) =>
        accept(await api<TokenResponse>("/api/auth/register", { method: "POST", body: { full_name, email, password } })),
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
