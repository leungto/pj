"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Checkbox } from "@/components/ui/checkbox"
import { toast } from "sonner"
import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import * as z from "zod"
import { Loader2 } from "lucide-react"
// 更新导入路径
import { seatService as seat } from "@/services/seat"
import { locationService as location, type Location } from "@/services/location"

// 特性数据
const features = [
  { id: "power", label: "电源插座" },
  { id: "window", label: "靠窗" },
  { id: "quiet", label: "安静区" },
  { id: "group", label: "小组讨论区" },
]

// 表单验证模式
const formSchema = z.object({
  number: z.string().min(2, {
    message: "座位编号至少需要2个字符",
  }),
  locationId: z.string({
    required_error: "请选择位置",
  }),
  features: z.array(z.string()).optional(),
  description: z.string().optional(),
})

export function NewSeatForm() {
  const router = useRouter()
  const [isLoading, setIsLoading] = useState(false)
  const [isLoadingLocations, setIsLoadingLocations] = useState(true)
  const [locations, setLocations] = useState<Location[]>([])

  // 初始化表单
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      features: [],
    },
  })

  // 加载位置数据
  useEffect(() => {
    const fetchLocations = async () => {
      try {
        const data = await location.getAllLocations()
        setLocations(data)
      } catch (error) {
        console.error("Failed to fetch locations:", error)
        toast.error("加载失败", {
          description: "无法加载位置数据，请稍后再试",
        })
      } finally {
        setIsLoadingLocations(false)
      }
    }

    fetchLocations()
  }, [])

  // 提交表单
  async function onSubmit(values: z.infer<typeof formSchema>) {
    setIsLoading(true)
    try {
      await seat.createSeat(values)
      toast.success("座位已添加", {
        description: "新座位已成功添加到系统",
      })
      router.push("/admin/seats")
    } catch (error) {
      console.error("Failed to create seat:", error)
      toast.error("添加失败", {
        description: error.message || "无法添加座位，请稍后再试",
      })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>添加新座位</CardTitle>
        <CardDescription>在系统中添加新的座位信息</CardDescription>
      </CardHeader>
      <CardContent>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
            <FormField
              control={form.control}
              name="number"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>座位编号</FormLabel>
                  <FormControl>
                    <Input placeholder="例如: A-101" {...field} />
                  </FormControl>
                  <FormDescription>输入唯一的座位编号</FormDescription>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="locationId"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>位置</FormLabel>
                  <Select onValueChange={field.onChange} defaultValue={field.value} disabled={isLoadingLocations}>
                    <FormControl>
                      <SelectTrigger>
                        <SelectValue placeholder={isLoadingLocations ? "加载中..." : "选择位置"} />
                      </SelectTrigger>
                    </FormControl>
                    <SelectContent>
                      {isLoadingLocations ? (
                        <div className="flex items-center justify-center p-2">
                          <Loader2 className="h-4 w-4 animate-spin" />
                          <span className="ml-2">加载中...</span>
                        </div>
                      ) : locations.length > 0 ? (
                        locations.map((location) => (
                          <SelectItem key={location.id} value={location.id}>
                            {location.name}
                          </SelectItem>
                        ))
                      ) : (
                        <div className="p-2 text-center text-muted-foreground">没有可用位置</div>
                      )}
                    </SelectContent>
                  </Select>
                  <FormDescription>选择座位所在的位置</FormDescription>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="features"
              render={() => (
                <FormItem>
                  <div className="mb-4">
                    <FormLabel>特性</FormLabel>
                    <FormDescription>选择座位具有的特性</FormDescription>
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    {features.map((feature) => (
                      <FormField
                        key={feature.id}
                        control={form.control}
                        name="features"
                        render={({ field }) => {
                          return (
                            <FormItem key={feature.id} className="flex flex-row items-start space-x-3 space-y-0">
                              <FormControl>
                                <Checkbox
                                  checked={field.value?.includes(feature.id)}
                                  onCheckedChange={(checked) => {
                                    return checked
                                      ? field.onChange([...(field.value || []), feature.id])
                                      : field.onChange(field.value?.filter((value) => value !== feature.id))
                                  }}
                                />
                              </FormControl>
                              <FormLabel className="font-normal">{feature.label}</FormLabel>
                            </FormItem>
                          )
                        }}
                      />
                    ))}
                  </div>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="description"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>描述</FormLabel>
                  <FormControl>
                    <Input placeholder="座位描述（可选）" {...field} />
                  </FormControl>
                  <FormDescription>添加关于座位的额外信息</FormDescription>
                  <FormMessage />
                </FormItem>
              )}
            />
            <Button type="submit" disabled={isLoading}>
              {isLoading && (
                <div className="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-primary border-t-transparent"></div>
              )}
              添加座位
            </Button>
          </form>
        </Form>
      </CardContent>
    </Card>
  )
}
