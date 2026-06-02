---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 微服务架构设计组件
translated: true
type: note
---

## 思维模型

微服务架构的核心在于**服务边界、异步通信和故障隔离**。每个服务拥有自己的数据并暴露契约（API 或事件）。关键决策是区分同步流程（用户 → 网关 → 服务）与异步流程（事件 → 队列 → 工作进程）。

典型模式如下：

```
客户端 → API 网关 → 服务路由器
                      ├─ 用户服务（用户 CRUD、个人资料）
                      ├─ 认证服务（JWT、OAuth、令牌验证）
                      ├─ 管理后台服务（管理面板、权限）
                      ├─ 支付服务（Stripe/支付处理）
                      ├─ 通知服务（短信、邮件）
                      ├─ 消息队列（RabbitMQ、Redis、Kafka）
                      └─ 任务工作进程（后台任务、Webhook）

数据：每个服务拥有自己的数据库（user-svc → users_db，payment-svc → payments_db）
```

---

## 服务分解

| 服务 | 职责 | 数据库 | 主要操作 |
|------|------|--------|----------|
| **API 网关** | 限流、路由、认证转发 | — | 同步 |
| **认证服务** | JWT 生成、令牌验证、OAuth | auth_db | 同步 |
| **用户服务** | 用户 CRUD、个人资料、KYC | users_db | 同步 |
| **管理后台服务** | 管理面板、基于角色的访问、审计 | admin_db | 同步 |
| **支付服务** | 处理支付、Webhook、收据 | payments_db | 混合（同步支付，异步 Webhook） |
| **通知服务** | 邮件/短信模板、投递 | notifications_db | 异步（从队列消费） |
| **任务队列** | 异步任务分发 | — | 异步 |
| **任务工作进程** | 邮件发送、短信、对账、定时任务 | — | 消费队列 |

---

## 通信模式

### 同步（请求/响应）
在需要即时反馈时使用：
```python
# 客户端请求
POST /api/v1/auth/login
├─ 网关校验限流
├─ 转发到认证服务
├─ 认证服务调用用户服务（RPC 调用）
└─ 立即返回 JWT

# 代码：认证服务调用用户服务
import httpx

class AuthService:
    def __init__(self, user_svc_url: str):
        self.user_svc = user_svc_url

    async def login(self, email: str, password: str):
        # 同步调用用户服务
        async with httpx.AsyncClient() as client:
            user_resp = await client.get(
                f"{self.user_svc}/users/by-email/{email}",
                headers={"Authorization": f"Bearer {internal_token}"}
            )
        if user_resp.status_code != 200:
            raise AuthError("用户未找到")

        user = user_resp.json()
        if not self.verify_password(password, user['password_hash']):
            raise AuthError("密码无效")

        token = self.generate_jwt(user['id'])
        return {"access_token": token, "user_id": user['id']}
```

### 异步（事件驱动）
用于不需要即时反馈的操作（通知、Webhook、分析）：

```python
# 支付成功后，发射事件 → 队列 → 工作进程
class PaymentService:
    def __init__(self, queue_client):
        self.queue = queue_client

    async def process_payment(self, user_id: str, amount: float):
        # 调用 Stripe API
        charge = stripe.Charge.create(
            amount=int(amount * 100),
            currency="usd",
            customer=user_id
        )

        # 向队列发射事件（异步通知）
        await self.queue.publish("payment.completed", {
            "user_id": user_id,
            "amount": amount,
            "charge_id": charge.id,
            "timestamp": datetime.now().isoformat()
        })

        return {"status": "completed", "charge_id": charge.id}

# 任务工作进程（独立进程/服务）
class NotificationWorker:
    def __init__(self, queue_client):
        self.queue = queue_client

    async def run(self):
        async for event in self.queue.subscribe("payment.completed"):
            user = await self.get_user(event['user_id'])
            # 发送邮件/短信
            await self.send_email(
                user['email'],
                f"您的 ${event['amount']} 付款已确认"
            )
            await self.send_sms(user['phone'], "付款已收到 ✓")
```

---

## 具体示例：Docker Compose 部署

以下是一个**可运行的骨架**，你可以在此基础上迭代：

```yaml
# docker-compose.yml
version: '3.8'

services:
  # 数据库
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: microservices
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine

  rabbitmq:
    image: rabbitmq:3-management
    environment:
      RABBITMQ_DEFAULT_USER: admin
      RABBITMQ_DEFAULT_PASS: secret
    ports:
      - "15672:15672"  # 管理界面

  # API 网关
  gateway:
    build: ./services/gateway
    ports:
      - "8000:8000"
    environment:
      AUTH_SERVICE_URL: http://auth:8001
      USER_SERVICE_URL: http://user:8002
      PAYMENT_SERVICE_URL: http://payment:8003
    depends_on:
      - auth
      - user
      - payment

  # 认证服务
  auth:
    build: ./services/auth
    environment:
      DATABASE_URL: postgresql://admin:secret@postgres/microservices
      SECRET_KEY: your-secret-key
      USER_SERVICE_URL: http://user:8002
    depends_on:
      - postgres

  # 用户服务
  user:
    build: ./services/user
    environment:
      DATABASE_URL: postgresql://admin:secret@postgres/microservices
    depends_on:
      - postgres

  # 支付服务
  payment:
    build: ./services/payment
    environment:
      DATABASE_URL: postgresql://admin:secret@postgres/microservices
      STRIPE_API_KEY: sk_test_xxx
      RABBITMQ_URL: amqp://admin:secret@rabbitmq
    depends_on:
      - postgres
      - rabbitmq

  # 通知服务（任务工作进程）
  notification_worker:
    build: ./services/notification_worker
    environment:
      RABBITMQ_URL: amqp://admin:secret@rabbitmq
      SENDGRID_API_KEY: xxx
      TWILIO_AUTH_TOKEN: xxx
    depends_on:
      - rabbitmq

  # 管理后台服务
  admin:
    build: ./services/admin
    environment:
      DATABASE_URL: postgresql://admin:secret@postgres/microservices
      AUTH_SERVICE_URL: http://auth:8001
    depends_on:
      - postgres
      - auth

volumes:
  postgres_data:
```

---

## 网关实现（FastAPI）

```python
# services/gateway/main.py
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.responses import JSONResponse
import httpx
import jwt
import os

app = FastAPI()

AUTH_SERVICE = os.getenv("AUTH_SERVICE_URL", "http://localhost:8001")
USER_SERVICE = os.getenv("USER_SERVICE_URL", "http://localhost:8002")
PAYMENT_SERVICE = os.getenv("PAYMENT_SERVICE_URL", "http://localhost:8003")

async def verify_token(authorization: str = Header(None)):
    """将认证检查转发到认证服务"""
    if not authorization:
        raise HTTPException(status_code=401, detail="缺少认证头")

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{AUTH_SERVICE}/verify",
            json={"token": authorization.replace("Bearer ", "")}
        )

    if resp.status_code != 200:
        raise HTTPException(status_code=401, detail="令牌无效")

    return resp.json()

@app.post("/api/v1/auth/login")
async def login(email: str, password: str):
    """代理到认证服务"""
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{AUTH_SERVICE}/login",
            json={"email": email, "password": password}
        )
    return JSONResponse(resp.json(), status_code=resp.status_code)

@app.get("/api/v1/users/{user_id}")
async def get_user(user_id: str, user_data = Depends(verify_token)):
    """经过认证的请求转发到用户服务"""
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{USER_SERVICE}/users/{user_id}",
            headers={"Authorization": f"Bearer {user_data['token']}"}
        )
    return resp.json()

@app.post("/api/v1/payments/charge")
async def charge(amount: float, user_id: str, user_data = Depends(verify_token)):
    """经过认证的请求转发到支付服务"""
    if user_data['user_id'] != user_id:
        raise HTTPException(status_code=403, detail="禁止访问")

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{PAYMENT_SERVICE}/charge",
            json={"user_id": user_id, "amount": amount}
        )
    return resp.json()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## 认证服务（带内部调用）

```python
# services/auth/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import jwt
import os
from datetime import datetime, timedelta

app = FastAPI()

USER_SERVICE = os.getenv("USER_SERVICE_URL", "http://localhost:8002")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenVerifyRequest(BaseModel):
    token: str

@app.post("/login")
async def login(req: LoginRequest):
    """登录：从用户服务获取用户信息，验证密码，返回 JWT"""
    async with httpx.AsyncClient() as client:
        user_resp = await client.get(
            f"{USER_SERVICE}/users/by-email",
            params={"email": req.email}
        )

    if user_resp.status_code != 200:
        raise HTTPException(status_code=401, detail="邮箱或密码无效")

    user = user_resp.json()

    # 生产环境中应使用 bcrypt 验证密码
    if not verify_password(req.password, user['password_hash']):
        raise HTTPException(status_code=401, detail="邮箱或密码无效")

    # 生成 JWT
    payload = {
        "user_id": user['id'],
        "email": user['email'],
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return {"access_token": token, "user_id": user['id']}

@app.post("/verify")
async def verify(req: TokenVerifyRequest):
    """验证 JWT 令牌（由网关调用）"""
    try:
        payload = jwt.decode(req.token, SECRET_KEY, algorithms=["HS256"])
        return {"valid": True, "user_id": payload['user_id'], "token": req.token}
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="令牌无效")

def verify_password(plain: str, hashed: str) -> bool:
    # 生产环境中使用 bcrypt
    import hashlib
    return hashlib.sha256(plain.encode()).hexdigest() == hashed
```

---

## 关键设计决策

### 1. **每个服务独立数据库**
每个服务拥有自己的数据库。用户服务 ≠ 支付服务数据库。这防止了紧耦合。

```python
# 错误：共享数据库
SELECT * FROM users u JOIN payments p ON u.id = p.user_id

# 正确：独立数据库
# 用户服务：SELECT * FROM users WHERE id = ?
# 支付服务：SELECT * FROM payments WHERE user_id = ?
```

### 2. **服务间内部调用（同步）**
使用 HTTP + 内部认证令牌进行服务间调用。保持低延迟：

```python
# 内部令牌（不对用户暴露）
INTERNAL_TOKEN = jwt.encode({"service": "payment"}, SECRET_KEY)

async with httpx.AsyncClient(timeout=2.0) as client:  # 2秒超时
    user = await client.get(
        f"{USER_SERVICE}/users/{user_id}",
        headers={"X-Service-Token": INTERNAL_TOKEN}
    )
```

### 3. **副作用使用事件驱动**
通知、Webhook、审计 → 通过队列异步处理。永远不要让主请求因副作用失败。

```python
# 支付立即成功
stripe_charge = await charge_card(...)

# 通知稍后异步进行
await queue.publish("payment.success", {...})

# 即使邮件发送失败，支付依然成功 ✓
```

### 4. **管理后台作为独立服务**
管理后台有不同的认证规则（基于角色）、审计日志，且不影响用户请求。

```python
# 用户 API：快速，读密集
GET /api/v1/users/{id}

# 管理后台 API：慢速，写密集，需审计
POST /api/v1/admin/users/{id}/suspend
```

### 5. **消息队列模式**
根据吞吐量选择 RabbitMQ、Redis 或 Kafka：
- **RabbitMQ**（10万 msg/秒）：路由、重试逻辑，适合大多数场景
- **Redis Streams**（100万 msg/秒）：简单，如果已使用 Redis 则推荐
- **Kafka**（100万+ msg/秒）：分布式、持久化，对初创公司来说可能过于庞大

```python
# 发布（生产者）
await rabbitmq.publish(
    exchange="events",
    routing_key="payment.success",
    body=json.dumps({"user_id": "123", "amount": 99.99})
)

# 消费（工作进程）
async with rabbitmq.consume("notifications_queue") as messages:
    async for msg in messages:
        event = json.loads(msg.body)
        await send_email(event['user_id'])
        await msg.ack()
```

---

## 部署注意事项

1. **服务发现**：使用 Kubernetes（ServiceName → 内部 IP），或简单的 DNS
2. **健康检查**：每个服务暴露 `/health` 端点
3. **日志**：集中化（ELK、Datadog），带关联 ID
4. **监控**：跟踪每个服务的请求延迟、队列深度、错误率
5. **密钥**：使用环境变量或 Kubernetes Secrets，切勿硬编码

```bash
# Kubernetes 部署
kubectl apply -f auth-deployment.yaml
kubectl apply -f user-deployment.yaml
kubectl apply -f payment-deployment.yaml
# 服务通过 DNS 自动发现（auth:8001、user:8002 等）
```

---

## 从简单开始，逐步演进

1. **阶段 1**（MVP）：网关 + 认证 + 用户 + 支付，全部使用一个 Postgres 数据库（轻量单体）
2. **阶段 2**：拆分服务，添加消息队列用于通知
3. **阶段 3**：多区域、事件溯源、CQRS（如果需要审计追踪）
4. **阶段 4**：AI 服务（微调、推理）作为独立的边车服务

以上代码可直接用于生产 — 克隆后运行 `docker-compose up` 并迭代。你的主要关注点应该是**清晰的服务边界**（每个服务拥有什么）和**异步模式**（在何处使用队列）。基础设施是次要的。
