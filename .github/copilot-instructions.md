# MarketDataAPI - AI Agent Instructions

## Architecture Overview

This is a financial market data platform with **CFI-based instrument classification** as the core organizing principle. The system processes ESMA FIRDS/FITRS data for MiFID II transparency calculations.

### Key Architectural Decisions
- **CFI codes (ISO 10962) are the single source of truth** for instrument classification - all routing, validation, and file filtering is CFI-driven
- **JSON-based unified models** replaced complex polymorphic inheritance for better maintainability
- **Dual database support**: SQLite (development) and Azure SQL (production) with identical schemas
- **Modular Swagger API** organized by business domain (instruments, entities, transparency, MIC, relationships)

## Critical Project Structure

```
src/marketdata_api/
├── cli.py                    # Rich/Click-based professional CLI
├── config.py                 # Environment-aware config with dual DB support
├── constants.py              # Centralized HTTP codes, pagination, error messages
├── database/                 # Database initialization and session management
├── models/sqlite/            # Unified SQLAlchemy models (JSON + promoted fields)
├── services/                 # Business logic layer (sqlite/ and sqlserver/ variants)
├── swagger/                  # Modular API (config.py, models/, resources/)
└── routes/                   # Flask routes organized by domain

deployment/mapi.bat           # CLI wrapper script (sets PYTHONPATH, SQLITE_DB_PATH)
alembic/                      # Database migrations (auto-imports all models)
```

## Essential Developer Workflows

### CLI Usage (Primary Interface)
```bash
# Use the wrapper script for proper environment setup
deployment\mapi.bat instruments list --limit 10 --type equity
deployment\mapi.bat transparency calculate SE0000108656
deployment\mapi.bat init --force  # Database initialization
```

### Database Operations
- **Always check database state**: CLI auto-detects missing DB and offers initialization
- **Migrations**: Use `alembic upgrade head` - all models auto-imported in `alembic/env.py`
- **Dual DB setup**: Environment variable `DATABASE_TYPE=sqlite|azure_sql` controls database backend

### Package Building
```bash
python -m build  # Creates wheel/source in build/dist/
pip install -e . # Development installation
```

## Project-Specific Patterns

### CFI-Driven File Filtering
```python
# CFI first character maps directly to FIRDS file types
# C=Collective Investment, D=Debt, E=Equity, etc.
instrument_type = cfi_code[0] if cfi_code else None
```

### Model Design Pattern
- **Promoted fields**: Frequently-used FIRDS attributes moved to dedicated columns for performance
- **JSON storage**: Type-specific data in `firds_data` and `processed_attributes` columns
- **Base model**: All models inherit from `base_model.Base` with common audit fields

### Service Layer Architecture
```python
# Services have database-specific implementations
from marketdata_api.services.sqlite.instrument_service import SqliteInstrumentService
from marketdata_api.services.sqlserver.instrument_service import SqlServerInstrumentService
```

### Environment Configuration
- **SQLITE_DB_PATH**: Must be set for CLI operations (handled by `deployment/mapi.bat`)
- **PYTHONPATH**: Include `src/` directory for development
- **Database detection**: `database_exists()` function checks for proper database setup

## Critical Integration Points

### FIRDS Data Processing
- **10 instrument types supported**: C,D,E,F,H,I,J,O,R,S (all ESMA FIRDS categories)
- **Regex-based file matching**: Precise patterns prevent false positives during file processing
- **Auto-detection**: Instrument types determined from FIRDS filenames

### MIC Code System (ISO 10383)
- **Dual-mode operations**: Local database storage + remote validation via ISO registry
- **Official data source**: `https://www.iso20022.org/.../ISO10383_MIC.csv`
- **Caching**: 60-minute cache for remote operations

### API Structure
- **Domain-organized endpoints**: `/api/v1/instruments`, `/api/v1/entities`, `/api/v1/transparency`
- **Swagger modularization**: Resources split by business domain, not technical layers
- **CFI validation**: Real-time validation on all instrument operations

## Error Handling Patterns

- **Rich CLI output**: Use `console.print()` with color coding and status indicators
- **Database errors**: Graceful fallback with user-friendly initialization prompts
- **Validation**: CFI code validation at API and CLI levels with detailed error messages

## Development Constraints & Preferences

### Required Libraries & Frameworks
- **Database**: SQLAlchemy 2.0+ only (no raw SQL)
- **CLI**: Rich + Click framework for all CLI enhancements
- **API**: Flask-RESTX for Swagger documentation
- **Async**: Use aiohttp for external API calls, not requests

### Forbidden Libraries
- **No Django**: This is a Flask-based project
- **No FastAPI**: Stick to Flask ecosystem
- **No Pandas operations on large datasets**: Use SQLAlchemy for data processing

### Code Style Requirements
- **Type hints**: Always use type annotations
- **Error handling**: Use Rich console for user-facing errors
- **Logging**: Use the configured logger, never print() statements
- **Database**: Always use service layer, never direct model access in routes

### Architecture Rules
- **CFI-first**: All instrument logic must start with CFI code validation
- **Service pattern**: Business logic belongs in services/, not routes/
- **No circular imports**: Import from lower-level modules only
- **Database agnostic**: Code must work with both SQLite and Azure SQL

## AI Agent Communication Guidelines

### When to Provide Feedback
- **Better approaches**: If you identify a more efficient or maintainable solution than what's requested, suggest it
- **Constraint conflicts**: If a request conflicts with these instructions, explain the constraint instead of ignoring it
- **Architecture improvements**: Suggest CFI-driven alternatives when non-CFI approaches are requested

### Example Responses
- "That approach would work, but using CFI-based filtering here would be more consistent with the architecture..."
- "I notice you're asking for raw SQL, but our constraints require SQLAlchemy. Here's how to achieve the same result..."
- "This request conflicts with our 'no circular imports' rule. Here's an alternative approach..."

### Documentation Style
- **Keep it concise**: No one reads verbose documentation - focus on essential information only
- **No emojis**: Professional documentation should be clean and emoji-free
- **Bullet points over paragraphs**: Scannable content is more useful
- **Action-oriented**: Focus on what developers need to do, not background theory

## Testing and Debugging

- **Test configuration**: `config/pytest.ini` for test settings
- **Logging**: Automatic log rotation in `logs/` directory
- **Debug config**: `debug_config.py` for development troubleshooting

When working with this codebase, always consider the CFI-driven architecture first - most decisions about instrument handling, file routing, and business logic stem from the CFI classification system.

## Documentation Policy

**CRITICAL**: Stop creating new .md files. The project has 68+ markdown files - this is documentation sprawl.

### Documentation Rules
- **Before creating ANY .md file**: Update existing files instead
- **Target**: <10 total .md files maximum
- **Core files only**: README.md, CHANGELOG.md, DEPLOYMENT.md, PROJECT_STRUCTURE.md, component READMEs
- **Forbidden**: *_SUMMARY.md, *_ARCHITECTURE.md, *_PLAN.md, temporary analysis files
- **Information hierarchy**: 
  - Project info → README.md
  - Changes → CHANGELOG.md  
  - Setup → README.md or DEPLOYMENT.md
  - Development notes → Issues/tickets, not files
  - Architecture → Inline comments + README.md sections

### Consolidation Priority
1. Delete redundant summary/analysis files
2. Merge related documentation into existing core files
3. Move temporary content to issues or delete entirely
4. Keep only essential, user-facing documentation