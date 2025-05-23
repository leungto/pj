import { API_BASE_URL, API_TIMEOUT } from "./config"
import { getAuthToken } from "./auth-utils"

/**
 * API请求错误
 */
export class ApiError extends Error {
  status: number
  data: any

  constructor(message: string, status: number, data?: any) {
    super(message)
    this.name = "ApiError"
    this.status = status
    this.data = data
  }
}

/**
 * 基础请求选项
 */
interface RequestOptions extends RequestInit {
  timeout?: number
}

/**
 * 发送API请求
 * @param endpoint API端点
 * @param options 请求选项
 * @returns 响应数据
 */
export async function apiRequest<T = any>(endpoint: string, options: RequestOptions = {}): Promise<T> {
  const { timeout = API_TIMEOUT, ...fetchOptions } = options

  // 确保headers存在
  if (!fetchOptions.headers) {
    fetchOptions.headers = {}
  }

  // 如果不是FormData，设置Content-Type
  if (fetchOptions.body && !(fetchOptions.body instanceof FormData) && !fetchOptions.headers["Content-Type"]) {
    ;(fetchOptions.headers as Record<string, string>)["Content-Type"] = "application/json"
  }

  // 添加认证令牌（如果存在）
  const token = typeof window !== "undefined" ? getAuthToken() : null
  if (token) {
    ;(fetchOptions.headers as Record<string, string>)["Authorization"] = `Bearer ${token}`
  }

  // 构建完整URL
  const url = `${API_BASE_URL}${endpoint.startsWith("/") ? endpoint : `/${endpoint}`}`

  // 创建AbortController用于超时处理
  const controller = new AbortController()
  const timeoutId = setTimeout(() => controller.abort(), timeout)

  try {
    // 发送请求
    const response = await fetch(url, {
      ...fetchOptions,
      signal: controller.signal,
      credentials: "include", // 包含跨域请求的Cookie
    })

    // 清除超时
    clearTimeout(timeoutId)

    // 解析响应数据
    const data = await response.json().catch(() => ({}))

    // 处理错误响应
    if (!response.ok) {
      throw new ApiError(data.message || `API请求失败: ${response.status}`, response.status, data)
    }

    return data as T
  } catch (error) {
    // 清除超时
    clearTimeout(timeoutId)

    // 处理超时错误
    if (error.name === "AbortError") {
      throw new ApiError("请求超时", 408)
    }

    // 重新抛出其他错误
    throw error
  }
}

/**
 * API服务
 */
export const api = {
  /**
   * 发送GET请求
   */
  get: <T = any>(endpoint: string, options: RequestOptions = {}) => {
    return apiRequest<T>(endpoint, { ...options, method: "GET" })
  },

  /**
   * 发送POST请求
   */
  post: <T = any>(endpoint: string, data?: any, options: RequestOptions = {}) => {
    const body = data instanceof FormData ? data : JSON.stringify(data)
    return apiRequest<T>(endpoint, { ...options, method: "POST", body })
  },

  /**
   * 发送PUT请求
   */
  put: <T = any>(endpoint: string, data?: any, options: RequestOptions = {}) => {
    const body = data instanceof FormData ? data : JSON.stringify(data)
    return apiRequest<T>(endpoint, { ...options, method: "PUT", body })
  },

  /**
   * 发送DELETE请求
   */
  delete: <T = any>(endpoint: string, options: RequestOptions = {}) => {
    return apiRequest<T>(endpoint, { ...options, method: "DELETE" })
  },

  /**
   * 发送PATCH请求
   */
  patch: <T = any>(endpoint: string, data?: any, options: RequestOptions = {}) => {
    const body = data instanceof FormData ? data : JSON.stringify(data)
    return apiRequest<T>(endpoint, { ...options, method: "PATCH", body })
  },
}
