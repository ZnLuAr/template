// Package infra 存放外部系统与 model 接口的实现。
package infra

import (
	"time"

	"__module_path__/internal/model"
)

// SystemClock 实现 model.Clock，本包内唯一的系统时间触点。
type SystemClock struct{}

// NewSystemClock 构造 SystemClock。
func NewSystemClock() *SystemClock { return &SystemClock{} }

// CurrentHour 返回本地当前小时。
func (SystemClock) CurrentHour() int { return time.Now().Hour() }

var _ model.Clock = (*SystemClock)(nil) // 编译期断言：实现接口
