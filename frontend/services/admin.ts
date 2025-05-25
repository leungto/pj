import { api } from "@/lib/api"

// 管理员仪表盘统计数据
export interface DashboardStats {
  totalSeats: number
  totalUsers: number
  todayCheckinRate: number
}

/**
 * 管理员服务
 */
export const adminService = {
  /**
   * 获取管理员仪表盘统计数据
   */
  getDashboardStats: () => {
    return api.get<DashboardStats>("/admin/dashboard-stats")
  },
}
