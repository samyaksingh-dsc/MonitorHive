import aiohttp
import asyncio
import ssl
import socket
from datetime import datetime
from typing import Dict, Any, Tuple
import OpenSSL
from sqlalchemy.orm import Session
import models
from urllib.parse import urlparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def check_website_health(url: str) -> Dict[str, Any]:
    """
    Check website health including response time and status code.
    """
    try:
        async with aiohttp.ClientSession() as session:
            start_time = datetime.now()
            async with session.get(url, timeout=30) as response:
                end_time = datetime.now()
                response_time = (end_time - start_time).total_seconds()
                
                return {
                    "is_up": response.status < 400,
                    "status_code": response.status,
                    "response_time": response_time,
                    "error_message": None
                }
    except Exception as e:
        return {
            "is_up": False,
            "status_code": 0,
            "response_time": 0,
            "error_message": str(e)
        }

async def check_ssl_certificate(url: str) -> Dict[str, Any]:
    """
    Check SSL certificate validity and details.
    """
    try:
        hostname = urlparse(url).hostname
        context = ssl.create_default_context()
        
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                
                not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                issuer = dict(x[0] for x in cert['issuer'])
                
                return {
                    "is_valid": True,
                    "expires_at": not_after,
                    "issuer": issuer.get('organizationName', 'Unknown'),
                    "error_message": None
                }
    except Exception as e:
        return {
            "is_valid": False,
            "expires_at": None,
            "issuer": None,
            "error_message": str(e)
        }

async def check_security_headers(url: str) -> Dict[str, Any]:
    """
    Check security headers and calculate security score.
    """
    security_headers = {
        'Strict-Transport-Security': 10,
        'Content-Security-Policy': 10,
        'X-Frame-Options': 10,
        'X-Content-Type-Options': 10,
        'Referrer-Policy': 10,
        'Permissions-Policy': 10,
        'X-XSS-Protection': 5,
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                headers = response.headers
                score = 0
                found_headers = {}
                
                for header, points in security_headers.items():
                    if header in headers:
                        score += points
                        found_headers[header] = headers[header]
                
                return {
                    "headers": found_headers,
                    "score": score,
                    "error_message": None
                }
    except Exception as e:
        return {
            "headers": {},
            "score": 0,
            "error_message": str(e)
        }

async def monitor_website(db: Session, website: models.Website) -> None:
    """
    Monitor a website and store results in database.
    """
    try:
        # Check basic health
        health_result = await check_website_health(str(website.url))
        monitoring_result = models.MonitoringResult(
            website_id=website.id,
            **{key: health_result[key] for key in ['is_up', 'status_code', 'response_time']}  # Only include valid fields
        )
        db.add(monitoring_result)
        
        # Check SSL if website is up
        if health_result["is_up"]:
            ssl_result = await check_ssl_certificate(str(website.url))
            ssl_check = models.SSLCheck(
                website_id=website.id,
                is_valid=ssl_result["is_valid"],
                expires_at=ssl_result["expires_at"],
                issuer=ssl_result["issuer"],
                error_message=ssl_result["error_message"]
            )
            db.add(ssl_check)
            
            # Check security headers
            security_result = await check_security_headers(str(website.url))
            security_header = models.SecurityHeader(
                website_id=website.id,
                headers=security_result["headers"],
                score=security_result["score"],
                error_message=security_result.get("error_message", None)  # Include error_message safely
            )
            db.add(security_header)
        
        db.commit()
        
    except Exception as e:
        logger.error(f"Error monitoring website {website.url}: {str(e)}")
        db.rollback()
        raise

async def monitor_all_websites(db: Session) -> None:
    """
    Monitor all active websites.
    """
    websites = db.query(models.Website).filter(models.Website.is_active == True).all()
    tasks = [monitor_website(db, website) for website in websites]
    await asyncio.gather(*tasks)