
## How It Works

```
Email arrives in Supabase
        ↓
n8n runs every hour
        ↓
Ollama (local AI) reads the email
  → scores risk 0–100
  → extracts category, urgency, summary
  → recommends: auto_approve / review / escalate
        ↓
n8n writes to Supabase:
  ├── requests table       (the approval request)
  ├── email_summaries table (the AI summary)
  └── activity_log table   (audit trail)
        ↓

**Risk scoring logic:**
| Risk Score | Status |
|---|---|
| 0 – 34 | ✅ Auto-approved |
| 35 – 69 | 🟡 Pending (manual review) |
| 70 – 100 | 🔴 Escalated (admin required) |

---

## Stack

| Layer | Tool | Cost |
|---|---|---|
| Database | [Supabase](https://supabase.com) | Free tier |
| Automation | [n8n](https://n8n.io) | Self-hosted, free |
| AI Model | [Ollama](https://ollama.com) + llama3.2 | Free, runs locally |

---

## Prerequisites

- [Node.js](https://nodejs.org) v18+
- [n8n](https://n8n.io) installed globally
- [Ollama](https://ollama.com) installed
- A [Supabase](https://supabase.com) account (free)

---

## Setup Guide

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/auto-review-agent.git
cd auto-review-agent
```

### 2. Set up Supabase

1. Create a new project at [supabase.com](https://supabase.com)
2. Go to **SQL Editor** and run all migration files in order:

```bash
# Run these in your Supabase SQL Editor one by one:
supabase/migrations/001_create_emails.sql
supabase/migrations/002_create_email_summaries.sql
supabase/migrations/003_create_profiles.sql
supabase/migrations/004_create_requests.sql
supabase/migrations/005_create_activity_log.sql
supabase/migrations/006_create_dashboard_stats_view.sql
```

3. Copy your **Project URL** and **anon key** from Project Settings → API

### 3. Set up Ollama

```bash
# Install Ollama from https://ollama.com then pull the model:
ollama pull llama3.2

# Ollama will now run automatically at http://127.0.0.1:11434
# If it's not running, start it with:
ollama serve
```

### 4. Set up n8n

```bash
# Install n8n globally
npm install -g n8n

# Start n8n
n8n start
# Opens at http://localhost:5678
```

Then import the workflow:
1. Open n8n at `http://localhost:5678`
2. Go to **Workflows → Add Workflow → Import from file**
3. Upload `n8n/auto_review_agent_final.json`
4. Open the workflow and replace the Supabase URL and API key in every node with your own (see `docs/configuration.md`)
5. Hit **Test Workflow** to verify everything works


## Project Structure

```
auto-review-agent/
├── README.md
├── n8n/
│   └── auto_review_agent_final.json   # Import this into n8n
├── supabase/
│   └── migrations/
│       ├── 001_create_emails.sql
│       ├── 002_create_email_summaries.sql
│       ├── 003_create_profiles.sql
│       ├── 004_create_requests.sql
│       ├── 005_create_activity_log.sql
│       └── 006_create_dashboard_stats_view.sql
└── docs/
    └── configuration.md               # How to configure credentials
```

-
## n8n Workflow Overview

The workflow has 9 nodes:

```
Schedule Trigger (every hour)
  → Fetch Unread Emails       (Supabase REST)
  → Build Ollama Payload      (Code — safely serializes email body)
  → Analyze with Ollama       (HTTP POST to 127.0.0.1:11434)
  → Parse Ollama Response     (Code — extracts + validates AI fields)
  ├── Save Request            (Supabase — requests table)
  ├── Save Email Summary      (Supabase — email_summaries table)
  → Build Activity Log        (Code)
  → Save Activity Log         (Supabase — activity_log table)
  → Mark Email as Read        (Supabase PATCH)
```

---

## Adding Test Emails

To add a mock email for testing, run this in your Supabase SQL Editor:

```sql
INSERT INTO public.emails (sender, subject, body, read)
VALUES (
  'test.user@company.com',
  'Request for IT Access',
  'Hi, I need access to the production server for deployment...',
  false
);
```

Then run the n8n workflow manually.


