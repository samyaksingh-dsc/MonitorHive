from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from database import get_db
from services.monitor_service import monitor_website, check_website_health, check_ssl_certificate, check_security_headers
from utils.security import get_current_active_user

router = APIRouter(
    prefix="/monitor",
    tags=["monitoring"]
)

@router.post("/websites/", response_model=schemas.Website)
async def add_website_for_monitoring(
    website: schemas.WebsiteCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Add a new website and start monitoring it."""
    # Create website record
    db_website = models.Website(
        **website.model_dump(),
        owner_id=current_user.id
    )
    db.add(db_website)
    db.commit()
    db.refresh(db_website)
    
    # Start initial monitoring
    await monitor_website(db, db_website)
    
    return db_website

@router.get("/websites/", response_model=List[schemas.Website])
async def get_monitored_websites(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get all monitored websites for current user."""
    return db.query(models.Website).filter(
        models.Website.owner_id == current_user.id,
        models.Website.is_active == True
    ).all()

@router.post("/websites/{website_id}/check")
async def check_website(
    website_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Manually trigger a website check."""
    website = db.query(models.Website).filter(
        models.Website.id == website_id,
        models.Website.owner_id == current_user.id
    ).first()
    
    if not website:
        raise HTTPException(status_code=404, detail="Website not found")
    
    await monitor_website(db, website)
    return {"status": "success", "message": "Website check completed"}

@router.get("/websites/{website_id}/health")
async def get_website_health(
    website_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get current health status of a website."""
    website = db.query(models.Website).filter(
        models.Website.id == website_id,
        models.Website.owner_id == current_user.id
    ).first()
    
    if not website:
        raise HTTPException(status_code=404, detail="Website not found")
    
    health_result = await check_website_health(str(website.url))
    return health_result

@router.get("/websites/{website_id}/ssl")
async def get_website_ssl(
    website_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get SSL certificate status of a website."""
    website = db.query(models.Website).filter(
        models.Website.id == website_id,
        models.Website.owner_id == current_user.id
    ).first()
    
    if not website:
        raise HTTPException(status_code=404, detail="Website not found")
    
    ssl_result = await check_ssl_certificate(str(website.url))

    ssl_checks = db.query(models.SSLCheck).filter(models.SSLCheck.website_id == website_id).all()
    return ssl_result

@router.get("/websites/{website_id}/security")
async def get_website_security(
    website_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get security headers status of a website."""
    website = db.query(models.Website).filter(
        models.Website.id == website_id,
        models.Website.owner_id == current_user.id
    ).first()
    
    if not website:
        raise HTTPException(status_code=404, detail="Website not found")
    
    security_result = await check_security_headers(str(website.url))
    return security_result

@router.get("/websites/{website_id}/results", response_model=List[schemas.MonitoringResult])
async def get_monitoring_history(
    website_id: int,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get monitoring history for a website."""
    website = db.query(models.Website).filter(
        models.Website.id == website_id,
        models.Website.owner_id == current_user.id
    ).first()
    
    if not website:
        raise HTTPException(status_code=404, detail="Website not found")
    
    return db.query(models.MonitoringResult).filter(
        models.MonitoringResult.website_id == website_id
    ).order_by(models.MonitoringResult.timestamp.desc()).limit(limit).all()