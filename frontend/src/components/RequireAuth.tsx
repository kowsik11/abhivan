import { SignedIn, SignedOut, RedirectToSignIn } from "@clerk/clerk-react";
import type { ReactNode } from "react";

const RequireAuth = ({ children, redirectTo }: { children: ReactNode; redirectTo?: string }) => (
  <>
    <SignedIn>{children}</SignedIn>
    <SignedOut>
      <RedirectToSignIn redirectUrl={redirectTo} />
    </SignedOut>
  </>
);

export default RequireAuth;
