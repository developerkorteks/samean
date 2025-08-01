import re
import logging
from typing import Dict, List, Any, Union, Tuple

from .validator import validate_url, validate_image_url, validate_slug, validate_title

logger = logging.getLogger(__name__)

def fill_optional_fields(item: Dict[str, Any]) -> Dict[str, Any]:
    """
    Mengisi field opsional yang kosong dengan data dummy.
    
    Args:
        item: Item yang akan diisi field opsionalnya
        
    Returns:
        Dict[str, Any]: Item dengan field opsional yang telah diisi
    """
    # Buat salinan item untuk dimodifikasi
    filled_item = item.copy()
    
    # Field opsional untuk AnimeScheduleItem
    if "type" not in filled_item or not filled_item["type"]:
        filled_item["type"] = "TV"
    
    if "score" not in filled_item or not filled_item["score"]:
        filled_item["score"] = "N/A"
    
    if "genres" not in filled_item or not filled_item["genres"]:
        filled_item["genres"] = ["Anime"]
    
    if "release_time" not in filled_item or not filled_item["release_time"]:
        filled_item["release_time"] = "N/A"
    
    return filled_item

def validate_schedule_item(item: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
    """
    Memvalidasi item jadwal rilis.
    
    Args:
        item: Item yang akan divalidasi
        
    Returns:
        Tuple[bool, Dict[str, Any]]: (is_valid, validated_item)
    """
    # Log item untuk debugging
    logger.info(f"Validasi item jadwal: {item}")
    
    # Validasi judul
    title_valid = validate_title(item.get("title", ""))
    if not title_valid:
        logger.warning(f"Judul tidak valid: {item.get('title', '')}")
    
    # Validasi URL
    url_valid = validate_url(item.get("url", ""))
    if not url_valid:
        logger.warning(f"URL tidak valid: {item.get('url', '')}")
    
    # Validasi anime_slug
    slug_valid = validate_slug(item.get("anime_slug", ""))
    if not slug_valid:
        logger.warning(f"Slug tidak valid: {item.get('anime_slug', '')}")
    
    # Validasi cover_url
    cover_valid = validate_image_url(item.get("cover_url", ""))
    if not cover_valid:
        logger.warning(f"Cover tidak valid: {item.get('cover_url', '')}")
    
    # Item valid jika semua field wajib valid
    is_valid = title_valid and url_valid and slug_valid and cover_valid
    
    if is_valid:
        logger.info("Item jadwal valid")
        # Isi field opsional yang kosong dengan data dummy
        validated_item = fill_optional_fields(item)
        return True, validated_item
    else:
        logger.warning("Item jadwal tidak valid")
        return False, {}

def check_url_cover_validity(data: List[Dict[str, Any]]) -> bool:
    """
    Memeriksa validitas URL dan cover pada semua item.
    
    Args:
        data: Data yang akan diperiksa
        
    Returns:
        bool: True jika semua URL dan cover valid, False jika tidak
    """
    for item in data:
        if not validate_url(item.get("url", "")):
            logger.error(f"URL tidak valid pada item jadwal: {item.get('url', '')}")
            return False
        if not validate_image_url(item.get("cover_url", "")):
            logger.error(f"Cover tidak valid pada item jadwal: {item.get('cover_url', '')}")
            return False
    
    return True

def validate_jadwal_data(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Memvalidasi dan menyusun data JSON untuk endpoint jadwal_rilis.
    
    Args:
        data: Data yang akan divalidasi
        
    Returns:
        Dict[str, Any]: Data yang telah divalidasi dengan confidence_score
    """
    logger.info("Memulai validasi data jadwal_rilis")
    
    # Inisialisasi hasil dengan confidence_score default 0.0
    result = {
        "confidence_score": 0.0,
        "data": []
    }
    
    # Periksa validitas URL dan cover pada semua item
    # Jika ada URL atau cover yang tidak valid, langsung set confidence_score: 0.0
    if not check_url_cover_validity(data):
        logger.error("Ditemukan URL atau cover yang tidak valid, confidence_score: 0.0")
        return result
    
    # Validasi setiap item
    valid_items = []
    if isinstance(data, list):
        logger.info(f"Validasi jadwal_rilis: {len(data)} item")
        for item in data:
            is_valid, validated_item = validate_schedule_item(item)
            if is_valid:
                valid_items.append(validated_item)
        logger.info(f"Jadwal valid: {len(valid_items)}/{len(data)}")
    else:
        logger.warning("Data jadwal_rilis bukan list")
    
    # Periksa apakah ada minimal 1 item valid
    if len(valid_items) > 0:
        logger.info("Jadwal memiliki minimal 1 item valid")
        
        # Hitung confidence_score berdasarkan kelengkapan data
        if len(data) > 0:
            item_score = len(valid_items) / len(data)
            
            # Confidence score minimal 0.8 jika ada item valid
            result["confidence_score"] = round(max(0.8, 0.8 + (item_score * 0.2)), 2)
            logger.info(f"Confidence score: {result['confidence_score']}")
        
        # Update hasil dengan data yang valid
        result["data"] = valid_items
    else:
        logger.warning("Tidak ada item valid")
    
    return result

def validate_jadwal_all_data(data: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
    """
    Memvalidasi dan menyusun data JSON untuk endpoint jadwal_rilis (semua hari).
    
    Args:
        data: Data yang akan divalidasi
        
    Returns:
        Dict[str, Any]: Data yang telah divalidasi dengan confidence_score
    """
    logger.info("Memulai validasi data jadwal_rilis (semua hari)")
    
    # Inisialisasi hasil dengan confidence_score default 0.0
    result = {
        "confidence_score": 0.0,
        "Monday": [],
        "Tuesday": [],
        "Wednesday": [],
        "Thursday": [],
        "Friday": [],
        "Saturday": [],
        "Sunday": []
    }
    
    # Periksa validitas URL dan cover pada semua item
    all_items = []
    for day, items in data.items():
        all_items.extend(items)
    
    if not check_url_cover_validity(all_items):
        logger.error("Ditemukan URL atau cover yang tidak valid, confidence_score: 0.0")
        return result
    
    # Validasi setiap hari
    valid_days = 0
    total_valid_items = 0
    total_items = 0
    
    for day, items in data.items():
        valid_items = []
        if isinstance(items, list):
            logger.info(f"Validasi jadwal {day}: {len(items)} item")
            for item in items:
                is_valid, validated_item = validate_schedule_item(item)
                if is_valid:
                    valid_items.append(validated_item)
            logger.info(f"Jadwal {day} valid: {len(valid_items)}/{len(items)}")
            
            if len(valid_items) > 0:
                valid_days += 1
                total_valid_items += len(valid_items)
            
            total_items += len(items)
            
            # Update hasil dengan data yang valid
            result[day] = valid_items
    
    # Periksa apakah ada minimal 1 hari dengan 1 item valid
    if valid_days > 0:
        logger.info(f"Jadwal memiliki {valid_days} hari dengan minimal 1 item valid")
        
        # Hitung confidence_score berdasarkan kelengkapan data
        if total_items > 0:
            item_score = total_valid_items / total_items
            
            # Confidence score minimal 0.8 jika ada item valid
            result["confidence_score"] = round(max(0.8, 0.8 + (item_score * 0.2)), 2)
            logger.info(f"Confidence score: {result['confidence_score']}")
    else:
        logger.warning("Tidak ada hari dengan item valid")
    
    return result