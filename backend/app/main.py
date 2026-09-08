import os
import uuid
import shutil
from datetime import datetime, timedelta
from typing import List, Optional
from pathlib import Path

from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from app.config import settings
from app.database import engine, Base, get_db, migrate_database_columns
from app.models import (
    User,
    Conversation,
    Message,
    FarmerGoal,
    CropObservation,
    AgentInvestigation,
    ActionPlan,
    FollowUp,
)
from app.services.auth import (
    hash_password,
    verify_password,
    generate_session_token,
    generate_reset_token,
    get_user_by_token,
    get_user_by_email,
)
from fastapi import Header
from app.schemas import (
    UserSignupRequest,
    UserLoginRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    AuthResponse,
    UserProfileResponse,
    ChatRequest,
    ChatResponse,
    GoalSummaryResponse,
    FollowUpSubmitRequest,
    FollowUpSubmitResponse,
    WeatherInfoResponse,
    SchemeInfoResponse,
    DashboardDataResponse,
    AgentActivityStep,
    PossibleCause,
    ActionPlanSchema,
)
from app.agents.graph import agent_graph
from app.agents.specialized import FollowUpAgent
from app.services.multilingual import MultilingualService
from app.tools.weather_service import weather_tool
from app.tools.govt_schemes import govt_schemes_tool
from app.tools.crop_image_analyzer import crop_image_analyzer

# Initialize Database tables
Base.metadata.create_all(bind=engine)
migrate_database_columns()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Multilingual, Voice-First, Goal-Driven Agricultural AI Agent for Indian Farmers",
    version="1.0.0"
)

# Enable Production CORS for frontend (Vercel domains, custom origins, localhost)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if settings.CORS_ORIGINS else ["*"],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount uploads directory for static image access
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(settings.UPLOAD_DIR)), name="uploads")


# --- Seed Initial Demo Data ---
def ensure_default_user_and_samples(db: Session):
    user = db.query(User).first()
    if not user:
        user = User(id="farmer-default-001", preferred_language="kn")
        db.add(user)
        db.commit()
    return user



# --- Authentication Dependency & Endpoints ---

def get_current_user_optional(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)) -> Optional[User]:
    """
    Extracts Bearer token from header and resolves user. Returns None if unauthenticated.
    """
    if not authorization:
        return None
    parts = authorization.split()
    if len(parts) == 2 and parts[0].lower() == "bearer":
        token = parts[1]
        return get_user_by_token(token, db)
    return None

@app.post("/auth/signup", response_model=AuthResponse)
def auth_signup(payload: UserSignupRequest, db: Session = Depends(get_db)):
    clean_email = payload.email.strip().lower()
    
    # Check if user already exists
    existing = get_user_by_email(clean_email, db)
    if existing:
        raise HTTPException(
            status_code=400,
            detail="An account with this email address already exists. Please log in."
        )

    # Create new secure user
    token = generate_session_token()
    new_user = User(
        id=str(uuid.uuid4()),
        name=payload.name.strip(),
        email=clean_email,
        phone=payload.phone.strip() if payload.phone else None,
        password_hash=hash_password(payload.password),
        auth_token=token,
        preferred_language=payload.preferred_language or "kn"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    user_profile = UserProfileResponse(
        id=new_user.id,
        name=new_user.name,
        email=new_user.email,
        phone=new_user.phone,
        preferred_language=new_user.preferred_language,
        created_at=new_user.created_at
    )
    return AuthResponse(
        token=token,
        user=user_profile,
        message="Account created successfully!"
    )

@app.post("/auth/login", response_model=AuthResponse)
def auth_login(payload: UserLoginRequest, db: Session = Depends(get_db)):
    clean_email = payload.email.strip().lower()
    user = get_user_by_email(clean_email, db)

    if not user or not user.password_hash or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password. Please verify your credentials and try again."
        )

    # Generate fresh session token
    token = generate_session_token()
    user.auth_token = token
    db.commit()
    db.refresh(user)

    user_profile = UserProfileResponse(
        id=user.id,
        name=user.name or "Farmer",
        email=user.email,
        phone=user.phone,
        preferred_language=user.preferred_language or "kn",
        created_at=user.created_at
    )
    return AuthResponse(
        token=token,
        user=user_profile,
        message="Logged in successfully!"
    )

@app.get("/auth/me", response_model=UserProfileResponse)
def auth_me(user: Optional[User] = Depends(get_current_user_optional)):
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated or session expired. Please log in.")
    return UserProfileResponse(
        id=user.id,
        name=user.name or "Farmer",
        email=user.email,
        phone=user.phone,
        preferred_language=user.preferred_language or "kn",
        created_at=user.created_at
    )

@app.post("/auth/logout")
def auth_logout(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    user = get_current_user_optional(authorization, db)
    if user:
        user.auth_token = None
        db.commit()
    return {"status": "ok", "message": "Logged out successfully"}

@app.post("/auth/forgot-password")
def auth_forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    clean_email = payload.email.strip().lower()
    user = get_user_by_email(clean_email, db)

    if not user:
        # Prevent account enumeration: return success message even if not found
        return {
            "status": "ok",
            "message": "If an account exists with this email, instructions and reset code have been generated."
        }

    reset_token = generate_reset_token()
    user.reset_token = reset_token
    user.reset_token_expiry = datetime.utcnow() + timedelta(hours=1)
    db.commit()

    # In local/demo environment, we provide the reset_token directly in response for immediate testing
    return {
        "status": "ok",
        "message": "Password reset token generated successfully.",
        "reset_token": reset_token
    }

@app.post("/auth/reset-password")
def auth_reset_password(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    clean_email = payload.email.strip().lower()
    user = get_user_by_email(clean_email, db)

    if not user or not user.reset_token:
        raise HTTPException(status_code=400, detail="Invalid reset request.")

    if user.reset_token != payload.token.strip():
        raise HTTPException(status_code=400, detail="Invalid or expired reset token.")

    if user.reset_token_expiry and datetime.utcnow() > user.reset_token_expiry:
        raise HTTPException(status_code=400, detail="Reset token has expired. Please request a new one.")

    # Apply new password
    user.password_hash = hash_password(payload.new_password)
    user.reset_token = None
    user.reset_token_expiry = None
    user.auth_token = generate_session_token()
    db.commit()

    return {"status": "ok", "message": "Password has been successfully updated. You can now log in."}


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "KrishiRakshak AI"}

@app.get("/")
def read_root():
    return {
        "status": "online",
        "project": settings.PROJECT_NAME,
        "tagline": settings.TAGLINE,
        "demo_mode": settings.DEMO_MODE,
        "supported_languages": list(settings.LANGUAGES.keys())
    }


# 1. POST /chat — Conversational Agent Endpoint
@app.post("/chat", response_model=ChatResponse)
def handle_chat(request: ChatRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == request.user_id).first() if request.user_id else None
    if not user:
        user = ensure_default_user_and_samples(db)

    # Resolve or create conversation
    conv = None
    if request.conversation_id:
        conv = db.query(Conversation).filter(Conversation.id == request.conversation_id).first()
    if not conv:
        conv = Conversation(
            id=str(uuid.uuid4()),
            user_id=user.id,
            language=request.language or user.preferred_language or "kn"
        )
        db.add(conv)
        db.commit()
        db.refresh(conv)

    # Save user message to database
    user_msg = Message(
        conversation_id=conv.id,
        sender="farmer",
        text=request.message,
        image_url=request.image_url
    )
    db.add(user_msg)
    db.commit()

    # Determine language
    lang = request.language or conv.language or MultilingualService.detect_language(request.message)

    # Construct initial AgentState for LangGraph
    initial_state = {
        "user_id": user.id,
        "conversation_id": conv.id,
        "goal_id": request.goal_id,
        "current_language": lang,
        "farmer_problem": request.message,
        "image_url": request.image_url,
        "agent_activity_steps": []
    }

    # Execute LangGraph Decision Engine
    graph_output = agent_graph.invoke(initial_state)

    detected_lang = graph_output.get("current_language", lang)
    crop = graph_output.get("crop", "chilli")
    problem = request.message
    farmer_goal_text = graph_output.get("farmer_goal", "Investigate crop condition")
    urgency = graph_output.get("urgency", "Medium")
    goal_status = graph_output.get("goal_status", "Investigating")
    final_text = graph_output.get("final_response_text", "")
    activity_steps = graph_output.get("agent_activity_steps", [])
    possible_causes = graph_output.get("possible_causes", [])
    action_plan_data = graph_output.get("action_plan")
    follow_up_plan = graph_output.get("follow_up_plan")
    missing_info = graph_output.get("missing_information", [])

    # Persist or update FarmerGoal if action plan generated or goal defined
    goal_record = None
    if request.goal_id:
        goal_record = db.query(FarmerGoal).filter(FarmerGoal.id == request.goal_id).first()
    
    if not goal_record and goal_status != "Conversational":
        goal_record = FarmerGoal(
            user_id=user.id,
            crop=crop,
            problem=problem,
            goal=farmer_goal_text,
            urgency=urgency,
            status=goal_status,
            language=detected_lang
        )
        db.add(goal_record)
        db.commit()
        db.refresh(goal_record)
    elif goal_record:
        goal_record.status = goal_status
        goal_record.crop = crop
        goal_record.updated_at = datetime.utcnow()
        db.commit()

    # Save observation if image uploaded
    if request.image_url and goal_record:
        obs = CropObservation(
            goal_id=goal_record.id if goal_record else None,
            image_url=request.image_url,
            symptoms=graph_output.get("symptoms", []),
            affected_percentage=25.0
        )
        db.add(obs)
        db.commit()

    # Save Action Plan & Follow-Up in DB if available
    action_plan_schema = None
    if action_plan_data and goal_record:
        plan_record = ActionPlan(
            goal_id=goal_record.id if goal_record else None,
            immediate_actions=action_plan_data.get("immediate_actions", []),
            short_term_actions=action_plan_data.get("short_term_actions", []),
            monitoring_actions=action_plan_data.get("monitoring_actions", []),
            escalation_conditions=action_plan_data.get("escalation_conditions", []),
            localized_summary=action_plan_data.get("localized_summary", "")
        )
        db.add(plan_record)
        db.commit()
        db.refresh(plan_record)

        action_plan_schema = ActionPlanSchema(
            id=plan_record.id,
            goal_id=goal_record.id if goal_record else None,
            immediate_actions=plan_record.immediate_actions,
            short_term_actions=plan_record.short_term_actions,
            monitoring_actions=plan_record.monitoring_actions,
            escalation_conditions=plan_record.escalation_conditions,
            localized_summary=plan_record.localized_summary
        )

        # Schedule follow-up
        fu_record = FollowUp(
            goal_id=goal_record.id if goal_record else None,
            scheduled_date=datetime.utcnow() + timedelta(days=3),
            status="Scheduled"
        )
        db.add(fu_record)
        db.commit()

    # Save Agent Response Message
    agent_msg = Message(
        conversation_id=conv.id,
        sender="krishirakshak_agent",
        text=final_text,
        metadata_json={
            "goal_id": goal_record.id if goal_record else None,
            "causes": possible_causes,
            "status": goal_status
        }
    )
    db.add(agent_msg)
    db.commit()

    formatted_causes = [
        PossibleCause(
            cause=c["cause"],
            probability=c["probability"],
            confidence_score=c["confidence_score"],
            symptoms_matched=c.get("symptoms_matched", []),
            explanation=c.get("explanation", "")
        )
        for c in possible_causes
    ]

    steps = [
        AgentActivityStep(step_id=s["step_id"], label=s["label"], status=s.get("status", "completed"))
        for s in activity_steps
    ]

    next_fu_str = (datetime.utcnow() + timedelta(days=3)).strftime("%Y-%m-%d") if action_plan_data else None

    return ChatResponse(
        user_id=user.id,
        conversation_id=conv.id,
        goal_id=goal_record.id if goal_record else None,
        detected_language=detected_lang,
        response_text=final_text,
        agent_activity_steps=steps,
        goal_defined=farmer_goal_text,
        goal_status=goal_status,
        missing_information=missing_info,
        possible_causes=formatted_causes,
        action_plan=action_plan_schema,
        next_follow_up_date=next_fu_str,
        urgency=urgency
    )


# 2. GET /goals — List all ongoing and completed farmer goals
@app.get("/goals", response_model=List[GoalSummaryResponse])
def get_all_goals(user_id: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(FarmerGoal)
    if user_id:
        query = query.filter(FarmerGoal.user_id == user_id)
    goals = query.order_by(FarmerGoal.updated_at.desc()).all()

    results = []
    for g in goals:
        latest_obs = db.query(CropObservation).filter(CropObservation.goal_id == g.id).order_by(CropObservation.created_at.desc()).first()
        latest_plan = db.query(ActionPlan).filter(ActionPlan.goal_id == g.id).order_by(ActionPlan.created_at.desc()).first()
        latest_fu = db.query(FollowUp).filter(FollowUp.goal_id == g.id).order_by(FollowUp.created_at.desc()).first()

        plan_schema = None
        if latest_plan:
            plan_schema = ActionPlanSchema(
                id=latest_plan.id,
                goal_id=g.id,
                immediate_actions=latest_plan.immediate_actions or [],
                short_term_actions=latest_plan.short_term_actions or [],
                monitoring_actions=latest_plan.monitoring_actions or [],
                escalation_conditions=latest_plan.escalation_conditions or [],
                localized_summary=latest_plan.localized_summary
            )

        fu_date = latest_fu.scheduled_date.strftime("%Y-%m-%d") if latest_fu else None

        results.append(GoalSummaryResponse(
            id=g.id,
            user_id=g.user_id,
            crop=g.crop,
            problem=g.problem,
            goal=g.goal,
            urgency=g.urgency,
            status=g.status,
            language=g.language,
            created_at=g.created_at,
            updated_at=g.updated_at,
            latest_image_url=latest_obs.image_url if latest_obs else None,
            action_plan=plan_schema,
            next_follow_up_date=fu_date,
            possible_causes=[]
        ))
    return results


# 3. GET /goal/{id} — Retrieve detailed goal state
@app.get("/goal/{goal_id}", response_model=GoalSummaryResponse)
def get_goal_by_id(goal_id: str, db: Session = Depends(get_db)):
    g = db.query(FarmerGoal).filter(FarmerGoal.id == goal_id).first()
    if not g:
        raise HTTPException(status_code=404, detail="Goal not found")

    latest_obs = db.query(CropObservation).filter(CropObservation.goal_id == g.id).order_by(CropObservation.created_at.desc()).first()
    latest_plan = db.query(ActionPlan).filter(ActionPlan.goal_id == g.id).order_by(ActionPlan.created_at.desc()).first()
    latest_fu = db.query(FollowUp).filter(FollowUp.goal_id == g.id).order_by(FollowUp.created_at.desc()).first()

    plan_schema = None
    if latest_plan:
        plan_schema = ActionPlanSchema(
            id=latest_plan.id,
            goal_id=g.id,
            immediate_actions=latest_plan.immediate_actions or [],
            short_term_actions=latest_plan.short_term_actions or [],
            monitoring_actions=latest_plan.monitoring_actions or [],
            escalation_conditions=latest_plan.escalation_conditions or [],
            localized_summary=latest_plan.localized_summary
        )

    fu_date = latest_fu.scheduled_date.strftime("%Y-%m-%d") if latest_fu else None

    return GoalSummaryResponse(
        id=g.id,
        user_id=g.user_id,
        crop=g.crop,
        problem=g.problem,
        goal=g.goal,
        urgency=g.urgency,
        status=g.status,
        language=g.language,
        created_at=g.created_at,
        updated_at=g.updated_at,
        latest_image_url=latest_obs.image_url if latest_obs else None,
        action_plan=plan_schema,
        next_follow_up_date=fu_date,
        possible_causes=[]
    )


# 4. POST /goal/{id}/follow-up — Execute Closed-Loop Follow-Up Agent
@app.post("/goal/{goal_id}/follow-up", response_model=FollowUpSubmitResponse)
def submit_goal_follow_up(goal_id: str, request: FollowUpSubmitRequest, db: Session = Depends(get_db)):
    goal = db.query(FarmerGoal).filter(FarmerGoal.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    # Get initial image observation
    initial_obs = db.query(CropObservation).filter(CropObservation.goal_id == goal.id).order_by(CropObservation.created_at.asc()).first()
    prev_image = initial_obs.image_url if initial_obs else ""

    lang = request.language or goal.language or "kn"

    # Execute Follow-Up Agent
    eval_result = FollowUpAgent.evaluate_follow_up(
        previous_image=prev_image,
        new_image=request.new_image_url or prev_image,
        farmer_response=request.farmer_response,
        condition_assessment=request.condition_assessment or "",
        lang=lang,
        crop=goal.crop
    )

    # Update goal status
    goal.status = eval_result["goal_status"]
    goal.updated_at = datetime.utcnow()

    # Save new follow-up record
    fu_record = FollowUp(
        goal_id=goal.id,
        scheduled_date=datetime.utcnow(),
        farmer_response=request.farmer_response,
        new_image_url=request.new_image_url,
        status=eval_result["comparison_result"],
        comparison_notes=eval_result.get("response_text")
    )
    db.add(fu_record)

    # If action plan updated, save new version
    updated_plan_schema = None
    if eval_result.get("updated_action_plan"):
        u_plan = eval_result["updated_action_plan"]
        new_plan_row = ActionPlan(
            goal_id=goal.id,
            immediate_actions=u_plan.get("immediate_actions", []),
            short_term_actions=u_plan.get("short_term_actions", []),
            monitoring_actions=u_plan.get("monitoring_actions", []),
            escalation_conditions=u_plan.get("escalation_conditions", []),
            localized_summary=u_plan.get("localized_summary", "")
        )
        db.add(new_plan_row)
        db.commit()
        db.refresh(new_plan_row)

        updated_plan_schema = ActionPlanSchema(
            id=new_plan_row.id,
            goal_id=goal.id,
            immediate_actions=new_plan_row.immediate_actions,
            short_term_actions=new_plan_row.short_term_actions,
            monitoring_actions=new_plan_row.monitoring_actions,
            escalation_conditions=new_plan_row.escalation_conditions,
            localized_summary=new_plan_row.localized_summary
        )
    else:
        db.commit()

    return FollowUpSubmitResponse(
        goal_id=goal.id,
        status=goal.status,
        observation_result=eval_result["comparison_result"],
        response_text=eval_result["response_text"],
        updated_action_plan=updated_plan_schema,
        comparison_details=eval_result.get("comparison_details", {}),
        prevention_guidance=eval_result.get("prevention_guidance"),
        expert_escalation_recommended=eval_result["expert_escalation_recommended"],
        expert_contacts=eval_result["expert_contacts"]
    )


# 5. POST /upload-image — Upload leaf or crop photo
@app.post("/upload-image")
async def upload_crop_image(file: UploadFile = File(...)):
    # 1. Validate file extension
    ext = os.path.splitext(file.filename or "")[1].lower()
    allowed_exts = {".jpg", ".jpeg", ".png", ".webp"}
    if ext not in allowed_exts:
        raise HTTPException(
            status_code=400,
            detail="Invalid image format. Only JPG, JPEG, PNG, and WebP images are supported."
        )

    # 2. Validate MIME type
    if file.content_type and not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is not a valid image."
        )

    # 3. Read and validate size (Max 10 MB)
    max_size = 10 * 1024 * 1024
    content = await file.read()
    if len(content) > max_size:
        raise HTTPException(
            status_code=400,
            detail="Image size exceeds the 10 MB limit. Please upload a smaller photo."
        )

    filename = f"{uuid.uuid4().hex}{ext}"
    file_path = settings.UPLOAD_DIR / filename

    with open(file_path, "wb") as buffer:
        buffer.write(content)

    return {
        "filename": filename,
        "image_url": f"/uploads/{filename}",
        "size_bytes": len(content),
        "status": "uploaded"
    }


# 6. @app.post("/analyze-image")
def analyze_image_endpoint(image_url: str = Form(...), crop_hint: str = Form("chilli")):
    res = crop_image_analyzer.analyze_crop_image(image_url, crop_hint)
    return res


# 7. GET /weather — Weather and Agro-Meteorological Risk
@app.get("/weather", response_model=WeatherInfoResponse)
def get_weather_endpoint(location: str = "Mandya, Karnataka"):
    data = weather_tool.get_weather(location)
    return WeatherInfoResponse(**data)


# 8. GET /schemes — Government Schemes and Farmer Assistance
@app.get("/schemes", response_model=List[SchemeInfoResponse])
def get_schemes_endpoint(location: str = "", context: str = ""):
    schemes = govt_schemes_tool.search(location, context)
    return [SchemeInfoResponse(**s) for s in schemes]


# 9. GET /dashboard — High-Level Dashboard Statistics
@app.get("/dashboard", response_model=DashboardDataResponse)
def get_dashboard_data(db: Session = Depends(get_db)):
    active_count = db.query(FarmerGoal).filter(FarmerGoal.status != "Completed").count()
    completed_count = db.query(FarmerGoal).filter(FarmerGoal.status == "Completed").count()

    recent_goals_raw = db.query(FarmerGoal).order_by(FarmerGoal.updated_at.desc()).limit(5).all()
    recent_goals = []
    for g in recent_goals_raw:
        obs = db.query(CropObservation).filter(CropObservation.goal_id == g.id).first()
        recent_goals.append(GoalSummaryResponse(
            id=g.id,
            user_id=g.user_id,
            crop=g.crop,
            problem=g.problem,
            goal=g.goal,
            urgency=g.urgency,
            status=g.status,
            language=g.language,
            created_at=g.created_at,
            updated_at=g.updated_at,
            latest_image_url=obs.image_url if obs else None,
            action_plan=None,
            next_follow_up_date=None,
            possible_causes=[]
        ))

    weather_data = WeatherInfoResponse(**weather_tool.get_weather("Mandya, Karnataka"))
    schemes_data = [SchemeInfoResponse(**s) for s in govt_schemes_tool.search()[:4]]

    return DashboardDataResponse(
        active_goals_count=active_count,
        resolved_goals_count=completed_count,
        recent_goals=recent_goals,
        weather_summary=weather_data,
        top_schemes=schemes_data
    )
