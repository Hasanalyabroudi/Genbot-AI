"use client"

import type React from "react"
import { useState } from "react"
import { useRouter } from "next/navigation"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"

export default function LoginPage() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const router = useRouter()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    // For demo purposes, simple redirect logic:
    if (email.includes("admin")) {
      router.push("/admin/dashboard")
    } else {
      router.push("/user/dashboard")
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-white px-4 py-12">
      <Card className="w-full max-w-md bg-white border border-[#24424D] shadow-xl">
        <CardHeader className="space-y-1">
          <CardTitle className="text-2xl font-bold text-[#1B708F]">Login</CardTitle>
          <CardDescription className="text-[#335F6F]">
            Enter your credentials to access your account
          </CardDescription>
        </CardHeader>
        <form onSubmit={handleSubmit}>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="email" className="text-[#335F6F]">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="name@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="bg-white border-[#66BEDE] focus:ring-[#66BEDE] text-[#1B708F] placeholder:text-[#335F6F]"
              />
            </div>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <Label htmlFor="password" className="text-[#335F6F]">Password</Label>
                <Link href="/forgot-password" className="text-sm text-[#539AB3] underline-offset-4 hover:underline">
                  Forgot password?
                </Link>
              </div>
              <Input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="bg-white border-[#66BEDE] focus:ring-[#66BEDE] text-[#1B708F] placeholder:text-[#335F6F]"
              />
            </div>
          </CardContent>
          <CardFooter className="flex flex-col space-y-4">
            <Button type="submit" className="w-full bg-[#62B7D5] hover:bg-[#539AB3] text-white">
              Login
            </Button>
            <div className="text-center text-sm text-[#335F6F]">
              Don&apos;t have an account?{" "}
              <Link href="/register" className="text-[#539AB3] underline-offset-4 hover:underline">
                Register
              </Link>
            </div>
          </CardFooter>
        </form>
      </Card>
    </div>
  )
}
