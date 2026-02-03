# XYZ AI Nexus - Multi-Agent System

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)
![LangGraph](https://img.shields.io/badge/LangGraph-0.2+-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

**Production-ready Multi-Agent AI System untuk XYZ Operations**

Sistem ini mengimplementasikan arsitektur multi-agent dengan pola Hub-and-Spoke (Orchestrator-Workers) untuk menangani query kompleks yang melibatkan berbagai domain operasional XYZ.

## 🎯 Overview

XYZ AI Nexus adalah sistem kecerdasan buatan berbasis multi-agent yang dirancang untuk mengintegrasikan data dan insights dari berbagai departemen XYZ:

- **Upstream Agent**: Data produksi migas, status sumur, jadwal lifting
- **Logistics Agent**: Tracking kapal tanker, prakiraan cuaca, status pengiriman  
- **Finance Agent**: Analisis revenue, biaya operasional, profitabilitas

### Arsitektur

```
┌─────────────────────────────────────────────────────────┐
│                    User Query                            │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │    ORCHESTRATOR        │
         │  (Intent Classifier)    │
         └────────┬───────────────┘
                  │
    ┌─────────────┼──────────────┐
    │             │              │
    ▼             ▼              ▼
┌────────┐  ┌──────────┐  ┌──────────┐
│Upstream│  │Logistics │  │ Finance  │
│ Agent  │  │  Agent   │  │  Agent   │
└───┬────┘  └────┬─────┘  └────┬─────┘
    │            │             │
    │      ┌─────▼─────┐       │
    └─────►│Synthesizer├───────┘
           └─────┬─────┘
                 │
                 ▼
         ┌───────────────┐
         │Final Response │
         └───────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- OpenAI API Key (atau Anthropic API Key)
- Git

### Installation

1. **Clone repository**
```bash
git clone https://github.com/dimasananda0501/multi-agent-system.git
cd xyz-ai-nexus
```

2. **Setup virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

5. **Run the API**
```bash
python main.py
```

API akan berjalan di `http://localhost:8000`

### Quick Test

```bash
# Health check
curl http://localhost:8000/health

# Test query
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the current production in Rokan block?",
    "user_id": "test_user"
  }'
```

## 📚 Usage Examples

### Example 1: Single Agent Query (Upstream)
```python
import requests

response = requests.post(
    "http://localhost:8000/query",
    json={
        "query": "What is the current oil production in Mahakam block?",
        "user_id": "manager_001"
    }
)

print(response.json()["response"])
# Output: "The Mahakam block is currently producing 85,000 BOPD..."
```

### Example 2: Multi-Agent Query (Upstream + Logistics)
```python
response = requests.post(
    "http://localhost:8000/query",
    json={
        "query": "What's the status of Rokan production and its shipment to Balongan?",
        "user_id": "manager_001"
    }
)

# System akan otomatis memanggil Upstream Agent untuk produksi
# dan Logistics Agent untuk status pengiriman
```

### Example 3: Complex Query (All Agents)
```python
response = requests.post(
    "http://localhost:8000/query",
    json={
        "query": "Calculate the profitability of Cepu block considering current production and shipping delays",
        "user_id": "cfo_001"
    }
)

# System memanggil:
# 1. Upstream Agent -> produksi Cepu
# 2. Logistics Agent -> delay pengiriman
# 3. Finance Agent -> kalkulasi profitabilitas
# 4. Synthesizer -> gabungkan insights
```

## 🏗️ Project Structure

```
multi-agent-system/
├── src/
│   ├── agents/                    # Specialist agents
│   │   ├── upstream_agent.py
│   │   ├── logistics_agent.py
│   │   └── finance_agent.py
│   ├── orchestrator/              # Orchestrator & routing
│   │   └── orchestrator.py
│   ├── tools/                     # Agent tools (MCP-compatible)
│   │   ├── upstream_tools.py
│   │   ├── logistics_tools.py
│   │   └── finance_tools.py
│   └── utils/                     # Utilities
│       ├── config.py
│       ├── logger.py
│       └── state.py
├── tests/                         # Test suite
│   └── test_agents.py
├── deployment/                    # Deployment configs
│   ├── Dockerfile
│   └── docker-compose.yml
├── docs/                          # Documentation
│   ├── ARCHITECTURE.md
│   ├── API_REFERENCE.md
│   └── DEPLOYMENT.md
├── main.py                        # FastAPI application
├── requirements.txt               # Dependencies
├── .env.example                   # Environment template
└── README.md
```

## 🔧 Configuration

Edit `.env` file untuk konfigurasi:

```bash
# API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...  # Optional

# Application
API_PORT=8000
LOG_LEVEL=INFO
MAX_ITERATIONS=10

# Models
DEFAULT_LLM_MODEL=gpt-4o-mini    # Untuk worker agents
ORCHESTRATOR_MODEL=gpt-4o        # Untuk orchestrator (reasoning)

# LangSmith (Optional - untuk monitoring)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=ls-...
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_agents.py -v

# Run only unit tests (skip integration)
pytest -m "not integration"
```

## 📊 API Documentation

Setelah menjalankan aplikasi, akses dokumentasi interaktif di:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Main Endpoints

#### `POST /query`
Proses query user melalui multi-agent system.

**Request:**
```json
{
  "query": "What is production in Rokan?",
  "user_id": "user_123",
  "user_role": "manager"
}
```

**Response:**
```json
{
  "session_id": "uuid...",
  "query": "What is production in Rokan?",
  "routing_decision": "UPSTREAM",
  "response": "The Rokan block is currently producing 150,000 BOPD...",
  "agents_involved": ["upstream"],
  "execution_time_ms": 1234.56,
  "timestamp": "2026-02-02T10:30:00Z"
}
```

#### `GET /health`
Health check endpoint.

#### `GET /agents`
List semua agent dan capabilities mereka.

## 🚢 Deployment

### Docker Deployment

1. **Build image**
```bash
docker build -t xyz-ai-nexus .
```

2. **Run container**
```bash
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your_key \
  xyz-ai-nexus
```

### Hugging Face Spaces Deployment

1. **Create new Space di Hugging Face**
   - Pilih "Docker" sebagai SDK
   - Set visibility (public/private)

2. **Push ke Hugging Face**
```bash
git remote add hf https://huggingface.co/spaces/dimasananda0501/multi-agent-system
git push hf main
```

3. **Configure secrets**
   - Di settings Space, tambahkan:
     - `OPENAI_API_KEY`
     - `ANTHROPIC_API_KEY` (optional)

4. **Space akan otomatis deploy**

Lihat [DEPLOYMENT.md](docs/DEPLOYMENT.md) untuk detail lengkap.

## 🎓 Architecture Deep Dive

### Orchestrator Pattern (Hub-and-Spoke)

Sistem ini menggunakan pola **Orchestrator-Workers** yang merupakan standar emas untuk sistem produksi:

**Keunggulan:**
- ✅ Kontrol terpusat - mudah di-debug dan di-monitor
- ✅ Fleksibilitas dinamis - routing berdasarkan intent classification
- ✅ Isolasi konteks - setiap agent hanya menerima data relevan
- ✅ Skalabilitas - mudah menambah agent baru

**Alur Kerja:**
1. User mengirim query ke Orchestrator
2. Orchestrator classify intent (menggunakan LLM)
3. Orchestrator route ke agent yang sesuai
4. Agent execute dengan tools mereka
5. Jika multi-agent, Synthesizer gabungkan hasil
6. Return unified response ke user

### Agent Specialization

Setiap agent punya:
- **Persona spesifik**: System prompt yang detail tentang expertise
- **Tools eksklusif**: Hanya tools yang relevan dengan domain
- **Temperature rendah**: 0.1 untuk faktual response

### Tool Design (MCP-Compatible)

Semua tools mengikuti **Model Context Protocol** untuk interoperabilitas:
- Docstring lengkap dengan contoh
- Type hints yang jelas
- Return value yang konsisten (Dict[str, Any])
- Error handling yang robust

## 🔍 Monitoring & Observability

### LangSmith Integration

Aktifkan tracing untuk monitoring:

```bash
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=your_langsmith_key
```

Setiap request akan di-trace:
- Input ke setiap agent
- Tool calls dan responses
- Execution time per step
- Token usage

### Custom Logging

Sistem menggunakan `structlog` untuk structured logging:

```python
from src.utils.logger import get_logger

logger = get_logger(__name__)
logger.info("Event", key1="value1", key2="value2")
```

Logs bisa di-parse dengan tools seperti Elasticsearch/Datadog.

## 🛡️ Security

### API Key Authentication (Optional)

```python
curl -X POST http://localhost:8000/query \
  -H "X-API-Key: your_secret_key" \
  -H "Content-Type: application/json" \
  -d '{"query": "..."}'
```

### RBAC (Role-Based Access Control)

Sistem mendukung role-based access:

```python
{
  "query": "...",
  "user_role": "manager"  # atau "user", "admin", "cfo"
}
```

Agent dapat membatasi akses tool berdasarkan role.

## 🤝 Contributing

1. Fork repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

MIT License - lihat [LICENSE](LICENSE) file.


## 🙏 Acknowledgments

- Penelitian ini mengikuti best practices dari paper **"Arsitektur dan Implementasi Sistem Multi-Agent AI"**
- Framework: LangChain, LangGraph, FastAPI
- Inspired by production multi-agent systems dari Google DeepMind, Anthropic
