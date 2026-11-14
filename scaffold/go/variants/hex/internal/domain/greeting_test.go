package domain

import "testing"

func TestGreetingFor(t *testing.T) {
	tests := []struct {
		name     string
		hour     int
		expected string
	}{
		{"深夜零点", 0, "Good night, Ada."},
		{"凌晨", 4, "Good night, Ada."},
		{"清晨", 5, "Good morning, Ada."},
		{"上午", 11, "Good morning, Ada."},
		{"下午", 12, "Good afternoon, Ada."},
		{"傍晚前", 17, "Good afternoon, Ada."},
		{"傍晚", 18, "Good evening, Ada."},
		{"晚上", 22, "Good evening, Ada."},
		{"深夜", 23, "Good night, Ada."},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := GreetingFor(tt.hour, "Ada")
			if err != nil {
				t.Fatalf("GreetingFor(%d) 意外报错: %v", tt.hour, err)
			}
			if got.Text != tt.expected {
				t.Fatalf("GreetingFor(%d) = %q, 期望 %q", tt.hour, got.Text, tt.expected)
			}
		})
	}
}

func TestGreetingCarriesRuleInputs(t *testing.T) {
	got, err := GreetingFor(9, "Ada")
	if err != nil {
		t.Fatalf("GreetingFor(9) 意外报错: %v", err)
	}
	if got.Hour != 9 || got.Name != "Ada" {
		t.Fatalf("GreetingFor 应携带规则输入，实际 Hour=%d Name=%q", got.Hour, got.Name)
	}
}

func TestGreetingForRejectsInvalidHour(t *testing.T) {
	for _, hour := range []int{-1, 24, 99} {
		if _, err := GreetingFor(hour, "Ada"); err == nil {
			t.Fatalf("GreetingFor(%d) 应报错，实际成功", hour)
		}
	}
}
