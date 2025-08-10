import logging
from typing import Dict, List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException, Query

from ...core.cache import get_from_cache_or_fetch, invalidate_cache
from ...schemas.anime import HomeData
from ...services.scraper_factory import ScraperFactory
from ...utils.validator import validate_home_data

router = APIRouter()
logger = logging.getLogger("app.api.endpoints.home")


@router.get("/", response_model=Dict[str, Any])
async def get_home_data(force_refresh: bool = False):
    """
    Get home page data.
    
    Args:
        force_refresh: Force refresh cache (optional, default: False)
    """
    scraper = ScraperFactory.get_default_scraper()
    if not scraper:
        raise HTTPException(status_code=503, detail="No active scraper available")
    
    cache_key = "home_data"
    
    # Invalidate cache if force_refresh is True
    if force_refresh:
        logger.info("Force refresh cache untuk home_data")
        invalidate_cache(cache_key)
    
    # Ambil data dari cache atau fetch baru
    raw_result = get_from_cache_or_fetch(cache_key, scraper.get_home_data)
    
    if not raw_result:
        raise HTTPException(status_code=500, detail="Failed to get home page data")
    
    # Log data mentah untuk debugging
    logger.info(f"Data mentah dari scraper: {raw_result.keys()}")
    
    if "top10" in raw_result:
        logger.info(f"Jumlah item top10: {len(raw_result['top10'])}")
        if raw_result['top10']:
            logger.info(f"Contoh item top10: {raw_result['top10'][0]}")
    
    if "new_eps" in raw_result:
        logger.info(f"Jumlah item new_eps: {len(raw_result['new_eps'])}")
        if raw_result['new_eps']:
            logger.info(f"Contoh item new_eps: {raw_result['new_eps'][0]}")
    
    if "movies" in raw_result:
        logger.info(f"Jumlah item movies: {len(raw_result['movies'])}")
        if raw_result['movies']:
            logger.info(f"Contoh item movies: {raw_result['movies'][0]}")
    
    if "jadwal_rilis" in raw_result:
        logger.info(f"Jumlah hari jadwal_rilis: {len(raw_result['jadwal_rilis'])}")
        for day, items in raw_result['jadwal_rilis'].items():
            logger.info(f"Jumlah item jadwal {day}: {len(items)}")
            if items:
                logger.info(f"Contoh item jadwal {day}: {items[0]}")
    
    # Validasi data sebelum mengembalikan respons
    validated_result = validate_home_data(raw_result)
    
    # Log hasil validasi
    logger.info(f"Confidence score: {validated_result['confidence_score']}")
    logger.info(f"Jumlah item valid - top10: {len(validated_result['top10'])}")
    logger.info(f"Jumlah item valid - new_eps: {len(validated_result['new_eps'])}")
    logger.info(f"Jumlah item valid - movies: {len(validated_result['movies'])}")
    logger.info(f"Jumlah hari valid - jadwal_rilis: {len(validated_result['jadwal_rilis'])}")
    
    return validated_result