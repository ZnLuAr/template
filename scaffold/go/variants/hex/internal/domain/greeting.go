// Package domain 存放纯领域规则与端口定义，零 IO，不依赖兄弟层。
package domain

import "fmt"

// GreetingFor 按一天中的时刻（0..23）生成问候语；hour 越界返回错误。
func GreetingFor(hour int, name string) (string, error) {
	if hour < 0 || hour > 23 {
		return "", fmt.Errorf("hour 必须在 0..23，收到 %d", hour)
	}
	var part string
	switch {
	case hour >= 5 && hour < 12:
		part = "Good morning"
	case hour >= 12 && hour < 18:
		part = "Good afternoon"
	case hour >= 18 && hour < 23:
		part = "Good evening"
	default:
		part = "Good night"
	}
	return fmt.Sprintf("%s, %s.", part, name), nil
}
