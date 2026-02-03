# Deployment Guide - XYZ AI Nexus

Panduan lengkap untuk deploy XYZ AI Nexus ke berbagai platform.

## Table of Contents
- [Local Development](#local-development)
- [Docker Deployment](#docker-deployment)
- [Hugging Face Spaces](#hugging-face-spaces)
- [Cloud Platforms](#cloud-platforms)
- [Production Checklist](#production-checklist)

---

## Local Development

### Quick Setup
```bash
# Clone repository
git clone https://github.com/dimasananda0501/multi-agent-system.git
cd xyz-ai-nexus

# Setup virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env dengan API keys Anda

# Run application
python main.py
```

Application akan berjalan di `http://localhost:8000`

---

## Docker Deployment

### Build and Run with Docker

```bash
# Build image
docker build -t xyz-ai-nexus -f deployment/Dockerfile .

# Run container
docker run -d \
  --name xyz-api \
  -p 8000:8000 \
  -e OPENAI_API_KEY=your_key_here \
  -v $(pwd)/data:/app/data \
  xyz-ai-nexus

# Check logs
docker logs -f xyz-api

# Stop container
docker stop xyz-api
```

### Docker Compose (Recommended)

Docker Compose menjalankan API + Redis untuk caching:

```bash
# Start all services (Dijalankan dari root project agar .env terbaca otomatis)
docker-compose -f deployment/docker-compose.yml up -d

# View logs
docker-compose -f deployment/docker-compose.yml logs -f

# Stop all services
docker-compose -f deployment/docker-compose.yml down

# Rebuild after code changes
docker-compose -f deployment/docker-compose.yml up -d --build
```

**Services:**
- API: http://localhost:8000
- Redis: localhost:6379
- Nginx (optional): http://localhost

---

## Hugging Face Spaces

### Step 1: Prepare Repository

1. **Create Dockerfile for HF Spaces**

Create `Dockerfile` di root project:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port (HF Spaces uses 7860 by default)
EXPOSE 7860

# Set environment for HF Spaces
ENV API_PORT=7860
ENV API_HOST=0.0.0.0

# Run application
CMD ["python", "main.py"]
```

2. **Create README.md with HF metadata**

Add to top of README.md:

```yaml
---
title: XYZ AI Nexus
emoji: 🛢️
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: mit
---
```

### Step 2: Create Space on Hugging Face

1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Name: `xyz-ai-nexus`
4. License: MIT
5. SDK: Docker
6. Visibility: Public atau Private

### Step 3: Push to Hugging Face

```bash
# Add Hugging Face remote
git remote add hf https://huggingface.co/spaces/dimasananda0501/multi-agent-system

# Push code
git add .
git commit -m "Initial deployment"
git push hf main
```

### Step 4: Configure Secrets

Di Space settings, tambahkan secrets:

- `OPENAI_API_KEY`: Your OpenAI API key
- `ANTHROPIC_API_KEY`: (Optional) Your Anthropic API key
- `LANGCHAIN_API_KEY`: (Optional) LangSmith key

### Step 5: Monitor Deployment

Space akan otomatis build dan deploy. Monitor di:
- Build logs: Tab "Logs" di Space
- Runtime logs: Tab "Logs" → "Runtime"

**Access API:**
- Space URL: `https://dimasananda0501-multi-agent-system.hf.space`
- API docs: `https://dimasananda0501-multi-agent-system.hf.space/docs`

---

## Cloud Platforms

### Google Cloud Run

```bash
# 1. Build and push to GCR
gcloud builds submit --tag gcr.io/PROJECT_ID/xyz-ai-nexus

# 2. Deploy to Cloud Run
gcloud run deploy xyz-ai-nexus \
  --image gcr.io/PROJECT_ID/xyz-ai-nexus \
  --platform managed \
  --region asia-southeast2 \
  --allow-unauthenticated \
  --set-env-vars "OPENAI_API_KEY=your_key"

# 3. Get URL
gcloud run services describe xyz-ai-nexus --format='value(status.url)'
```

### AWS ECS (Fargate)

```bash
# 1. Push to ECR
aws ecr get-login-password --region ap-southeast-1 | \
  docker login --username AWS --password-stdin ACCOUNT.dkr.ecr.ap-southeast-1.amazonaws.com

docker tag xyz-ai-nexus:latest ACCOUNT.dkr.ecr.ap-southeast-1.amazonaws.com/xyz:latest
docker push ACCOUNT.dkr.ecr.ap-southeast-1.amazonaws.com/xyz:latest

# 2. Create task definition (task-definition.json)
# 3. Create ECS service
aws ecs create-service \
  --cluster xyz-cluster \
  --service-name xyz-api \
  --task-definition xyz-task \
  --desired-count 2 \
  --launch-type FARGATE
```

### Azure Container Apps

```bash
# 1. Create container registry
az acr create --resource-group xyz-rg \
  --name xyzacr --sku Basic

# 2. Build and push
az acr build --registry xyzacr \
  --image xyz-ai-nexus:latest .

# 3. Deploy container app
az containerapp create \
  --name xyz-api \
  --resource-group xyz-rg \
  --environment xyz-env \
  --image xyzacr.azurecr.io/xyz-ai-nexus:latest \
  --target-port 8000 \
  --ingress external \
  --secrets openai-key=YOUR_KEY \
  --env-vars OPENAI_API_KEY=secretref:openai-key
```

---

## Production Checklist

### Before Deployment

- [ ] **Environment Variables**: Semua API keys configured
- [ ] **Security**:
  - [ ] API key authentication enabled
  - [ ] CORS properly configured
  - [ ] HTTPS enabled
- [ ] **Monitoring**:
  - [ ] LangSmith tracing enabled
  - [ ] Logging configured
  - [ ] Error tracking (Sentry/Datadog)
- [ ] **Testing**:
  - [ ] All tests passing
  - [ ] Load testing completed
  - [ ] Edge cases handled
- [ ] **Documentation**:
  - [ ] API docs up-to-date
  - [ ] README complete
  - [ ] Architecture diagram created

### Configuration for Production

Update `.env` for production:

```bash
# Production settings
APP_ENV=production
LOG_LEVEL=WARNING
API_HOST=0.0.0.0
API_PORT=8000

# Use production-grade models
DEFAULT_LLM_MODEL=gpt-4o-mini  # Fast + cheap untuk workers
ORCHESTRATOR_MODEL=gpt-4o      # Smart untuk routing

# Security
ALLOWED_ORIGINS=https://yourdomain.com
API_KEY_HEADER=X-API-Key

# Monitoring
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=xyz-production

# Resource limits
MAX_ITERATIONS=10
AGENT_TIMEOUT=300
```

### Scaling Considerations

**Horizontal Scaling:**
- Deploy multiple API instances behind load balancer
- Use Redis for shared state/caching
- Consider rate limiting per user

**Vertical Scaling:**
- Increase memory for better LLM performance
- Use GPUs for custom models (if self-hosting LLM)

**Cost Optimization:**
- Cache frequent queries (Redis)
- Use cheaper models for simple tasks (routing)
- Implement request batching for tools

### Monitoring & Observability

**Metrics to Track:**
- Request latency (p50, p95, p99)
- Token usage per agent
- Error rates by agent type
- Cache hit rates
- LLM API latency

**Alerts to Setup:**
- API downtime
- High error rates (>5%)
- Slow response times (>10s)
- LLM API failures
- High token costs

**Tools:**
- LangSmith: LLM tracing & debugging
- Prometheus + Grafana: Metrics & dashboards
- Sentry: Error tracking
- Datadog/NewRelic: APM

### Backup & Recovery

**Data to Backup:**
- Vector database (Chroma)
- Conversation logs
- Configuration files

**Recovery Plan:**
- Database snapshots: Daily
- Config version control: Git
- Disaster recovery time: <1 hour

---

## Troubleshooting

### Common Issues

**1. OpenAI API Rate Limits**
```python
# Solution: Implement retry with exponential backoff
# Already handled in LangChain, but can add:
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
def call_llm():
    ...
```

**2. Memory Issues (Large Context)**
```python
# Solution: Truncate messages
MAX_MESSAGES = 20
state["messages"] = state["messages"][-MAX_MESSAGES:]
```

**3. Slow Response Times**
```python
# Solutions:
# - Use faster models (gpt-4o-mini instead of gpt-4)
# - Cache common queries
# - Parallel agent execution
# - Reduce max_iterations
```

**4. Docker Build Fails**
```bash
# Clear Docker cache
docker system prune -a

# Rebuild from scratch
docker-compose build --no-cache
```

---

## Support & Maintenance

### Regular Maintenance Tasks

**Weekly:**
- Review error logs
- Check token usage/costs
- Update dependencies (security patches)

**Monthly:**
- Review agent performance metrics
- Optimize prompts based on failures
- Update documentation

**Quarterly:**
- Major version upgrades
- Architecture review
- Security audit

### Getting Help

- **GitHub Issues**: Report bugs atau feature requests
- **Discussions**: Tanya pertanyaan
- **Email**: support@xyz-nexus.ai

---

**Last Updated**: February 2026
