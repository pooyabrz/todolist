import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection parameters with default values
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "todolist_db")

# Construct database URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create SQLAlchemy engine
# echo=True: Print all SQL statements (useful for debugging)
# pool_pre_ping=True: Verify connections before using them
engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10
)

# Create session factory
# autocommit=False: Don't auto-commit transactions
# autoflush=False: Don't auto-flush changes
# bind=engine: Bind session to our database engine
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for all SQLAlchemy models
Base = declarative_base()


def get_db():
    """
    Dependency function to get database session.
    Yields a database session and ensures it's closed after use.
    
    Usage:
        db = next(get_db())
        try:
            # Use db session
            pass
        finally:
            db.close()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_database_connection():
    """
    Check if database connection is working properly.
    Prints connection status and database information.
    """
    try:
        with engine.connect() as connection:
            # Execute a simple query to test connection
            result = connection.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            
            print("✅ Database connection successful!")
            print(f"📊 Database: {DB_NAME}")
            print(f"🖥️  Host: {DB_HOST}:{DB_PORT}")
            print(f"🔧 PostgreSQL version: {version.split(',')[0]}")
            
    except Exception as e:
        print("❌ Database connection failed!")
        print(f"Error: {e}")
        print("\nTroubleshooting:")
        print("1. Check if PostgreSQL is running: docker ps")
        print("2. Verify .env file configuration")
        print("3. Check Docker logs: docker logs todolist-db")
