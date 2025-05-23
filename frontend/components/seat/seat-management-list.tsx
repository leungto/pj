"use client"

import { useEffect, useState } from "react"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Button } from "@/components/ui/button"
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
import { Loader2, MoreHorizontal, Pencil, Trash } from "lucide-react"
// 更新导入路径
import { seatService as seat, type Seat } from "@/services/seat"

export function SeatManagementList() {
  const [seats, setSeats] = useState<Seat[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // 加载座位数据
  useEffect(() => {
    const fetchSeats = async () => {
      try {
        const data = await seat.getAllSeats()
        setSeats(data)
      } catch (err) {
        console.error("Failed to fetch seats:", err)
        setError("无法加载座位数据，请稍后再试")
        toast.error("加载失败", {
          description: "无法加载座位数据，请稍后再试",
        })
      } finally {
        setIsLoading(false)
      }
    }

    fetchSeats()
  }, [])

  // 删除座位
  const deleteSeat = async (id: string) => {
    try {
      await seat.deleteSeat(id)
      setSeats(seats.filter((seat) => seat.id !== id))
      toast.success("座位已删除", {
        description: "座位已成功从系统中删除",
      })
    } catch (err) {
      console.error("Failed to delete seat:", err)
      toast.error("删除失败", {
        description: "无法删除座位，请稍后再试",
      })
    }
  }

  // 更新座位状态
  const toggleSeatStatus = async (id: string, currentStatus: string) => {
    try {
      const newStatus = currentStatus === "可用" ? "维护中" : "可用"
      await seat.updateSeatStatus(id, { status: newStatus as any })
      setSeats(
        seats.map((seat) => {
          if (seat.id === id) {
            return { ...seat, status: newStatus as any }
          }
          return seat
        }),
      )
      toast.success("座位状态已更新", {
        description: "座位状态已成功更新",
      })
    } catch (err) {
      console.error("Failed to update seat status:", err)
      toast.error("更新失败", {
        description: "无法更新座位状态，请稍后再试",
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

  // 空状态
  if (seats.length === 0) {
    return (
      <div className="flex justify-center items-center h-64 flex-col gap-4">
        <p className="text-muted-foreground">系统中还没有任何座位</p>
        <Button asChild>
          <a href="/admin/seats/new">添加新座位</a>
        </Button>
      </div>
    )
  }

  return (
    <div className="rounded-md border">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>座位编号</TableHead>
            <TableHead>位置</TableHead>
            <TableHead>状态</TableHead>
            <TableHead>特性</TableHead>
            <TableHead className="text-right">操作</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {seats.map((seat) => (
            <TableRow key={seat.id}>
              <TableCell className="font-medium">{seat.number}</TableCell>
              <TableCell>{seat.location}</TableCell>
              <TableCell>
                <Badge
                  variant={seat.status === "可用" ? "default" : seat.status === "已预约" ? "secondary" : "destructive"}
                >
                  {seat.status}
                </Badge>
              </TableCell>
              <TableCell>
                <div className="flex flex-wrap gap-1">
                  {seat.features.map((feature, index) => (
                    <Badge key={index} variant="outline">
                      {feature}
                    </Badge>
                  ))}
                </div>
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
                    <DropdownMenuItem onClick={() => toggleSeatStatus(seat.id, seat.status)}>
                      {seat.status === "可用" ? "设为维护" : "设为可用"}
                    </DropdownMenuItem>
                    <DropdownMenuItem>
                      <Pencil className="mr-2 h-4 w-4" />
                      编辑
                    </DropdownMenuItem>
                    <DropdownMenuSeparator />
                    <AlertDialog>
                      <AlertDialogTrigger asChild>
                        <DropdownMenuItem
                          onSelect={(e) => e.preventDefault()}
                          className="text-destructive focus:text-destructive"
                        >
                          <Trash className="mr-2 h-4 w-4" />
                          删除
                        </DropdownMenuItem>
                      </AlertDialogTrigger>
                      <AlertDialogContent>
                        <AlertDialogHeader>
                          <AlertDialogTitle>确认删除座位?</AlertDialogTitle>
                          <AlertDialogDescription>
                            此操作不可撤销。这将永久删除该座位及其所有相关数据。
                          </AlertDialogDescription>
                        </AlertDialogHeader>
                        <AlertDialogFooter>
                          <AlertDialogCancel>取消</AlertDialogCancel>
                          <AlertDialogAction onClick={() => deleteSeat(seat.id)}>删除</AlertDialogAction>
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
  )
}
