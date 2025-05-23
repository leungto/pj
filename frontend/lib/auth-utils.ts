export function saveAuthToken(token: string) {
  // 设置 Cookie，有效期为7天
  document.cookie = `auth_token=${token}; path=/; max-age=${60 * 60 * 24 * 7}; SameSite=Lax`
}

// 从 Cookie 中获取认证令牌
export function getAuthToken(): string | null {
  const cookies = document.cookie.split("; ")
  const tokenCookie = cookies.find((cookie) => cookie.startsWith("auth_token="))
  return tokenCookie ? tokenCookie.split("=")[1] : null
}

// 清除认证令牌
export function clearAuthToken() {
  document.cookie = "auth_token=; path=/; max-age=0"
}

// 检查是否已认证
export function isAuthenticated(): boolean {
  return !!getAuthToken()
}
