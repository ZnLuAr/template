package domain

// Clock 是查询型端口：当前时刻的来源，infra 提供实现，service 只依赖此接口。
type Clock interface {
	CurrentHour() int
}
