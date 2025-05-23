"use client"

import { createContext, useContext, useEffect, useState, type ReactNode } from "react"
import { useRouter } from "next/navigation"
import { authService as auth } from "@/services/auth"
import { toast } from "sonner"
import { saveAuthToken, clearAuthToken, getAuthToken } from "@/lib/auth-utils"

// 用户信息
interface User {
  id: string
  name: string
  email: string
  role: string
}

// 认证上下文状态
interface AuthContextType {
  user: User | null
  isLoading: boolean
  isAuthenticated: boolean
  login: (email: string, password: string) => Promise<void>
  register: (name: string, email: string, password: string, confirmPassword: string) => Promise<void>
  logout: () => void
}

// 创建认证上下文
const AuthContext = createContext<AuthContextType | undefined>(undefined)

// 认证提供者属性
interface AuthProviderProps {
  children: ReactNode
}

// 保存用户角色到cookie
function saveUserRole(role: string) {
  document.cookie = `user_role=${role}; path=/; max-age=${60 * 60 * 24 * 7}; SameSite=Lax`
}

// 清除用户角色cookie
function clearUserRole() {
  document.cookie = "user_role=; path=/; max-age=0"
}

// 认证提供者组件
export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const router = useRouter()

  // 加载用户信息
  useEffect(() => {
    const loadUser = async () => {
      try {
        // 检查是否有认证令牌
        const token = getAuthToken()
        if (!token) {
          setIsLoading(false)
          return
        }

        // 获取当前用户信息
        const userData = await auth.getCurrentUser()
        setUser(userData)

        // 保存用户角色到cookie，以便服务器端组件和中间件可以访问
        if (userData && userData.role) {
          saveUserRole(userData.role)
          console.log(`User role saved to cookie: ${userData.role}`)
        }
      } catch (error) {
        console.error("Failed to load user:", error)
        // 如果获取用户信息失败，清除令牌和角色
        clearAuthToken()
        clearUserRole()
      } finally {
        setIsLoading(false)
      }
    }

    loadUser()
  }, [])

  // 登录
  const login = async (email: string, password: string) => {
    setIsLoading(true)
    try {
      const response = await auth.login({ email, password })
      saveAuthToken(response.token)
      setUser(response.user)

      // 保存用户角色到cookie
      if (response.user && response.user.role) {
        saveUserRole(response.user.role)
        console.log(`User role saved to cookie after login: ${response.user.role}`)
      }

      router.push("/dashboard")
    } catch (error) {
      console.error("Login failed:", error)
      toast.error("登录失败", {
        description: error.message || "请检查您的邮箱和密码",
      })
      throw error
    } finally {
      setIsLoading(false)
    }
  }

  // 注册
  const register = async (name: string, email: string, password: string, confirmPassword: string) => {
    setIsLoading(true)
    try {
      await auth.register({ name, email, password, confirmPassword })
      toast.success("注册成功", {
        description: "请使用您的新账号登录",
      })
      router.push("/login")
    } catch (error) {
      console.error("Registration failed:", error)
      toast.error("注册失败", {
        description: error.message || "请检查您的注册信息",
      })
      throw error
    } finally {
      setIsLoading(false)
    }
  }

  // 退出登录
  const logout = () => {
    clearAuthToken()
    clearUserRole()
    setUser(null)
    router.push("/login")
    toast.info("已退出登录")
  }

  // 提供上下文值
  const value = {
    user,
    isLoading,
    isAuthenticated: !!user,
    login,
    register,
    logout,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

// 使用认证上下文的钩子
export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider")
  }
  return context
}
