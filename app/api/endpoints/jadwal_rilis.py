import logging
from typing import Dict, List, Optional, Union, Any
from fastapi import APIRouter, Depends, HTTPException, Query

from ...core.cache import get_from_cache_or_fetch, invalidate_cache
from ...schemas.anime import AnimeSchedule, AnimeScheduleItem
from ...services.scraper_factory import ScraperFactory
from ...utils.jadwal_validator import validate_jadwal_all_data, validate_jadwal_data

router = APIRouter()
logger = logging.getLogger("app.api.endpoints.jadwal_rilis")


@router.get("/", response_model=Dict[str, Any])
async def get_jadwal_rilis_all(force_refresh: bool = False):
    """
    Get release schedule for all days.
    
    Args:
        force_refresh: Force refresh cache (optional, default: False)
    """
    scraper = ScraperFactory.get_default_scraper()
    if not scraper:
        raise HTTPException(status_code=503, detail="No active scraper available")
    
    cache_key = "jadwal_rilis_all"
    
    # Invalidate cache if force_refresh is True
    if force_refresh:
        logger.info("Force refresh cache untuk jadwal_rilis_all")
        invalidate_cache(cache_key)
    
    # Ambil data dari cache atau fetch baru
    raw_result = get_from_cache_or_fetch(cache_key, scraper.get_jadwal_rilis)
    
    if not raw_result:
        raise HTTPException(status_code=500, detail="Failed to get release schedule data")
    
    # Log data mentah untuk debugging
    if isinstance(raw_result, dict):
        logger.info(f"Data mentah dari scraper: {raw_result.keys()}")
        
        for day, items in raw_result.items():
            logger.info(f"Jumlah item jadwal {day}: {len(items)}")
            if items:
                logger.info(f"Contoh item jadwal {day}: {items[0]}")
    else:
        logger.warning("Data mentah bukan dictionary")
    
    # Validasi data sebelum mengembalikan respons
    if isinstance(raw_result, dict):
        validated_result = validate_jadwal_all_data(raw_result)
    else:
        logger.error("Data mentah bukan dictionary, tidak dapat divalidasi")
        raise HTTPException(status_code=500, detail="Invalid data format from scraper")
    
    # Log hasil validasi
    logger.info(f"Confidence score: {validated_result['confidence_score']}")
    for day, items in validated_result.items():
        if day != "confidence_score":
            logger.info(f"Jumlah item valid - {day}: {len(items)}")
    
    return validated_result


@router.get("/{day}", response_model=Dict[str, Any])
async def get_jadwal_rilis_by_day(day: str, force_refresh: bool = False):
    """
    Get release schedule for a specific day.
    
    Args:
        day: Day of the week (monday, tuesday, etc.)
        force_refresh: Force refresh cache (optional, default: False)
    """
    # Validate day
    valid_days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    if day.lower() not in valid_days:
        raise HTTPException(status_code=400, detail=f"Invalid day. Valid days are: {', '.join(valid_days)}")
    
    scraper = ScraperFactory.get_default_scraper()
    if not scraper:
        raise HTTPException(status_code=503, detail="No active scraper available")
    
    cache_key = f"jadwal_rilis_{day.lower()}"
    
    # Invalidate cache if force_refresh is True
    if force_refresh:
        logger.info(f"Force refresh cache untuk jadwal_rilis_{day.lower()}")
        invalidate_cache(cache_key)
    
    # Ambil data dari cache atau fetch baru
    raw_result = get_from_cache_or_fetch(cache_key, scraper.get_jadwal_rilis, day.lower())
    
    if not raw_result:
        raise HTTPException(status_code=500, detail="Failed to get release schedule data")
    
    # Log data mentah untuk debugging
    if isinstance(raw_result, list):
        logger.info(f"Data mentah dari scraper: {len(raw_result)} item")
        if raw_result:
            logger.info(f"Contoh item jadwal: {raw_result[0]}")
        
        # Validasi data sebelum mengembalikan respons
        validated_result = validate_jadwal_data(raw_result)
    else:
        logger.error("Data mentah bukan list, tidak dapat divalidasi")
        raise HTTPException(status_code=500, detail="Invalid data format from scraper")
    
    # Log hasil validasi
    logger.info(f"Confidence score: {validated_result['confidence_score']}")
    logger.info(f"Jumlah item valid: {len(validated_result['data'])}")
    
    return validated_result