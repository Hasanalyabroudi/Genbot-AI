import type React from "react"
import { UserHeader } from "@/components/user-header"

export default function UserLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="flex min-h-screen flex-col">
      <UserHeader />
      <div className="flex-1">{children}</div>
    </div>
  )
}

