import logging
from typing import Dict, List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException, Query

from ...core.cache import get_from_cache_or_fetch, invalidate_cache
from ...schemas.anime import AnimeDetail
from ...services.scraper_factory import ScraperFactory
from ...utils.anime_detail_validator import validate_anime_detail

router = APIRouter()
logger = logging.getLogger("app.api.endpoints.anime_detail")


@router.get("/", response_model=Dict[str, Any])
async def get_anime_detail(anime_slug: str = Query(..., description="Anime slug"), force_refresh: bool = False):
    """
    Get anime details.
    
    Args:
        anime_slug: Anime slug
        force_refresh: Force refresh cache (optional, default: False)
    """
    scraper = ScraperFactory.get_default_scraper()
    if not scraper:
        raise HTTPException(status_code=503, detail="No active scraper available")
    
    cache_key = f"anime_detail_{anime_slug}"
    
    # Invalidate cache if force_refresh is True
    if force_refresh:
        logger.info(f"Force refresh cache untuk anime_detail_{anime_slug}")
        invalidate_cache(cache_key)
    
    # Ambil data dari cache atau fetch baru
    raw_result = get_from_cache_or_fetch(cache_key, scraper.get_anime_details, anime_slug)
    
    if not raw_result:
        raise HTTPException(status_code=404, detail=f"Anime with slug '{anime_slug}' not found")
    
    # Log data mentah untuk debugging
    logger.info(f"Data mentah dari scraper: {raw_result.keys() if isinstance(raw_result, dict) else 'bukan dict'}")
    
    # Validasi data sebelum mengembalikan respons
    if isinstance(raw_result, dict):
        validated_result = validate_anime_detail(raw_result)
        
        # Log hasil validasi
        logger.info(f"Confidence score: {validated_result['confidence_score']}")
        
        return validated_result
    else:
        logger.error("Data mentah bukan dictionary, tidak dapat divalidasi")
        raise HTTPException(status_code=500, detail="Invalid data format from scraper")