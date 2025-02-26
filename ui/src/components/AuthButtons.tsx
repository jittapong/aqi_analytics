"use client"

import { signIn, signOut } from "next-auth/react"
import { Button } from "@/components/ui/button"

export function LoginButton() {
  return <Button onClick={() => signIn("keycloak")}>Sign in</Button>
}

export function LogoutButton() {
  return <Button onClick={() => signOut()}>Sign out</Button>
}

