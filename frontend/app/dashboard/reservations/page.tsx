import { ReservationList } from "@/components/reservation/reservation-list"
import { Button } from "@/components/ui/button"
import Link from "next/link"

export default function ReservationsPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">我的预约</h1>
          <p className="text-muted-foreground">管理您的座位预约</p>
        </div>
        <Button asChild>
          <Link href="/dashboard/reservations/new">新预约</Link>
        </Button>
      </div>
      <ReservationList />
    </div>
  )
}
