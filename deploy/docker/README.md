# Docker 容器化

在仓库根目录执行：

```bash
docker build -t llmops-lab-api:dev .
docker run --rm -p 8000:8000 llmops-lab-api:dev
curl -fsS http://127.0.0.1:8000/health
```

镜像使用 UID/GID 10001 的非 root 用户运行，且只安装应用运行所需的依赖。

用于生产环境前，建议：
- 将基础镜像固定到经过验证的版本或 digest。
- 扫描镜像中的漏洞，并建立镜像更新流程。
- 配置 CPU、内存等资源限制。
- 如果 API 暴露在本机可信环境之外，应通过带认证与访问控制的入口提供服务。
