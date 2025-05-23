import { api } from "@/lib/api"

// 时间段信息
export interface TimeSlot {
  id: string
  slot: string
}

/**
 * 时间段服务
 */
export const timeSlotService = {
  /**
   * 获取所有时间段
   */
  getAllTimeSlots: () => {
    return api.get<TimeSlot[]>("/time-slots")
  },

  /**
   * 获取可用时间段
   * 根据日期和座位ID获取可用的时间段
   */
  getAvailableTimeSlots: (date: string, seatId?: string) => {
    let endpoint = `/time-slots/available?date=${date}`
    if (seatId) {
      endpoint += `&seatId=${seatId}`
    }
    return api.get<TimeSlot[]>(endpoint)
  },
}
