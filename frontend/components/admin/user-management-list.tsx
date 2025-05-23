"use client"

import { useEffect, useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { toast } from "sonner"
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { userService, type User, type UserRole, type UserStatus } from "@/services/user"
import { Loader2, MoreHorizontal, Search, X, UserCog, ShieldCheck, Ban } from "lucide-react"
import { format, parseISO } from "date-fns"

export function UserManagementList() {
  const [users, setUsers] = useState<User[]>([])
  const [filteredUsers, setFilteredUsers] = useState<User[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [searchTerm, setSearchTerm] = useState("")

  // 加载用户数据
  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const data = await userService.getAllUsers()
        setUsers(data)
        setFilteredUsers(data)
      } catch (err) {
        console.error("Failed to fetch users:", err)
        setError("无法加载用户数据，请稍后再试")
        toast.error("加载失败", {
          description: "无法加载用户数据，请稍后再试",
        })
      } finally {
        setIsLoading(false)
      }
    }

    fetchUsers()
  }, [])

  // 搜索过滤
  useEffect(() => {
    if (!searchTerm.trim()) {
      setFilteredUsers(users)
      return
    }

    const lowerSearchTerm = searchTerm.toLowerCase()
    const filtered = users.filter(
      (user) =>
        user.name.toLowerCase().includes(lowerSearchTerm) ||
        user.email.toLowerCase().includes(lowerSearchTerm) ||
        user.id.toLowerCase().includes(lowerSearchTerm),
    )
    setFilteredUsers(filtered)
  }, [searchTerm, users])

  // 删除用户
  const deleteUser = async (id: string) => {
    try {
      await userService.deleteUser(id)
      setUsers(users.filter((user) => user.id !== id))
      setFilteredUsers(filteredUsers.filter((user) => user.id !== id))
      toast.success("用户已删除", {
        description: "用户已成功从系统中删除",
      })
    } catch (err) {
      console.error("Failed to delete user:", err)
      toast.error("删除失败", {
        description: "无法删除用户，请稍后再试",
      })
    }
  }

  // 更新用户角色
  const updateUserRole = async (id: string, role: UserRole) => {
    try {
      const updatedUser = await userService.updateUserRole(id, { role })
      setUsers(users.map((user) => (user.id === id ? updatedUser : user)))
      setFilteredUsers(filteredUsers.map((user) => (user.id === id ? updatedUser : user)))
      toast.success("角色已更新", {
        description: `用户角色已更新为 ${role === "admin" ? "管理员" : "普通用户"}`,
      })
    } catch (err) {
      console.error("Failed to update user role:", err)
      toast.error("更新失败", {
        description: "无法更新用户角色，请稍后再试",
      })
    }
  }

  // 更新用户状态
  const updateUserStatus = async (id: string, status: UserStatus) => {
    try {
      const updatedUser = await userService.updateUserStatus(id, { status })
      setUsers(users.map((user) => (user.id === id ? updatedUser : user)))
      setFilteredUsers(filteredUsers.map((user) => (user.id === id ? updatedUser : user)))

      let statusText = "活跃"
      if (status === "inactive") statusText = "未激活"
      if (status === "banned") statusText = "已禁用"

      toast.success("状态已更新", {
        description: `用户状态已更新为${statusText}`,
      })
    } catch (err) {
      console.error("Failed to update user status:", err)
      toast.error("更新失败", {
        description: "无法更新用户状态，请稍后再试",
      })
    }
  }

  // 加载中状态
  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    )
  }

  // 错误状态
  if (error) {
    return (
      <div className="flex justify-center items-center h-64 flex-col gap-4">
        <p className="text-destructive">{error}</p>
        <Button onClick={() => window.location.reload()}>重试</Button>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2">
        <div className="relative flex-1">
          <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input
            type="search"
            placeholder="搜索用户..."
            className="pl-8"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
          {searchTerm && (
            <Button
              variant="ghost"
              size="sm"
              className="absolute right-0 top-0 h-full px-3"
              onClick={() => setSearchTerm("")}
            >
              <X className="h-4 w-4" />
              <span className="sr-only">清除</span>
            </Button>
          )}
        </div>
      </div>

      {filteredUsers.length === 0 ? (
        <div className="flex justify-center items-center h-64">
          <p className="text-muted-foreground">没有找到匹配的用户</p>
        </div>
      ) : (
        <div className="rounded-md border">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>用户名</TableHead>
                <TableHead>邮箱</TableHead>
                <TableHead>角色</TableHead>
                <TableHead>状态</TableHead>
                <TableHead>注册时间</TableHead>
                <TableHead>最后登录</TableHead>
                <TableHead className="text-right">操作</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredUsers.map((user) => (
                <TableRow key={user.id}>
                  <TableCell className="font-medium">{user.name}</TableCell>
                  <TableCell>{user.email}</TableCell>
                  <TableCell>
                    <Badge variant={user.role === "admin" ? "default" : "secondary"}>
                      {user.role === "admin" ? "管理员" : "普通用户"}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <Badge
                      variant={
                        user.status === "active" ? "default" : user.status === "inactive" ? "secondary" : "destructive"
                      }
                    >
                      {user.status === "active" ? "活跃" : user.status === "inactive" ? "未激活" : "已禁用"}
                    </Badge>
                  </TableCell>
                  <TableCell>{format(parseISO(user.createdAt), "yyyy-MM-dd")}</TableCell>
                  <TableCell>
                    {user.lastLoginAt ? format(parseISO(user.lastLoginAt), "yyyy-MM-dd HH:mm") : "从未登录"}
                  </TableCell>
                  <TableCell className="text-right">
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button variant="ghost" className="h-8 w-8 p-0">
                          <span className="sr-only">打开菜单</span>
                          <MoreHorizontal className="h-4 w-4" />
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuLabel>操作</DropdownMenuLabel>
                        <DropdownMenuItem
                          onClick={() => updateUserRole(user.id, user.role === "admin" ? "user" : "admin")}
                        >
                          {user.role === "admin" ? (
                            <>
                              <UserCog className="mr-2 h-4 w-4" />
                              设为普通用户
                            </>
                          ) : (
                            <>
                              <ShieldCheck className="mr-2 h-4 w-4" />
                              设为管理员
                            </>
                          )}
                        </DropdownMenuItem>
                        <DropdownMenuSeparator />
                        {user.status !== "active" && (
                          <DropdownMenuItem onClick={() => updateUserStatus(user.id, "active")}>
                            <ShieldCheck className="mr-2 h-4 w-4" />
                            激活用户
                          </DropdownMenuItem>
                        )}
                        {user.status !== "banned" && (
                          <DropdownMenuItem onClick={() => updateUserStatus(user.id, "banned")}>
                            <Ban className="mr-2 h-4 w-4" />
                            禁用用户
                          </DropdownMenuItem>
                        )}
                        <DropdownMenuSeparator />
                        <AlertDialog>
                          <AlertDialogTrigger asChild>
                            <DropdownMenuItem
                              onSelect={(e) => e.preventDefault()}
                              className="text-destructive focus:text-destructive"
                            >
                              <X className="mr-2 h-4 w-4" />
                              删除用户
                            </DropdownMenuItem>
                          </AlertDialogTrigger>
                          <AlertDialogContent>
                            <AlertDialogHeader>
                              <AlertDialogTitle>确认删除用户?</AlertDialogTitle>
                              <AlertDialogDescription>
                                此操作不可撤销。这将永久删除该用户及其所有相关数据。
                              </AlertDialogDescription>
                            </AlertDialogHeader>
                            <AlertDialogFooter>
                              <AlertDialogCancel>取消</AlertDialogCancel>
                              <AlertDialogAction onClick={() => deleteUser(user.id)}>删除</AlertDialogAction>
                            </AlertDialogFooter>
                          </AlertDialogContent>
                        </AlertDialog>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      )}
    </div>
  )
}
