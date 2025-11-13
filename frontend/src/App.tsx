import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { SignIn, SignUp, AuthenticateWithRedirectCallback, SignedIn, SignedOut } from "@clerk/clerk-react";
import type { ReactNode } from "react";
import RequireAuth from "./components/RequireAuth";
import Index from "./pages/Index";
import NotFound from "./pages/NotFound";
import Home from "./pages/Home";

const queryClient = new QueryClient();

const AuthLayout = ({ children }: { children: ReactNode }) => (
  <div className="flex min-h-screen items-center justify-center bg-background px-4">
    <div className="w-full max-w-xl">{children}</div>
  </div>
);

const HomeRoute = () => (
  <>
    <SignedIn>
      <Navigate to="/home" replace />
    </SignedIn>
    <SignedOut>
      <Index />
    </SignedOut>
  </>
);

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<HomeRoute />} />
          <Route
            path="/sign-in/*"
            element={
              <AuthLayout>
                <SignIn routing="path" path="/sign-in" redirectUrl="/home" afterSignInUrl="/home" />
              </AuthLayout>
            }
          />
          <Route
            path="/sign-up/*"
            element={
              <AuthLayout>
                <SignUp routing="path" path="/sign-up" redirectUrl="/home" afterSignUpUrl="/home" />
              </AuthLayout>
            }
          />
          <Route
            path="/home"
            element={
              <RequireAuth redirectTo="/home">
                <Home />
              </RequireAuth>
            }
          />
          <Route path="/sso-callback" element={<AuthenticateWithRedirectCallback redirectUrl="/home" />} />
          {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
