// Command __project_name__ 是 CLI 入口：只做参数翻译与组装，不含业务规则。
package main

import (
	"flag"
	"fmt"
	"os"

	"__module_path__/internal/infra"
	"__module_path__/internal/service"
)

func main() {
	name := flag.String("name", "world", "要问候的名字")
	recent := flag.Int("recent", 0, "问候后同时打印最近 N 条历史")
	flag.Parse()

	// 组装只发生在 entry：infra 适配器注入 service。
	greeter := service.NewGreeter(infra.NewSystemClock(), infra.NewInMemoryGreetingLog())
	greeting, err := greeter.Greet(*name)
	if err != nil {
		fmt.Fprintf(flag.CommandLine.Output(), "__project_name__: %v\n", err)
		flag.Usage()
		os.Exit(2) // 错误路径必须以非零退出码结束
	}
	fmt.Println(greeting.Text)
	for _, item := range greeter.Recent(*recent) {
		fmt.Println(item.Text)
	}
}
