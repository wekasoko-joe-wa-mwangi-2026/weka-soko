# Weka Soko — Project Knowledge Base
*Generated from Claude session — March 31, 2026*

---

## Platform Overview

**Weka Soko** is a Kenyan classified ads marketplace where sellers post free and pay KSh 250 only when a serious buyer locks in. Features include anonymous chat, M-Pesa payments, escrow, and buyer/seller reviews.

---

## Live URLs

| Service | URL |
|---|---|
| **Frontend (Next.js)** | https://weka-soko-nextjs.vercel.app |
| **Backend (Railway)** | https://wekasokobackend.up.railway.app |
| **Admin Panel** | https://weka-soko-admin-gamma.vercel.app |

---

## GitHub Repositories

| Repo | Purpose |
|---|---|
| `weka-soko-backend` | Node.js/Express API |
| `weka-soko-nextjs` | Next.js 14 SSR frontend |
| `weka-soko-admin` | React admin panel |

All repos under GitHub account: `wekasoko-joe-wa-mwangi-2026`

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 14 (App Router, SSR/SSG) |
| Backend | Node.js + Express |
| Database | PostgreSQL (Railway managed) |
| Hosting — Frontend | Vercel |
| Hosting — Backend | Railway |
| Payments | M-Pesa STK Push (Daraja API) |
| Email | SendGrid |
| Photos | Cloudinary |
| Real-time | Socket.io |
| Auth | JWT + Google OAuth 2.0 |
| Push Notifications | Web Push (VAPID) |

---

## Railway Environment Variables

```env
PORT=8080
NODE_ENV=production
DATABASE_URL=${Postgres.DATABASE_URL}
JWT_SECRET=weka-soko-jwt-secret-key-2026-random-string-change-this
FRONTEND_URL=https://weka-soko-nextjs.vercel.app
BACKEND_URL=https://wekasokobackend.up.railway.app
ADMIN_URL=https://weka-soko-admin-gamma.vercel.app
EMAIL_FROM=wekasoko@gmail.com
SENDGRID_API_KEY=SG.xxx...
CLOUDINARY_CLOUD_NAME=ddfikbhzq
CLOUDINARY_API_KEY=331658443599452
CLOUDINARY_API_SECRET=xxx...
MPESA_BASE_URL=https://sandbox.safaricom.co.ke
MPESA_SHORTCODE=5673935
MPESA_CONSUMER_KEY=xxx...
MPESA_CONSUMER_SECRET=xxx...
MPESA_PASSKEY=xxx...
MPESA_CALLBACK_URL=https://wekasokobackend.up.railway.app/api/payments/mpesa/callback
GOOGLE_CLIENT_ID=xxx...
GOOGLE_CLIENT_SECRET=xxx...
ESCROW_FEE_PERCENT=7.5
ESCROW_RELEASE_HOURS=48
UNLOCK_FEE_KES=250
VAPID_PUBLIC_KEY=xxx...
VAPID_PRIVATE_KEY=xxx...
VAPID_SUBJECT=mailto:wekasoko@gmail.com
```

**Critical:** `PORT=8080` must be set manually — Railway routes external traffic to 8080.

---

## Vercel Environment Variables

### weka-soko-nextjs
```env
NEXT_PUBLIC_API_URL=https://wekasokobackend.up.railway.app
```

### weka-soko-admin
```env
REACT_APP_API_URL=https://wekasokobackend.up.railway.app
```

---

## Next.js Project Structure

```
weka-soko-nextjs/
├── package.json
├── next.config.js
├── vercel.json
├── jsconfig.json          ← REQUIRED for @/ path aliases
├── .env.local             ← DO NOT commit, add to Vercel env vars
├── lib/
│   └── utils.js           ← API, fmtKES, ago, CATS, KENYA_COUNTIES, CAT_PHOTOS
├── components/
│   └── all.jsx            ← All UI components (3400+ lines, 'use client')
└── app/
    ├── globals.css
    ├── layout.jsx
    ├── page.jsx           ← SSR home page
    ├── HomeClient.jsx     ← Interactive shell
    ├── sitemap.js
    ├── robots.js
    ├── listings/[id]/
    │   ├── page.jsx       ← SSR listing detail with OG metadata
    │   └── ListingPageClient.jsx
    ├── dashboard/
    │   └── page.jsx
    └── sold/
        ├── page.jsx
        └── SoldPageClient.jsx
```

**Key rule:** `jsconfig.json` must exist at the root with:
```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": { "@/*": ["./*"] }
  }
}
```

---

## Backend File Structure (key files)

```
weka-soko-backend/
└── src/
    ├── index.js                    ← Entry point, CORS, rate limiters, Socket.io
    ├── db/
    │   ├── pool.js                 ← PostgreSQL connection pool
    │   └── migrate_all.js         ← Auto-runs on startup, idempotent
    ├── middleware/
    │   └── auth.js                ← requireAuth, requireAdmin middleware
    ├── routes/
    │   ├── auth.js                ← Register, login, Google OAuth, verify email
    │   ├── listings.js            ← CRUD + photos (Cloudinary outside transactions)
    │   ├── payments.js            ← M-Pesa STK push + callback
    │   ├── chat.js                ← Socket.io chat routes
    │   ├── admin.js               ← Admin panel routes
    │   ├── notifications.js
    │   ├── requests.js            ← Buyer requests (What Buyers Want)
    │   ├── pitches.js             ← Seller pitches on buyer requests
    │   ├── reviews.js
    │   ├── vouchers.js
    │   └── push.js                ← Web push subscriptions
    └── services/
        ├── email.service.js       ← SendGrid (never await in request handlers)
        ├── cloudinary.service.js  ← Photo upload/delete
        ├── cron.service.js        ← Scheduled jobs
        └── moderation.service.js  ← Chat content moderation
```

---

## Critical Rules (Hard-Won Lessons)

### Railway / Backend
- **`PORT=8080`** must be set manually as an env var — Railway routes external traffic to 8080
- **Never `await sendEmail()`** inside request handlers — causes timeout. Fire and forget with `.catch()`
- **Cloudinary uploads** must happen outside database transactions
- **`migrate_all.js` FK ordering** — foreign key references must come after the referenced table is created (e.g. `linked_request_id` referencing `buyer_requests` must be added AFTER `buyer_requests` table)
- **Auth rate limiter** — `authLimiter` caps at 50 requests per 15 min per IP. `skipSuccessfulRequests: true` so testing doesn't burn the limit
- **`sendWelcomeMessage`** from `notification.service.js` — wrap in try/catch, it can crash the process if WhatsApp is not configured

### Next.js / Frontend
- **`jsconfig.json`** is required for `@/` imports to resolve
- **URL token handling** (`reset_token`, `verify_email`, `auth_token`) must run **before** the URL router in `HomeClient.jsx`, otherwise they get swallowed
- **`'use client'`** directive required at top of all interactive components
- **Vercel Deployment Protection** — new projects default to locked. Disable under Settings → Deployment Protection
- **`NEXT_PUBLIC_` prefix** required for any env var used in the browser

### Database
- PostgreSQL managed by Railway
- `DATABASE_URL` auto-injected via `${{Postgres.DATABASE_URL}}` reference
- SSL required in production: `ssl: { rejectUnauthorized: false }`

### Google OAuth
- Redirect URI must be: `https://wekasokobackend.up.railway.app/api/auth/google/callback`
- Authorised JS origins: frontend URL + backend URL
- "deleted_client" error = OAuth client was deleted in Google Cloud Console, must recreate

---

## Admin Account

- **Email:** wekasoko@gmail.com
- **Password:** WekaSoko@2024!
- **Role:** admin / super
- Created via `/api/auth/seed-admin` endpoint (protected by `SEED_SECRET` env var)
- After creation, delete `SEED_SECRET` from Railway variables

---

## M-Pesa Configuration

- **Till Number:** 5673935
- **Unlock Fee:** KSh 250 (non-refundable)
- **Escrow Fee:** 7.5% of item price
- **Mode:** SANDBOX (switch to production when ready)
- **Callback URL:** `https://wekasokobackend.up.railway.app/api/payments/mpesa/callback`

---

## Auth Flow

### Email Sign Up
1. User submits form → POST `/api/auth/register`
2. User created with `is_verified=false`
3. Verification email sent in background (no await)
4. Frontend shows "check your email" screen
5. User clicks link → `?verify_email=TOKEN` → GET `/api/auth/verify-email`
6. Account verified, JWT returned → auto login

### Google OAuth
1. User clicks "Sign in with Google" → GET `/api/auth/google`
2. Redirected to Google consent screen
3. Google redirects to `/api/auth/google/callback`
4. Backend exchanges code for token, upserts user
5. Backend redirects to `FRONTEND_URL?auth_token=...&auth_user=...`
6. HomeClient.jsx reads params → stores token → user logged in

### Password Reset
1. User submits email → POST `/api/auth/forgot-password`
2. Email sent with link: `FRONTEND_URL?reset_token=TOKEN`
3. HomeClient.jsx reads `reset_token` param → shows `ResetPasswordModal`
4. User submits new password → POST `/api/auth/reset-password`

### Admin Login
- Separate endpoint: POST `/api/auth/admin-login`
- Regular `/api/auth/login` blocks admin accounts (returns 403)

---

## Cron Jobs (auto-started)

| Job | Schedule | Purpose |
|---|---|---|
| follow-ups | Every 30 min | Send follow-up notifications |
| expiry | Daily | Mark expired listings |
| response-rates | Every hour | Recalculate seller response rates |
| escrow | Every hour | Auto-release held escrow |
| payments | Every 15 min | Check pending M-Pesa payments |
| unpaid-listings | Every hour | Clean up unpaid listing slots |

---

## Deployment Checklist

### Railway (Backend)
- [ ] `PORT=8080` set
- [ ] `DATABASE_URL` linked to Postgres service
- [ ] `FRONTEND_URL` = current Vercel URL
- [ ] `BACKEND_URL` = Railway URL
- [ ] `MPESA_SHORTCODE=5673935`
- [ ] `MPESA_CALLBACK_URL` uses Railway URL
- [ ] `GOOGLE_CLIENT_ID` + `GOOGLE_CLIENT_SECRET` set
- [ ] `SEED_SECRET` deleted after admin created
- [ ] Deploy logs show: `Port: 8080 | Env: production` + `✅ DB migration complete`

### Vercel (Frontend)
- [ ] `NEXT_PUBLIC_API_URL` set to Railway URL
- [ ] Deployment Protection turned OFF (Settings → Deployment Protection)
- [ ] `jsconfig.json` present in repo root

### Google Cloud Console
- [ ] OAuth 2.0 client exists (not deleted)
- [ ] Authorised redirect URI: `https://wekasokobackend.up.railway.app/api/auth/google/callback`
- [ ] Authorised JS origins include current Vercel URL

### SendGrid
- [ ] `wekasoko@gmail.com` verified as sender (Settings → Sender Authentication)

---

## Common Errors & Fixes

| Error | Cause | Fix |
|---|---|---|
| `Service Unavailable` | Wrong port | Set `PORT=8080` in Railway variables |
| `Migration failed: current transaction is aborted` | FK reference before table creation in `migrate_all.js` | Move `addCol` for `linked_request_id` to after `buyer_requests` table |
| `Error 401: deleted_client` | Google OAuth client deleted | Recreate in Google Cloud Console |
| `Application failed to respond` | Node process crash | Check for unhandled promise rejections; `sendWelcomeMessage` crashing |
| `Module not found: @/lib/utils` | Missing `jsconfig.json` | Add `jsconfig.json` with path aliases to repo root |
| `api is defined multiple times` | `api()` function in both `all.jsx` and imported from utils | Remove local `api()` from `all.jsx`, use `apiCall` from utils |
| Reset password link goes to homepage | URL router runs before token handler | Token handler must run first in `HomeClient.jsx` useEffect |
| Signups timing out | `await sendEmail()` blocking request | Remove `await` from all `sendEmail()` calls |
| Auth rate limit hit during testing | 50 req/15min limit per IP | Wait 15 min or temporarily raise limit in `index.js` |
| Vercel shows "Access Required" | Deployment Protection enabled | Settings → Deployment Protection → turn off |

---

## Key Accounts

- **Google/Gmail:** wekasoko@gmail.com
- **Railway:** wekasoko@gmail.com
- **Vercel:** wekasoko@gmail.com  
- **GitHub:** wekasoko-joe-wa-mwangi-2026
- **SendGrid:** wekasoko@gmail.com
- **Cloudinary:** cloud name `ddfikbhzq`
- **M-Pesa Till:** 5673935

---

*Last updated: March 31, 2026*
