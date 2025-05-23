import { NextResponse } from "next/server"
import type { NextRequest } from "next/server"

// 需要认证的路径
const protectedPaths = ["/dashboard", "/admin"]

// 需要管理员权限的路径
const adminPaths = ["/admin"]

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl
  const token = request.cookies.get("auth_token")?.value

  // 从认证令牌中获取用户角色
  // 在实际应用中，这里应该解析JWT令牌或从服务器验证
  const role = request.cookies.get("user_role")?.value

  // 检查是否是受保护的路径
  const isProtectedPath = protectedPaths.some((path) => pathname.startsWith(path))

  // 检查是否是管理员路径
  const isAdminPath = adminPaths.some((path) => pathname.startsWith(path))

  // 如果是受保护的路径但没有认证令牌，重定向到登录页面
  if (isProtectedPath && !token) {
    const url = new URL("/login", request.url)
    url.searchParams.set("callbackUrl", encodeURI(pathname))
    return NextResponse.redirect(url)
  }

  // 如果是管理员路径但用户不是管理员，重定向到仪表盘
  // 添加调试日志
  if (isAdminPath) {
    console.log(`Checking admin access: path=${pathname}, role=${role}`)
    if (role !== "admin") {
      console.log("User is not admin, redirecting from middleware")
      return NextResponse.redirect(new URL("/dashboard", request.url))
    }
  }

  // 如果已经认证但访问登录或注册页面，重定向到仪表盘
  if ((pathname === "/login" || pathname === "/register") && token) {
    return NextResponse.redirect(new URL("/dashboard", request.url))
  }

  return NextResponse.next()
}

// 配置匹配的路径
export const config = {
  matcher: ["/dashboard/:path*", "/admin/:path*", "/login", "/register"],
}
