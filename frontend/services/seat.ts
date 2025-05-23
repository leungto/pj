import { api } from "@/lib/api"

// 座位状态
export type SeatStatus = "可用" | "已预约" | "维护中"

// 座位信息
export interface Seat {
  id: string
  number: string
  location: string
  status: SeatStatus
  features: string[]
  description?: string
}

// 创建座位请求
export interface CreateSeatRequest {
  number: string
  locationId: string
  features: string[]
  description?: string
}

// 更新座位状态请求
export interface UpdateSeatStatusRequest {
  status: SeatStatus
}

/**
 * 座位服务
 */
export const seatService = {
  /**
   * 获取所有座位
   */
  getAllSeats: () => {
    return api.get<Seat[]>("/seats")
  },

  /**
   * 获取可用座位
   */
  getAvailableSeats: (date: string, timeSlotId?: string) => {
    let endpoint = `/seats/available?date=${date}`
    if (timeSlotId) {
      endpoint += `&timeSlotId=${timeSlotId}`
    }
    return api.get<Seat[]>(endpoint)
  },

  /**
   * 创建新座位
   */
  createSeat: (data: CreateSeatRequest) => {
    return api.post<Seat>("/seats", data)
  },

  /**
   * 更新座位状态
   */
  updateSeatStatus: (id: string, data: UpdateSeatStatusRequest) => {
    return api.patch<Seat>(`/seats/${id}/status`, data)
  },

  /**
   * 删除座位
   */
  deleteSeat: (id: string) => {
    return api.delete(`/seats/${id}`)
  },

  /**
   * 获取座位详情
   */
  getSeat: (id: string) => {
    return api.get<Seat>(`/seats/${id}`)
  },
}
