import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from app.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False, default="Farmer")
    email = Column(String, unique=True, index=True, nullable=True)
    phone = Column(String, nullable=True)
    password_hash = Column(String, nullable=True)
    auth_token = Column(String, nullable=True, index=True)
    reset_token = Column(String, nullable=True)
    reset_token_expiry = Column(DateTime, nullable=True)
    preferred_language = Column(String, default="kn")  # 'kn', 'hi', 'te', 'en'
    created_at = Column(DateTime, default=datetime.utcnow)

    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")
    goals = relationship("FarmerGoal", back_populates="user", cascade="all, delete-orphan")

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    language = Column(String, default="kn")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, default=generate_uuid)
    conversation_id = Column(String, ForeignKey("conversations.id"), nullable=False)
    sender = Column(String, nullable=False)  # 'farmer' or 'krishirakshak_agent'
    text = Column(Text, nullable=False)
    audio_url = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    metadata_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    conversation = relationship("Conversation", back_populates="messages")

class FarmerGoal(Base):
    __tablename__ = "farmer_goals"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    crop = Column(String, nullable=False)
    problem = Column(Text, nullable=False)
    goal = Column(Text, nullable=False)
    urgency = Column(String, default="Medium")  # 'Low', 'Medium', 'High', 'Severe'
    status = Column(String, default="Investigating")  
    # Statuses: 'Investigating', 'Action Plan Active', 'Monitoring', 'Improving', 'Needs Attention', 'Completed'
    language = Column(String, default="kn")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="goals")
    observations = relationship("CropObservation", back_populates="goal", cascade="all, delete-orphan")
    investigations = relationship("AgentInvestigation", back_populates="goal", cascade="all, delete-orphan")
    action_plans = relationship("ActionPlan", back_populates="goal", cascade="all, delete-orphan")
    follow_ups = relationship("FollowUp", back_populates="goal", cascade="all, delete-orphan")

class CropObservation(Base):
    __tablename__ = "crop_observations"

    id = Column(String, primary_key=True, default=generate_uuid)
    goal_id = Column(String, ForeignKey("farmer_goals.id"), nullable=False)
    image_url = Column(String, nullable=True)
    symptoms = Column(JSON, default=list)  # list of strings
    affected_percentage = Column(Float, default=10.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    goal = relationship("FarmerGoal", back_populates="observations")

class AgentInvestigation(Base):
    __tablename__ = "agent_investigations"

    id = Column(String, primary_key=True, default=generate_uuid)
    goal_id = Column(String, ForeignKey("farmer_goals.id"), nullable=False)
    investigation_plan = Column(JSON, default=list)  # list of steps planned
    tool_results = Column(JSON, default=dict)  # results from executed tools
    possible_causes = Column(JSON, default=list)  # causes with probability & rationale
    confidence = Column(Float, default=0.75)
    created_at = Column(DateTime, default=datetime.utcnow)

    goal = relationship("FarmerGoal", back_populates="investigations")

class ActionPlan(Base):
    __tablename__ = "action_plans"

    id = Column(String, primary_key=True, default=generate_uuid)
    goal_id = Column(String, ForeignKey("farmer_goals.id"), nullable=False)
    immediate_actions = Column(JSON, default=list)
    short_term_actions = Column(JSON, default=list)
    monitoring_actions = Column(JSON, default=list)
    escalation_conditions = Column(JSON, default=list)
    localized_summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    goal = relationship("FarmerGoal", back_populates="action_plans")

class FollowUp(Base):
    __tablename__ = "follow_ups"

    id = Column(String, primary_key=True, default=generate_uuid)
    goal_id = Column(String, ForeignKey("farmer_goals.id"), nullable=False)
    scheduled_date = Column(DateTime, nullable=False)
    farmer_response = Column(Text, nullable=True)
    new_image_url = Column(String, nullable=True)
    status = Column(String, default="Scheduled")  # 'Scheduled', 'Improving', 'Stable', 'Worsening', 'Completed'
    comparison_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    goal = relationship("FarmerGoal", back_populates="follow_ups")
