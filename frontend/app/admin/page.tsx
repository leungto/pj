"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { RecentReservations } from "@/components/reservation/recent-reservations"
import { CheckinStats } from "@/components/admin/checkin-stats"
import { Loader2 } from "lucide-react"
import { adminService, type DashboardStats } from "@/services/admin"

export default function AdminDashboardPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // 加载统计数据
  useEffect(() => {
    const fetchStats = async () => {
      try {
        const data = await adminService.getDashboardStats()
        setStats(data)
      } catch (err) {
        console.error("Failed to fetch dashboard stats:", err)
        setError("无法加载统计数据")
      } finally {
        setIsLoading(false)
      }
    }

    fetchStats()
  }, [])
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">管理员仪表盘</h1>
        <p className="text-muted-foreground">管理系统和查看统计数据</p>
      </div>
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle>总座位数</CardTitle>
            <CardDescription>系统中的座位总数</CardDescription>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <div className="flex items-center space-x-2">
                <Loader2 className="h-4 w-4 animate-spin" />
                <span className="text-muted-foreground">加载中...</span>
              </div>
            ) : error ? (
              <div className="text-destructive">加载失败</div>
            ) : (
              <div className="text-3xl font-bold">{stats?.totalSeats || 0}</div>
            )}
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle>总用户数</CardTitle>
            <CardDescription>注册用户总数</CardDescription>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <div className="flex items-center space-x-2">
                <Loader2 className="h-4 w-4 animate-spin" />
                <span className="text-muted-foreground">加载中...</span>
              </div>
            ) : error ? (
              <div className="text-destructive">加载失败</div>
            ) : (
              <div className="text-3xl font-bold">{stats?.totalUsers || 0}</div>
            )}
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle>今日签到率</CardTitle>
            <CardDescription>今日预约签到比例</CardDescription>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <div className="flex items-center space-x-2">
                <Loader2 className="h-4 w-4 animate-spin" />
                <span className="text-muted-foreground">加载中...</span>
              </div>
            ) : error ? (
              <div className="text-destructive">加载失败</div>
            ) : (
              <div className="text-3xl font-bold">{stats?.todayCheckinRate || 0}%</div>
            )}
          </CardContent>
        </Card>
      </div>
      <div className="grid gap-6 md:grid-cols-2">
        <CheckinStats />
        <RecentReservations isAdmin={true} />
      </div>
    </div>
  )
}
