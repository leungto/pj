"use client"

import type React from "react"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { CalendarDays, Home, Settings, Users, LayoutDashboard } from "lucide-react"

interface NavItem {
  title: string
  href: string
  icon: React.ComponentType<{ className?: string }>
}

const navItems: NavItem[] = [
  {
    title: "管理仪表盘",
    href: "/admin",
    icon: LayoutDashboard,
  },
  {
    title: "座位管理",
    href: "/admin/seats",
    icon: Settings,
  },
  {
    title: "用户管理",
    href: "/admin/users",
    icon: Users,
  },
  {
    title: "预约管理",
    href: "/admin/reservations",
    icon: CalendarDays,
  },
  {
    title: "返回用户界面",
    href: "/dashboard",
    icon: Home,
  },
]

export function AdminNav() {
  const pathname = usePathname()

  return (
    <nav className="grid gap-2">
      {navItems.map((item) => (
        <Button
          key={item.href}
          variant={pathname === item.href ? "secondary" : "ghost"}
          className={cn("justify-start", pathname === item.href && "bg-muted font-medium")}
          asChild
        >
          <Link href={item.href}>
            <item.icon className="mr-2 h-4 w-4" />
            {item.title}
          </Link>
        </Button>
      ))}
    </nav>
  )
}
