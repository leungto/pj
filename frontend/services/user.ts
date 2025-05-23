import { api } from "@/lib/api"

// 用户角色
export type UserRole = "user" | "admin"

// 用户状态
export type UserStatus = "active" | "inactive" | "banned"

// 用户信息
export interface User {
  id: string
  name: string
  email: string
  role: string
  status: UserStatus
  createdAt: string
  updatedAt: string
  lastLoginAt?: string
}

// 更新用户角色请求
export interface UpdateUserRoleRequest {
  role: UserRole
}

// 更新用户状态请求
export interface UpdateUserStatusRequest {
  status: UserStatus
}

// 更新用户信息请求
export interface UpdateUserRequest {
  name?: string
  email?: string
  password?: string
}

// 修改密码请求
export interface ChangePasswordRequest {
  currentPassword: string
  newPassword: string
  confirmPassword: string
}

/**
 * 用户服务
 */
export const userService = {
  /**
   * 获取所有用户
   */
  getAllUsers: (params?: { q?: string; role?: string }) => {
    let endpoint = "/users"
    const queryParams = []
    
    if (params?.q) {
      queryParams.push(`q=${encodeURIComponent(params.q)}`)
    }
    
    if (params?.role) {
      queryParams.push(`role=${encodeURIComponent(params.role)}`)
    }
    
    if (queryParams.length > 0) {
      endpoint += `?${queryParams.join("&")}`
    }
    
    return api.get<User[]>(endpoint)
  },

  /**
   * 获取特定用户
   */
  getUser: (id: string) => {
    return api.get<User>(`/users/${id}`)
  },

  /**
   * 更新用户角色
   */
  updateUserRole: (id: string, data: UpdateUserRoleRequest) => {
    return api.patch<User>(`/users/${id}/role`, data)
  },

  /**
   * 更新用户状态
   */
  updateUserStatus: (id: string, data: UpdateUserStatusRequest) => {
    return api.patch<User>(`/users/${id}/status`, data)
  },

  /**
   * 更新用户信息
   */
  updateUser: (id: string, data: UpdateUserRequest) => {
    return api.put<User>(`/users/${id}`, data)
  },

  /**
   * 修改密码
   */
  changePassword: (id: string, data: ChangePasswordRequest) => {
    return api.post<{ message: string; success: boolean }>(`/users/${id}/change-password`, data)
  },

  /**
   * 删除用户
   */
  deleteUser: (id: string) => {
    return api.delete(`/users/${id}`)
  },

  /**
   * 搜索用户
   */
  searchUsers: (query: string) => {
    return api.get<User[]>(`/users/search?q=${encodeURIComponent(query)}`)
  },
}
