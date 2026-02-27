from fastapi import FastAPI
from .supabase_client import supabase


# 1️⃣ Create FastAPI app instance
app = FastAPI()

# 2️⃣ Root endpoint (optional)
@app.get("/")
def root():
    return {"message": "Email Agent Reader API running"}

# 3️⃣ Health check endpoint
@app.get("/health")
def health():
    return {"status": "ok"}



@app.get("/emails")
def get_emails():
    # Fetch all rows from your table called 'emails'
    data = supabase.table("emails").select("*").execute()
    return {"emails": data.data}