package service

import (
	"testing"

	"__module_path__/internal/domain"
)

// fakeClock 是 domain.Clock 替身，测试不触真实时间。
type fakeClock struct{ hour int }

func (c fakeClock) CurrentHour() int { return c.hour }

// fakeLog 是 domain.GreetingLog 替身，测试不触真实存储。
type fakeLog struct{ saved []domain.Greeting }

func (l *fakeLog) Save(greeting domain.Greeting) { l.saved = append(l.saved, greeting) }

func (l *fakeLog) Recent(limit int) []domain.Greeting {
	if limit > len(l.saved) {
		limit = len(l.saved)
	}
	var out []domain.Greeting
	for i := len(l.saved) - 1; i >= len(l.saved)-limit; i-- {
		out = append(out, l.saved[i])
	}
	return out
}

func TestGreetAppliesRuleAndRecordsHistory(t *testing.T) {
	log := &fakeLog{}
	greeting, err := NewGreeter(fakeClock{9}, log).Greet("Ada")
	if err != nil {
		t.Fatalf("Greet 意外报错: %v", err)
	}
	if greeting.Text != "Good morning, Ada." {
		t.Fatalf("Greet = %q, 期望 %q", greeting.Text, "Good morning, Ada.")
	}
	// 编排可见：规则被应用，副作用被记录。
	if len(log.saved) != 1 || log.saved[0] != greeting {
		t.Fatalf("Greet 应把问候记入历史，实际 %v", log.saved)
	}
}

func TestRecentReadsThroughLogPort(t *testing.T) {
	greeter := NewGreeter(fakeClock{9}, &fakeLog{})
	if _, err := greeter.Greet("Ada"); err != nil {
		t.Fatalf("Greet 意外报错: %v", err)
	}
	if _, err := greeter.Greet("Grace"); err != nil {
		t.Fatalf("Greet 意外报错: %v", err)
	}
	recent := greeter.Recent(1)
	if len(recent) != 1 || recent[0].Name != "Grace" {
		t.Fatalf("Recent(1) = %v, 期望只有 Grace", recent)
	}
}
