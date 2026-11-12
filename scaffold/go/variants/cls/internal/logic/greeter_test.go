package logic

import "testing"

// fakeClock 是 model.Clock 替身，测试不触真实时间。
type fakeClock struct{ hour int }

func (c fakeClock) CurrentHour() int { return c.hour }

func TestGreet(t *testing.T) {
	tests := []struct {
		name     string
		hour     int
		expected string
	}{
		{"上午", 9, "Good morning, Ada."},
		{"晚上", 21, "Good evening, Ada."},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := NewGreeter(fakeClock{tt.hour}).Greet("Ada")
			if err != nil {
				t.Fatalf("Greet 意外报错: %v", err)
			}
			if got != tt.expected {
				t.Fatalf("Greet = %q, 期望 %q", got, tt.expected)
			}
		})
	}
}
