import { UserDetail } from "@/components/admin/user-detail"
import { Button } from "@/components/ui/button"
import Link from "next/link"

export default function UserDetailPage({ params }: { params: { id: string } }) {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">用户详情</h1>
          <p className="text-muted-foreground">查看和管理用户信息</p>
        </div>
        <Button variant="outline" asChild>
          <Link href="/admin/users">返回</Link>
        </Button>
      </div>
      <UserDetail userId={params.id} />
    </div>
  )
}
