# Configuration Guide

After importing the n8n workflow, you need to replace the hardcoded Supabase credentials with your own.

## Finding your Supabase credentials

1. Go to [supabase.com](https://supabase.com) → your project
2. Click **Project Settings** → **API**
3. Copy:
   - **Project URL** — looks like `https://abcdefgh.supabase.co`
   - **anon / public key** — the long JWT string

## Updating the n8n workflow

Open each of these nodes and replace the `apikey` and `Authorization` header values:

| Node | What to update |
|---|---|
| Fetch Unread Emails | apikey + Authorization headers |
| Save Request | apikey + Authorization headers |
| Save Email Summary | apikey + Authorization headers |
| Save Activity Log | apikey + Authorization headers |
| Mark Email as Read | apikey + Authorization headers + URL |

The URL in **Mark Email as Read** should use your project ID:
```
https://YOUR_PROJECT_ID.supabase.co/rest/v1/emails?id=eq.{{ $('Parse Ollama Response').first().json.email_id }}
```

## Changing the AI model

The workflow uses `llama3.2` by default. To use a different model:

1. Pull it: `ollama pull mistral` (or `phi3`, `qwen2.5:0.5b` for faster/smaller)
2. Open the **Analyze with Ollama** node
3. Change `"model": "llama3.2"` to `"model": "mistral"` inside the **Build Ollama Payload** code node

## Changing the schedule

The workflow runs every hour by default. To change it:
1. Open the **Schedule Trigger** node
2. Adjust the interval as needed
