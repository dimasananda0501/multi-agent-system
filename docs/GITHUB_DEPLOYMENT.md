# GitHub & Deployment Guide

Panduan lengkap untuk push project ke GitHub dan deploy ke Hugging Face Spaces.

## Part 1: Setup GitHub Repository

### Step 1: Create GitHub Repository

1. **Buka GitHub.com dan login**
2. **Click "New Repository"** atau buka https://github.com/new
3. **Isi detail repository:**
   - Repository name: `xyz-ai-nexus`
   - Description: `Multi-Agent AI System for XYZ Operations`
   - Visibility: Public atau Private (pilih sesuai kebutuhan)
   - ❌ **Jangan** centang "Initialize with README" (kita sudah punya)
   - ❌ **Jangan** add .gitignore atau license (kita sudah punya)
4. **Click "Create repository"**

### Step 2: Initialize Git dan Push

Di terminal, di dalam folder project:

```bash
# 1. Initialize git (jika belum)
git init

# 2. Add all files
git add .

# 3. Commit
git commit -m "Initial commit: Multi-Agent AI System"

# 4. Rename branch to main (jika perlu)
git branch -M main

# 5. Add remote (ganti YOUR_USERNAME dengan username GitHub Anda)
git remote add origin https://github.com/YOUR_USERNAME/xyz-ai-nexus.git

# 6. Push to GitHub
git push -u origin main
```

**Troubleshooting:**
- Jika diminta login, gunakan Personal Access Token (bukan password)
- Generate token di: Settings → Developer settings → Personal access tokens
- Scope yang dibutuhkan: `repo` (full control)

### Step 3: Setup GitHub Secrets

Untuk CI/CD pipeline, tambahkan secrets:

1. **Go to repository settings**
   - Repository → Settings → Secrets and variables → Actions
2. **Add secrets:**
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `DOCKERHUB_USERNAME`: (Optional) Docker Hub username
   - `DOCKERHUB_TOKEN`: (Optional) Docker Hub token

### Step 4: Verify CI/CD

Setelah push, GitHub Actions akan otomatis run:
- Tab "Actions" di repository
- Monitor test, lint, dan build status
- Green checkmark = success ✅

---

## Part 2: Deploy to Hugging Face Spaces

### Step 1: Create Hugging Face Account

1. **Buka** https://huggingface.co/join
2. **Sign up** dengan email atau GitHub
3. **Verify email**

### Step 2: Create New Space

1. **Go to** https://huggingface.co/spaces
2. **Click "Create new Space"**
3. **Fill details:**
   - Space name: `xyz-ai-nexus`
   - License: `MIT`
   - SDK: **Docker** (penting!)
   - Visibility: Public atau Private
4. **Click "Create Space"**

### Step 3: Prepare Repository for HF Spaces

**A. Create Dockerfile for HF Spaces**

HF Spaces menggunakan port 7860 by default. Create `Dockerfile` di root:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose HF Spaces port
EXPOSE 7860

# Set environment for HF Spaces
ENV API_PORT=7860
ENV API_HOST=0.0.0.0

# Run application
CMD ["python", "main.py"]
```

**B. Update README.md Header**

Add metadata di paling atas `README.md`:

```yaml
---
title: XYZ AI Nexus
emoji: 🛢️
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: mit
app_port: 7860
---
```

**C. Commit changes:**

```bash
git add Dockerfile README.md
git commit -m "Add HF Spaces configuration"
git push origin main
```

### Step 4: Push to Hugging Face

**Option A: Direct Push (Recommended)**

```bash
# 1. Add HF remote (ganti YOUR_USERNAME)
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/xyz-ai-nexus

# 2. Push to HF
git push hf main
```

**If authentication required:**
```bash
# Use HF token as password
# Token from: https://huggingface.co/settings/tokens
git push https://YOUR_USERNAME:YOUR_HF_TOKEN@huggingface.co/spaces/YOUR_USERNAME/xyz-ai-nexus
```

**Option B: Sync from GitHub (Automatic)**

1. **In Space settings:**
   - Click "Settings" tab
   - Scroll to "Repository"
   - Click "Connect to GitHub"
   - Select your GitHub repository
   - Enable "Automatic sync"

Now setiap push ke GitHub akan otomatis deploy ke HF Spaces!

### Step 5: Configure Secrets in HF Spaces

1. **Go to Space Settings**
2. **Scroll to "Repository secrets"**
3. **Add secrets:**
   - Name: `OPENAI_API_KEY`
   - Value: your OpenAI API key
   - Click "Add"

Repeat untuk secrets lain jika ada (Anthropic, LangSmith, dll)

### Step 6: Monitor Deployment

1. **Build Logs:**
   - Tab "Logs" di Space
   - Monitor Docker build process
   - Wait for "Running on..." message

2. **Runtime Logs:**
   - Tab "Logs" → "Runtime"
   - Monitor API startup
   - Check for errors

3. **Test API:**
   - Space URL: `https://YOUR_USERNAME-xyz-ai-nexus.hf.space`
   - Docs: Add `/docs` to URL
   - Health: Add `/health` to URL

**Example test:**
```bash
curl https://YOUR_USERNAME-xyz-ai-nexus.hf.space/health
```

---

## Part 3: Ongoing Development Workflow

### Daily Workflow

```bash
# 1. Make changes to code
# 2. Test locally
python main.py
# Test with: python examples/demo.py

# 3. Run tests
pytest

# 4. Commit and push
git add .
git commit -m "Description of changes"
git push origin main

# 5. Automatically:
# - GitHub Actions runs tests
# - Docker image builds
# - HF Spaces deploys (if auto-sync enabled)
```

### Branching Strategy

```bash
# Feature development
git checkout -b feature/new-agent
# ... make changes ...
git commit -m "Add new specialist agent"
git push origin feature/new-agent
# Create Pull Request on GitHub

# After review, merge to main
# Automatic deployment triggers
```

### Hotfix Process

```bash
# Urgent fix needed
git checkout -b hotfix/api-error
# ... fix issue ...
git commit -m "Fix API error handling"
git push origin hotfix/api-error
# Fast merge to main
```

---

## Part 4: Monitoring & Maintenance

### Check Application Health

**GitHub:**
- Actions tab: CI/CD status
- Issues tab: Bug reports
- Insights: Contribution stats

**Hugging Face:**
- Logs: Runtime errors
- Analytics: API usage (if enabled)
- Community: User feedback

### Update Dependencies

```bash
# Check for updates
pip list --outdated

# Update specific package
pip install --upgrade langchain

# Update requirements.txt
pip freeze > requirements.txt

# Test and push
pytest
git add requirements.txt
git commit -m "Update dependencies"
git push
```

### Rollback Deployment

If something breaks:

**On GitHub:**
```bash
# Revert to previous commit
git revert HEAD
git push origin main
```

**On HF Spaces:**
- Space Settings → "Factory Reboot"
- Or manually select specific commit to deploy

---

## Part 5: Advanced Deployment Options

### Custom Domain (HF Spaces Pro)

1. **Upgrade to Pro:** https://huggingface.co/pricing
2. **In Space settings:**
   - "Custom domain"
   - Add your domain (e.g., `api.xyz-nexus.ai`)
   - Configure DNS CNAME record

### Multiple Environments

**Staging Environment:**
```bash
# Create staging space
# Push to staging first
git remote add hf-staging https://huggingface.co/spaces/YOUR_USERNAME/xyz-nexus-staging
git push hf-staging develop

# Test on staging
# If OK, push to production
git checkout main
git merge develop
git push hf main
```

### Monitoring & Alerts

**Setup monitoring:**
1. **LangSmith:** Already configured via env vars
2. **Sentry:** Add to requirements.txt, configure in main.py
3. **Uptime monitoring:** 
   - UptimeRobot: https://uptimerobot.com
   - Monitor: `https://YOUR-SPACE.hf.space/health`
   - Alert if down

**Alert channels:**
- Email notifications
- Slack webhook
- Discord webhook

---

## Part 6: Troubleshooting

### Common Issues

**1. Build fails on HF Spaces**
```
Error: Python package installation failed
```
**Solution:**
- Check requirements.txt syntax
- Ensure all packages are compatible with Python 3.11
- Check build logs for specific error

**2. API returns 500 error**
```
Internal Server Error
```
**Solution:**
- Check runtime logs in HF Spaces
- Verify API keys are set in secrets
- Test locally first with same config

**3. Slow response times**
```
Timeout after 30s
```
**Solution:**
- Optimize agent iterations (reduce max_iterations)
- Use faster models (gpt-4o-mini)
- Enable caching with Redis

**4. Out of memory**
```
Container killed - Out of memory
```
**Solution:**
- Reduce context window size
- Limit concurrent requests
- Upgrade to HF Pro (more resources)

**5. Git push rejected**
```
! [rejected] main -> main (non-fast-forward)
```
**Solution:**
```bash
git pull --rebase origin main
git push origin main
```

---

## Checklist Summary

### Pre-Deployment ✓
- [ ] All tests passing locally
- [ ] Environment variables documented
- [ ] README.md complete
- [ ] .gitignore configured
- [ ] License file added

### GitHub Setup ✓
- [ ] Repository created
- [ ] Code pushed
- [ ] Secrets configured
- [ ] CI/CD pipeline running
- [ ] Branch protection enabled (optional)

### HF Spaces Setup ✓
- [ ] Space created
- [ ] Dockerfile configured for port 7860
- [ ] README.md has HF metadata
- [ ] Secrets configured
- [ ] Deployment successful
- [ ] Health endpoint responding

### Post-Deployment ✓
- [ ] API tested with real queries
- [ ] Logs monitored for errors
- [ ] Performance acceptable
- [ ] Documentation updated
- [ ] Team notified

---

## Support & Resources

**Documentation:**
- GitHub Docs: https://docs.github.com
- HF Spaces Docs: https://huggingface.co/docs/hub/spaces
- Docker Docs: https://docs.docker.com

**Community:**
- GitHub Issues: Report bugs
- HF Community: Discussion forum
- Discord: Real-time help

**Contact:**
- Email: support@xyz-nexus.ai
- GitHub: @yourusername

---

**Last Updated**: February 2026  
**Version**: 1.0
