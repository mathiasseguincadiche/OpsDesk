const TOKEN_KEY = "opsdesk-token";

export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
  }
}

export const tokenStore = {
  get: () => {
    try { return localStorage.getItem(TOKEN_KEY); } catch { return null; }
  },
  set: (token: string | null) => {
    try {
      if (token) localStorage.setItem(TOKEN_KEY, token);
      else localStorage.removeItem(TOKEN_KEY);
    } catch { /* storage unavailable */ }
  },
};

let onUnauthorized: (() => void) | null = null;
export const setUnauthorizedHandler = (handler: () => void) => { onUnauthorized = handler; };

type Query = Record<string, string | number | boolean | string[] | undefined | null>;

function buildUrl(path: string, query?: Query) {
  const url = new URL(path, window.location.origin);
  if (query) {
    for (const [key, value] of Object.entries(query)) {
      if (value === undefined || value === null || value === "") continue;
      if (Array.isArray(value)) value.forEach((v) => url.searchParams.append(key, v));
      else url.searchParams.set(key, String(value));
    }
  }
  return url.pathname + url.search;
}

export async function api<T>(path: string, options: { method?: string; body?: unknown; query?: Query } = {}): Promise<T> {
  const headers: Record<string, string> = { Accept: "application/json" };
  const token = tokenStore.get();
  if (token) headers.Authorization = `Bearer ${token}`;
  if (options.body !== undefined) headers["Content-Type"] = "application/json";

  let response: Response;
  try {
    response = await fetch(buildUrl(path, options.query), {
      method: options.method ?? "GET",
      headers,
      body: options.body !== undefined ? JSON.stringify(options.body) : undefined,
    });
  } catch {
    throw new ApiError(0, "Impossible de joindre le serveur. Vérifiez votre connexion.");
  }

  if (response.status === 401 && token && !path.startsWith("/api/auth/login")) {
    onUnauthorized?.();
  }
  if (response.status === 204) return undefined as T;

  const data = await response.json().catch(() => null);
  if (!response.ok) {
    const detail = data?.detail;
    const message = typeof detail === "string" ? detail : `Erreur ${response.status}`;
    throw new ApiError(response.status, message);
  }
  return data as T;
}
