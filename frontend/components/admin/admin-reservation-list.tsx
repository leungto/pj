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
import { reservationService, type Reservation } from "@/services/reservation"
import { Loader2, MoreHorizontal, CheckSquare, Search, X } from "lucide-react"
import { format, isToday, parseISO } from "date-fns"

export function AdminReservationList() {
  const [reservations, setReservations] = useState<Reservation[]>([])
  const [filteredReservations, setFilteredReservations] = useState<Reservation[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [searchTerm, setSearchTerm] = useState("")

  // 加载所有预约
  useEffect(() => {
    const fetchReservations = async () => {
      try {
        // 这里假设有一个获取所有预约的API
        const data = await reservationService.getAllRecentReservations(100)
        setReservations(data)
        setFilteredReservations(data)
      } catch (err) {
        console.error("Failed to fetch reservations:", err)
        setError("无法加载预约数据，请稍后再试")
        toast.error("加载失败", {
          description: "无法加载预约数据，请稍后再试",
        })
      } finally {
        setIsLoading(false)
      }
    }

    fetchReservations()
  }, [])

  // 搜索过滤
  useEffect(() => {
    if (!searchTerm.trim()) {
      setFilteredReservations(reservations)
      return
    }

    const lowerSearchTerm = searchTerm.toLowerCase()
    const filtered = reservations.filter(
      (reservation) =>
        reservation.seatNumber.toLowerCase().includes(lowerSearchTerm) ||
        reservation.location.toLowerCase().includes(lowerSearchTerm) ||
        reservation.userId.toLowerCase().includes(lowerSearchTerm) ||
        reservation.date.includes(lowerSearchTerm),
    )
    setFilteredReservations(filtered)
  }, [searchTerm, reservations])

  // 取消预约
  const cancelReservation = async (id: string) => {
    try {
      await reservationService.cancelReservation(id)
      const updatedReservations = reservations.map((res) => (res.id === id ? { ...res, status: "已取消" } : res))
      setReservations(updatedReservations)
      setFilteredReservations(filteredReservations.map((res) => (res.id === id ? { ...res, status: "已取消" } : res)))
      toast.success("预约已取消", {
        description: "预约已成功取消",
      })
    } catch (err) {
      console.error("Failed to cancel reservation:", err)
      toast.error("取消失败", {
        description: "无法取消预约，请稍后再试",
      })
    }
  }

  // 签到
  const handleCheckin = async (id: string) => {
    try {
      const updatedReservation = await reservationService.checkin(id)
      const updatedReservations = reservations.map((res) => (res.id === id ? updatedReservation : res))
      setReservations(updatedReservations)
      setFilteredReservations(filteredReservations.map((res) => (res.id === id ? updatedReservation : res)))
      toast.success("签到成功", {
        description: "预约已成功签到",
      })
    } catch (err) {
      console.error("Failed to check in:", err)
      toast.error("签到失败", {
        description: "无法完成签到，请稍后再试",
      })
    }
  }

  // 检查预约是否可以签到（今天的预约且未签到）
  const canCheckin = (reservation: Reservation) => {
    return reservation.status === "已预约" && isToday(parseISO(reservation.date))
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
            placeholder="搜索预约..."
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

      {filteredReservations.length === 0 ? (
        <div className="flex justify-center items-center h-64">
          <p className="text-muted-foreground">没有找到匹配的预约</p>
        </div>
      ) : (
        <div className="rounded-md border">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>座位编号</TableHead>
                <TableHead>位置</TableHead>
                <TableHead>用户ID</TableHead>
                <TableHead>日期</TableHead>
                <TableHead>时间段</TableHead>
                <TableHead>状态</TableHead>
                <TableHead>签到时间</TableHead>
                <TableHead className="text-right">操作</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredReservations.map((reservation) => (
                <TableRow key={reservation.id}>
                  <TableCell className="font-medium">{reservation.seatNumber}</TableCell>
                  <TableCell>{reservation.location}</TableCell>
                  <TableCell>{reservation.userId}</TableCell>
                  <TableCell>{reservation.date}</TableCell>
                  <TableCell>{reservation.timeSlot}</TableCell>
                  <TableCell>
                    <Badge
                      variant={
                        reservation.status === "已签到"
                          ? "default"
                          : reservation.status === "已取消"
                            ? "destructive"
                            : "secondary"
                      }
                    >
                      {reservation.status}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    {reservation.checkinTime ? format(new Date(reservation.checkinTime), "yyyy-MM-dd HH:mm") : "-"}
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
                        {canCheckin(reservation) && (
                          <DropdownMenuItem onClick={() => handleCheckin(reservation.id)}>
                            <CheckSquare className="mr-2 h-4 w-4" />
                            签到
                          </DropdownMenuItem>
                        )}
                        {reservation.status !== "已取消" && reservation.status !== "已签到" && (
                          <>
                            <DropdownMenuSeparator />
                            <AlertDialog>
                              <AlertDialogTrigger asChild>
                                <DropdownMenuItem
                                  onSelect={(e) => e.preventDefault()}
                                  className="text-destructive focus:text-destructive"
                                >
                                  <X className="mr-2 h-4 w-4" />
                                  取消预约
                                </DropdownMenuItem>
                              </AlertDialogTrigger>
                              <AlertDialogContent>
                                <AlertDialogHeader>
                                  <AlertDialogTitle>确认取消预约?</AlertDialogTitle>
                                  <AlertDialogDescription>
                                    此操作不可撤销。这将永久取消该座位预约。
                                  </AlertDialogDescription>
                                </AlertDialogHeader>
                                <AlertDialogFooter>
                                  <AlertDialogCancel>取消</AlertDialogCancel>
                                  <AlertDialogAction onClick={() => cancelReservation(reservation.id)}>
                                    确认
                                  </AlertDialogAction>
                                </AlertDialogFooter>
                              </AlertDialogContent>
                            </AlertDialog>
                          </>
                        )}
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
