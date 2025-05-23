"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { toast } from "sonner"
import { userService, type User } from "@/services/user"
import { Loader2 } from "lucide-react"
import { format, parseISO } from "date-fns"

interface UserDetailProps {
  userId: string
}

export function UserDetail({ userId }: UserDetailProps) {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // 加载用户数据
  useEffect(() => {
    const fetchUser = async () => {
      try {
        const data = await userService.getUser(userId)
        setUser(data)
      } catch (err) {
        console.error("Failed to fetch user:", err)
        setError("无法加载用户数据，请稍后再试")
        toast.error("加载失败", {
          description: "无法加载用户数据，请稍后再试",
        })
      } finally {
        setIsLoading(false)
      }
    }

    fetchUser()
  }, [userId])

  // 加载中状态
  if (isLoading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>用户信息</CardTitle>
          <CardDescription>加载用户信息中...</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex justify-center items-center h-32">
            <Loader2 className="h-6 w-6 animate-spin text-primary" />
          </div>
        </CardContent>
      </Card>
    )
  }

  // 错误状态
  if (error) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>用户信息</CardTitle>
          <CardDescription>加载用户信息失败</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex justify-center items-center h-32">
            <p className="text-muted-foreground">{error}</p>
          </div>
        </CardContent>
      </Card>
    )
  }

  // 用户不存在
  if (!user) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>用户信息</CardTitle>
          <CardDescription>未找到用户信息</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex justify-center items-center h-32">
            <p className="text-muted-foreground">未找到该用户</p>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>用户信息</CardTitle>
        <CardDescription>查看和管理用户信息</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex justify-between">
          <span className="text-sm font-medium">用户名:</span>
          <span className="text-sm">{user.name}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-sm font-medium">邮箱:</span>
          <span className="text-sm">{user.email}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-sm font-medium">角色:</span>
          <Badge variant={user.role === "admin" ? "default" : "secondary"}>
            {user.role === "admin" ? "管理员" : "普通用户"}
          </Badge>
        </div>
        <div className="flex justify-between">
          <span className="text-sm font-medium">状态:</span>
          <Badge
            variant={user.status === "active" ? "default" : user.status === "inactive" ? "secondary" : "destructive"}
          >
            {user.status === "active" ? "活跃" : user.status === "inactive" ? "未激活" : "已禁用"}
          </Badge>
        </div>
        <div className="flex justify-between">
          <span className="text-sm font-medium">注册时间:</span>
          <span className="text-sm">{format(parseISO(user.createdAt), "yyyy-MM-dd HH:mm")}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-sm font-medium">最后登录:</span>
          <span className="text-sm">
            {user.lastLoginAt ? format(parseISO(user.lastLoginAt), "yyyy-MM-dd HH:mm") : "从未登录"}
          </span>
        </div>
      </CardContent>
    </Card>
  )
}
