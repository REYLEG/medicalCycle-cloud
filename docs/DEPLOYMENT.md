# MedicalCycle Cloud - Deployment Guide

## Overview

This guide covers deploying MedicalCycle Cloud to production environments.

## Prerequisites

- Docker & Docker Compose
- PostgreSQL 14+ (managed service or self-hosted)
- Redis 7+ (managed service or self-hosted)
- Domain name with SSL certificate
- Cloud provider account (AWS, GCP, Azure, etc.)

## Local Development Deployment

### Quick Start with Docker Compose

```bash
# Clone repository
git clone https://github.com/REYLEG/medicalCycle-cloud.git
cd medicalCycle-cloud

# Configure environment
cp backend/.env.example backend/.env
# Edit backend/.env with your settings

# Start services
docker-compose up -d

# Initialize database
docker-compose exec backend python -m app.db.init_db

# Check status
docker-compose ps
```

Access the API at `http://localhost:8000`
API Documentation: `http://localhost:8000/api/docs`

## Production Deployment

### 1. Environment Configuration

Create `.env` file with production values:

```bash
cp backend/.env.production.example backend/.env.production
```

**Critical settings to change:**
- `SECRET_KEY` - Generate with: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
- `DATABASE_URL` - Use managed PostgreSQL service
- `REDIS_URL` - Use managed Redis service
- `ALLOWED_ORIGINS` - Set to your domain
- `ENCRYPTION_KEY` - Generate with: `python -c "import secrets; print(secrets.token_hex(16))"`

### 2. Database Setup

#### Option A: AWS RDS

```bash
# Create RDS PostgreSQL instance
aws rds create-db-instance \
  --db-instance-identifier medicalcycle-prod \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --engine-version 15.1 \
  --master-username medicalcycle_prod \
  --master-user-password STRONG_PASSWORD \
  --allocated-storage 100 \
  --backup-retention-period 30 \
  --multi-az
```

#### Option B: Google Cloud SQL

```bash
# Create Cloud SQL PostgreSQL instance
gcloud sql instances create medicalcycle-prod \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=us-central1 \
  --backup \
  --retained-backups-count=30
```

#### Option C: Self-Hosted

```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE medicalcycle_prod;
CREATE USER medicalcycle_prod WITH PASSWORD 'strong_password';
ALTER ROLE medicalcycle_prod SET client_encoding TO 'utf8';
ALTER ROLE medicalcycle_prod SET default_transaction_isolation TO 'read committed';
ALTER ROLE medicalcycle_prod SET default_transaction_deferrable TO on;
ALTER ROLE medicalcycle_prod SET default_transaction_level TO 'read committed';
GRANT ALL PRIVILEGES ON DATABASE medicalcycle_prod TO medicalcycle_prod;
```

### 3. Redis Setup

#### Option A: AWS ElastiCache

```bash
aws elasticache create-cache-cluster \
  --cache-cluster-id medicalcycle-redis \
  --cache-node-type cache.t3.micro \
  --engine redis \
  --engine-version 7.0 \
  --num-cache-nodes 1
```

#### Option B: Google Cloud Memorystore

```bash
gcloud redis instances create medicalcycle-redis \
  --size=1 \
  --region=us-central1 \
  --redis-version=7.0
```

#### Option C: Self-Hosted

```bash
# Install Redis
sudo apt-get install redis-server

# Configure Redis
sudo nano /etc/redis/redis.conf
# Set: requirepass strong_password

# Start Redis
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

### 4. Docker Deployment

#### Build Docker Image

```bash
# Build image
docker build -t medicalcycle-backend:latest ./backend

# Tag for registry
docker tag medicalcycle-backend:latest your-registry/medicalcycle-backend:latest

# Push to registry
docker push your-registry/medicalcycle-backend:latest
```

#### Deploy with Docker Compose

```bash
# Use production compose file
docker-compose -f docker-compose.prod.yml up -d

# Check logs
docker-compose -f docker-compose.prod.yml logs -f backend

# Initialize database
docker-compose -f docker-compose.prod.yml exec backend python -m app.db.init_db
```

### 5. Kubernetes Deployment

#### Create Namespace

```bash
kubectl create namespace medicalcycle
```

#### Create Secrets

```bash
kubectl create secret generic medicalcycle-secrets \
  --from-literal=database-url=postgresql://... \
  --from-literal=redis-url=redis://... \
  --from-literal=secret-key=... \
  -n medicalcycle
```

#### Deploy Application

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: medicalcycle-backend
  namespace: medicalcycle
spec:
  replicas: 3
  selector:
    matchLabels:
      app: medicalcycle-backend
  template:
    metadata:
      labels:
        app: medicalcycle-backend
    spec:
      containers:
      - name: backend
        image: your-registry/medicalcycle-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: medicalcycle-secrets
              key: database-url
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: medicalcycle-secrets
              key: redis-url
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: medicalcycle-secrets
              key: secret-key
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
```

Deploy:
```bash
kubectl apply -f deployment.yaml
```

### 6. SSL/TLS Configuration

#### Using Let's Encrypt with Nginx

```nginx
# /etc/nginx/sites-available/medicalcycle
upstream backend {
    server localhost:8000;
}

server {
    listen 80;
    server_name api.medicalcycle.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.medicalcycle.com;

    ssl_certificate /etc/letsencrypt/live/api.medicalcycle.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.medicalcycle.com/privkey.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "DENY" always;

    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Install certificate:
```bash
sudo certbot certonly --nginx -d api.medicalcycle.com
```

### 7. Monitoring & Logging

#### Application Logs

```bash
# View logs
docker-compose -f docker-compose.prod.yml logs -f backend

# Save logs to file
docker-compose -f docker-compose.prod.yml logs backend > app.log
```

#### Database Monitoring

```bash
# Connect to PostgreSQL
psql -h db.example.com -U medicalcycle_prod -d medicalcycle_prod

# Check connections
SELECT datname, count(*) FROM pg_stat_activity GROUP BY datname;

# Check slow queries
SELECT query, mean_time FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10;
```

#### Health Checks

```bash
# Check API health
curl https://api.medicalcycle.com/health

# Check database connection
curl https://api.medicalcycle.com/api/v1/auth/me -H "Authorization: Bearer <token>"
```

### 8. Backup & Recovery

#### Database Backup

```bash
# Full backup
pg_dump -h db.example.com -U medicalcycle_prod medicalcycle_prod > backup.sql

# Compressed backup
pg_dump -h db.example.com -U medicalcycle_prod medicalcycle_prod | gzip > backup.sql.gz

# Restore from backup
psql -h db.example.com -U medicalcycle_prod medicalcycle_prod < backup.sql
```

#### Automated Backups

```bash
# Create backup script
#!/bin/bash
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -h db.example.com -U medicalcycle_prod medicalcycle_prod | gzip > $BACKUP_DIR/backup_$DATE.sql.gz

# Add to crontab (daily at 2 AM)
0 2 * * * /path/to/backup.sh
```

### 9. Security Hardening

#### Firewall Rules

```bash
# Allow only necessary ports
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

#### Database Security

```bash
# Restrict database access
# In PostgreSQL pg_hba.conf
host    medicalcycle_prod    medicalcycle_prod    app_server_ip/32    md5

# Enable SSL for database connections
# In postgresql.conf
ssl = on
ssl_cert_file = '/path/to/cert.pem'
ssl_key_file = '/path/to/key.pem'
```

#### Application Security

```bash
# Set proper file permissions
chmod 600 .env
chmod 600 .env.production

# Use secrets management
# AWS Secrets Manager, Google Secret Manager, HashiCorp Vault, etc.
```

### 10. Scaling

#### Horizontal Scaling

```bash
# Scale with Docker Compose
docker-compose -f docker-compose.prod.yml up -d --scale backend=3

# Scale with Kubernetes
kubectl scale deployment medicalcycle-backend --replicas=5 -n medicalcycle
```

#### Load Balancing

Use cloud provider load balancer:
- AWS: Application Load Balancer (ALB)
- GCP: Cloud Load Balancing
- Azure: Azure Load Balancer

### 11. Maintenance

#### Regular Tasks

- [ ] Monitor logs daily
- [ ] Check disk space weekly
- [ ] Review security logs weekly
- [ ] Update dependencies monthly
- [ ] Run backups daily
- [ ] Test backup restoration monthly
- [ ] Security audit quarterly
- [ ] Penetration testing annually

#### Updating Application

```bash
# Pull latest code
git pull origin main

# Build new image
docker build -t medicalcycle-backend:latest ./backend

# Deploy update
docker-compose -f docker-compose.prod.yml up -d backend
```

## Troubleshooting

### Database Connection Issues

```bash
# Test connection
psql -h db.example.com -U medicalcycle_prod -d medicalcycle_prod -c "SELECT 1"

# Check connection string
echo $DATABASE_URL
```

### Redis Connection Issues

```bash
# Test connection
redis-cli -h redis.example.com ping

# Check connection string
echo $REDIS_URL
```

### Application Not Starting

```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs backend

# Check environment variables
docker-compose -f docker-compose.prod.yml exec backend env | grep -E "DATABASE|REDIS|SECRET"
```

## Performance Tuning

### PostgreSQL

```sql
-- Increase shared buffers
ALTER SYSTEM SET shared_buffers = '256MB';

-- Increase effective cache size
ALTER SYSTEM SET effective_cache_size = '1GB';

-- Increase work memory
ALTER SYSTEM SET work_mem = '16MB';

-- Reload configuration
SELECT pg_reload_conf();
```

### Redis

```bash
# Increase maxmemory
CONFIG SET maxmemory 256mb

# Set eviction policy
CONFIG SET maxmemory-policy allkeys-lru
```

## Support

For deployment issues, please open an issue on GitHub or contact: support@medicalcycle.local
