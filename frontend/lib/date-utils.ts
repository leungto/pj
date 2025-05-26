/**
 * 日期处理工具函数
 * 统一处理日期格式化，避免时区转换问题
 */

/**
 * 将Date对象转换为YYYY-MM-DD格式的字符串
 * 使用本地时间，不进行UTC转换
 */
export function formatDateToString(date: Date): string {
    return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}

/**
 * 获取今天的日期字符串（YYYY-MM-DD格式）
 */
export function getTodayString(): string {
    return formatDateToString(new Date())
}

/**
 * 检查给定的日期字符串是否是今天
 */
export function isDateToday(dateString: string): boolean {
    return dateString === getTodayString()
}

/**
 * 格式化日期时间字符串为显示格式
 */
export function formatDateTime(dateTimeString: string, format: 'date' | 'time' | 'datetime' = 'datetime'): string {
    const date = new Date(dateTimeString)

    switch (format) {
        case 'date':
            return formatDateToString(date)
        case 'time':
            return `${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
        case 'datetime':
            return `${formatDateToString(date)} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
        default:
            return formatDateToString(date)
    }
}

/**
 * 检查日期字符串是否是今天或未来的日期
 * 用于过滤显示相关的预约
 */
export function isDateTodayOrFuture(dateString: string): boolean {
    const today = getTodayString()
    return dateString >= today
}