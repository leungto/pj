"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Calendar } from "@/components/ui/calendar"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { toast } from "sonner"
import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import * as z from "zod"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { cn } from "@/lib/utils"
import { format } from "date-fns"
import { CalendarIcon, Loader2 } from "lucide-react"
import { seatService as seat } from "@/services/seat"
import { timeSlotService as timeSlot, type TimeSlot } from "@/services/time-slot"
import { reservationService as reservation } from "@/services/reservation"

// 表单验证模式
const formSchema = z.object({
  seatId: z.string({
    required_error: "请选择座位",
  }),
  date: z.date({
    required_error: "请选择日期",
  }),
  timeSlotId: z.string({
    required_error: "请选择时间段",
  }),
})

export function NewReservationForm() {
  const router = useRouter()
  const [isLoading, setIsLoading] = useState(false)
  const [isLoadingSeats, setIsLoadingSeats] = useState(false)
  const [isLoadingTimeSlots, setIsLoadingTimeSlots] = useState(false)
  const [availableSeats, setAvailableSeats] = useState<{ id: string; number: string; location: string }[]>([])
  const [timeSlots, setTimeSlots] = useState<TimeSlot[]>([])

  // 初始化表单
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
  })

  // 监听日期和时间段变化，加载可用座位
  const selectedDate = form.watch("date")
  const selectedTimeSlotId = form.watch("timeSlotId")

  useEffect(() => {
    if (!selectedDate) {
      setAvailableSeats([])
      return
    }

    const fetchAvailableSeats = async () => {
      setIsLoadingSeats(true)
      try {
        const formattedDate = format(selectedDate, "yyyy-MM-dd")
        const data = await seat.getAvailableSeats(formattedDate, selectedTimeSlotId)
        setAvailableSeats(
          data.map((seat) => ({
            id: seat.id,
            number: seat.number,
            location: seat.location,
          })),
        )
      } catch (error) {
        console.error("Failed to fetch available seats:", error)
        toast.error("加载失败", {
          description: "无法加载可用座位，请稍后再试",
        })
      } finally {
        setIsLoadingSeats(false)
      }
    }

    fetchAvailableSeats()
  }, [selectedDate, selectedTimeSlotId])

  // 监听日期和座位变化，加载可用时间段
  const selectedSeatId = form.watch("seatId")

  useEffect(() => {
    if (!selectedDate) {
      setTimeSlots([])
      return
    }

    const fetchTimeSlots = async () => {
      setIsLoadingTimeSlots(true)
      try {
        const formattedDate = format(selectedDate, "yyyy-MM-dd")
        const data = await timeSlot.getAvailableTimeSlots(formattedDate, selectedSeatId)
        setTimeSlots(data)
      } catch (error) {
        console.error("Failed to fetch time slots:", error)
        toast.error("加载失败", {
          description: "无法加载可用时间段，请稍后再试",
        })
      } finally {
        setIsLoadingTimeSlots(false)
      }
    }

    fetchTimeSlots()
  }, [selectedDate, selectedSeatId])

  // 提交表单
  async function onSubmit(values: z.infer<typeof formSchema>) {
    setIsLoading(true)
    try {
      await reservation.createReservation({
        seatId: values.seatId,
        date: values.date,
        timeSlotId: values.timeSlotId,
      })
      toast.success("预约成功", {
        description: "您的座位已成功预约",
      })
      router.push("/dashboard/reservations")
    } catch (error) {
      console.error("Failed to create reservation:", error)
      toast.error("预约失败", {
        description: error instanceof Error ? error.message : "无法创建预约，请稍后再试",
      })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>预约座位</CardTitle>
        <CardDescription>选择您想要预约的座位和时间</CardDescription>
      </CardHeader>
      <CardContent>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
            <FormField
              control={form.control}
              name="date"
              render={({ field }) => (
                <FormItem className="flex flex-col">
                  <FormLabel>日期</FormLabel>
                  <Popover>
                    <PopoverTrigger asChild>
                      <FormControl>
                        <Button
                          variant={"outline"}
                          className={cn("w-full pl-3 text-left font-normal", !field.value && "text-muted-foreground")}
                        >
                          {field.value ? format(field.value, "yyyy-MM-dd") : <span>选择日期</span>}
                          <CalendarIcon className="ml-auto h-4 w-4 opacity-50" />
                        </Button>
                      </FormControl>
                    </PopoverTrigger>
                    <PopoverContent className="w-auto p-0" align="start">
                      <Calendar
                        mode="single"
                        selected={field.value}
                        onSelect={field.onChange}
                        disabled={(date) => date < new Date()}
                        initialFocus
                      />
                    </PopoverContent>
                  </Popover>
                  <FormDescription>选择您想要预约的日期</FormDescription>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="seatId"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>座位</FormLabel>
                  <Select
                    onValueChange={field.onChange}
                    defaultValue={field.value}
                    disabled={!selectedDate || isLoadingSeats}
                  >
                    <FormControl>
                      <SelectTrigger>
                        <SelectValue placeholder={isLoadingSeats ? "加载中..." : "选择座位"} />
                      </SelectTrigger>
                    </FormControl>
                    <SelectContent>
                      {isLoadingSeats ? (
                        <div className="flex items-center justify-center p-2">
                          <Loader2 className="h-4 w-4 animate-spin" />
                          <span className="ml-2">加载中...</span>
                        </div>
                      ) : availableSeats.length > 0 ? (
                        availableSeats.map((seat) => (
                          <SelectItem key={seat.id} value={seat.id}>
                            {seat.number} - {seat.location}
                          </SelectItem>
                        ))
                      ) : (
                        <div className="p-2 text-center text-muted-foreground">没有可用座位</div>
                      )}
                    </SelectContent>
                  </Select>
                  <FormDescription>选择您想要预约的座位</FormDescription>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="timeSlotId"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>时间段</FormLabel>
                  <Select
                    onValueChange={field.onChange}
                    defaultValue={field.value}
                    disabled={!selectedDate || isLoadingTimeSlots}
                  >
                    <FormControl>
                      <SelectTrigger>
                        <SelectValue placeholder={isLoadingTimeSlots ? "加载中..." : "选择时间段"} />
                      </SelectTrigger>
                    </FormControl>
                    <SelectContent>
                      {isLoadingTimeSlots ? (
                        <div className="flex items-center justify-center p-2">
                          <Loader2 className="h-4 w-4 animate-spin" />
                          <span className="ml-2">加载中...</span>
                        </div>
                      ) : timeSlots.length > 0 ? (
                        timeSlots.map((timeSlot) => (
                          <SelectItem key={timeSlot.id} value={timeSlot.id}>
                            {timeSlot.slot}
                          </SelectItem>
                        ))
                      ) : (
                        <div className="p-2 text-center text-muted-foreground">没有可用时间段</div>
                      )}
                    </SelectContent>
                  </Select>
                  <FormDescription>选择您想要预约的时间段</FormDescription>
                  <FormMessage />
                </FormItem>
              )}
            />
            <Button type="submit" disabled={isLoading}>
              {isLoading && (
                <div className="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-primary border-t-transparent"></div>
              )}
              提交预约
            </Button>
          </form>
        </Form>
      </CardContent>
    </Card>
  )
}
