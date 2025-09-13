# Scripts Directory

This directory contains utility and analysis scripts for the MarketDataAPI project. Each script serves a specific purpose in maintaining, analyzing, or operating the system.

**Note**: The main CLI has been moved to `marketdata_cli.py` in the project root with modern Click framework and Rich formatting. Use `mapi.bat [command]` or `python marketdata_cli.py [command]` for interactive operations.

## Core Operational Scripts

### `backup_db.py`
**Purpose**: Database backup utility for creating backups of the MarketDataAPI database.

**Usage**:
```bash
python scripts/backup_db.py
```

**Key Features**:
- Creates timestamped database backups
- Supports both SQLite and Azure SQL databases
- Configurable backup locations
- Automated backup validation

**When to Use**: Before major database operations, during maintenance windows, or as part of regular backup procedures.

---

## Database Management Scripts

### `upgrade_production_db.py`
**Purpose**: Production database upgrade tool for safely applying schema changes and migrations.

**Usage**:
```bash
python scripts/upgrade_production_db.py
```

**Key Features**:
- Checks current database state and Alembic version tracking
- Initializes Alembic version table if missing
- Applies all pending migrations safely
- Provides detailed upgrade progress and validation
- Supports rollback capabilities
- Comprehensive error handling and logging

**When to Use**: 
- Upgrading production database schema to match development
- Applying new Alembic migrations to existing databases
- Initial setup of Alembic version tracking

**Safety Features**:
- Pre-upgrade validation and compatibility checks
- Backup recommendations before major changes
- Step-by-step progress reporting
- Rollback guidance if issues occur

---

### `init_azure_sql.py`
**Purpose**: Azure SQL database initialization and setup utility.

**Usage**:
```bash
python scripts/init_azure_sql.py
```

**Key Features**:
- Creates initial Azure SQL database structure
- Sets up authentication and connection parameters
- Configures database permissions and users
- Validates Azure SQL connectivity

**When to Use**: Initial setup of new Azure SQL databases, or when reconfiguring database connections.

---

### `create_migration.py`
**Purpose**: Alembic migration creation helper for database schema changes.

**Usage**:
```bash
python scripts/create_migration.py "migration_description"
```

**Key Features**:
- Generates new Alembic migration files
- Auto-detects model changes
- Provides migration templates
- Validates migration syntax

**When to Use**: When making changes to SQLAlchemy models that require database schema updates.

---

## Analysis and Monitoring Scripts

### `analyze_production_schema.py`
**Purpose**: Comprehensive database schema analysis and health monitoring tool.

**Usage**:
```bash
python scripts/analyze_production_schema.py
```

**Key Features**:
- Detailed schema structure analysis
- Migration level tracking and validation
- Feature availability detection (transparency tables, relationships, etc.)
- Table and column inventory
- Schema compatibility checking
- Performance and health metrics

**Output Includes**:
- Table count and structure overview
- Current migration level and status
- Available features and capabilities
- Missing tables or columns identification
- Schema health indicators

**When to Use**:
- Regular database health monitoring
- Before and after schema upgrades
- Troubleshooting schema-related issues
- Documenting current database state
- Validating feature availability

---

### `validate_refactoring.py`
**Purpose**: Code validation tool for ensuring application integrity after refactoring.

**Usage**:
```bash
python scripts/validate_refactoring.py
```

**Key Features**:
- Import validation for all route modules
- API endpoint accessibility testing
- Database connection validation
- Configuration verification
- Route registration testing
- Swagger documentation validation

**When to Use**: After major code refactoring, before deployments, or when troubleshooting import/routing issues.

---

## Infrastructure and Integration Scripts

### `azure_firewall_helper.py`
**Purpose**: Azure firewall management utility for database access control.

**Usage**:
```bash
python scripts/azure_firewall_helper.py [add|remove|list] [ip_address]
```

**Key Features**:
- Automatic IP address detection
- Azure firewall rule management
- Temporary and permanent rule creation
- Rule cleanup and maintenance
- Azure CLI integration

**When to Use**: 
- Setting up development environment access to Azure SQL
- Managing IP whitelist for database connections
- Troubleshooting Azure connectivity issues

---

### `sync_entity_relationships.py`
**Purpose**: GLEIF entity relationship synchronization and maintenance.

**Usage**:
```bash
python scripts/sync_entity_relationships.py [entity_lei] [options]
```

**Key Features**:
- Direct and ultimate parent/child relationship sync
- Batch processing with configurable sizes
- Relationship pruning and cleanup
- API rate limiting and error handling
- Progress tracking and reporting

**When to Use**: 
- Updating entity relationship data from GLEIF
- Maintaining entity hierarchy accuracy
- Bulk relationship data updates

---

## Documentation and Development Scripts

### `generate_docs.py`
**Purpose**: Automated API documentation generation from OpenAPI specifications.

**Usage**:
```bash
python scripts/generate_docs.py
```

**Key Features**:
- OpenAPI/Swagger documentation generation
- Route documentation extraction
- Model schema documentation
- Example request/response generation
- Multi-format output (HTML, Markdown, JSON)

**When to Use**: After API changes, before releases, or when updating documentation.

---

### `update_docs.py`
**Purpose**: Documentation update and maintenance utility.

**Usage**:
```bash
python scripts/update_docs.py
```

**Key Features**:
- Automated documentation updates
- README synchronization
- API documentation refresh
- Documentation validation
- Cross-reference checking

**When to Use**: Regular documentation maintenance, after feature additions, or before releases.

---

## Script Categories Summary

### 🔧 **Core Operations**
- `cli.py` - Main command-line interface
- `backup_db.py` - Database backup utility

### 🗄️ **Database Management**
- `upgrade_production_db.py` - Production database upgrades
- `init_azure_sql.py` - Azure SQL initialization
- `create_migration.py` - Migration generation

### 📊 **Analysis & Monitoring**
- `analyze_production_schema.py` - Schema analysis and health monitoring
- `validate_refactoring.py` - Code validation after changes

### ☁️ **Infrastructure**
- `azure_firewall_helper.py` - Azure firewall management
- `sync_entity_relationships.py` - GLEIF entity synchronization

### 📖 **Documentation**
- `generate_docs.py` - API documentation generation
- `update_docs.py` - Documentation maintenance

## Best Practices

1. **Always backup** before running database modification scripts
2. **Test in development** before running scripts in production
3. **Review logs** for any errors or warnings after script execution
4. **Keep scripts updated** with the latest configuration and dependencies
5. **Use version control** to track script changes and improvements

## Dependencies

Most scripts require:
- Python 3.8+
- MarketDataAPI project dependencies (see `requirements.txt`)
- Proper database configuration
- Azure CLI (for Azure-related scripts)
- Active database connection

## Troubleshooting

### Common Issues:
1. **Import errors**: Ensure the project root is in Python path
2. **Database connection issues**: Check configuration and firewall settings
3. **Permission errors**: Verify database credentials and access rights
4. **Azure connectivity**: Use `azure_firewall_helper.py` to manage access

### Getting Help:
- Check script logs for detailed error messages
- Use `python script_name.py --help` for usage information
- Refer to project documentation for configuration details
- Run `analyze_production_schema.py` for database health insights

---

*Last updated: July 26, 2025*
