import re
import logging
from typing import Dict, List, Any, Union, Tuple

from .validator import validate_url, validate_image_url, validate_slug, validate_title

logger = logging.getLogger(__name__)

def validate_streaming_server(server: Dict[str, Any]) -> bool:
    """
    Memvalidasi streaming server.
    
    Args:
        server: Server yang akan divalidasi
        
    Returns:
        bool: True jika server valid, False jika tidak
    """
    # Validasi server_name
    if not server.get("server_name", ""):
        logger.warning(f"Server name tidak valid: {server.get('server_name', '')}")
        return False
    
    # Validasi streaming_url
    url_valid = validate_url(server.get("streaming_url", ""))
    if not url_valid:
        logger.warning(f"Streaming URL tidak valid: {server.get('streaming_url', '')}")
        return False
    
    return True

def fill_optional_streaming_server_fields(server: Dict[str, Any]) -> Dict[str, Any]:
    """
    Mengisi field opsional yang kosong dengan data dummy untuk streaming server.
    
    Args:
        server: Server yang akan diisi field opsionalnya
        
    Returns:
        Dict[str, Any]: Server dengan field opsional yang telah diisi
    """
    # Buat salinan server untuk dimodifikasi
    filled_server = server.copy()
    
    # Tidak ada field opsional untuk streaming server
    
    return filled_server

def validate_episode_detail(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Memvalidasi dan menyusun data JSON untuk endpoint episode-detail.
    
    Args:
        data: Data yang akan divalidasi
        
    Returns:
        Dict[str, Any]: Data yang telah divalidasi dengan confidence_score
    """
    logger.info("Memulai validasi data episode-detail")
    
    # Inisialisasi hasil dengan confidence_score default 0.0 dan tipe data Dict[str, Any]
    result: Dict[str, Any] = {
        "confidence_score": 0.0,
        "message": "Data berhasil diambil",
        "source": "samehadaku.how"
    }
    
    # Validasi field wajib
    title_valid = validate_title(data.get("title", ""))
    if not title_valid:
        logger.warning(f"Title tidak valid: {data.get('title', '')}")
        return result
    
    thumbnail_url_valid = validate_image_url(data.get("thumbnail_url", ""))
    if not thumbnail_url_valid and "anime_info" in data and "thumbnail_url" in data["anime_info"]:
        # Coba ambil thumbnail_url dari anime_info jika ada
        thumbnail_url_valid = validate_image_url(data["anime_info"]["thumbnail_url"])
    
    if not thumbnail_url_valid:
        logger.warning(f"Thumbnail URL tidak valid: {data.get('thumbnail_url', '')}")
        return result
    
    # Validasi streaming_servers
    streaming_servers_valid = False
    valid_servers = []
    
    if "streaming_servers" in data and isinstance(data["streaming_servers"], list):
        for server in data["streaming_servers"]:
            if validate_streaming_server(server):
                valid_servers.append(fill_optional_streaming_server_fields(server))
        
        if valid_servers:
            streaming_servers_valid = True
    
    if not streaming_servers_valid:
        logger.warning("Streaming servers tidak valid")
        return result
    
    # Semua field wajib valid, set confidence_score
    result["confidence_score"] = 1.0
    
    # Salin field wajib
    result["title"] = data["title"]
    if "thumbnail_url" in data and thumbnail_url_valid:
        result["thumbnail_url"] = data["thumbnail_url"]
    elif "anime_info" in data and "thumbnail_url" in data["anime_info"] and thumbnail_url_valid:
        result["thumbnail_url"] = data["anime_info"]["thumbnail_url"]
    result["streaming_servers"] = valid_servers
    
    # Field opsional
    if "release_info" in data:
        result["release_info"] = data["release_info"]
    else:
        result["release_info"] = "N/A"
    
    if "download_links" in data:
        result["download_links"] = data["download_links"]
    else:
        result["download_links"] = {}
    
    if "navigation" in data:
        result["navigation"] = data["navigation"]
    else:
        result["navigation"] = {
            "previous_episode_url": None,
            "next_episode_url": None,
            "all_episodes_url": None
        }
    
    if "anime_info" in data:
        result["anime_info"] = data["anime_info"]
    else:
        result["anime_info"] = {}
    
    if "other_episodes" in data:
        result["other_episodes"] = data["other_episodes"]
    else:
        result["other_episodes"] = []
    
    return result