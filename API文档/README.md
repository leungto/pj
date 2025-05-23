# 座位预订系统 API 文档

## 简介

本文档描述了座位预订系统的API接口规范。系统使用RESTful API风格，支持JSON格式的数据交换。

## 基础信息

- **基础URL**: `/api`
- **认证方式**: JWT (JSON Web Token)
- **数据格式**: JSON

## 通用响应格式

所有API响应均遵循以下格式：

```json
{
  "code": 200,        // HTTP状态码
  "message": "成功",  // 响应消息
  "data": {}          // 响应数据（具体格式因接口而异）
}
```

## 错误代码

系统统一的错误代码规范：

| HTTP状态码 | 错误代码范围 | 说明                     |
|------------|--------------|--------------------------| 
| 400        | 1000-1999    | 请求参数错误             |
| 401        | 2000-2999    | 认证相关错误             |
| 403        | 3000-3999    | 权限相关错误             |
| 404        | 4000-4999    | 资源不存在               |
| 409        | 5000-5999    | 资源冲突                 |
| 500        | 9000-9999    | 服务器内部错误           |

## API目录

### 用户认证
- [用户登录](用户登陆.md)
- [用户注册](用户注册.md)

### 座位管理
- 座位列表
- 座位详情
- 座位预订

### 预订管理
- 创建预订
- 取消预订
- 查看预订历史

### 管理功能
- 用户管理
- 座位配置管理
- 系统参数设置

## 认证说明

除了登录和注册接口外，所有API都需要在请求头中包含有效的认证令牌：

```
Authorization: Bearer {token}
```

未提供有效令牌的请求将收到`401 Unauthorized`错误响应。 