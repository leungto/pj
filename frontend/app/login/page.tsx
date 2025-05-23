import { LoginForm } from "@/components/auth/login-form"
import Link from "next/link"

export default function LoginPage() {
  return (
    <div className="flex min-h-screen flex-col">
      <div className="flex min-h-screen flex-col items-center justify-center px-4 py-8">
        <div className="mx-auto w-full max-w-md space-y-6">
          <div className="space-y-2 text-center">
            <h1 className="text-3xl font-bold">登录</h1>
            <p className="text-gray-500 dark:text-gray-400">输入您的账号信息登录系统</p>
          </div>
          <LoginForm />
          <div className="text-center text-sm">
            还没有账号?{" "}
            <Link href="/register" className="underline underline-offset-4 hover:text-primary">
              注册账号
            </Link>
          </div>
          <div className="text-center text-sm">
            <Link href="/" className="underline underline-offset-4 hover:text-primary">
              返回首页
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}
