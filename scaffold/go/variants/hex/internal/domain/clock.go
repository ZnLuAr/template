package domain

// Clock 是端口：infra 提供实现，service 只依赖此接口。
type Clock interface {
	CurrentHour() int
}
