import logging
from typing import Dict, List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException, Query

from ...core.cache import get_from_cache_or_fetch, invalidate_cache
from ...schemas.anime import EpisodeDetail
from ...services.scraper_factory import ScraperFactory
from ...utils.episode_detail_validator import validate_episode_detail

router = APIRouter()
logger = logging.getLogger("app.api.endpoints.episode_detail")


@router.get("/", response_model=Dict[str, Any])
async def get_episode_detail(episode_url: str = Query(..., description="Episode URL"), force_refresh: bool = False):
    """
    Get episode details.
    
    Args:
        episode_url: Episode URL
        force_refresh: Force refresh cache (optional, default: False)
    """
    scraper = ScraperFactory.get_default_scraper()
    if not scraper:
        raise HTTPException(status_code=503, detail="No active scraper available")
    
    cache_key = f"episode_detail_{episode_url}"
    
    # Invalidate cache if force_refresh is True
    if force_refresh:
        logger.info(f"Force refresh cache untuk episode_detail_{episode_url}")
        invalidate_cache(cache_key)
    
    # Ambil data dari cache atau fetch baru
    raw_result = get_from_cache_or_fetch(cache_key, scraper.get_episode_details, episode_url)
    
    if not raw_result:
        raise HTTPException(status_code=404, detail=f"Episode with URL '{episode_url}' not found")
    
    # Log data mentah untuk debugging
    logger.info(f"Data mentah dari scraper: {raw_result.keys() if isinstance(raw_result, dict) else 'bukan dict'}")
    
    # Validasi data sebelum mengembalikan respons
    if isinstance(raw_result, dict):
        validated_result = validate_episode_detail(raw_result)
        
        # Log hasil validasi
        logger.info(f"Confidence score: {validated_result['confidence_score']}")
        
        return validated_result
    else:
        logger.error("Data mentah bukan dictionary, tidak dapat divalidasi")
        raise HTTPException(status_code=500, detail="Invalid data format from scraper")