## 项目简介

flinks 是一个 Python 脚本，旨在从给定的域名列表中生成可能存在开放重定向漏洞的 URL。该脚本通过结合常见的开放重定向参数和测试路径，生成一系列 URL，供后续的漏洞扫描工具（如 httpx 和 nuclei）使用。脚本支持 HTTP 和 HTTPS 协议，并提供去重功能，确保生成的 URL 列表中不包含重复项。

## 功能特点

- 协议支持：支持 HTTP 和 HTTPS 协议。
- 自定义参数：允许用户指定开放重定向参数和测试路径。
- 去重功能：自动去除重复的 URL，确保输出唯一。
- 错误处理：健壮的错误处理机制，确保脚本在遇到问题时能妥善处理。
- 日志记录：记录脚本执行过程，便于调试和跟踪。

## 安装要求

- Python 3.x
- 无需额外依赖库

## 使用方法

1. 克隆仓库

bash

```bash
git clone https://github.com/gguowang/flink.git
cd flinks
```



2. 准备输入文件

- 创建一个文本文件（例如 domains.txt），每行输入一个域名。

- 示例：

  ```text
  example.com
  test.com
  ```

- 运行脚本

bash

```bash
python3 flinks.py -i domains.txt -o output.txt
```

命令行参数说明：

- -i：输入文件或目录（必需）
- -o：输出文件（必需）
- -p：协议（http 或 https，默认为 http）
- --params：自定义开放重定向参数（逗号分隔，例如 redirect,url,next）
- --paths：自定义测试路径（逗号分隔，例如 /,/login,/auth）
- 示例命令

生成基于 HTTPS 协议的 URL，并使用自定义参数和路径：

bash

```bash
python3 flinks.py -i domains.txt -o output.txt -p https --params redirect,url,next --paths /,/login,/auth
```

5. 输出文件

- 生成的 URL 将保存在指定的输出文件中（例如 output.txt）。

与其他工具配合使用

该脚本生成的 URL 可以与 httpx 和 nuclei 等工具配合使用，进行开放重定向漏洞的检测。

示例流程：

bash

```bash
cat output.txt | httpx -silent | tee assets-httpx -fc 404,500
nuclei -l assets-httpx -t open-redirect.yaml
```

- httpx：过滤存活的 URL，排除状态码为 404 或 500 的响应。
- nuclei：使用 open-redirect.yaml 模板检测开放重定向漏洞。

## 贡献

欢迎提交 issue 和 pull request，帮助改进脚本功能和文档。

## 许可证

本项目采用 MIT 许可证。详情请参阅 LICENSE 文件。
