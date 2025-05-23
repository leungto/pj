"use client"

import { Button } from "@/components/ui/button"
import { useEffect } from "react"

export default function DashboardError({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  useEffect(() => {
    // 记录错误到错误报告服务
    console.error(error)
  }, [error])

  return (
    <div className="flex h-screen w-full flex-col items-center justify-center gap-4">
      <div className="text-center">
        <h2 className="text-2xl font-bold tracking-tight">出现了一些问题</h2>
        <p className="text-muted-foreground mt-2">加载仪表盘时发生错误，请重试。</p>
      </div>
      <Button onClick={reset}>重试</Button>
    </div>
  )
}
