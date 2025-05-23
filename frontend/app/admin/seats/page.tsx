import { SeatManagementList } from "@/components/seat/seat-management-list"
import { Button } from "@/components/ui/button"
import Link from "next/link"

export default function AdminSeatsPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">座位管理</h1>
          <p className="text-muted-foreground">管理系统中的所有座位</p>
        </div>
        <Button asChild>
          <Link href="/admin/seats/new">添加座位</Link>
        </Button>
      </div>
      <SeatManagementList />
    </div>
  )
}
