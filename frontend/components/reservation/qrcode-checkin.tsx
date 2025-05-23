"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { toast } from "sonner"
import { reservationService } from "@/services/reservation"
import { QrCode, Loader2 } from "lucide-react"

export function QRCodeCheckin() {
  const [reservationCode, setReservationCode] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  // 处理签到
  const handleCheckin = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!reservationCode.trim()) {
      toast.error("请输入预约码", {
        description: "预约码不能为空",
      })
      return
    }

    setIsLoading(true)
    try {
      // 假设预约码就是预约ID，实际应用中可能需要先解析预约码
      await reservationService.checkin(reservationCode)
      toast.success("签到成功", {
        description: "您已成功签到",
      })
      setReservationCode("")
    } catch (err) {
      console.error("Failed to check in:", err)
      toast.error("签到失败", {
        description: "无效的预约码或预约不存在",
      })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>扫码签到</CardTitle>
        <CardDescription>扫描二维码或输入预约码完成签到</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          <div className="flex justify-center">
            <div className="border border-dashed rounded-md p-6 w-48 h-48 flex items-center justify-center">
              <QrCode className="h-24 w-24 text-muted-foreground" />
            </div>
          </div>
          <form onSubmit={handleCheckin} className="space-y-4">
            <div className="space-y-2">
              <label htmlFor="reservation-code" className="text-sm font-medium">
                预约码
              </label>
              <Input
                id="reservation-code"
                placeholder="输入预约码"
                value={reservationCode}
                onChange={(e) => setReservationCode(e.target.value)}
                disabled={isLoading}
              />
            </div>
            <Button type="submit" className="w-full" disabled={isLoading}>
              {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
              签到
            </Button>
          </form>
        </div>
      </CardContent>
    </Card>
  )
}
