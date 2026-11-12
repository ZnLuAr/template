// Package infra 存放外部系统与端口的实现。
package infra

import (
	"time"

	"__module_path__/internal/domain"
)

// SystemClock 实现 domain.Clock，本包内唯一的系统时间触点。
type SystemClock struct{}

// NewSystemClock 构造 SystemClock。
func NewSystemClock() *SystemClock { return &SystemClock{} }

// CurrentHour 返回本地当前小时。
func (SystemClock) CurrentHour() int { return time.Now().Hour() }

var _ domain.Clock = (*SystemClock)(nil) // 编译期断言：实现端口
