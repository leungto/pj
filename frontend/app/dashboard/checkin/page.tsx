import { CheckinList } from "@/components/reservation/checkin-list"
import { QRCodeCheckin } from "@/components/reservation/qrcode-checkin"

export default function CheckinPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">签到</h1>
        <p className="text-muted-foreground">为您的预约签到</p>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <QRCodeCheckin />
        <CheckinList />
      </div>
    </div>
  )
}
