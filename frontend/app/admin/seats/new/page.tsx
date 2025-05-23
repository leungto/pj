import { NewSeatForm } from "@/components/seat/new-seat-form"
import { Button } from "@/components/ui/button"
import Link from "next/link"

export default function NewSeatPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">添加座位</h1>
          <p className="text-muted-foreground">在系统中添加新的座位</p>
        </div>
        <Button variant="outline" asChild>
          <Link href="/admin/seats">返回</Link>
        </Button>
      </div>
      <NewSeatForm />
    </div>
  )
}
