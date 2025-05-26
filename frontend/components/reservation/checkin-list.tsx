"use client"

import { useEffect, useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { toast } from "sonner"
import { reservationService, type Reservation } from "@/services/reservation"
import { isDateToday } from "@/lib/date-utils"
import { Loader2, CheckCircle } from "lucide-react"
import { format } from "date-fns"

export function CheckinList() {
  const [reservations, setReservations] = useState<Reservation[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // 加载今日可签到的预约
  useEffect(() => {
    const fetchReservations = async () => {
      try {
        const data = await reservationService.getTodayCheckinReservations()
        setReservations(data)
      } catch (err) {
        console.error("Failed to fetch today's reservations:", err)
        setError("无法加载今日预约数据")
        toast.error("加载失败", {
          description: "无法加载今日预约数据，请稍后再试",
        })
      } finally {
        setIsLoading(false)
      }
    }

    fetchReservations()
  }, [])

  // 签到
  const handleCheckin = async (id: string) => {
    try {
      const updatedReservation = await reservationService.checkin(id)
      setReservations(reservations.map((reservation) => (reservation.id === id ? updatedReservation : reservation)))
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

  // 加载中状态
  if (isLoading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>今日预约</CardTitle>
          <CardDescription>您今天的预约列表</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex justify-center items-center h-64">
            <Loader2 className="h-8 w-8 animate-spin text-primary" />
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
          <CardTitle>今日预约</CardTitle>
          <CardDescription>您今天的预约列表</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex justify-center items-center h-64 flex-col gap-4">
            <p className="text-destructive">{error}</p>
            <Button onClick={() => window.location.reload()}>重试</Button>
          </div>
        </CardContent>
      </Card>
    )
  }

  // 空状态
  if (reservations.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>今日预约</CardTitle>
          <CardDescription>您今天的预约列表</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex justify-center items-center h-64 flex-col gap-4">
            <p className="text-muted-foreground">您今天没有预约</p>
            <Button asChild>
              <a href="/dashboard/reservations/new">创建新预约</a>
            </Button>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>今日预约</CardTitle>
        <CardDescription>您今天的预约列表</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {reservations.map((reservation) => (
            <div key={reservation.id} className="flex items-center justify-between p-4 border rounded-md">
              <div className="space-y-1">
                <p className="font-medium">座位 {reservation.seatNumber}</p>
                <p className="text-sm text-muted-foreground">{reservation.location}</p>
                <p className="text-sm text-muted-foreground">{reservation.timeSlot}</p>
              </div>
              <div className="flex flex-col items-end gap-2">
                {reservation.status === "已签到" ? (
                  <div className="flex items-center text-green-600">
                    <CheckCircle className="h-4 w-4 mr-1" />
                    <span className="text-sm">
                      已签到 {reservation.checkinTime && format(new Date(reservation.checkinTime), "HH:mm")}
                    </span>
                  </div>
                ) : (
                  <Button onClick={() => handleCheckin(reservation.id)}>签到</Button>
                )}
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
