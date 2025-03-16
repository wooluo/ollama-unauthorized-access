# ollama-unauthorized-access

通过收集ollama默认开放端口，然后就可以探测含有哪些模型，因默认配置没有限制，导致可以未授权访问使用，算力会被他人使用。
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
![image](https://github.com/user-attachments/assets/c0c2b3df-281d-4c1c-8996-b119b06e9928)

可以通过模型连接工具就可以调用对方的模型了，相当于免费使用算力了。

  
