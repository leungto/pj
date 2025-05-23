"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Loader2 } from "lucide-react"
import { reservationService } from "@/services/reservation"
import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis, Tooltip, Legend } from "recharts"

export function CheckinStats() {
  const [data, setData] = useState<{ name: string; total: number; checkedIn: number }[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // 加载签到统计数据
  useEffect(() => {
    const fetchCheckinStats = async () => {
      try {
        const statsData = await reservationService.getCheckinStats()
        setData(statsData)
      } catch (err) {
        console.error("Failed to fetch checkin stats:", err)
        setError("无法加载签到统计数据")
      } finally {
        setIsLoading(false)
      }
    }

    fetchCheckinStats()
  }, [])

  // 加载中状态
  if (isLoading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>签到统计</CardTitle>
          <CardDescription>预约签到情况统计</CardDescription>
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
          <CardTitle>签到统计</CardTitle>
          <CardDescription>预约签到情况统计</CardDescription>
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
          <CardTitle>签到统计</CardTitle>
          <CardDescription>预约签到情况统计</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex justify-center items-center h-[350px]">
            <p className="text-muted-foreground">暂无签到数据</p>
          </div>
        </CardContent>
      </Card>
    )
  }

  // 计算签到率
  const formattedData = data.map((item) => ({
    ...item,
    checkinRate: item.total > 0 ? Math.round((item.checkedIn / item.total) * 100) : 0,
  }))

  return (
    <Card>
      <CardHeader>
        <CardTitle>签到统计</CardTitle>
        <CardDescription>预约签到情况统计</CardDescription>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={350}>
          <BarChart data={formattedData}>
            <XAxis dataKey="name" stroke="#888888" fontSize={12} tickLine={false} axisLine={false} />
            <YAxis
              stroke="#888888"
              fontSize={12}
              tickLine={false}
              axisLine={false}
              tickFormatter={(value) => `${value}`}
            />
            <Tooltip
              formatter={(value, name) => {
                if (name === "checkinRate") return [`${value}%`, "签到率"]
                return [value, name === "total" ? "总预约数" : "已签到数"]
              }}
            />
            <Legend
              formatter={(value) => {
                if (value === "total") return "总预约数"
                if (value === "checkedIn") return "已签到数"
                return "签到率"
              }}
            />
            <Bar dataKey="total" fill="#8884d8" name="total" />
            <Bar dataKey="checkedIn" fill="#82ca9d" name="checkedIn" />
            <Bar dataKey="checkinRate" fill="#ffc658" name="checkinRate" />
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}
