import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Tambahkan path ke PYTHONPATH agar dapat mengimpor modul dari app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.utils.movie_validator import validate_movie_item, validate_movie_data

class TestMovieValidator(unittest.TestCase):
    @patch('app.utils.movie_validator.validate_title')
    @patch('app.utils.movie_validator.validate_url')
    @patch('app.utils.movie_validator.validate_slug')
    @patch('app.utils.movie_validator.validate_image_url')
    def test_validate_movie_item(self, mock_validate_image_url, mock_validate_slug, mock_validate_url, mock_validate_title):
        # Setup mocks
        mock_validate_title.return_value = True
        mock_validate_url.return_value = True
        mock_validate_slug.return_value = True
        mock_validate_image_url.return_value = True
        
        # Test valid item
        item = {
            "judul": "Example Title",
            "url": "https://example.com",
            "anime_slug": "example-slug",
            "cover": "https://example.com/image.jpg"
        }
        is_valid, validated_item = validate_movie_item(item)
        self.assertTrue(is_valid)
        self.assertEqual(validated_item["judul"], "Example Title")
        self.assertEqual(validated_item["url"], "https://example.com")
        self.assertEqual(validated_item["anime_slug"], "example-slug")
        self.assertEqual(validated_item["cover"], "https://example.com/image.jpg")
        
        # Verify optional fields are filled
        self.assertEqual(validated_item["tanggal"], "N/A")
        self.assertEqual(validated_item["genres"], ["Anime"])
        self.assertEqual(validated_item["status"], "N/A")
        self.assertEqual(validated_item["skor"], "N/A")
        self.assertEqual(validated_item["sinopsis"], "N/A")
        self.assertEqual(validated_item["views"], "N/A")
        
        # Test invalid item (missing title)
        mock_validate_title.return_value = False
        is_valid, validated_item = validate_movie_item(item)
        self.assertFalse(is_valid)
        
        # Reset mock
        mock_validate_title.return_value = True
        
        # Test invalid item (missing URL)
        mock_validate_url.return_value = False
        is_valid, validated_item = validate_movie_item(item)
        self.assertFalse(is_valid)
        
        # Reset mock
        mock_validate_url.return_value = True
        
        # Test invalid item (missing slug)
        mock_validate_slug.return_value = False
        is_valid, validated_item = validate_movie_item(item)
        self.assertFalse(is_valid)
        
        # Reset mock
        mock_validate_slug.return_value = True
        
        # Test invalid item (missing cover)
        mock_validate_image_url.return_value = False
        is_valid, validated_item = validate_movie_item(item)
        self.assertFalse(is_valid)
    
    @patch('app.utils.movie_validator.check_url_cover_validity')
    @patch('app.utils.movie_validator.validate_movie_item')
    def test_validate_movie_data(self, mock_validate_movie_item, mock_check_url_cover_validity):
        # Setup mocks
        mock_check_url_cover_validity.return_value = True
        mock_validate_movie_item.return_value = (True, {
            "judul": "Example Title",
            "url": "https://example.com",
            "anime_slug": "example-slug",
            "cover": "https://example.com/image.jpg",
            "tanggal": "N/A",
            "genres": ["Anime"],
            "status": "N/A",
            "skor": "N/A",
            "sinopsis": "N/A",
            "views": "N/A"
        })
        
        # Test valid data
        data = [
            {
                "judul": "Example Title",
                "url": "https://example.com",
                "anime_slug": "example-slug",
                "cover": "https://example.com/image.jpg"
            }
        ]
        
        result = validate_movie_data(data)
        self.assertGreaterEqual(result["confidence_score"], 0.8)
        self.assertEqual(len(result["data"]), 1)
        
        # Test invalid data (URL/cover not valid)
        mock_check_url_cover_validity.return_value = False
        
        result = validate_movie_data(data)
        self.assertEqual(result["confidence_score"], 0.0)
        self.assertEqual(len(result["data"]), 0)
        
        # Reset mock
        mock_check_url_cover_validity.return_value = True
        
        # Test invalid data (no valid items)
        mock_validate_movie_item.return_value = (False, {})
        
        result = validate_movie_data(data)
        self.assertEqual(result["confidence_score"], 0.0)
        self.assertEqual(len(result["data"]), 0)

if __name__ == '__main__':
    unittest.main()