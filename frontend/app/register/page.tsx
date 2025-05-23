import { RegisterForm } from "@/components/auth/register-form"
import Link from "next/link"

export default function RegisterPage() {
  return (
    <div className="flex min-h-screen flex-col">
      <div className="flex min-h-screen flex-col items-center justify-center px-4 py-8">
        <div className="mx-auto w-full max-w-md space-y-6">
          <div className="space-y-2 text-center">
            <h1 className="text-3xl font-bold">注册</h1>
            <p className="text-gray-500 dark:text-gray-400">创建您的账号以使用系统</p>
          </div>
          <RegisterForm />
          <div className="text-center text-sm">
            已有账号?{" "}
            <Link href="/login" className="underline underline-offset-4 hover:text-primary">
              登录
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
