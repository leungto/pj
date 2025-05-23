"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Loader2, CheckSquare } from "lucide-react"
// 更新导入路径
import { reservationService as reservation, type Reservation } from "@/services/reservation"
import { Button } from "@/components/ui/button"
import { toast } from "sonner"
import { isToday, parseISO } from "date-fns"

interface RecentReservationsProps {
  isAdmin?: boolean
}

export function RecentReservations({ isAdmin = false }: RecentReservationsProps) {
  const [reservations, setReservations] = useState<Reservation[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // 加载最近预约数据
  useEffect(() => {
    const fetchRecentReservations = async () => {
      try {
        // 如果是管理员，获取所有预约；否则只获取用户自己的预约
        const data = isAdmin
          ? await reservation.getAllRecentReservations(5)
          : await reservation.getRecentReservations(3)
        setReservations(data)
      } catch (err) {
        console.error("Failed to fetch recent reservations:", err)
        setError("无法加载最近预约数据")
      } finally {
        setIsLoading(false)
      }
    }

    fetchRecentReservations()
  }, [isAdmin])

  // 签到
  const handleCheckin = async (id: string) => {
    try {
      const updatedReservation = await reservation.checkin(id)
      setReservations(reservations.map((res) => (res.id === id ? updatedReservation : res)))
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
      <Card>
        <CardHeader>
          <CardTitle>最近预约</CardTitle>
          <CardDescription>{isAdmin ? "系统中的最近预约记录" : "您最近的预约记录"}</CardDescription>
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
          <CardTitle>最近预约</CardTitle>
          <CardDescription>{isAdmin ? "系统中的最近预约记录" : "您最近的预约记录"}</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex justify-center items-center h-32">
            <p className="text-muted-foreground">{error}</p>
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
          <CardTitle>最近预约</CardTitle>
          <CardDescription>{isAdmin ? "系统中的最近预约记录" : "您最近的预约记录"}</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex justify-center items-center h-32">
            <p className="text-muted-foreground">{isAdmin ? "系统中还没有任何预约" : "您还没有任何预约"}</p>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>最近预约</CardTitle>
        <CardDescription>{isAdmin ? "系统中的最近预约记录" : "您最近的预约记录"}</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {reservations.map((reservation) => (
            <div key={reservation.id} className="flex items-center justify-between space-x-4">
              <div className="space-y-1">
                <p className="text-sm font-medium leading-none">座位 {reservation.seatNumber}</p>
                <p className="text-sm text-muted-foreground">
                  {reservation.date} {reservation.timeSlot}
                </p>
                {isAdmin && <p className="text-xs text-muted-foreground">用户: {reservation.userId}</p>}
              </div>
              <div className="flex items-center gap-2">
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
                {isAdmin && canCheckin(reservation) && (
                  <Button size="sm" variant="outline" onClick={() => handleCheckin(reservation.id)}>
                    <CheckSquare className="h-4 w-4" />
                  </Button>
                )}
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
