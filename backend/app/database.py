from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

db_url = settings.DATABASE_URL
is_sqlite = db_url.startswith("sqlite")

if is_sqlite:
    # For SQLite, check_same_thread needs to be False for multithreaded FastAPI
    engine = create_engine(db_url, connect_args={"check_same_thread": False})
else:
    # PostgreSQL / Supabase connection pooling
    engine = create_engine(
        db_url,
        pool_pre_ping=True,
        pool_recycle=300,
        pool_size=10,
        max_overflow=20
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def migrate_database_columns():
    """
    Safely creates tables for PostgreSQL/Supabase, or migrates columns for SQLite.
    """
    from sqlalchemy import text
    try:
        # Create any missing tables (works on both PostgreSQL and SQLite)
        Base.metadata.create_all(bind=engine)
        
        if is_sqlite:
            with engine.connect() as conn:
                result = conn.execute(text("PRAGMA table_info(users)")).fetchall()
                existing_cols = [row[1] for row in result]
                
                new_columns = [
                    ("name", "VARCHAR DEFAULT 'Farmer' NOT NULL"),
                    ("email", "VARCHAR"),
                    ("phone", "VARCHAR"),
                    ("password_hash", "VARCHAR"),
                    ("auth_token", "VARCHAR"),
                    ("reset_token", "VARCHAR"),
                    ("reset_token_expiry", "DATETIME"),
                ]
                for col_name, col_type in new_columns:
                    if col_name not in existing_cols:
                        conn.execute(text(f"ALTER TABLE users ADD COLUMN {col_name} {col_type}"))
                        print(f"Migrated SQLite column users.{col_name}")
                conn.commit()
    except Exception as e:
        print("Database migration check note:", e)
