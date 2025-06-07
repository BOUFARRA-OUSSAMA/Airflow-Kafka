# Kafka Streaming Pipeline with Confluent Platform & Airflow

A complete data streaming solution using Apache Kafka, Confluent Platform, and Apache Airflow with Neon PostgreSQL integration.

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Apache Airflow │────│   Kafka Broker  │────│ Confluent Center│
│   (Scheduler)    │    │   (Streaming)   │    │  (Monitoring)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         └──────────────│ Schema Registry │──────────────┘
                        │   (Data Gov)    │
                        └─────────────────┘
                                 │
                        ┌─────────────────┐
                        │ Neon PostgreSQL │
                        │   (Metadata)    │
                        └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Git
- 4GB+ RAM

### 1. Clone & Setup
```bash
git clone <your-repo>
cd airflow-kafka-project
```

### 2. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit with your credentials
nano .env
```

### 3. Required Environment Variables
```env
EXTERNAL_IP=your.server.ip
NEON_DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
AIRFLOW_SECRET_KEY=your_secure_key
```

### 4. Launch Services
```bash
# Start all services
docker-compose -f docker-compose_mod.yml up -d

# Check status
docker-compose ps
```

## 📊 Access Points

| Service | URL | Credentials |
|---------|-----|-------------|
| **Airflow UI** | `http://localhost:8080` | Setup required |
| **Confluent Center** | `http://localhost:9021` | No auth |
| **Schema Registry** | `http://localhost:8081` | API only |

## 🔧 Services

### Kafka Ecosystem
- **Zookeeper** `:2181` - Coordination service
- **Kafka Broker** `:9092` - Message streaming
- **Schema Registry** `:8081` - Schema management
- **Control Center** `:9021` - Web-based monitoring

### Airflow
- **Webserver** `:8080` - DAG management & monitoring
- **Backend**: Neon PostgreSQL (cloud-hosted)

## 📝 DAGs Available

### `kafka_stream.py`
Streams random user data from external API to Kafka topics:
- Fetches user data from `randomuser.me`
- Formats and validates data
- Produces to `users_created` topic
- Includes error handling & logging

## 🛠️ Development

### Create New DAG
```bash
# Add your DAG file
echo "from airflow import DAG..." > dags/my_new_dag.py

# Restart Airflow to pick up changes
docker-compose restart webserver
```

### Monitor Kafka Topics
```bash
# List topics
docker exec -it broker kafka-topics --bootstrap-server localhost:9092 --list

# Consume messages
docker exec -it broker kafka-console-consumer \
  --bootstrap-server localhost:9092 \
  --topic users_created \
  --from-beginning
```

### Check Logs
```bash
# Airflow logs
docker-compose logs webserver

# Kafka logs
docker-compose logs broker
```

## 🔍 Troubleshooting

### Common Issues

**Airflow DB Connection Failed**
```bash
# Check Neon connection
docker exec -it airflow-webserver python -c "
import psycopg2
conn = psycopg2.connect('$NEON_DATABASE_URL')
print('✅ Connection successful')
"
```

**Kafka Connection Refused**
```bash
# Check broker health
docker exec -it broker kafka-broker-api-versions --bootstrap-server localhost:9092
```

**Out of Memory**
```bash
# Check resource usage
docker stats
```

## 🔒 Security Notes

- Keep `.env` file secure (excluded from git)
- Use strong secrets for production
- Consider VPN for production deployments
- Enable SSL/TLS for external access

## 📚 Useful Commands

```bash
# Scale Kafka (if needed)
docker-compose up -d --scale broker=3

# Reset everything
docker-compose down -v

# View resource usage
docker-compose top
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---
**Built with** ❤️ using Apache Kafka, Confluent Platform, Apache Airflow & Neon PostgreSQL
