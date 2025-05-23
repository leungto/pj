import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { RecentReservations } from "@/components/reservation/recent-reservations"
import { CheckinStats } from "@/components/admin/checkin-stats"

export default function AdminDashboardPage() {
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
            <div className="text-3xl font-bold">48</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle>总用户数</CardTitle>
            <CardDescription>注册用户总数</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">156</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle>今日签到率</CardTitle>
            <CardDescription>今日预约签到比例</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">78%</div>
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
