import { Loader2 } from "lucide-react"

export default function DashboardLoading() {
  return (
    <div className="flex h-screen w-full items-center justify-center">
      <div className="flex flex-col items-center gap-2">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
        <p className="text-sm text-muted-foreground">加载中，请稍候...</p>
      </div>
    </div>
  )
}
