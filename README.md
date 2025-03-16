# ollama-unauthorized-access

```
ollama git:(main) ✗ source venv/bin/activate

(venv) ➜  ollama git:(main) ✗ python main.py -h       
usage: main.py [-h] [--endpoint ENDPOINT] [--max-workers MAX_WORKERS] [--no-color] urls_file

测试服务端点

positional arguments:
  urls_file             包含 URL 的文件路径

options:
  -h, --help            show this help message and exit
  --endpoint ENDPOINT   要测试的具体端点，默认为 /v1/models
  --max-workers MAX_WORKERS
                        最大并发请求数量，默认是5
  --no-color            禁用颜色输出，默认开启颜色

  ```


使用脚本探测未限制ollama模型
  ```
python main.py ip.txt --endpoint /v1/models
  ```

可以通过模型连接工具就可以调用对方的模型了，相当于免费使用算力了。

  
