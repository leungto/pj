import { api } from "@/lib/api"

// 位置信息
export interface Location {
  id: string
  name: string
}

/**
 * 位置服务
 */
export const locationService = {
  /**
   * 获取所有位置
   */
  getAllLocations: () => {
    return api.get<Location[]>("/locations")
  },
}
