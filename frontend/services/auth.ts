import { api } from "@/lib/api"
import { saveAuthToken, clearAuthToken, getAuthToken } from "@/lib/auth-utils"

// 用户登录请求参数
export interface LoginRequest {
  email: string
  password: string
}

// 用户注册请求参数
export interface RegisterRequest {
  name: string
  email: string
  password: string
  confirmPassword: string
}

// 认证响应
export interface AuthResponse {
  user: {
    id: string
    name: string
    email: string
    role: string
  }
  token: string
}

/**
 * 认证服务
 */
export const authService = {
  /**
   * 用户登录
   */
  login: (data: LoginRequest) => {
    return api.post<AuthResponse>("/auth/login", data)
  },

  /**
   * 用户注册
   */
  register: (data: RegisterRequest) => {
    return api.post<AuthResponse>("/auth/register", data)
  },

  /**
   * 获取当前用户信息
   */
  getCurrentUser: () => {
    return api.get<AuthResponse["user"]>("/auth/me")
  },

  /**
   * 退出登录
   */
  logout: () => {
    clearAuthToken()
    return Promise.resolve()
  },

  /**
   * 保存认证令牌
   */
  saveToken: (token: string) => {
    saveAuthToken(token)
  },

  /**
   * 获取认证令牌
   */
  getToken: () => {
    return typeof window !== "undefined" ? getAuthToken() : null
  },

  /**
   * 检查是否已认证
   */
  isAuthenticated: () => {
    return !!authService.getToken()
  },
}
