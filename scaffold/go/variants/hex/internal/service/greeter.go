// Package service 编排领域规则与端口，不关心 infra 的具体实现。
package service

import (
	"__module_path__/internal/domain"
)

// Greeter 是问候 use case。
type Greeter struct {
	clock domain.Clock
}

// NewGreeter 构造 Greeter；clock 由 entry 注入。
func NewGreeter(clock domain.Clock) *Greeter {
	return &Greeter{clock: clock}
}

// Greet 按当前时刻问候。
func (g *Greeter) Greet(name string) (string, error) {
	return domain.GreetingFor(g.clock.CurrentHour(), name)
}
