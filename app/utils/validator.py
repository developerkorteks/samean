import re
import logging
from typing import Dict, List, Any, Union, Tuple

logger = logging.getLogger(__name__)

def validate_url(url: str) -> bool:
    """
    Memvalidasi format URL.
    
    Args:
        url: URL yang akan divalidasi
        
    Returns:
        bool: True jika URL valid, False jika tidak
    """
    if not url or url == "N/A" or url == "-":
        return False
    
    # URL harus dimulai dengan https://
    if not url.startswith('https://'):
        logger.warning(f"URL tidak valid (harus https://): {url}")
        return False
    
    # Validasi URL dengan regex
    url_pattern = re.compile(
        r'^https://'  # harus https://
        r'([a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?\.)+' # domain
        r'[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?' # subdomain
        r'(/[a-zA-Z0-9_\-\.~%/]+)*/?$' # path
    )
    
    is_valid = bool(url_pattern.match(url))
    if not is_valid:
        logger.warning(f"URL tidak valid (format tidak sesuai): {url}")
    
    return is_valid

def validate_image_url(url: str) -> bool:
    """
    Memvalidasi format URL gambar.
    
    Args:
        url: URL gambar yang akan divalidasi
        
    Returns:
        bool: True jika URL gambar valid, False jika tidak
    """
    if not url or url == "N/A" or url == "-":
        return False
    
    # Validasi URL dasar terlebih dahulu
    if not validate_url(url):
        return False
    
    # Cek ekstensi file gambar yang diizinkan
    valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
    has_valid_extension = any(url.lower().endswith(ext) for ext in valid_extensions)
    
    if not has_valid_extension:
        logger.warning(f"URL gambar tidak valid (ekstensi tidak sesuai): {url}")
        return False
    
    return True

def validate_slug(slug: str) -> bool:
    """
    Memvalidasi format slug.
    
    Args:
        slug: Slug yang akan divalidasi
        
    Returns:
        bool: True jika slug valid, False jika tidak
    """
    if not slug or slug == "N/A" or slug == "-":
        return False
    
    # Regex untuk validasi slug (huruf kecil, angka, dan strip)
    # Format: ^[a-z0-9]+(-[a-z0-9]+)*$
    slug_pattern = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')
    
    is_valid = bool(slug_pattern.match(slug))
    if not is_valid:
        logger.warning(f"Slug tidak valid: {slug}")
    
    return is_valid

def validate_title(title: str) -> bool:
    """
    Memvalidasi judul (minimal 2 huruf, maksimal 200 karakter, bermakna).
    
    Args:
        title: Judul yang akan divalidasi
        
    Returns:
        bool: True jika judul valid, False jika tidak
    """
    if not title or title == "N/A" or title == "-":
        return False
    
    # Judul harus memiliki minimal 2 karakter dan maksimal 200 karakter
    title_length_valid = 2 <= len(title.strip()) <= 200
    if not title_length_valid:
        logger.warning(f"Judul tidak valid (panjang): {title}")
        return False
    
    # Judul harus memiliki setidaknya satu kata berawalan huruf kapital
    has_capitalized_word = bool(re.search(r'\b[A-Z][a-zA-Z]*\b', title))
    
    # Judul tidak boleh mengandung lebih dari 3 tanda baca berturut-turut
    no_excessive_punctuation = not bool(re.search(r'[\.\,\;\:\!\?\-\_\(\)\[\]\{\}\<\>\"\'\`\~\@\#\$\%\^\&\*\+\=\/\\\|]{4,}', title))
    
    # Judul tidak boleh mengandung tag HTML
    no_html_tags = not bool(re.search(r'<[^>]*>', title))
    
    is_valid = title_length_valid and has_capitalized_word and no_excessive_punctuation and no_html_tags
    
    if not is_valid:
        if not has_capitalized_word:
            logger.warning(f"Judul tidak valid (tidak ada kata berawalan huruf kapital): {title}")
        if not no_excessive_punctuation:
            logger.warning(f"Judul tidak valid (terlalu banyak tanda baca berturut-turut): {title}")
        if not no_html_tags:
            logger.warning(f"Judul tidak valid (mengandung tag HTML): {title}")
    
    return is_valid

def fill_optional_fields(item: Dict[str, Any], is_jadwal: bool = False) -> Dict[str, Any]:
    """
    Mengisi field opsional yang kosong dengan data dummy.
    
    Args:
        item: Item yang akan diisi field opsionalnya
        is_jadwal: True jika item adalah bagian dari jadwal_rilis
        
    Returns:
        Dict[str, Any]: Item dengan field opsional yang telah diisi
    """
    # Buat salinan item untuk dimodifikasi
    filled_item = item.copy()
    
    if is_jadwal:
        # Field opsional untuk AnimeScheduleItem (jadwal_rilis)
        if "type" not in filled_item or not filled_item["type"]:
            filled_item["type"] = "TV"
        
        if "score" not in filled_item or not filled_item["score"]:
            filled_item["score"] = "N/A"
        
        if "genres" not in filled_item or not filled_item["genres"]:
            filled_item["genres"] = ["Anime"]
        
        if "release_time" not in filled_item or not filled_item["release_time"]:
            filled_item["release_time"] = "N/A"
    else:
        # Cek jenis item berdasarkan field yang ada
        if "episode" in item:
            # AnimeTerbaru (new_eps)
            if "episode" not in filled_item or not filled_item["episode"]:
                filled_item["episode"] = "N/A"
            
            if "rilis" not in filled_item or not filled_item["rilis"]:
                filled_item["rilis"] = "N/A"
        elif "tanggal" in item:
            # AnimeMovie (movies)
            if "tanggal" not in filled_item or not filled_item["tanggal"]:
                filled_item["tanggal"] = "N/A"
            
            if "genres" not in filled_item or not filled_item["genres"]:
                filled_item["genres"] = ["Anime"]
        else:
            # AnimeMingguan (top10)
            if "rating" not in filled_item or not filled_item["rating"]:
                filled_item["rating"] = "N/A"
            
            if "genres" not in filled_item or not filled_item["genres"]:
                filled_item["genres"] = ["Anime"]
    
    return filled_item

def validate_item(item: Dict[str, Any], is_jadwal: bool = False) -> Tuple[bool, Dict[str, Any]]:
    """
    Memvalidasi item anime (top10, new_eps, movies, jadwal_rilis).
    
    Args:
        item: Item yang akan divalidasi
        is_jadwal: True jika item adalah bagian dari jadwal_rilis
        
    Returns:
        Tuple[bool, Dict[str, Any]]: (is_valid, validated_item)
    """
    # Tentukan field yang akan divalidasi berdasarkan jenis item
    if is_jadwal:
        title_field = "title"
        cover_field = "cover_url"
    else:
        title_field = "judul"
        cover_field = "cover"
    
    # Log item untuk debugging
    logger.info(f"Validasi item: {item}")
    
    # Validasi judul
    title_valid = validate_title(item.get(title_field, ""))
    if not title_valid:
        logger.warning(f"Judul tidak valid: {item.get(title_field, '')}")
    
    # Validasi URL
    url_valid = validate_url(item.get("url", ""))
    if not url_valid:
        logger.warning(f"URL tidak valid: {item.get('url', '')}")
    
    # Validasi anime_slug
    slug_valid = validate_slug(item.get("anime_slug", ""))
    if not slug_valid:
        logger.warning(f"Slug tidak valid: {item.get('anime_slug', '')}")
    
    # Validasi cover/cover_url
    cover_valid = validate_image_url(item.get(cover_field, ""))
    if not cover_valid:
        logger.warning(f"Cover tidak valid: {item.get(cover_field, '')}")
    
    # Item valid jika semua field valid
    is_valid = title_valid and url_valid and slug_valid and cover_valid
    
    if is_valid:
        logger.info("Item valid")
        # Isi field opsional yang kosong dengan data dummy
        validated_item = fill_optional_fields(item, is_jadwal)
        return True, validated_item
    else:
        logger.warning("Item tidak valid")
        return False, {}

def check_url_cover_validity(data: Dict[str, Any]) -> bool:
    """
    Memeriksa validitas URL dan cover pada semua item.
    
    Args:
        data: Data yang akan diperiksa
        
    Returns:
        bool: True jika semua URL dan cover valid, False jika tidak
    """
    # Periksa URL dan cover pada top10
    if "top10" in data and isinstance(data["top10"], list):
        for item in data["top10"]:
            if not validate_url(item.get("url", "")):
                logger.error(f"URL tidak valid pada item top10: {item.get('url', '')}")
                return False
            if not validate_image_url(item.get("cover", "")):
                logger.error(f"Cover tidak valid pada item top10: {item.get('cover', '')}")
                return False
    
    # Periksa URL dan cover pada new_eps
    if "new_eps" in data and isinstance(data["new_eps"], list):
        for item in data["new_eps"]:
            if not validate_url(item.get("url", "")):
                logger.error(f"URL tidak valid pada item new_eps: {item.get('url', '')}")
                return False
            if not validate_image_url(item.get("cover", "")):
                logger.error(f"Cover tidak valid pada item new_eps: {item.get('cover', '')}")
                return False
    
    # Periksa URL dan cover pada movies
    if "movies" in data and isinstance(data["movies"], list):
        for item in data["movies"]:
            if not validate_url(item.get("url", "")):
                logger.error(f"URL tidak valid pada item movies: {item.get('url', '')}")
                return False
            if not validate_image_url(item.get("cover", "")):
                logger.error(f"Cover tidak valid pada item movies: {item.get('cover', '')}")
                return False
    
    # Periksa URL dan cover pada jadwal_rilis
    if "jadwal_rilis" in data and isinstance(data["jadwal_rilis"], dict):
        for day, items in data["jadwal_rilis"].items():
            if isinstance(items, list):
                for item in items:
                    if not validate_url(item.get("url", "")):
                        logger.error(f"URL tidak valid pada item jadwal {day}: {item.get('url', '')}")
                        return False
                    if not validate_image_url(item.get("cover_url", "")):
                        logger.error(f"Cover tidak valid pada item jadwal {day}: {item.get('cover_url', '')}")
                        return False
    
    return True

def validate_home_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Memvalidasi dan menyusun data JSON untuk endpoint home.
    
    Args:
        data: Data yang akan divalidasi
        
    Returns:
        Dict[str, Any]: Data yang telah divalidasi dengan confidence_score
    """
    logger.info("Memulai validasi data home")
    
    # Inisialisasi hasil dengan confidence_score default 0.0
    result = {
        "confidence_score": 0.0,
        "top10": [],
        "new_eps": [],
        "movies": [],
        "jadwal_rilis": {}
    }
    
    # Periksa validitas URL dan cover pada semua item
    # Jika ada URL atau cover yang tidak valid, langsung set confidence_score: 0.0
    if not check_url_cover_validity(data):
        logger.error("Ditemukan URL atau cover yang tidak valid, confidence_score: 0.0")
        return result
    
    # Validasi top10
    valid_top10 = []
    if "top10" in data and isinstance(data["top10"], list):
        logger.info(f"Validasi top10: {len(data['top10'])} item")
        for item in data["top10"]:
            is_valid, validated_item = validate_item(item)
            if is_valid:
                valid_top10.append(validated_item)
        logger.info(f"Top10 valid: {len(valid_top10)}/{len(data['top10'])}")
    else:
        logger.warning("Data top10 tidak ditemukan atau bukan list")
    
    # Validasi new_eps
    valid_new_eps = []
    if "new_eps" in data and isinstance(data["new_eps"], list):
        logger.info(f"Validasi new_eps: {len(data['new_eps'])} item")
        for item in data["new_eps"]:
            is_valid, validated_item = validate_item(item)
            if is_valid:
                valid_new_eps.append(validated_item)
        logger.info(f"New_eps valid: {len(valid_new_eps)}/{len(data['new_eps'])}")
    else:
        logger.warning("Data new_eps tidak ditemukan atau bukan list")
    
    # Validasi movies
    valid_movies = []
    if "movies" in data and isinstance(data["movies"], list):
        logger.info(f"Validasi movies: {len(data['movies'])} item")
        for item in data["movies"]:
            is_valid, validated_item = validate_item(item)
            if is_valid:
                valid_movies.append(validated_item)
        logger.info(f"Movies valid: {len(valid_movies)}/{len(data['movies'])}")
    else:
        logger.warning("Data movies tidak ditemukan atau bukan list")
    
    # Validasi jadwal_rilis
    valid_jadwal = {}
    if "jadwal_rilis" in data and isinstance(data["jadwal_rilis"], dict):
        logger.info(f"Validasi jadwal_rilis: {len(data['jadwal_rilis'])} hari")
        for day, items in data["jadwal_rilis"].items():
            valid_items = []
            if isinstance(items, list):
                logger.info(f"Validasi jadwal {day}: {len(items)} item")
                for item in items:
                    is_valid, validated_item = validate_item(item, is_jadwal=True)
                    if is_valid:
                        valid_items.append(validated_item)
                logger.info(f"Jadwal {day} valid: {len(valid_items)}/{len(items)}")
            if valid_items:
                valid_jadwal[day] = valid_items
    else:
        logger.warning("Data jadwal_rilis tidak ditemukan atau bukan dict")
    
    # Periksa apakah semua bagian memiliki minimal 1 item valid
    if (len(valid_top10) > 0 and
        len(valid_new_eps) > 0 and
        len(valid_movies) > 0 and
        len(valid_jadwal) > 0):
        logger.info("Semua bagian memiliki minimal 1 item valid")
        
        # Hitung confidence_score berdasarkan kelengkapan data
        total_items = len(data.get("top10", [])) + len(data.get("new_eps", [])) + len(data.get("movies", []))
        total_jadwal_items = sum(len(items) for items in data.get("jadwal_rilis", {}).values())
        
        valid_items = len(valid_top10) + len(valid_new_eps) + len(valid_movies)
        valid_jadwal_items = sum(len(items) for items in valid_jadwal.values())
        
        if total_items > 0 and total_jadwal_items > 0:
            item_score = valid_items / total_items
            jadwal_score = valid_jadwal_items / total_jadwal_items
            
            # Confidence score adalah rata-rata dari kedua skor, dengan minimal 0.8
            raw_score = (item_score + jadwal_score) / 2
            # Skala ulang skor ke rentang 0.8-1.0 jika semua bagian valid
            result["confidence_score"] = round(max(0.8, 0.8 + (raw_score * 0.2)), 2)
            logger.info(f"Confidence score: {result['confidence_score']}")
        
        # Update hasil dengan data yang valid
        result["top10"] = valid_top10
        result["new_eps"] = valid_new_eps
        result["movies"] = valid_movies
        result["jadwal_rilis"] = valid_jadwal
    else:
        logger.warning("Tidak semua bagian memiliki minimal 1 item valid")
        logger.warning(f"Top10 valid: {len(valid_top10)}")
        logger.warning(f"New_eps valid: {len(valid_new_eps)}")
        logger.warning(f"Movies valid: {len(valid_movies)}")
        logger.warning(f"Jadwal valid: {len(valid_jadwal)}")
    
    return result