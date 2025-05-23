import { NewReservationForm } from "@/components/reservation/new-reservation-form"
import { Button } from "@/components/ui/button"
import Link from "next/link"

export default function NewReservationPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">新预约</h1>
          <p className="text-muted-foreground">创建新的座位预约</p>
        </div>
        <Button variant="outline" asChild>
          <Link href="/dashboard/reservations">返回</Link>
        </Button>
      </div>
      <NewReservationForm />
    </div>
  )
}
