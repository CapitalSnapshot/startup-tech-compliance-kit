# Example inventory (fictional)

This shows the shape of `infra/inventory/host-inventory.md` after prompt B2. All names and values are made up. Credential values are never recorded, only paths and key names.

## Host

| Item | Value |
| --- | --- |
| Provider and size | Example VPS, 2 vCPU, 4 GB |
| OS | Debian 12 |
| Runtime | PHP 8.3.x (docs claimed 8.5) |
| Database | MariaDB 11.8.x, local to the host |
| Web server | Apache with 6 virtual hosts |
| Last OS update | 11 months ago |

## Hostnames

| Hostname | Served by | Target | Notes |
| --- | --- | --- | --- |
| app.example.com | Apache vhost 1 | Application | Main user-facing site |
| api.example.com | Apache vhost 2 | Application | Public API |
| www.example.com | Apache vhost 3 | Dead port | Needs a redirect decision |
| (3 more) | | | |

## Scheduled jobs and processes

| Item | Schedule or start | Survives reboot? |
| --- | --- | --- |
| Nightly report snapshot | cron, 02:00 | Yes |
| Queue worker | Started by hand | No (finding) |

## Credential files (paths and key names only)

| Path | Keys | Status |
| --- | --- | --- |
| /var/www/app/.env | DB_PASS, MAIL_KEY, PAY_KEY | Live |
| /var/www/old/.env | DB_PASS, MAIL_KEY | Stale copy |

## TLS and edge

Certificates issued by an edge provider origin certificate; the edge account is held under one person's personal email (finding).

## Source

Checkout at /var/www/app tracks repository `acme/app-old` (the migration work lives in `acme/app`). The checkout sits inside the web root.

## External systems

| System | Holds | Owner account |
| --- | --- | --- |
| Payments provider | Webhook URL | Company account |
| Email provider | Sending domain, API key | Company account |
| DNS and edge | Zone | Personal email (finding) |

## Differences from plan

1. Runtime is PHP 8.3, not 8.5: build images on 8.3.
2. Seven hostnames, not one: all need certificates and redirects.
3. Queue worker has no process manager: add one.
