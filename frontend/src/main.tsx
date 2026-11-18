import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { Toaster } from "sonner";
import App from "./App";
import { AuthProvider } from "./lib/auth";
import { ApiError } from "./lib/api";
import { useTheme } from "./lib/theme";
import "./index.css";

function ThemedToaster() {
  const { dark } = useTheme();
  return (
    <Toaster
      theme={dark ? "dark" : "light"}
      position="bottom-right"
      closeButton
      toastOptions={{ classNames: { toast: "!rounded-xl !border-line !shadow-pop !font-sans", description: "!text-muted" } }}
    />
  );
}

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 15_000,
      refetchOnWindowFocus: true,
      retry: (count, error) => !(error instanceof ApiError && error.status >= 400 && error.status < 500) && count < 2,
    },
  },
});

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <AuthProvider>
          <App />
          <ThemedToaster />
        </AuthProvider>
      </BrowserRouter>
    </QueryClientProvider>
  </StrictMode>,
);
