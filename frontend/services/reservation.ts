import { api } from "@/lib/api"

// 预约状态
export type ReservationStatus = "已预约" | "已签到" | "已取消"

// 预约信息
export interface Reservation {
  id: string
  seatId: string
  seatNumber: string
  location: string
  userId: string
  date: string
  timeSlot: string
  status: ReservationStatus
  checkinTime?: string // 签到时间
  createdAt: string
  updatedAt: string
}

// 创建预约请求
export interface CreateReservationRequest {
  seatId: string
  date: string | Date
  timeSlotId: string
}

/**
 * 预约服务
 */
export const reservationService = {
  /**
   * 获取用户的所有预约
   */
  getUserReservations: () => {
    return api.get<Reservation[]>("/reservations/user")
  },

  /**
   * 创建新预约
   */
  createReservation: (data: CreateReservationRequest) => {
    // 如果日期是Date对象，转换为ISO字符串
    const formattedData = {
      ...data,
      date: data.date instanceof Date ? data.date.toISOString().split("T")[0] : data.date,
    }
    return api.post<Reservation>("/reservations", formattedData)
  },

  /**
   * 取消预约
   */
  cancelReservation: (id: string) => {
    return api.delete<Reservation>(`/reservations/${id}`)
  },

  /**
   * 获取预约详情
   */
  getReservation: (id: string) => {
    return api.get<Reservation>(`/reservations/${id}`)
  },

  /**
   * 获取最近的预约
   */
  getRecentReservations: (limit = 5) => {
    return api.get<Reservation[]>(`/reservations/recent?limit=${limit}`)
  },

  /**
   * 获取所有最近的预约（管理员用）
   */
  getAllRecentReservations: (limit = 5) => {
    return api.get<Reservation[]>(`/reservations/all/recent?limit=${limit}`)
  },

  /**
   * 获取预约统计数据
   */
  getReservationStats: () => {
    return api.get<{ name: string; total: number }[]>("/reservations/stats")
  },

  /**
   * 签到
   */
  checkin: (id: string) => {
    return api.post<Reservation>(`/reservations/${id}/checkin`)
  },

  /**
   * 获取今日可签到的预约
   */
  getTodayCheckinReservations: () => {
    return api.get<Reservation[]>("/reservations/today-checkin")
  },

  /**
   * 获取签到统计数据
   */
  getCheckinStats: () => {
    return api.get<{ name: string; total: number; checkedIn: number }[]>("/reservations/checkin-stats")
  },
}
