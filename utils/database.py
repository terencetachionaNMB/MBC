"""
Database utilities for NMB BI Portal
Handles PostgreSQL connections, session management, and ORM setup
"""

import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text, TIMESTAMP, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import func
from datetime import datetime
import streamlit as st

# Base class for ORM models
Base = declarative_base()

# Database connection
def get_database_url():
    """Get database URL from environment variables"""
    return os.environ.get('DATABASE_URL', '')

@st.cache_resource
def get_database_engine():
    """Create and cache database engine"""
    database_url = get_database_url()
    if not database_url:
        raise ValueError("DATABASE_URL environment variable not set")
    
    # Create engine with connection pooling
    engine = create_engine(
        database_url,
        pool_pre_ping=True,  # Verify connections before using
        pool_size=5,
        max_overflow=10,
        echo=False  # Set to True for SQL debugging
    )
    return engine

def get_session() -> Session:
    """Get database session"""
    engine = get_database_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()

def init_database():
    """Initialize database schema from schema.sql file"""
    try:
        engine = get_database_engine()
        
        # Read and execute schema.sql
        schema_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'schema.sql')
        
        if os.path.exists(schema_path):
            with open(schema_path, 'r') as f:
                schema_sql = f.read()
            
            # Execute schema SQL
            with engine.connect() as connection:
                # Split by semicolon and execute each statement
                statements = [s.strip() for s in schema_sql.split(';') if s.strip()]
                for statement in statements:
                    if statement:
                        connection.execute(text(statement))
                connection.commit()
            
            return True, "Database initialized successfully"
        else:
            return False, f"Schema file not found: {schema_path}"
            
    except Exception as e:
        return False, f"Database initialization error: {str(e)}"

def test_database_connection():
    """Test database connectivity"""
    try:
        engine = get_database_engine()
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            return True, "Database connection successful"
    except Exception as e:
        return False, f"Database connection failed: {str(e)}"

# ORM Models (matching schema.sql)

class User(Base):
    """User model for authentication"""
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    role_level = Column(Integer, nullable=False, default=4)
    department = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(TIMESTAMP)
    login_count = Column(Integer, default=0)

class Role(Base):
    """Role model for RBAC"""
    __tablename__ = 'roles'
    
    role_id = Column(Integer, primary_key=True)
    role_level = Column(Integer, unique=True, nullable=False)
    role_name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    permissions = Column(Text)  # JSON stored as text
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

class Bookmark(Base):
    """User bookmarks for saved dashboard configurations"""
    __tablename__ = 'bookmarks'
    
    bookmark_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    dashboard_name = Column(String(100), nullable=False)
    bookmark_name = Column(String(200), nullable=False)
    filter_config = Column(Text)  # JSON stored as text
    description = Column(Text)
    is_default = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

class Favorite(Base):
    """User favorites (accounts, customers, products)"""
    __tablename__ = 'favorites'
    
    favorite_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    favorite_type = Column(String(50), nullable=False)
    favorite_ref = Column(String(100), nullable=False)
    favorite_name = Column(String(200))
    notes = Column(Text)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

class Notification(Base):
    """User notifications"""
    __tablename__ = 'notifications'
    
    notification_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(50), default='info')
    priority = Column(Integer, default=3)
    is_read = Column(Boolean, default=False)
    link_to_dashboard = Column(String(200))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    read_at = Column(TIMESTAMP)

class AuditLog(Base):
    """Audit log for user actions"""
    __tablename__ = 'audit_log'
    
    log_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    username = Column(String(100))
    action = Column(String(100), nullable=False)
    dashboard_accessed = Column(String(100))
    details = Column(Text)  # JSON stored as text
    ip_address = Column(String(50))
    user_agent = Column(Text)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

# Helper functions for common queries

def get_user_by_username(username: str):
    """Get user by username"""
    session = get_session()
    try:
        user = session.query(User).filter(User.username == username).first()
        return user
    finally:
        session.close()

def get_user_by_email(email: str):
    """Get user by email"""
    session = get_session()
    try:
        user = session.query(User).filter(User.email == email).first()
        return user
    finally:
        session.close()

def get_user_by_id(user_id: int):
    """Get user by ID"""
    session = get_session()
    try:
        user = session.query(User).filter(User.user_id == user_id).first()
        return user
    finally:
        session.close()

def create_user(username: str, email: str, password_hash: str, role_level: int = 4, **kwargs):
    """Create new user"""
    session = get_session()
    try:
        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            role_level=role_level,
            **kwargs
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def update_user_login(user_id: int):
    """Update user login timestamp and count"""
    session = get_session()
    try:
        user = session.query(User).filter(User.user_id == user_id).first()
        if user:
            user.last_login = datetime.utcnow()
            user.login_count = (user.login_count or 0) + 1
            session.commit()
    finally:
        session.close()

def log_user_action(user_id: int, username: str, action: str, dashboard: str = None, details: str = None):
    """Log user action to audit trail"""
    session = get_session()
    try:
        log_entry = AuditLog(
            user_id=user_id,
            username=username,
            action=action,
            dashboard_accessed=dashboard,
            details=details
        )
        session.add(log_entry)
        session.commit()
    except Exception as e:
        session.rollback()
        # Don't fail if logging fails
        pass
    finally:
        session.close()

def get_user_notifications(user_id: int, unread_only: bool = False):
    """Get user notifications"""
    session = get_session()
    try:
        query = session.query(Notification).filter(Notification.user_id == user_id)
        if unread_only:
            query = query.filter(Notification.is_read == False)
        notifications = query.order_by(Notification.created_at.desc()).all()
        return notifications
    finally:
        session.close()

def mark_notification_read(notification_id: int):
    """Mark notification as read"""
    session = get_session()
    try:
        notification = session.query(Notification).filter(
            Notification.notification_id == notification_id
        ).first()
        if notification:
            notification.is_read = True
            notification.read_at = datetime.utcnow()
            session.commit()
    finally:
        session.close()

def get_user_bookmarks(user_id: int, dashboard_name: str = None):
    """Get user bookmarks, optionally filtered by dashboard"""
    session = get_session()
    try:
        query = session.query(Bookmark).filter(Bookmark.user_id == user_id)
        if dashboard_name:
            query = query.filter(Bookmark.dashboard_name == dashboard_name)
        bookmarks = query.order_by(Bookmark.created_at.desc()).all()
        return bookmarks
    finally:
        session.close()

def create_bookmark(user_id: int, dashboard_name: str, bookmark_name: str, filter_config: str = None, **kwargs):
    """Create user bookmark"""
    session = get_session()
    try:
        bookmark = Bookmark(
            user_id=user_id,
            dashboard_name=dashboard_name,
            bookmark_name=bookmark_name,
            filter_config=filter_config,
            **kwargs
        )
        session.add(bookmark)
        session.commit()
        session.refresh(bookmark)
        return bookmark
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def get_user_favorites(user_id: int, favorite_type: str = None):
    """Get user favorites, optionally filtered by type"""
    session = get_session()
    try:
        query = session.query(Favorite).filter(Favorite.user_id == user_id)
        if favorite_type:
            query = query.filter(Favorite.favorite_type == favorite_type)
        favorites = query.order_by(Favorite.created_at.desc()).all()
        return favorites
    finally:
        session.close()

def add_favorite(user_id: int, favorite_type: str, favorite_ref: str, favorite_name: str = None, notes: str = None):
    """Add item to user favorites"""
    session = get_session()
    try:
        favorite = Favorite(
            user_id=user_id,
            favorite_type=favorite_type,
            favorite_ref=favorite_ref,
            favorite_name=favorite_name,
            notes=notes
        )
        session.add(favorite)
        session.commit()
        session.refresh(favorite)
        return favorite
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def remove_favorite(user_id: int, favorite_id: int):
    """Remove item from user favorites"""
    session = get_session()
    try:
        favorite = session.query(Favorite).filter(
            Favorite.favorite_id == favorite_id,
            Favorite.user_id == user_id
        ).first()
        if favorite:
            session.delete(favorite)
            session.commit()
            return True
        return False
    finally:
        session.close()
