// Package logic 编排业务规则与外部能力，不关心 infra 的具体实现。
package logic

import (
	"__module_path__/internal/model"
)

// Greeter 是问候业务逻辑。
type Greeter struct {
	clock model.Clock
}

// NewGreeter 构造 Greeter；clock 由 entry 注入。
func NewGreeter(clock model.Clock) *Greeter {
	return &Greeter{clock: clock}
}

// Greet 按当前时刻问候。
func (g *Greeter) Greet(name string) (string, error) {
	return model.GreetingFor(g.clock.CurrentHour(), name)
}
