import requests
import json
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from typing import Optional, Dict, Any
import colorama
from colorama import Fore, Back, Style

colorama.init()

def test_model_endpoint(base_url: str, endpoint: str = '/v1/models') -> Dict[str, Any]:
    """
    测试指定的服务端点
    
    :param base_url: 基本的 URL，不包括路径部分
    :param endpoint: 要测试的具体端点，默认为 '/v1/models'
    :return: 包含测试结果的字典
    """
    try:
        full_url = f"{base_url}{endpoint}"
        response = requests.get(full_url, timeout=10)  # 增加超时时间
        
        if response.status_code == 200 and 'application/json' in response.headers.get('Content-Type', ''):
            data = json.loads(response.text)
            models = data.get('data', [])
            return {
                'status': 'success',
                'url': full_url,
                'models_count': len(models),
                'models': models,  # 新增了models字段
                'response': data
            }
        else:
            return {
                'status': 'error',
                'url': full_url,
                'message': f"响应码: {response.status_code}, 内容类型: {response.headers.get('Content-Type', '')}"
            }
            
    except requests.exceptions.RequestException as e:
        return {
            'status': 'error',
            'url': base_url,
            'message': str(e)
        }

def print_model_info(models: list, use_color: bool = True) -> None:
    """打印模型信息，假设每个模型包含name或者其他标识符字段"""
    if not models:
        message = "无可用模型"
        if use_color:
            print(Fore.YELLOW + message + Style.RESET_ALL)
        else:
            print(message)
        return
    
    for model in models:
        model_name = model.get('name', model.get('id', '未命名模型'))
        version = model.get('version', '未指定版本')
        description = model.get('description', '')
        
        if use_color:
            prefix = Fore.CYAN + "✓" + Style.RESET_ALL
            name_color = Fore.GREEN
        else:
            prefix = "✓"
            name_color = ""
        
        print(f"{prefix} {model_name}")
        if description and (use_color or not use_color):
            if use_color:
                desc_prefix = ForeBLUE + "⚠" + Style.RESET_ALL
            else:
                desc_prefix = "⚠"
            print(f"   {desc_prefix} {description}")
        if version != '未指定版本':
            ver_str = f"Version: {version}"
            if use_color:
                print(ForeYELLOW + f"   {ver_str}" + Style.RESET_ALL)
            else:
                print(f"   {ver_str}")

def main():
    # 定义命令行参数
    parser = argparse.ArgumentParser(description='测试服务端点')
    parser.add_argument('urls_file', type=str, help='包含 URL 的文件路径')
    parser.add_argument('--endpoint', type=str, default='/v1/models',
                        help='要测试的具体端点，默认为 /v1/models')
    parser.add_argument('--max-workers', type=int, default=5,
                        help='最大并发请求数量，默认是5')
    parser.add_argument('--no-color', action='store_false',
                        dest='use_color', default=True,
                        help='禁用颜色输出，默认开启颜色')
    
    args = parser.parse_args()
    
    # 读取 URL 列表
    try:
        with open(args.urls_file, 'r') as f:
            urls = [line.strip() for line in f.readlines()]
            urls = [u for u in urls if u]  # 过滤空行
    except FileNotFoundError:
        if args.use_color:
            print(Fore.RED + "错误: 文件未找到。" + Style.RESET_ALL)
        else:
            print("错误: 文件未找到。")
        return
    
    with ThreadPoolExecutor(max_workers=args.max_workers) as executor:
        # 提交任务，使用字典记录URL到future的映射
        futures = {executor.submit(test_model_endpoint, url, args.endpoint): url for url in urls}
        
        finished_count = 0
        total_urls = len(urls)
        
        for future in as_completed(futures):
            finished_count += 1
            url = futures[future]
            
            try:
                result = future.result()
                if args.use_color:
                    color_wrapper = {
                        str: lambda s, c=Fore.GREEN: f"{c}{s}{Style.RESET_ALL}",
                        int: lambda i, c=Fore.BLUE: f"{c}{i}{Style.RESET_ALL}"
                    }
                else:
                    color_wrapper = {}
                
                status = result.get('status', '未知')
                if status == 'success':
                    print(f"URL {url} 测试通过:")
                    # 使用颜色装饰输出
                    for key in ['models_count']:
                        value = result.get(key)
                        typ = type(value)
                        stringify_func = (color_wrapper[typ]
                                        if typ in color_wrapper else str)
                        decorated_value = stringify_func(value)
                        print(f"{key}: {decorated_value}")
                    # 打印模型信息
                    models = result['models']
                    print_model_info(models, args.use_color)
                else:
                    print(f"URL {url} 测试失败:")
                    for key in ['message']:
                        value = result.get(key, '')
                        typ = type(value)
                        stringify_func = (color_wrapper[typ]
                                        if typ in color_wrapper else str)
                        decorated_value = stringify_func(value)
                        print(f"{key}: {decorated_value}")
                
                # 输出完成的进度提示
                progress = f"[{finished_count}/{total_urls}]-Complete"
                if args.use_color:
                    progress = Fore.YELLOW + progress + Style.RESET_ALL
                print(progress)
            
            except Exception as e:
                print(f"处理URL {url} 时发生错误: {e}")
                
if __name__ == "__main__":
    main()
