import { RedirectType } from "next/dist/client/components/redirect";
import { redirect } from "next/navigation";

type RedirectToLogin = (type?: RedirectType) => never;

export const redirectToLogin: RedirectToLogin = (type?: RedirectType) => {
  if (typeof window !== 'undefined') {
      // do your stuff with sessionStorage
      window.sessionStorage.setItem("previous-page", window.location.pathname);
  }

  redirect("/login", type);
};
