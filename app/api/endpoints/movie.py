import logging
from typing import Dict, List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException, Query

from ...core.cache import get_from_cache_or_fetch, invalidate_cache
from ...schemas.anime import AnimeMovie
from ...services.scraper_factory import ScraperFactory
from ...utils.movie_validator import validate_movie_data

router = APIRouter()
logger = logging.getLogger("app.api.endpoints.movie")


@router.get("/", response_model=Dict[str, Any])
async def get_movie_list(page: int = Query(1, ge=1, description="Page number"), force_refresh: bool = False):
    """
    Get anime movie list.
    
    Args:
        page: Page number (default: 1)
        force_refresh: Force refresh cache (optional, default: False)
    """
    scraper = ScraperFactory.get_default_scraper()
    if not scraper:
        raise HTTPException(status_code=503, detail="No active scraper available")
    
    cache_key = f"movie_list_page_{page}"
    
    # Invalidate cache if force_refresh is True
    if force_refresh:
        logger.info(f"Force refresh cache untuk movie_list_page_{page}")
        invalidate_cache(cache_key)
    
    # Ambil data dari cache atau fetch baru
    raw_result = get_from_cache_or_fetch(cache_key, scraper.get_movie_list, page)
    
    if not raw_result:
        raise HTTPException(status_code=500, detail="Failed to get movie list data")
    
    # Log data mentah untuk debugging
    if isinstance(raw_result, list):
        logger.info(f"Data mentah dari scraper: {len(raw_result)} item")
        if raw_result:
            logger.info(f"Contoh item movie: {raw_result[0]}")
        
        # Validasi data sebelum mengembalikan respons
        validated_result = validate_movie_data(raw_result)
        
        # Log hasil validasi
        logger.info(f"Confidence score: {validated_result['confidence_score']}")
        logger.info(f"Jumlah item valid: {len(validated_result['data'])}")
        
        return validated_result
    else:
        logger.error("Data mentah bukan list, tidak dapat divalidasi")
        raise HTTPException(status_code=500, detail="Invalid data format from scraper")