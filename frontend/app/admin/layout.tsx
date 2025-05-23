import type React from "react"
import { AdminNav } from "@/components/layout/admin-nav"
import { UserNav } from "@/components/layout/user-nav"
import { redirect } from "next/navigation"
import { cookies } from "next/headers"

export default async function AdminLayout({
  children,
}: {
  children: React.ReactNode
}) {
  // 获取当前用户角色
  // 在服务器组件中，我们不能直接使用客户端的authService
  // 所以我们直接从cookie中获取角色信息
  const cookieStore = cookies()
  const userRole = cookieStore.get("user_role")?.value

  // 如果不是管理员，重定向到仪表盘
  if (userRole !== "admin") {
    console.log("User is not admin, redirecting to dashboard")
    redirect("/dashboard")
  }

  return (
    <div className="flex min-h-screen flex-col">
      <header className="sticky top-0 z-10 border-b bg-background">
        <div className="flex h-16 items-center px-4 sm:px-6">
          <div className="flex items-center justify-center">
            <span className="text-xl font-bold">座位预约系统 - 管理后台</span>
          </div>
          <div className="ml-auto flex items-center space-x-4">
            <UserNav />
          </div>
        </div>
      </header>
      <div className="flex flex-1">
        <aside className="hidden w-64 border-r bg-background md:block">
          <div className="flex h-full flex-col gap-2 p-4">
            <AdminNav />
          </div>
        </aside>
        <main className="flex-1 p-4 md:p-6">{children}</main>
      </div>
    </div>
  )
}
