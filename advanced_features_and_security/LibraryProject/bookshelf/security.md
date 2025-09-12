# Security Configuration

This project is secured with the following Django settings:

- **SECURE_SSL_REDIRECT = True** → Forces HTTPS connections.
- **SECURE_HSTS_SECONDS = 31536000, SECURE_HSTS_INCLUDE_SUBDOMAINS = True, SECURE_HSTS_PRELOAD = True** → Enforces HSTS for 1 year, all subdomains included.
- **SESSION_COOKIE_SECURE = True, CSRF_COOKIE_SECURE = True** → Cookies only sent via HTTPS.
- **X_FRAME_OPTIONS = "DENY"** → Protects against clickjacking.
- **SECURE_CONTENT_TYPE_NOSNIFF = True** → Prevents MIME-sniffing.
- **SECURE_BROWSER_XSS_FILTER = True** → Enables browser XSS protection.

### Deployment Notes
- SSL/TLS certificates managed by Let’s Encrypt.
- Nginx is configured to redirect all HTTP to HTTPS and forward secure traffic to Django.

