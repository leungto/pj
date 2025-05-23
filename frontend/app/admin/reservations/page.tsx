import { AdminReservationList } from "@/components/admin/admin-reservation-list"

export default function AdminReservationsPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">预约管理</h1>
          <p className="text-muted-foreground">管理系统中的所有预约</p>
        </div>
      </div>
      <AdminReservationList />
    </div>
  )
}
