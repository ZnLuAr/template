package model

// Clock 是接口（按需引入，见 docs/reference/layout.md 渐进条款）：infra 提供实现，logic 只依赖此接口。
type Clock interface {
	CurrentHour() int
}
