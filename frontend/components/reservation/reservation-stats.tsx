"use client"

import { useEffect, useState } from "react"
import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis } from "recharts"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Loader2 } from "lucide-react"
// 更新导入路径
import { reservationService as reservation } from "@/services/reservation"

export function ReservationStats() {
  const [data, setData] = useState<{ name: string; total: number }[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // 加载预约统计数据
  useEffect(() => {
    const fetchReservationStats = async () => {
      try {
        const statsData = await reservation.getReservationStats()
        setData(statsData)
      } catch (err) {
        console.error("Failed to fetch reservation stats:", err)
        setError("无法加载预约统计数据")
      } finally {
        setIsLoading(false)
      }
    }

    fetchReservationStats()
  }, [])

  // 加载中状态
  if (isLoading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>预约统计</CardTitle>
          <CardDescription>本周预约数量统计</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex justify-center items-center h-[350px]">
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
          <CardTitle>预约统计</CardTitle>
          <CardDescription>本周预约数量统计</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex justify-center items-center h-[350px]">
            <p className="text-muted-foreground">{error}</p>
          </div>
        </CardContent>
      </Card>
    )
  }

  // 空状态
  if (data.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>预约统计</CardTitle>
          <CardDescription>本周预约数量统计</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex justify-center items-center h-[350px]">
            <p className="text-muted-foreground">暂无预约数据</p>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>预约统计</CardTitle>
        <CardDescription>本周预约数量统计</CardDescription>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={350}>
          <BarChart data={data}>
            <XAxis dataKey="name" stroke="#888888" fontSize={12} tickLine={false} axisLine={false} />
            <YAxis
              stroke="#888888"
              fontSize={12}
              tickLine={false}
              axisLine={false}
              tickFormatter={(value) => `${value}`}
            />
            <Bar dataKey="total" fill="currentColor" radius={[4, 4, 0, 0]} className="fill-primary" />
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}
