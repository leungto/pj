"use client"

import { useEffect, useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
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
// 更新导入路径
import { reservationService as reservation, type Reservation } from "@/services/reservation"
import { Loader2, CheckSquare } from "lucide-react"
// import { format, isToday, parseISO } from "date-fns"
import { format } from "date-fns"
import { isDateToday } from "@/lib/date-utils"

export function ReservationList() {
  const [reservations, setReservations] = useState<Reservation[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // 加载预约数据
  useEffect(() => {
    const fetchReservations = async () => {
      try {
        const data = await reservation.getUserReservations()
        setReservations(data)
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

  // 取消预约
  const cancelReservation = async (id: string) => {
    try {
      await reservation.cancelReservation(id)
      setReservations(reservations.filter((reservation) => reservation.id !== id))
      toast.success("预约已取消", {
        description: "您的预约已成功取消",
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
      const updatedReservation = await reservation.checkin(id)
      setReservations(reservations.map((res) => (res.id === id ? updatedReservation : res)))
      toast.success("签到成功", {
        description: "您已成功签到",
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
    // return reservation.status === "已预约" && isToday(parseISO(reservation.date))
    return reservation.status === "已预约" && isDateToday(reservation.date)
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
  if (reservations.length === 0) {
    return (
      <div className="flex justify-center items-center h-64 flex-col gap-4">
        <p className="text-muted-foreground">您还没有任何预约</p>
        <Button asChild>
          <a href="/dashboard/reservations/new">创建新预约</a>
        </Button>
      </div>
    )
  }

  return (
    <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      {reservations.map((reservation) => (
        <Card key={reservation.id}>
          <CardHeader>
            <CardTitle>座位 {reservation.seatNumber}</CardTitle>
            <CardDescription>{reservation.location}</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-sm font-medium">日期:</span>
                <span className="text-sm">{reservation.date}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm font-medium">时间段:</span>
                <span className="text-sm">{reservation.timeSlot}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm font-medium">状态:</span>
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
              </div>
              {reservation.checkinTime && (
                <div className="flex justify-between">
                  <span className="text-sm font-medium">签到时间:</span>
                  <span className="text-sm">{format(new Date(reservation.checkinTime), "yyyy-MM-dd HH:mm")}</span>
                </div>
              )}
            </div>
          </CardContent>
          <CardFooter className="flex justify-between">
            {canCheckin(reservation) ? (
              <Button variant="outline" className="w-full" onClick={() => handleCheckin(reservation.id)}>
                <CheckSquare className="mr-2 h-4 w-4" />
                签到
              </Button>
            ) : (
              <Button variant="outline">查看详情</Button>
            )}
            {reservation.status !== "已取消" && reservation.status !== "已签到" && (
              <AlertDialog>
                <AlertDialogTrigger asChild>
                  <Button variant="destructive">取消预约</Button>
                </AlertDialogTrigger>
                <AlertDialogContent>
                  <AlertDialogHeader>
                    <AlertDialogTitle>确认取消预约?</AlertDialogTitle>
                    <AlertDialogDescription>此操作不可撤销。这将永久取消您的座位预约。</AlertDialogDescription>
                  </AlertDialogHeader>
                  <AlertDialogFooter>
                    <AlertDialogCancel>取消</AlertDialogCancel>
                    <AlertDialogAction onClick={() => cancelReservation(reservation.id)}>确认</AlertDialogAction>
                  </AlertDialogFooter>
                </AlertDialogContent>
              </AlertDialog>
            )}
          </CardFooter>
        </Card>
      ))}
    </div>
  )
}
