# Production Deployment & RAG Guide - XYZ AI Nexus

Panduan ini menjelaskan langkah-langkah untuk mendeploy sistem multi-agent ke cloud production, mengintegrasikan API, serta membangun Vector Database untuk Retrieval-Augmented Generation (RAG).

## 1. Cloud Production Deployment

Untuk deployment production, disarankan menggunakan container orchestration seperti Google Cloud Run, AWS ECS, atau Azure Container Apps.

### A. Strategi Deployment (CI/CD)
Gunakan GitHub Actions untuk otomatisasi build dan push image ke Container Registry (GCR/ECR/ACR).

**Contoh Workflow GitHub Actions (`.github/workflows/deploy.yml`):**
```yaml
name: Deploy to Production
on:
  push:
    branches: [ main ]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build Docker Image
        run: docker build -t gcr.io/your-project/xyz-ai-nexus:latest -f deployment/Dockerfile .
      - name: Push to GCR
        run: docker push gcr.io/your-project/xyz-ai-nexus:latest
      - name: Deploy to Cloud Run
        run: |
          gcloud run deploy xyz-ai-nexus \
            --image gcr.io/your-project/xyz-ai-nexus:latest \
            --platform managed \
            --region asia-southeast2 \
            --set-env-vars "OPENAI_API_KEY=${{ secrets.OPENAI_API_KEY }}"
```

### B. Scalability & Availability
- **Horizontal Pod Autoscaling**: Set CPU/Memory threshold untuk auto-scaling.
- **Multi-Region**: Deploy di minimal 2 region untuk high availability.
- **External Redis**: Gunakan managed Redis (seperti Google Cloud Memorystore) sebagai pengganti container Redis lokal untuk shared session state.

---

## 2. Integrasi Antar API

Sistem ini dirancang untuk berinteraksi dengan API internal maupun eksternal melalui **Agent Tools**.

### Mekanisme Integrasi:
1. **Authentication**: Gunakan API Keys atau OAuth2 yang disimpan di Environment Variables.
2. **Tool Definition**: Buat class tool di `src/tools/` yang membungkus call ke API lain menggunakan `httpx`.
3. **Error Handling**: Implementasikan retry logic (menggunakan `tenacity`) untuk menangani API yang tidak stabil.

**Contoh Integrasi API Eksternal:**
```python
@tool
async def get_external_data(query: str) -> Dict:
    """Mengambil data dari API pihak ketiga (misal: Data Produksi Pusat)."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.external.com/data?q={query}",
            headers={"Authorization": f"Bearer {os.getenv('EXTERNAL_API_KEY')}"}
        )
        return response.json()
```

---

## 3. Membangun Vector Database & RAG

RAG memungkinkan agent menjawab pertanyaan berdasarkan dokumen internal yang tidak ada dalam training data LLM.

### A. Arsitektur Vector DB
Kami menggunakan **ChromaDB** sebagai vector store karena kemudahannya dalam integrasi dengan LangChain.

1. **Ingestion Pipeline**: 
   - Load dokumen (PDF, MD, TXT).
   - Split dokumen menjadi chunks (misal: 1000 karakter per chunk).
   - Generate embedding menggunakan OpenAI `text-embedding-3-small`.
   - Simpan di ChromaDB.

2. **Retrieval**:
   - Saat user bertanya, sistem melakukan semantic search ke ChromaDB.
   - Mengambil 3-5 chunk paling relevan.

### B. Implementasi Kode
Berikut adalah cara membangun vector database di sistem ini:

```python
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader

# 1. Load & Split
loader = TextLoader("path/to/your/document.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

# 2. Initialize DB
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(
    documents=docs, 
    embedding=embeddings,
    persist_directory="./data/chroma_db"
)

# 3. Penggunaan dalam Agent Tool
@tool
def search_internal_docs(query: str):
    """Cari informasi di basis data internal untuk menjawab pertanyaan kompleks."""
    results = vectorstore.similarity_search(query, k=3)
    return "\n".join([doc.page_content for doc in results])
```

### C. Maintenance Vector Database
- **Update Berkala**: Gunakan cron job untuk melakukan re-indexing jika dokumen berubah.
- **Filtering**: Implementasikan metadata filtering (misal: berdasarkan departemen) agar pencarian lebih akurat.

---

## 4. Keamanan di Production

- **API Key Proxy**: Jangan ekspos OpenAI Key ke client side. Client hanya berkomunikasi dengan API Nexus kita.
- **Inbound Security**: Batasi `ALLOWED_ORIGINS` di CORS settings.
- **Rate Limiting**: Gunakan Nginx atau Cloud Armor untuk mencegah brute force.
- **Logging Sensitive Data**: Pastikan logger tidak mencatat PII (Personally Identifiable Information) atau API Keys.

---

**Built with ❤️ by [dimasananda0501](https://github.com/dimasananda0501)**
