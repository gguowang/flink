#!/usr/bin/env python3
import argparse
import os
import logging
from urllib.parse import urljoin

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 默认的开放重定向参数
DEFAULT_REDIRECT_PARAMS = [
    "redirect", "url", "next", "target", "dest", "goto", "return", "to", 
    "callback", "redir", "redirect_uri", "redirect_url", "link", "out"
]

# 默认的测试路径
DEFAULT_TEST_PATHS = ["/", "/login", "/redirect", "/auth", "/home"]

def generate_redirect_urls(domain, protocol="http", params=DEFAULT_REDIRECT_PARAMS, paths=DEFAULT_TEST_PATHS):
    """为单个域名生成带有开放重定向参数的 URL"""
    urls = set()  # 使用集合存储 URL，确保单个域名生成的 URL 不重复
    domain = domain.strip()
    if not domain.startswith("http"):
        domain = f"{protocol}://{domain}"  # 添加协议前缀

    # 对每个测试路径和参数生成 URL
    for path in paths:
        for param in params:
            # 生成不带具体重定向目标的 URL，例如：http://example.com/login?redirect=
            url = urljoin(domain, path) + f"?{param}="
            urls.add(url)
    
    return urls

def process_input(input_path, output_file, protocol, params, paths):
    """处理输入文件并生成去重后的 URL 输出"""
    all_urls = set()  # 全局集合，用于存储所有唯一的 URL

    # 检查输入是文件还是目录
    if os.path.isfile(input_path):
        files = [input_path]
    elif os.path.isdir(input_path):
        files = [os.path.join(input_path, f) for f in os.listdir(input_path) if f.endswith(".txt")]
    else:
        logging.error(f"{input_path} 不是有效的文件或目录")
        return

    # 检查输出文件是否可写
    try:
        with open(output_file, "w") as out_f:
            pass
    except Exception as e:
        logging.error(f"无法写入输出文件 {output_file}: {e}")
        return

    # 处理每个文件
    for file in files:
        try:
            with open(file, "r") as in_f:
                for line in in_f:
                    domain = line.strip()
                    if domain:
                        urls = generate_redirect_urls(domain, protocol, params, paths)
                        all_urls.update(urls)  # 将生成的 URL 添加到全局集合
        except Exception as e:
            logging.error(f"处理文件 {file} 时出错: {e}")

    # 将去重后的 URL 写入输出文件
    with open(output_file, "w") as out_f:
        for url in sorted(all_urls):  # 按字母顺序排序，便于查看
            out_f.write(url + "\n")

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="从域名列表生成潜在的开放重定向 URL")
    parser.add_argument("-i", "--input", required=True, help="包含域名的输入文件或目录")
    parser.add_argument("-o", "--output", required=True, help="保存生成的 URL 的输出文件")
    parser.add_argument("-p", "--protocol", default="http", choices=["http", "https"], help="协议（http 或 https）")
    parser.add_argument("--params", help="自定义开放重定向参数列表（逗号分隔）")
    parser.add_argument("--paths", help="自定义测试路径列表（逗号分隔）")
    args = parser.parse_args()

    # 处理参数
    params = args.params.split(",") if args.params else DEFAULT_REDIRECT_PARAMS
    paths = args.paths.split(",") if args.paths else DEFAULT_TEST_PATHS

    # 处理输入并生成输出
    process_input(args.input, args.output, args.protocol, params, paths)
    logging.info(f"生成的唯一 URL 已保存到 {args.output}")

if __name__ == "__main__":
    main()
