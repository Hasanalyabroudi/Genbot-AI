"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { LogOut } from "lucide-react";

const navItems = [
  {
    title: "Dashboard",
    href: "/user/dashboard",
  },
  {
    title: "Chatbots",
    href: "/user/chatbots",
  },
  {
    title: "Favorites",
    href: "/user/favorites",
  },
];

export function UserHeader() {
  const pathname = usePathname();

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur">
      <div className="container mx-auto flex h-14 items-center">
        <div className="mr-4 flex items-center gap-2 font-bold md:mr-6">
          <Link href="/user/dashboard" className="hidden md:block">
            <span className="text-primary">Genbot</span>
          </Link>
        </div>
        <nav className="flex flex-1 items-center gap-4 md:gap-6">
          {navItems.map((item, index) => (
            <Link
              key={index}
              href={item.href}
              className={cn(
                "text-sm font-medium px-3 py-2 rounded-md transition-all hover:bg-primary",
                pathname === item.href
                  ? "bg-primary text-black shadow-md"  // Changed from text-white to text-black
                  : "text-muted-foreground hover:text-primary"
              )}
            >
              {item.title}
            </Link>
          ))}
          <div className="ml-auto flex items-center gap-2">
            <Link href="/">
              <Button variant="outline" size="sm" className="gap-1">
                <LogOut className="h-4 w-4" />
                <span className="hidden md:inline">Logout</span>
              </Button>
            </Link>
          </div>
        </nav>
      </div>
    </header>
  );
}
