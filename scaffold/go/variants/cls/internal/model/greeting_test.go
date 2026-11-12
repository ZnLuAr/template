package model

import "testing"

func TestGreetingFor(t *testing.T) {
	tests := []struct {
		hour     int
		expected string
	}{
		{0, "Good night, Ada."},
		{4, "Good night, Ada."},
		{5, "Good morning, Ada."},
		{11, "Good morning, Ada."},
		{12, "Good afternoon, Ada."},
		{17, "Good afternoon, Ada."},
		{18, "Good evening, Ada."},
		{22, "Good evening, Ada."},
		{23, "Good night, Ada."},
	}
	for _, tt := range tests {
		got, err := GreetingFor(tt.hour, "Ada")
		if err != nil || got != tt.expected {
			t.Errorf("GreetingFor(%d) = %q, %v；期望 %q", tt.hour, got, err, tt.expected)
		}
	}
}

func TestGreetingForRejectsInvalidHour(t *testing.T) {
	for _, hour := range []int{-1, 24, 99} {
		if _, err := GreetingFor(hour, "Ada"); err == nil {
			t.Errorf("GreetingFor(%d) 应报错", hour)
		}
	}
}
