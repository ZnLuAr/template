package infra

import (
	"__module_path__/internal/domain"
)

// InMemoryGreetingLog 实现 domain.GreetingLog，进程内保存问候历史。
// 演示用；换文件 / DB 存储时新写 adapter 即可，domain 与 service 不动。
type InMemoryGreetingLog struct {
	items []domain.Greeting
}

// NewInMemoryGreetingLog 构造 InMemoryGreetingLog。
func NewInMemoryGreetingLog() *InMemoryGreetingLog { return &InMemoryGreetingLog{} }

// Save 追加一条问候。
func (l *InMemoryGreetingLog) Save(greeting domain.Greeting) {
	l.items = append(l.items, greeting)
}

// Recent 返回最近 limit 条问候，新的在前。
func (l *InMemoryGreetingLog) Recent(limit int) []domain.Greeting {
	if limit > len(l.items) {
		limit = len(l.items)
	}
	if limit <= 0 {
		return nil
	}
	out := make([]domain.Greeting, 0, limit)
	for i := len(l.items) - 1; i >= len(l.items)-limit; i-- {
		out = append(out, l.items[i])
	}
	return out
}

var _ domain.GreetingLog = (*InMemoryGreetingLog)(nil) // 编译期断言：实现端口
