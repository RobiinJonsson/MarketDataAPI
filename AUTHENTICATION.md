n# 🔐 Authentication Security Guide

## Critical Security Requirements

### ⚠️ BEFORE DEPLOYING TO PRODUCTION

1. **Set Strong Secret Keys**:
   ```bash
   # Generate secure secrets
   python -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(32))"
   python -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_urlsafe(32))"
   ```

2. **Environment Variables** (Required for Production):
   ```bash
   export SECRET_KEY="your_super_secure_secret_key_here"
   export JWT_SECRET_KEY="your_different_jwt_secret_key_here"
   export AZURE_SQL_PASSWORD="your_database_password"
   ```

3. **Never Commit Secrets**:
   - ✅ Use `.env` files (gitignored)
   - ✅ Use environment variables
   - ❌ Never hardcode secrets in code
   - ❌ Never commit `.env` files

## Authentication Features

### User Types
- **User**: Read-only access to GET endpoints and frontend
- **Admin**: Full CRUD access including DataOps

### Rate Limiting
- Admin: 200 requests/minute
- User: 60 requests/minute
- Anonymous: 30 requests/minute

### Token Security
- Access tokens: 1 hour expiry
- Refresh tokens: 7 days expiry
- Automatic token refresh available

## CLI Commands

### Initial Setup
```bash
# Create default roles
mapi auth setup-roles

# Create admin user
mapi auth create-user --username admin --email admin@company.com --role admin

# Check status
mapi auth status
```

### User Management
```bash
# List users
mapi auth list-users

# Create user
mapi auth create-user --username john --email john@company.com --role user

# Assign role
mapi auth assign-role --username john --role admin

# Deactivate user
mapi auth deactivate-user --username john
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/register` - User registration (if enabled)
- `POST /api/v1/auth/refresh` - Token refresh
- `GET /api/v1/auth/me` - Current user info

### Usage Example
```bash
# Login
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your_password"}'

# Use token
curl -H "Authorization: Bearer your_jwt_token" \
  http://localhost:5000/api/v1/instruments
```

## Development vs Production

### SQLite Development
- Authentication **disabled** automatically
- No user management needed
- Full API access without tokens

### SQL Server Production
- Authentication **required**
- User accounts and roles enforced
- JWT tokens required for API access

## Security Best Practices

1. **Strong Passwords**: Minimum 8 characters, mixed case, numbers, symbols
2. **Regular Token Rotation**: Tokens expire automatically
3. **Environment Separation**: Different secrets for dev/staging/prod
4. **Audit Logging**: All authentication events are logged
5. **Rate Limiting**: Prevents brute force attacks

## Troubleshooting

### Common Issues
- **"Authentication disabled"**: You're using SQLite (expected for dev)
- **"Invalid token"**: Token expired, use refresh endpoint
- **"Insufficient permissions"**: User role doesn't allow operation
- **"Rate limited"**: Too many requests, wait and retry

### Check Authentication Status
```bash
mapi auth status
```

## Environment Variables Reference

### Required for Production
```bash
SECRET_KEY=                    # Flask secret key
JWT_SECRET_KEY=               # JWT signing key (should be different from SECRET_KEY)
AZURE_SQL_PASSWORD=           # Database password
```

### Optional
```bash
JWT_ACCESS_TOKEN_EXPIRES=1    # Hours (default: 1)
JWT_REFRESH_TOKEN_EXPIRES=168 # Hours (default: 168 = 7 days)
FLASK_ENV=production          # Environment mode
```

Remember: The authentication system is designed for production security while maintaining development simplicity!