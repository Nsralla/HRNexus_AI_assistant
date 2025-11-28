"""
Quick diagnostic script to test database connection
Run this to check if your Supabase database is accessible
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("[ERROR] DATABASE_URL environment variable is not set!")
    exit(1)

print("[OK] DATABASE_URL found")
print(f"  Host: {DATABASE_URL.split('@')[1].split('/')[0] if '@' in DATABASE_URL else 'unknown'}")

# Create engine with NullPool
is_pooler = "pooler.supabase.com" in DATABASE_URL
print(f"  Using Supabase pooler: {is_pooler}")

try:
    if is_pooler:
        engine = create_engine(
            DATABASE_URL,
            poolclass=NullPool,
            connect_args={"connect_timeout": 10}
        )
    else:
        engine = create_engine(DATABASE_URL)

    print("[OK] Database engine created")

    # Try to connect
    print("\nAttempting to connect to database...")
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("[OK] Database connection successful!")

        # Try to query a table
        print("\nChecking if tables exist...")
        result = conn.execute(text("SELECT tablename FROM pg_tables WHERE schemaname = 'public'"))
        tables = [row[0] for row in result]
        if tables:
            print(f"[OK] Found {len(tables)} tables: {', '.join(tables)}")
        else:
            print("[WARN] No tables found (database is empty)")

except Exception as e:
    print(f"\n[FAILED] DATABASE CONNECTION FAILED!")
    print(f"Error type: {type(e).__name__}")
    print(f"Error message: {str(e)}")

    error_msg = str(e).lower()
    if "db_termination" in error_msg or "shutdown" in error_msg:
        print("\n[DIAGNOSIS] Supabase pooler is terminating connections")
        print("   Possible causes:")
        print("   1. Database is paused (Supabase free tier) - Go to Supabase dashboard and resume it")
        print("   2. Too many connection attempts - Wait a few minutes and try again")
        print("   3. Wrong pooler configuration - Try using port 6543 (Transaction Pooler)")
    elif "password" in error_msg:
        print("\n[DIAGNOSIS] Password authentication failed")
        print("   Check that your DATABASE_URL password is correct")
    elif "timeout" in error_msg:
        print("\n[DIAGNOSIS] Connection timeout")
        print("   Database might be slow to respond or unreachable")

    exit(1)

print("\n[SUCCESS] All database checks passed!")
