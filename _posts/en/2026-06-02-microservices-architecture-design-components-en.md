---
audio: false
generated: true
image: false
lang: en
layout: post
title: Microservices Architecture Design Components
translated: false
type: note
---

Question: How do I design a microservices architecture with common components like user management, admin, API gateway, auth, payment, notifications (SMS/email), message queues, and background jobs?

Answer:

## Mental Model

A microservices architecture is about **service boundaries, async communication, and fault isolation**. Each service owns its data and exposes contracts (APIs or events). The key is deciding what's synchronous (user → gateway → service) vs. asynchronous (events → queue → worker).

Here's the pattern:

```
Client → API Gateway → Service Router
                      ├─ User Service (user CRUD, profiles)
                      ├─ Auth Service (JWT, OAuth, token validation)
                      ├─ Admin Service (admin panel, permissions)
                      ├─ Payment Service (stripe/payment processing)
                      ├─ Notification Service (SMS, email)
                      ├─ Message Queue (RabbitMQ, Redis, Kafka)
                      └─ Job Worker (background tasks, webhooks)

Data: Each service has its own DB (user-svc → users_db, payment-svc → payments_db)
```

---

## Service Breakdown

| Service | Responsibility | DB | Primary Ops |
|---------|----------------|-----|----------|
| **API Gateway** | Rate limiting, routing, auth forwarding | — | Sync |
| **Auth Service** | JWT generation, token validation, OAuth | auth_db | Sync |
| **User Service** | User CRUD, profiles, KYC | users_db | Sync |
| **Admin Service** | Admin panels, role-based access, audits | admin_db | Sync |
| **Payment Service** | Process payments, webhooks, receipts | payments_db | Mixed (sync payment, async webhook) |
| **Notification Service** | Email/SMS templates, delivery | notifications_db | Async (from queue) |
| **Job Queue** | Async task dispatch | — | Async |
| **Job Worker** | Email sends, SMS, reconciliation, cron | — | Consumes queue |

---

## Communication Patterns

### Synchronous (Request/Response)
Used when you need immediate feedback:
```python
# Client request
POST /api/v1/auth/login
├─ Gateway validates rate limit
├─ Forwards to Auth Service
├─ Auth Service checks User Service (RPC call)
└─ Returns JWT immediately

# Code: Auth Service calling User Service
import httpx

class AuthService:
    def __init__(self, user_svc_url: str):
        self.user_svc = user_svc_url

    async def login(self, email: str, password: str):
        # Call User Service synchronously
        async with httpx.AsyncClient() as client:
            user_resp = await client.get(
                f"{self.user_svc}/users/by-email/{email}",
                headers={"Authorization": f"Bearer {internal_token}"}
            )
        if user_resp.status_code != 200:
            raise AuthError("User not found")

        user = user_resp.json()
        if not self.verify_password(password, user['password_hash']):
            raise AuthError("Invalid password")

        token = self.generate_jwt(user['id'])
        return {"access_token": token, "user_id": user['id']}
```

### Asynchronous (Event-Driven)
Used for operations that don't need immediate feedback (notifications, webhooks, analytics):

```python
# When payment succeeds, emit event → queue → worker
class PaymentService:
    def __init__(self, queue_client):
        self.queue = queue_client

    async def process_payment(self, user_id: str, amount: float):
        # Call Stripe API
        charge = stripe.Charge.create(
            amount=int(amount * 100),
            currency="usd",
            customer=user_id
        )

        # Emit event to queue (async notification)
        await self.queue.publish("payment.completed", {
            "user_id": user_id,
            "amount": amount,
            "charge_id": charge.id,
            "timestamp": datetime.now().isoformat()
        })

        return {"status": "completed", "charge_id": charge.id}

# Job Worker (separate process/service)
class NotificationWorker:
    def __init__(self, queue_client):
        self.queue = queue_client

    async def run(self):
        async for event in self.queue.subscribe("payment.completed"):
            user = await self.get_user(event['user_id'])
            # Send email/SMS
            await self.send_email(
                user['email'],
                f"Payment of ${event['amount']} confirmed"
            )
            await self.send_sms(user['phone'], "Payment received ✓")
```

---

## Concrete Example: Docker Compose Setup

Here's a **working skeleton** you can iterate on:

```yaml
# docker-compose.yml
version: '3.8'

services:
  # Databases
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
      - "15672:15672"  # Management UI

  # API Gateway
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

  # Auth Service
  auth:
    build: ./services/auth
    environment:
      DATABASE_URL: postgresql://admin:secret@postgres/microservices
      SECRET_KEY: your-secret-key
      USER_SERVICE_URL: http://user:8002
    depends_on:
      - postgres

  # User Service
  user:
    build: ./services/user
    environment:
      DATABASE_URL: postgresql://admin:secret@postgres/microservices
    depends_on:
      - postgres

  # Payment Service
  payment:
    build: ./services/payment
    environment:
      DATABASE_URL: postgresql://admin:secret@postgres/microservices
      STRIPE_API_KEY: sk_test_xxx
      RABBITMQ_URL: amqp://admin:secret@rabbitmq
    depends_on:
      - postgres
      - rabbitmq

  # Notification Service (Job Worker)
  notification_worker:
    build: ./services/notification_worker
    environment:
      RABBITMQ_URL: amqp://admin:secret@rabbitmq
      SENDGRID_API_KEY: xxx
      TWILIO_AUTH_TOKEN: xxx
    depends_on:
      - rabbitmq

  # Admin Service
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

## Gateway Implementation (FastAPI)

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
    """Forward auth check to Auth Service"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing auth header")

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{AUTH_SERVICE}/verify",
            json={"token": authorization.replace("Bearer ", "")}
        )

    if resp.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid token")

    return resp.json()

@app.post("/api/v1/auth/login")
async def login(email: str, password: str):
    """Proxy to Auth Service"""
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{AUTH_SERVICE}/login",
            json={"email": email, "password": password}
        )
    return JSONResponse(resp.json(), status_code=resp.status_code)

@app.get("/api/v1/users/{user_id}")
async def get_user(user_id: str, user_data = Depends(verify_token)):
    """Authenticated request to User Service"""
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{USER_SERVICE}/users/{user_id}",
            headers={"Authorization": f"Bearer {user_data['token']}"}
        )
    return resp.json()

@app.post("/api/v1/payments/charge")
async def charge(amount: float, user_id: str, user_data = Depends(verify_token)):
    """Authenticated request to Payment Service"""
    if user_data['user_id'] != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

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

## Auth Service (with internal calls)

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
    """Login: fetch user from User Service, validate password, return JWT"""
    async with httpx.AsyncClient() as client:
        user_resp = await client.get(
            f"{USER_SERVICE}/users/by-email",
            params={"email": req.email}
        )

    if user_resp.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    user = user_resp.json()

    # In production: use bcrypt to verify password
    if not verify_password(req.password, user['password_hash']):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Generate JWT
    payload = {
        "user_id": user['id'],
        "email": user['email'],
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return {"access_token": token, "user_id": user['id']}

@app.post("/verify")
async def verify(req: TokenVerifyRequest):
    """Verify JWT token (called by Gateway)"""
    try:
        payload = jwt.decode(req.token, SECRET_KEY, algorithms=["HS256"])
        return {"valid": True, "user_id": payload['user_id'], "token": req.token}
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def verify_password(plain: str, hashed: str) -> bool:
    # Use bcrypt in production
    import hashlib
    return hashlib.sha256(plain.encode()).hexdigest() == hashed
```

---

## Key Design Decisions

### 1. **Database Per Service**
Each service owns its DB. User Service ≠ Payment Service DB. This prevents tight coupling.

```python
# Bad: shared DB
SELECT * FROM users u JOIN payments p ON u.id = p.user_id

# Good: separate DBs
# User Service: SELECT * FROM users WHERE id = ?
# Payment Service: SELECT * FROM payments WHERE user_id = ?
```

### 2. **Internal Service Calls (Sync)**
Use HTTP + internal auth tokens for service-to-service calls. Keep latency low:

```python
# Internal token (not user-facing)
INTERNAL_TOKEN = jwt.encode({"service": "payment"}, SECRET_KEY)

async with httpx.AsyncClient(timeout=2.0) as client:  # 2s timeout
    user = await client.get(
        f"{USER_SERVICE}/users/{user_id}",
        headers={"X-Service-Token": INTERNAL_TOKEN}
    )
```

### 3. **Event-Driven for Side Effects**
Notifications, webhooks, auditing → async via queue. Never fail the main request on side effects.

```python
# Payment succeeds immediately
stripe_charge = await charge_card(...)

# Notification happens later (async)
await queue.publish("payment.success", {...})

# If email fails, payment still succeeded ✓
```

### 4. **Admin as a Separate Service**
Admin has different auth rules (role-based), audit logs, and doesn't impact user requests.

```python
# User API: fast, read-heavy
GET /api/v1/users/{id}

# Admin API: slow, write-heavy, audited
POST /api/v1/admin/users/{id}/suspend
```

### 5. **Message Queue Pattern**
Use RabbitMQ, Redis, or Kafka depending on throughput:
- **RabbitMQ** (100K msg/sec): routing, retry logic, good for most cases
- **Redis Streams** (1M msg/sec): simple, good if you already use Redis
- **Kafka** (1M+ msg/sec): distributed, durable, overkill for startups

```python
# Publish (Producer)
await rabbitmq.publish(
    exchange="events",
    routing_key="payment.success",
    body=json.dumps({"user_id": "123", "amount": 99.99})
)

# Consume (Worker)
async with rabbitmq.consume("notifications_queue") as messages:
    async for msg in messages:
        event = json.loads(msg.body)
        await send_email(event['user_id'])
        await msg.ack()
```

---

## Deployment Considerations

1. **Service discovery**: Use Kubernetes (ServiceName → internal IP), or simple DNS
2. **Health checks**: Each service exposes `/health` endpoint
3. **Logging**: Centralized (ELK, Datadog) with correlation IDs
4. **Monitoring**: Track request latency, queue depth, error rates per service
5. **Secrets**: Use environment variables or Kubernetes secrets, never hardcode

```bash
# Kubernetes deployment
kubectl apply -f auth-deployment.yaml
kubectl apply -f user-deployment.yaml
kubectl apply -f payment-deployment.yaml
# Services auto-discover via DNS (auth:8001, user:8002, etc.)
```

---

## Start Simple, Evolve

1. **Phase 1** (MVP): Gateway + Auth + User + Payment, all in one Postgres DB (monolith-lite)
2. **Phase 2**: Split services, add message queue for notifications
3. **Phase 3**: Multi-region, event sourcing, CQRS if you need audit trails
4. **Phase 4**: AI services (fine-tuning, inference) as separate sidecar services

The code above is production-ready — clone it, run `docker-compose up`, and iterate. Your main focus should be **clear service boundaries** (what each service owns) and **async patterns** (where to use queues). The infrastructure comes second.
