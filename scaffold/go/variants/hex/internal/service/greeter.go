// Package service 编排领域规则与端口，不关心 infra 的具体实现。
package service

import (
	"__module_path__/internal/domain"
)

// Greeter 是问候 use case：应用规则生成问候并记录历史；Recent 读取历史。
type Greeter struct {
	clock domain.Clock
	log   domain.GreetingLog
}

// NewGreeter 构造 Greeter；clock 与 log 由 entry 注入。
func NewGreeter(clock domain.Clock, log domain.GreetingLog) *Greeter {
	return &Greeter{clock: clock, log: log}
}

// Greet 按当前时刻问候，并把结果记入历史。
func (g *Greeter) Greet(name string) (domain.Greeting, error) {
	greeting, err := domain.GreetingFor(g.clock.CurrentHour(), name)
	if err != nil {
		return domain.Greeting{}, err
	}
	g.log.Save(greeting)
	return greeting, nil
}

// Recent 返回最近 limit 条问候，新的在前。
func (g *Greeter) Recent(limit int) []domain.Greeting {
	return g.log.Recent(limit)
}
