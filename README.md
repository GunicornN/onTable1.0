# onTable

A restaurant management platform with QR code-based online ordering. Customers scan a QR code at their table, browse the menu, and place orders directly from their phone.

## Architecture

| Service | Technology | Description |
|---------|-----------|-------------|
| **Backend** | Django 3.x + DRF | REST API, restaurant dashboard, order management |
| **Frontend** | Vue.js 3 + Vuex | Customer-facing ordering interface |
| **Database** | PostgreSQL 11 + PostGIS 2.5 | Geolocation-enabled data storage |
| **Cache/Broker** | Redis | Celery task broker |
| **Workers** | Celery | Async tasks (QR code generation, emails) |
| **Proxy** | Nginx | Reverse proxy, rate limiting, static files |

## Features

- Restaurant registration with geolocation (PostGIS)
- Menu management (cards, categories, products)
- QR code generation for tables (PNG + PDF export)
- Online ordering flow (table selection, menu, cart, payment method)
- Employee management with invitation system
- Order tracking and management dashboard
- Document upload and storage
- Customer information management

## Getting Started

### Prerequisites

- Docker & Docker Compose

### Setup

1. Copy the environment file and configure it:
   ```bash
   cp conf/.env.example conf/.env.dev
   ```

2. Build and start the containers:
   ```bash
   docker-compose -f docker-compose.dev.yml up --build -d
   ```

3. Create a superuser:
   ```bash
   docker exec -it backend python /home/app/web/manage.py createsuperuser
   ```

4. Access the application:
   - Backend/Dashboard: http://localhost
   - API: http://localhost/api/
   - Frontend (ordering): http://localhost/orders/

### Environment Variables

See `conf/.env.example` for all required environment variables (database credentials, Django secret key, email settings, etc.).

## Project Structure

```
backend/
  company/          # Core models, serializers, API views
  company_manager/  # Restaurant dashboard (views, forms, templates)
  orders/           # Order processing
  home/             # Landing pages
  functionalities/  # QR code generation, PDF export
frontend/
  ontable1.1/       # Vue.js 3 customer ordering app
proxy/              # Nginx configuration
conf/               # Environment files
```

## Docker Services

```bash
# View running containers
docker ps

# Access backend shell
docker exec -it backend bash

# Access database
docker exec -it postgres11-postgis2.5 psql -U user -d onTable

# Access Redis CLI
docker exec -it redis redis-cli

# View logs
docker-compose -f docker-compose.dev.yml logs -f backend
```

## License

MIT
