"""Standalone admin seeder (the app also seeds on startup).
Run inside the backend container:
    docker compose exec backend python scripts/seed_admin.py
"""
from app.main import seed_admin

if __name__ == "__main__":
    seed_admin()
    print("Admin seeded (or already existed).")
