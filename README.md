## 快递100 MCP Server (Python)
通过`uv`安装`python`，最低版本要求为3.11

```bash
uv python install 3.11
```

### 获取快递100 API KEY
登录快递100获取 ![快递100官方](https://api.kuaidi100.com/extend/register?code=d1660fe0390d4084b4f27b19d2feee02) （注意不要泄露授权key，以防被他人盗用！！！）

### 一、STDIO方式：在线获取快递100 MCP服务运行（推荐）
通过`uvx`命令一步获取kuaidi100_mcp并使用
```json
{
  "mcpServers": {
    "kuaidi100": {
      "command": "uvx",
      "args": [
        "kuaidi100-mcp"
      ],
      "env": {
        "KUAIDI100_API_KEY": "<YOUR_API_KEY>"
      }
    }
  }
}
```

### 二、STDIO方式：下载本项目至本地，配置本地项目后运行
通过`uv`创建一个项目

```bash
uv init mcp_server_kuaidi100
```

将`api_mcp.py`拷贝到该目录下，通过如下命令测试mcp server是否正常运行

```bash
uv run --with mcp[cli] mcp run {YOUR_PATH}/mcp_server_kuaidi100/api_mcp.py
# 如果是mac，需要加转义符
uv run --with mcp\[cli\] mcp run {YOUR_PATH}/mcp_server_kuaidi100/api_mcp.py
```

如果没有报错则MCP Server启动成功

#### 在支持MCP的客户端中使用
在MCP Server配置文件中添加如下内容后保存

```json
{
  "mcpServers": {
    "kuaidi100": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "mcp[cli]",
        "mcp",
        "run",
        "{YOUR_PATH}/mcp_server_kuaidi100/api_mcp.py"
      ],
      "env": {
        "KUAIDI100_API_KEY": "<YOUR_API_KEY>"
      }
    }
  }
}
```

### 三、SSE方式：
配置SSE链接和KEY后使用（可能存在客户端支持问题）
```json
"kuaidi100": {
    "url": "https://api.kuaidi100.com/mcp/sse?key=<YOUR_API_KEY>"
}
```

### 测试

#### 物流轨迹查询：
![trae_test_queryTrace.png](https://file.kuaidi100.com/downloadfile/DTjS9PHPonJXikObm8OTcEA3OnuWBw0livDDJc73jYGMQmcwqfJpKhTzSVA-UwVX9LJZE3Nnnw7iLRgmekijRw)
#### 快递预估时效：
![trae_test_estimateTime.png](https://file.kuaidi100.com/downloadfile/NL6vRCRVQkmvdavX19DISKf8uCvrj3q5NkSNl0ALv8GOOUufxrYRTRxoZJ20_uF-MGURmZRcKxS5XfAaz9t39Q)
#### 快递预估价格
![trae_test_estimatePrice.png](https://file.kuaidi100.com/downloadfile/mPv7xFAUbsY5yFbaQZn7Z0ihtIU781pksXTTj-L2wwVgZ3dH-OSvqEdm3IaJzimTF_xIWbtHD6OFP8w2i35xsQ)

### Tips
如需获取账号信息（如 key、customer、secret），或免费试用100单，请访问[API开放平台](https://api.kuaidi100.com/home?code=d1660fe0390d4084b4f27b19d2feee02)进行注册
