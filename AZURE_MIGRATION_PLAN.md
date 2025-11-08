# Azure Migration Plan for MarketDataAPI

**Project**: MarketDataAPI  
**Branch**: dev_sql  
**Date**: November 4, 2025  
**Status**: Planning Phase

## Executive Summary

The MarketDataAPI project is **80% ready** for Azure hosting due to excellent architectural decisions including dual database support, service abstractions, and modular design. This migration focuses on configuration, security hardening, and cloud services integration rather than major code restructuring.

## Current Architecture Strengths ✅

- **Dual Database Support**: `DatabaseConfig` supports SQLite and Azure SQL
- **Service Abstraction**: Factory pattern with sqlite/ and sqlserver/ implementations  
- **Clean Separation**: Models, services, database layers properly isolated
- **Environment Configuration**: Robust `.env` and config system
- **Database Migrations**: Alembic ready for Azure SQL
- **Professional API**: Flask-RESTX with Swagger documentation
- **Modern Frontend**: TypeScript/Vite with build system

## Azure Resources & Costs

### Required Azure Services
```bash
# Resource Group (Already exists)
# az group create --name "MyFreeDBResourceGroup" --location "Sweden Central"

# Azure SQL Database (Basic tier - cheapest)
# Create with BOTH SQL and Entra ID authentication for flexibility
az sql server create --name "sqlsvr-marketdata-prod" --resource-group "MyFreeDBResourceGroup" --location "Sweden Central" --admin-user "marketdataadmin" --enable-ad-only-auth false
az sql db create --resource-group "MyFreeDBResourceGroup" --server "sqlsvr-marketdata-prod" --name "marketdata-prod" --service-objective Basic

# App Service Plan (F1 Free tier - for testing, or B1 for production)
# Free tier (60min CPU/day, sleeps after 20min inactivity):
az appservice plan create --name "asp-marketdata-free" --resource-group "MyFreeDBResourceGroup" --sku F1

# OR Basic tier for production (always-on, unlimited CPU):
# az appservice plan create --name "asp-marketdata-prod" --resource-group "MyFreeDBResourceGroup" --sku B1 --is-linux

# Web App (adjust plan name based on tier chosen above)
az webapp create --resource-group "MyFreeDBResourceGroup" --plan "asp-marketdata-free" --name "marketdata-api-prod" --runtime "PYTHON|3.11"

# Storage Account (Standard_LRS - cheapest)
az storage account create --name "stmarketdataprod" --resource-group "MyFreeDBResourceGroup" --location "Sweden Central" --sku Standard_LRS

# Key Vault
az keyvault create --name "kv-marketdata-prod" --resource-group "MyFreeDBResourceGroup" --location "Sweden Central"

# Application Insights (Basic)
az extension add --name application-insights
az monitor app-insights component create --app "marketdata-api-insights" --location "Sweden Central" --resource-group "MyFreeDBResourceGroup"
```

### Monthly Cost Estimate (Lowest Tiers)
| Service | Tier | Monthly Cost (USD) |
|---------|------|-------------------|
| Azure SQL Database | Basic (2GB) | ~$5 |
| App Service | **F1 Free Tier** (1GB RAM, 60min/day) | **$0** |  
| Storage Account | Standard_LRS (Hot, 5GB) | ~$0.11 |
| Key Vault | Standard (1000 operations) | ~$0.03 |
| Application Insights | Basic (5GB data) | ~$2.30 |
| **Total Estimated Cost** | | **~$7.44/month** |

### Cost Comparison: Free vs Paid App Service
| Tier | RAM | CPU Time | Always On | Cost | Best For |
|------|-----|----------|-----------|------|----------|
| **F1 (Free)** | 1GB | 60min/day | No | $0 | Development/Testing |
| **D1 (Shared)** | 1GB | 240min/day | No | ~$9.49 | Light Production |
| **B1 (Basic)** | 1.75GB | Unlimited | Yes | ~$13 | Production |

*Note: F1 Free tier has limitations - app sleeps after 20min inactivity and has 60min daily CPU quota.*

### Recommended Approach: Start Free, Scale Up
1. **Phase 1-2**: Use **F1 Free tier** for initial migration and testing (~$7.44/month total)
2. **Phase 3+**: Upgrade to **B1 Basic** when ready for production (~$20.44/month total)

### Storage Management Strategy (5GB Requirement)
With 5GB total storage needs, implement smart deletion policies:

```python
# Storage cleanup strategy
class StorageManager:
    def cleanup_old_files(self, retention_days=30):
        # Keep only last 30 days of FIRDS/FITRS files
        # Compress files older than 7 days
        # Archive critical files to cheaper cold storage tier
        pass
    
    def get_storage_stats(self):
        # Monitor storage usage
        # Alert when approaching 4GB (80% of limit)
        pass
```

**Storage Tier Strategy**:
- **Hot tier**: Current/recent files (last 7 days) - $0.0184/GB
- **Cool tier**: Archive files (7-30 days old) - $0.01/GB  
- **Archive tier**: Long-term storage (>30 days) - $0.00099/GB

With smart management, 5GB actual usage could cost ~$0.05-0.10/month instead of $0.11.

## Migration Phases

### Phase 1: Infrastructure Setup (Week 1)

**Objective**: Deploy Azure resources and establish connectivity

**Tasks**:
1. Create Azure subscription/resource group
2. Deploy infrastructure using provided CLI commands
3. Configure firewall rules for database access
4. Set up Key Vault with initial secrets

**Success Criteria**:
- All Azure resources provisioned
- Database connection from local development environment works
- Key Vault accessible with proper permissions

**Environment Variables**:
```env
# Phase 1: SQL Authentication (Development/Testing)
DATABASE_TYPE=azure_sql
AZURE_SQL_SERVER=sqlsvr-marketdata-prod.database.windows.net
AZURE_SQL_DATABASE=marketdata-prod
AZURE_SQL_USERNAME=marketdataadmin
AZURE_SQL_PASSWORD=<from-keyvault>
AZURE_SQL_PORT=1433
AZURE_SQL_AUTH_METHOD=sql

# Phase 2: Entra ID Authentication (Enterprise/Work)
# DATABASE_TYPE=azure_sql
# AZURE_SQL_SERVER=sqlsvr-marketdata-prod.database.windows.net
# AZURE_SQL_DATABASE=marketdata-prod
# AZURE_SQL_AUTH_METHOD=entra
# AZURE_TENANT_ID=<work-tenant-id>
```

### Phase 2: Database Migration (Week 1-2)

**Objective**: Migrate SQLite database to Azure SQL

**Prerequisites**:
- Azure SQL Database provisioned
- Connection string configured
- Local environment testing completed

**Steps**:
1. Update Alembic configuration for Azure SQL
2. Test connection with existing codebase
3. Run database migrations
4. Verify all models work correctly
5. Test CLI and API functionality

**Alembic Configuration Update**:
```ini
# config/alembic.ini
sqlalchemy.url = mssql+pyodbc://%(DB_USER)s:%(DB_PASS)s@%(DB_HOST)s:1433/%(DB_NAME)s?driver=ODBC+Driver+17+for+SQL+Server&Encrypt=yes&TrustServerCertificate=no
```

**Testing Commands**:
```bash
# Test database type detection
python -c "from marketdata_api.config import DatabaseConfig; print(DatabaseConfig.get_database_type())"

# Run migrations
alembic upgrade head

# Verify functionality
marketdata stats
marketdata instruments list --limit 5
```

**Success Criteria**:
- All Alembic migrations execute successfully
- CLI commands work with Azure SQL
- API endpoints return data correctly
- No performance degradation observed

### Phase 3: Authentication & Security (Week 2-3)

**Objective**: Implement authentication, authorization, and rate limiting

**New Components Required**:
```python
# src/marketdata_api/auth/
├── __init__.py
├── models.py          # User, Role, Permission models
├── decorators.py      # @require_auth, @require_role decorators  
├── jwt_handler.py     # JWT token management
├── middleware.py      # Authentication middleware
└── azure_ad.py       # Azure AD integration (optional)
```

**Dependencies to Add**:
```txt
# Add to requirements.txt
Flask-JWT-Extended==4.5.3
Flask-Limiter==3.5.0
bcrypt==4.1.2
```

**Rate Limiting Implementation**:
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["1000 per hour", "100 per minute"]
)

# Endpoint-specific limits
@limiter.limit("10 per minute")  # Lower limit for expensive operations
@limiter.limit("50 per minute")  # Higher limit for read operations
```

**Authentication Strategy Options**:
1. **JWT Tokens** (Recommended for API-first)
2. **Azure AD B2C** (Enterprise integration)
3. **Simple API Keys** (Minimal implementation)

**Success Criteria**:
- Authentication system functional
- Rate limiting prevents abuse
- API keys/tokens secure in Key Vault
- All endpoints properly protected

### Phase 4: Security Hardening (Week 3)

**Objective**: Implement production-grade security measures

**Security Components**:
```python
# Dependencies
Flask-Talisman==1.1.0  # Security headers
azure-keyvault-secrets==4.7.0  # Key Vault integration
azure-identity==1.15.0  # Azure authentication
```

**Key Vault Integration**:
```python
# src/marketdata_api/config/azure_config.py
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

class AzureConfig:
    def __init__(self):
        credential = DefaultAzureCredential()
        self.client = SecretClient(
            vault_url="https://kv-marketdata-prod.vault.azure.net/",
            credential=credential
        )
    
    def get_secret(self, name: str) -> str:
        return self.client.get_secret(name).value
```

**Security Headers**:
```python
from flask_talisman import Talisman

# Apply security headers
Talisman(app, 
    force_https=True,
    strict_transport_security=True,
    content_security_policy={
        'default-src': "'self'",
        'script-src': "'self' 'unsafe-inline'",
        'style-src': "'self' 'unsafe-inline'"
    }
)
```

**Secrets Migration Plan**:
1. Move all sensitive values to Key Vault
2. Update config.py to use Key Vault
3. Remove hardcoded secrets from code/env files
4. Test secret retrieval in all environments

**Success Criteria**:
- All secrets in Key Vault
- HTTPS enforced
- Security headers implemented
- No sensitive data in configuration files

### Phase 5: File Storage Migration (Week 3-4)

**Objective**: Move ESMA file storage from local filesystem to Azure Blob Storage

**Current State**: Files stored in `data/downloads/firds/` and `data/downloads/fitrs/`
**Target State**: Files in Azure Blob Storage containers

**Implementation**:
```python
# src/marketdata_api/services/azure_storage.py
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential

class AzureStorageService:
    def __init__(self):
        self.client = BlobServiceClient(
            account_url="https://stmarketdataprod.blob.core.windows.net",
            credential=DefaultAzureCredential()
        )
    
    def upload_firds_file(self, file_path: str, blob_name: str):
        container_client = self.client.get_container_client("firds")
        with open(file_path, "rb") as data:
            container_client.upload_blob(name=blob_name, data=data, overwrite=True)
    
    def download_firds_file(self, blob_name: str, local_path: str):
        blob_client = self.client.get_blob_client(container="firds", blob=blob_name)
        with open(local_path, "wb") as f:
            f.write(blob_client.download_blob().readall())
```

**Configuration Updates**:
```python
# Update src/marketdata_api/config.py
class esmaConfig:
    if os.getenv("AZURE_STORAGE_ACCOUNT"):
        # Azure Blob Storage mode
        storage_account = os.getenv("AZURE_STORAGE_ACCOUNT")
        firds_container = "firds"
        fitrs_container = "fitrs"
        use_azure_storage = True
    else:
        # Local filesystem fallback
        downloads_path = Path("data/downloads")
        firds_path = downloads_path / "firds"
        fitrs_path = downloads_path / "fitrs"
        use_azure_storage = False
```

**Migration Steps**:
1. Create blob containers (`firds`, `fitrs`)
2. Upload existing local files to blob storage
3. Update file management services to use Azure Storage
4. Test file download/upload functionality
5. Implement cleanup policies for old files

**Success Criteria**:
- All ESMA files stored in Azure Blob Storage
- File upload/download working correctly
- Local file system no longer required for file storage
- Cost-effective storage tier selected

### Phase 6: Monitoring & Logging (Week 4)

**Objective**: Implement comprehensive monitoring and logging

**Application Insights Setup**:
```python
# Dependencies
opencensus-ext-azure==1.1.13
opencensus-ext-flask==0.8.0

# src/marketdata_api/monitoring/insights.py
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.ext.flask.flask_middleware import FlaskMiddleware

def setup_monitoring(app):
    # Request tracking
    middleware = FlaskMiddleware(app)
    
    # Custom logging
    handler = AzureLogHandler(
        connection_string=os.getenv('APPLICATIONINSIGHTS_CONNECTION_STRING')
    )
    app.logger.addHandler(handler)
    
    # Custom metrics
    from opencensus.stats import aggregation as aggregation_module
    from opencensus.stats import measure as measure_module
    
    # Define custom metrics
    request_latency = measure_module.MeasureFloat(
        "request_latency", "Request latency", "ms"
    )
```

**Health Check Endpoints**:
```python
# src/marketdata_api/api/resources/health.py
@api.route('/health')
class HealthCheck(Resource):
    def get(self):
        try:
            # Database connectivity
            from sqlalchemy import text
            db.session.execute(text("SELECT 1"))
            
            # External API status
            openfigi_status = self._test_openfigi()
            gleif_status = self._test_gleif()
            
            # Azure services
            storage_status = self._test_azure_storage()
            
            return {
                'status': 'healthy',
                'timestamp': datetime.utcnow().isoformat(),
                'services': {
                    'database': 'connected',
                    'openfigi': openfigi_status,
                    'gleif': gleif_status,
                    'storage': storage_status
                },
                'version': app.config.get('VERSION', '1.0.0')
            }
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {
                'status': 'unhealthy', 
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }, 500
```

**Monitoring Dashboards**:
- API response times
- Database query performance  
- Error rates and exceptions
- External API dependency health
- File processing metrics

**Success Criteria**:
- Application Insights collecting telemetry
- Health check endpoints working
- Custom dashboards created
- Alerts configured for critical failures

### Phase 7: CI/CD Pipeline (Week 4-5)

**Objective**: Automate testing and deployment

**GitHub Actions Workflow**:
```yaml
# .github/workflows/azure-deploy.yml
name: Deploy to Azure

on:
  push:
    branches: [main, dev_sql]
  pull_request:
    branches: [main]

env:
  PYTHON_VERSION: '3.11'
  NODE_VERSION: '18'

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      sql-server:
        image: mcr.microsoft.com/mssql/server:2022-latest
        env:
          SA_PASSWORD: TestPass123!
          ACCEPT_EULA: Y
        ports:
          - 1433:1433
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ env.PYTHON_VERSION }}
    
    - name: Install Python dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -e .
    
    - name: Run Python tests
      env:
        DATABASE_TYPE: azure_sql
        AZURE_SQL_SERVER: localhost
        AZURE_SQL_DATABASE: marketdata_test
        AZURE_SQL_USERNAME: sa
        AZURE_SQL_PASSWORD: TestPass123!
      run: |
        pytest src/marketdata_api/tests/ -v --cov=marketdata_api
    
    - name: Set up Node.js
      uses: actions/setup-node@v4
      with:
        node-version: ${{ env.NODE_VERSION }}
        cache: 'npm'
        cache-dependency-path: frontend-modern/package-lock.json
    
    - name: Install frontend dependencies
      working-directory: frontend-modern
      run: npm ci
    
    - name: Build frontend
      working-directory: frontend-modern
      run: npm run build
    
    - name: Upload frontend artifacts
      uses: actions/upload-artifact@v4
      with:
        name: frontend-dist
        path: frontend-modern/dist/

  deploy-staging:
    if: github.ref == 'refs/heads/dev_sql'
    needs: test
    runs-on: ubuntu-latest
    environment: staging
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Download frontend artifacts
      uses: actions/download-artifact@v4
      with:
        name: frontend-dist
        path: frontend-modern/dist/
    
    - name: Deploy to Azure Web App (Staging)
      uses: azure/webapps-deploy@v2
      with:
        app-name: 'marketdata-api-staging'
        publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE_STAGING }}
        package: '.'

  deploy-production:
    if: github.ref == 'refs/heads/main'
    needs: test
    runs-on: ubuntu-latest
    environment: production
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Download frontend artifacts
      uses: actions/download-artifact@v4
      with:
        name: frontend-dist
        path: frontend-modern/dist/
    
    - name: Deploy to Azure Web App (Production)
      uses: azure/webapps-deploy@v2
      with:
        app-name: 'marketdata-api-prod'
        publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
        package: '.'
    
    - name: Run post-deployment tests
      run: |
        # Health check
        curl -f https://marketdata-api-prod.azurewebsites.net/health || exit 1
```

**Deployment Environments**:
- **Staging**: `dev_sql` branch → `marketdata-api-staging.azurewebsites.net`
- **Production**: `main` branch → `marketdata-api-prod.azurewebsites.net`

**Success Criteria**:
- Automated testing on all PRs
- Successful deployment to staging on `dev_sql` pushes
- Successful deployment to production on `main` pushes
- Post-deployment health checks passing

### Phase 8: Performance Optimization (Week 5)

**Objective**: Optimize for production performance and scalability

**Caching Implementation**:
```python
# Dependencies
Flask-Caching==2.1.0
redis==5.0.1

# Configuration
cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': os.getenv('REDIS_URL', 'redis://localhost:6379/0')
})

# Usage examples
@cache.cached(timeout=300, key_prefix='instruments')
def get_instruments_list():
    # Expensive database query
    pass

@cache.memoize(timeout=3600)
def get_cfi_classification(cfi_code):
    # CFI code analysis
    pass
```

**Database Connection Optimization**:
```python
# Update sql_server_database.py
def _create_engine(self):
    connection_string = self._build_connection_string()
    return create_engine(
        connection_string,
        pool_size=10,          # Connections to keep open
        max_overflow=20,       # Additional connections when needed
        pool_pre_ping=True,    # Validate connections before use
        pool_recycle=3600,     # Recycle connections after 1 hour
        echo=False             # Disable SQL logging in production
    )
```

**API Response Optimization**:
```python
# Implement pagination for large datasets
@api.route('/instruments')
class InstrumentList(Resource):
    def get(self):
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        
        instruments = Instrument.query.paginate(
            page=page, 
            per_page=per_page,
            error_out=False
        )
        
        return {
            'instruments': [i.to_dict() for i in instruments.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': instruments.total,
                'pages': instruments.pages
            }
        }
```

**Success Criteria**:
- API response times under 2 seconds for complex queries
- Database connection pool stable under load
- Caching reducing database queries by 70%+
- Frontend loading times under 3 seconds

## Environment Configurations

### Development Environment
```env
# .env (local development)
DATABASE_TYPE=sqlite
FLASK_ENV=development
DEBUG=true
SQLITE_DB_PATH=src/marketdata_api/database/marketdata.db
OPENFIGI_API_KEY=your_dev_key
```

### Staging Environment (Azure)
```env
# Azure App Service Configuration - Staging
DATABASE_TYPE=azure_sql
FLASK_ENV=staging
DEBUG=false
AZURE_SQL_SERVER=sql-marketdata-staging.database.windows.net
AZURE_SQL_DATABASE=marketdata-staging
AZURE_SQL_USERNAME=marketdataadmin
AZURE_SQL_PASSWORD=<from-keyvault>
APPLICATIONINSIGHTS_CONNECTION_STRING=<from-keyvault>
SECRET_KEY=<from-keyvault>
AZURE_STORAGE_ACCOUNT=stmarketdatastaging
```

### Production Environment (Azure)
```env
# Azure App Service Configuration - Production
DATABASE_TYPE=azure_sql
FLASK_ENV=production
DEBUG=false
AZURE_SQL_SERVER=sqlsvr-marketdata-prod.database.windows.net
AZURE_SQL_DATABASE=marketdata-prod
AZURE_SQL_USERNAME=marketdataadmin
AZURE_SQL_PASSWORD=<from-keyvault>
APPLICATIONINSIGHTS_CONNECTION_STRING=<from-keyvault>
SECRET_KEY=<from-keyvault>
AZURE_STORAGE_ACCOUNT=stmarketdataprod
REDIS_URL=<redis-connection-string>
```

## Risk Management

### Database Migration Risks
**Risk**: Data loss during SQLite to Azure SQL migration  
**Mitigation**: 
- Complete database backup before migration
- Test migration in staging environment first
- Keep SQLite database as rollback option
- Implement data verification scripts

**Risk**: Performance degradation with Azure SQL  
**Mitigation**:
- Load testing in staging environment
- Connection pooling implementation
- Query optimization and indexing
- Monitor query performance with Application Insights

### Security Risks
**Risk**: Exposure of API keys and secrets  
**Mitigation**:
- Immediate migration of all secrets to Key Vault
- Remove hardcoded secrets from codebase
- Implement proper access controls
- Regular security audits

**Risk**: Unauthorized API access  
**Mitigation**:
- Implement authentication before public deployment
- Rate limiting to prevent abuse
- IP whitelisting for sensitive operations
- Comprehensive logging and monitoring

### Infrastructure Risks
**Risk**: Azure service outages  
**Mitigation**:
- Multi-region deployment (future enhancement)
- Local development environment as fallback
- Comprehensive monitoring and alerting
- Service-level agreement understanding

**Risk**: Unexpected costs  
**Mitigation**:
- Start with lowest-tier services
- Implement cost alerts and budgets
- Monitor usage patterns
- Regular cost optimization reviews

## Success Metrics

### Technical Metrics
- **Database Migration**: 100% data integrity, <5s query response time
- **API Performance**: <2s response time for 95% of requests
- **Uptime**: 99.9% availability target
- **Security**: Zero critical vulnerabilities, all secrets in Key Vault

### Business Metrics
- **Cost**: Stay within $25/month budget initially
- **User Experience**: Frontend load time <3 seconds
- **Reliability**: <1% error rate on API calls
- **Scalability**: Handle 1000+ API requests/hour without degradation

## Timeline Summary

| Week | Phase | Key Deliverables | Success Criteria |
|------|-------|------------------|------------------|
| 1 | Infrastructure + DB Migration | Azure resources, database working | API functional with Azure SQL |
| 2-3 | Authentication + Security | Auth system, rate limiting | All endpoints protected |
| 3-4 | Storage + Monitoring | Blob storage, logging | Files in cloud, telemetry working |
| 4-5 | CI/CD + Performance | Automated deploy, optimization | Push-to-deploy functional |

## Next Actions

### Immediate (This Week)
1. **Create Azure Subscription**: Set up Azure account and billing
2. **Deploy Infrastructure**: Run provided Azure CLI commands
3. **Test Database Connection**: Verify Azure SQL connectivity from local environment
4. **Update Configuration**: Set `DATABASE_TYPE=azure_sql` in dev environment

### Week 1 Priorities
1. **Complete Database Migration**: Run Alembic against Azure SQL
2. **Verify Functionality**: Test all CLI commands and API endpoints
3. **Document Issues**: Track any compatibility problems
4. **Performance Baseline**: Establish baseline metrics for comparison

### Setup Commands to Run First
```bash
# 1. Check current database configuration
python -c "from marketdata_api.config import DatabaseConfig; print(f'Current DB type: {DatabaseConfig.get_database_type()}')"

# 2. Test current functionality
marketdata stats
marketdata instruments list --limit 3

# 3. Create Azure resources (requires Azure CLI)
az login
az group create --name "rg-marketdata-prod" --location "West Europe"
# ... (run full infrastructure commands)

# 4. Test Azure SQL connection
# (Update .env with Azure SQL settings first)
python -c "from marketdata_api.config import DatabaseConfig; print(f'New DB type: {DatabaseConfig.get_database_type()}')"

# 5. Run migration
alembic upgrade head

# 6. Verify migration success
marketdata stats
```

## Contact & Support

- **Technical Issues**: Create GitHub issues on the MarketDataAPI repository
- **Azure Support**: Utilize Azure support channels for infrastructure issues
- **Documentation**: This plan will be updated as implementation progresses

---

*This migration plan is a living document and should be updated as implementation progresses and requirements change.*