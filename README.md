# flink
Open Redirect URL Generator 是一个 Python 脚本，旨在从给定的域名列表中生成可能存在开放重定向漏洞的 URL。该脚本通过结合常见的开放重定向参数和测试路径，生成一系列 URL，供后续的漏洞扫描工具（如 httpx 和 nuclei）使用。脚本支持 HTTP 和 HTTPS 协议，并提供去重功能，确保生成的 URL 列表中不包含重复项。
