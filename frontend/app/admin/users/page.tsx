import { UserManagementList } from "@/components/admin/user-management-list"

export default function AdminUsersPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">用户管理</h1>
          <p className="text-muted-foreground">管理系统中的所有用户</p>
        </div>
      </div>
      <UserManagementList />
    </div>
  )
}
