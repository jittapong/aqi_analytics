"use client"

import { useSession } from "next-auth/react"
import { LoginButton, LogoutButton } from "@/components/AuthButtons"

export function AppBar() {
  const { data: session } = useSession()

  return (
    <header className="bg-blue-400 shadow-sm">
      <div className="mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex-shrink-0">
            <h1 className="text-lg font-semibold">AQI App</h1>
          </div>
          <nav className="flex items-center space-x-4">
            {session ? (
              <>
                <span className="text-sm text-gray-700">Signed in as {session.user?.email}</span>
                <LogoutButton />
              </>
            ) : (
              <LoginButton />
            )}
          </nav>
        </div>
      </div>
    </header>
  )
}

