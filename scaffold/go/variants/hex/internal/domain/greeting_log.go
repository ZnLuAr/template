package domain

// GreetingLog 是命令型端口：问候历史的存储，infra 提供实现，service 只依赖此接口。
type GreetingLog interface {
	Save(greeting Greeting)
	Recent(limit int) []Greeting
}
