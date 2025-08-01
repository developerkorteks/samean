import re
import logging
from typing import Dict, List, Any, Union, Tuple

from .validator import validate_url, validate_image_url, validate_slug, validate_title

logger = logging.getLogger(__name__)

def validate_episode_item(item: Dict[str, Any]) -> bool:
    """
    Memvalidasi item episode dalam episode_list.
    
    Args:
        item: Item yang akan divalidasi
        
    Returns:
        bool: True jika item valid, False jika tidak
    """
    # Validasi episode
    if not item.get("episode", ""):
        logger.warning(f"Episode tidak valid: {item.get('episode', '')}")
        return False
    
    # Validasi title
    title_valid = validate_title(item.get("title", ""))
    if not title_valid:
        logger.warning(f"Title tidak valid: {item.get('title', '')}")
        return False
    
    # Validasi URL
    url_valid = validate_url(item.get("url", ""))
    if not url_valid:
        logger.warning(f"URL tidak valid: {item.get('url', '')}")
        return False
    
    # Validasi episode_slug
    slug_valid = validate_slug(item.get("episode_slug", ""))
    if not slug_valid:
        logger.warning(f"Episode slug tidak valid: {item.get('episode_slug', '')}")
        return False
    
    return True

def fill_optional_episode_fields(item: Dict[str, Any]) -> Dict[str, Any]:
    """
    Mengisi field opsional yang kosong dengan data dummy untuk item episode.
    
    Args:
        item: Item yang akan diisi field opsionalnya
        
    Returns:
        Dict[str, Any]: Item dengan field opsional yang telah diisi
    """
    # Buat salinan item untuk dimodifikasi
    filled_item = item.copy()
    
    # Field opsional untuk AnimeEpisode
    if "release_date" not in filled_item or not filled_item["release_date"]:
        filled_item["release_date"] = "N/A"
    
    return filled_item

def validate_recommendation_item(item: Dict[str, Any]) -> bool:
    """
    Memvalidasi item recommendation.
    
    Args:
        item: Item yang akan divalidasi
        
    Returns:
        bool: True jika item valid, False jika tidak
    """
    # Validasi title
    title_valid = validate_title(item.get("title", ""))
    if not title_valid:
        logger.warning(f"Title tidak valid: {item.get('title', '')}")
        return False
    
    # Validasi URL
    url_valid = validate_url(item.get("url", ""))
    if not url_valid:
        logger.warning(f"URL tidak valid: {item.get('url', '')}")
        return False
    
    # Validasi anime_slug
    slug_valid = validate_slug(item.get("anime_slug", ""))
    if not slug_valid:
        logger.warning(f"Anime slug tidak valid: {item.get('anime_slug', '')}")
        return False
    
    # Validasi cover_url
    cover_valid = validate_image_url(item.get("cover_url", ""))
    if not cover_valid:
        logger.warning(f"Cover URL tidak valid: {item.get('cover_url', '')}")
        return False
    
    return True

def fill_optional_recommendation_fields(item: Dict[str, Any]) -> Dict[str, Any]:
    """
    Mengisi field opsional yang kosong dengan data dummy untuk item recommendation.
    
    Args:
        item: Item yang akan diisi field opsionalnya
        
    Returns:
        Dict[str, Any]: Item dengan field opsional yang telah diisi
    """
    # Buat salinan item untuk dimodifikasi
    filled_item = item.copy()
    
    # Field opsional untuk recommendation
    if "rating" not in filled_item or not filled_item["rating"]:
        filled_item["rating"] = "N/A"
    
    if "episode" not in filled_item or not filled_item["episode"]:
        filled_item["episode"] = "N/A"
    
    return filled_item

def validate_anime_detail(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Memvalidasi dan menyusun data JSON untuk endpoint anime-detail.
    
    Args:
        data: Data yang akan divalidasi
        
    Returns:
        Dict[str, Any]: Data yang telah divalidasi dengan confidence_score
    """
    logger.info("Memulai validasi data anime-detail")
    
    # Inisialisasi hasil dengan confidence_score default 0.0 dan tipe data Dict[str, Any]
    result: Dict[str, Any] = {
        "confidence_score": 0.0
    }
    
    # Validasi field wajib
    judul_valid = validate_title(data.get("judul", ""))
    if not judul_valid:
        logger.warning(f"Judul tidak valid: {data.get('judul', '')}")
        return result
    
    url_anime_valid = validate_url(data.get("url_anime", ""))
    if not url_anime_valid:
        logger.warning(f"URL anime tidak valid: {data.get('url_anime', '')}")
        return result
    
    anime_slug_valid = validate_slug(data.get("anime_slug", ""))
    if not anime_slug_valid:
        logger.warning(f"Anime slug tidak valid: {data.get('anime_slug', '')}")
        return result
    
    url_cover_valid = validate_image_url(data.get("url_cover", ""))
    if not url_cover_valid:
        logger.warning(f"URL cover tidak valid: {data.get('url_cover', '')}")
        return result
    
    # Validasi episode_list
    episode_list_valid = False
    valid_episodes = []
    
    if "episode_list" in data and isinstance(data["episode_list"], list):
        for item in data["episode_list"]:
            if validate_episode_item(item):
                valid_episodes.append(fill_optional_episode_fields(item))
        
        if valid_episodes:
            episode_list_valid = True
    
    if not episode_list_valid:
        logger.warning("Episode list tidak valid")
        return result
    
    # Validasi recommendations (opsional)
    valid_recommendations = []
    
    if "recommendations" in data and isinstance(data["recommendations"], list):
        for item in data["recommendations"]:
            if validate_recommendation_item(item):
                valid_recommendations.append(fill_optional_recommendation_fields(item))
    
    # Semua field wajib valid, set confidence_score
    result["confidence_score"] = 1.0
    
    # Salin field wajib
    result["judul"] = data["judul"]
    result["url_anime"] = data["url_anime"]
    result["anime_slug"] = data["anime_slug"]
    result["url_cover"] = data["url_cover"]
    result["episode_list"] = valid_episodes
    
    # Salin field opsional jika valid
    if valid_recommendations:
        result["recommendations"] = valid_recommendations
    
    # Field opsional lainnya
    if "status" in data:
        result["status"] = data["status"]
    else:
        result["status"] = "N/A"
    
    if "tipe" in data:
        result["tipe"] = data["tipe"]
    else:
        result["tipe"] = "N/A"
    
    if "skor" in data:
        result["skor"] = data["skor"]
    else:
        result["skor"] = "N/A"
    
    if "penonton" in data:
        result["penonton"] = data["penonton"]
    else:
        result["penonton"] = "N/A"
    
    if "sinopsis" in data:
        result["sinopsis"] = data["sinopsis"]
    else:
        result["sinopsis"] = "N/A"
    
    if "genre" in data:
        result["genre"] = data["genre"]
    else:
        result["genre"] = ["Anime"]
    
    if "details" in data:
        result["details"] = data["details"]
    else:
        result["details"] = {}
    
    if "rating" in data:
        result["rating"] = data["rating"]
    else:
        result["rating"] = {"score": "N/A", "users": "N/A"}
    
    return result