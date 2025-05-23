"use client"

import type React from "react"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { CalendarDays, Home, CheckSquare } from "lucide-react"

interface NavItem {
  title: string
  href: string
  icon: React.ComponentType<{ className?: string }>
}

// 更新 navItems 数组，添加签到选项
const navItems: NavItem[] = [
  {
    title: "仪表盘",
    href: "/dashboard",
    icon: Home,
  },
  {
    title: "我的预约",
    href: "/dashboard/reservations",
    icon: CalendarDays,
  },
  {
    title: "签到",
    href: "/dashboard/checkin",
    icon: CheckSquare,
  },
]

export function DashboardNav() {
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
