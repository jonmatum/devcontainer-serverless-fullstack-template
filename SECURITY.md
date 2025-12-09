# Security Best Practices

## Development vs Production

### This Template (Local Development)
- Configured for secure local development
- Uses dummy AWS credentials for local DynamoDB
- CORS configured for localhost
- Non-root users in containers
- Pinned dependency versions

### Before Production Deployment
**CRITICAL: Do NOT deploy this configuration directly to production.**

## Required Production Changes

### 1. AWS Credentials
```bash
# Remove from docker-compose.yml:
AWS_ACCESS_KEY_ID: dummy
AWS_SECRET_ACCESS_KEY: dummy

# Use instead:
# - IAM roles for EC2/ECS/Lambda
# - AWS Secrets Manager
# - Environment-specific configuration
```

### 2. CORS Configuration
```bash
# Set environment variable:
ALLOWED_ORIGINS=https://yourdomain.com,https://api.yourdomain.com
```

### 3. Remove Docker Socket
```yaml
# Remove from docker-compose.yml devcontainer service:
- /var/run/docker.sock:/var/run/docker.sock
```

### 4. Enable HTTPS/TLS
- Use AWS Certificate Manager
- Configure load balancer with TLS
- Enable Strict-Transport-Security headers

### 5. Network Security
- Deploy in VPC with private subnets
- Configure security groups restrictively
- Enable VPC endpoints for AWS services
- Use AWS WAF for API protection

## Production Deployment Checklist

- [ ] Remove dummy AWS credentials
- [ ] Configure IAM roles
- [ ] Set production ALLOWED_ORIGINS
- [ ] Enable HTTPS/TLS
- [ ] Remove Docker socket mount
- [ ] Configure AWS WAF
- [ ] Set up CloudWatch monitoring
- [ ] Enable CloudTrail logging
- [ ] Configure security groups
- [ ] Enable DynamoDB encryption
- [ ] Implement rate limiting
- [ ] Set up automated backups
- [ ] Review and update dependencies
- [ ] Perform security testing

## Regular Maintenance

### Update Dependencies
```bash
# Frontend
cd frontend/app
pnpm update --latest
pnpm audit

# Backend
cd backend
pipenv update
```

### Security Scanning
```bash
# Run security audits
pnpm audit          # Frontend
safety check        # Backend (pip install safety)
docker scan <image> # Container images
```

## Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [AWS Security Best Practices](https://aws.amazon.com/security/best-practices/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [Docker Security](https://docs.docker.com/engine/security/)

---

**Recommendation:** Review this file before deploying to production.


