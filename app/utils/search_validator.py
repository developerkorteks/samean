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
    
    # Field opsional untuk AnimeSearch
    if "status" not in filled_item or not filled_item["status"]:
        filled_item["status"] = "N/A"
    
    if "tipe" not in filled_item or not filled_item["tipe"]:
        filled_item["tipe"] = "N/A"
    
    if "skor" not in filled_item or not filled_item["skor"]:
        filled_item["skor"] = "N/A"
    
    if "penonton" not in filled_item or not filled_item["penonton"]:
        filled_item["penonton"] = "N/A"
    
    if "sinopsis" not in filled_item or not filled_item["sinopsis"]:
        filled_item["sinopsis"] = "N/A"
    
    if "genre" not in filled_item or not filled_item["genre"]:
        filled_item["genre"] = ["Anime"]
    
    return filled_item

def validate_search_item(item: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
    """
    Memvalidasi item search result.
    
    Args:
        item: Item yang akan divalidasi
        
    Returns:
        Tuple[bool, Dict[str, Any]]: (is_valid, validated_item)
    """
    # Log item untuk debugging
    logger.info(f"Validasi item search: {item}")
    
    # Validasi judul
    title_valid = validate_title(item.get("judul", ""))
    if not title_valid:
        logger.warning(f"Judul tidak valid: {item.get('judul', '')}")
    
    # Validasi URL
    url_valid = validate_url(item.get("url", ""))
    if not url_valid:
        logger.warning(f"URL tidak valid: {item.get('url', '')}")
    
    # Validasi anime_slug
    slug_valid = validate_slug(item.get("anime_slug", ""))
    if not slug_valid:
        logger.warning(f"Slug tidak valid: {item.get('anime_slug', '')}")
    
    # Validasi cover
    cover_valid = validate_image_url(item.get("cover", ""))
    if not cover_valid:
        logger.warning(f"Cover tidak valid: {item.get('cover', '')}")
    
    # Item valid jika semua field wajib valid
    is_valid = title_valid and url_valid and slug_valid and cover_valid
    
    if is_valid:
        logger.info("Item search valid")
        # Isi field opsional yang kosong dengan data dummy
        validated_item = fill_optional_fields(item)
        return True, validated_item
    else:
        logger.warning("Item search tidak valid")
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
            logger.error(f"URL tidak valid pada item search: {item.get('url', '')}")
            return False
        if not validate_image_url(item.get("cover", "")):
            logger.error(f"Cover tidak valid pada item search: {item.get('cover', '')}")
            return False
    
    return True

def validate_search_data(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Memvalidasi dan menyusun data JSON untuk endpoint search.
    
    Args:
        data: Data yang akan divalidasi
        
    Returns:
        Dict[str, Any]: Data yang telah divalidasi dengan confidence_score
    """
    logger.info("Memulai validasi data search")
    
    # Inisialisasi hasil dengan confidence_score default 0.0
    result = {
        "confidence_score": 0.0,
        "message": "Data berhasil diambil",
        "source": "samehadaku.how",
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
        logger.info(f"Validasi search: {len(data)} item")
        for item in data:
            is_valid, validated_item = validate_search_item(item)
            if is_valid:
                valid_items.append(validated_item)
        logger.info(f"Search valid: {len(valid_items)}/{len(data)}")
    else:
        logger.warning("Data search bukan list")
    
    # Periksa apakah ada minimal 1 item valid
    if len(valid_items) > 0:
        logger.info("Search memiliki minimal 1 item valid")
        
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