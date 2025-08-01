import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Tambahkan path ke PYTHONPATH agar dapat mengimpor modul dari app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.utils.jadwal_validator import validate_schedule_item, validate_jadwal_data, validate_jadwal_all_data

class TestJadwalValidator(unittest.TestCase):
    @patch('app.utils.jadwal_validator.validate_title')
    @patch('app.utils.jadwal_validator.validate_url')
    @patch('app.utils.jadwal_validator.validate_slug')
    @patch('app.utils.jadwal_validator.validate_image_url')
    def test_validate_schedule_item(self, mock_validate_image_url, mock_validate_slug, mock_validate_url, mock_validate_title):
        # Setup mocks
        mock_validate_title.return_value = True
        mock_validate_url.return_value = True
        mock_validate_slug.return_value = True
        mock_validate_image_url.return_value = True
        
        # Test valid item
        item = {
            "title": "Example Title",
            "url": "https://example.com",
            "anime_slug": "example-slug",
            "cover_url": "https://example.com/image.jpg"
        }
        is_valid, validated_item = validate_schedule_item(item)
        self.assertTrue(is_valid)
        self.assertEqual(validated_item["title"], "Example Title")
        self.assertEqual(validated_item["url"], "https://example.com")
        self.assertEqual(validated_item["anime_slug"], "example-slug")
        self.assertEqual(validated_item["cover_url"], "https://example.com/image.jpg")
        
        # Verify optional fields are filled
        self.assertEqual(validated_item["type"], "TV")
        self.assertEqual(validated_item["score"], "N/A")
        self.assertEqual(validated_item["genres"], ["Anime"])
        self.assertEqual(validated_item["release_time"], "N/A")
        
        # Test invalid item (missing title)
        mock_validate_title.return_value = False
        is_valid, validated_item = validate_schedule_item(item)
        self.assertFalse(is_valid)
        
        # Reset mock
        mock_validate_title.return_value = True
        
        # Test invalid item (missing URL)
        mock_validate_url.return_value = False
        is_valid, validated_item = validate_schedule_item(item)
        self.assertFalse(is_valid)
        
        # Reset mock
        mock_validate_url.return_value = True
        
        # Test invalid item (missing slug)
        mock_validate_slug.return_value = False
        is_valid, validated_item = validate_schedule_item(item)
        self.assertFalse(is_valid)
        
        # Reset mock
        mock_validate_slug.return_value = True
        
        # Test invalid item (missing cover)
        mock_validate_image_url.return_value = False
        is_valid, validated_item = validate_schedule_item(item)
        self.assertFalse(is_valid)
        
        # Reset all mocks for next test
        mock_validate_title.reset_mock()
        mock_validate_url.reset_mock()
        mock_validate_slug.reset_mock()
        mock_validate_image_url.reset_mock()
    
    @patch('app.utils.jadwal_validator.check_url_cover_validity')
    @patch('app.utils.jadwal_validator.validate_schedule_item')
    def test_validate_jadwal_data(self, mock_validate_schedule_item, mock_check_url_cover_validity):
        # Setup mocks
        mock_check_url_cover_validity.return_value = True
        mock_validate_schedule_item.return_value = (True, {
            "title": "Example Title",
            "url": "https://example.com",
            "anime_slug": "example-slug",
            "cover_url": "https://example.com/image.jpg",
            "type": "TV",
            "score": "N/A",
            "genres": ["Anime"],
            "release_time": "N/A"
        })
        
        # Test valid data
        data = [
            {
                "title": "Example Title",
                "url": "https://example.com",
                "anime_slug": "example-slug",
                "cover_url": "https://example.com/image.jpg"
            }
        ]
        
        result = validate_jadwal_data(data)
        self.assertGreaterEqual(result["confidence_score"], 0.8)
        self.assertEqual(len(result["data"]), 1)
        
        # Test invalid data (URL/cover not valid)
        mock_check_url_cover_validity.return_value = False
        
        result = validate_jadwal_data(data)
        self.assertEqual(result["confidence_score"], 0.0)
        self.assertEqual(len(result["data"]), 0)
        
        # Reset mock
        mock_check_url_cover_validity.return_value = True
        
        # Test invalid data (no valid items)
        mock_validate_schedule_item.return_value = (False, {})
        
        result = validate_jadwal_data(data)
        self.assertEqual(result["confidence_score"], 0.0)
        self.assertEqual(len(result["data"]), 0)
    
    @patch('app.utils.jadwal_validator.check_url_cover_validity')
    @patch('app.utils.jadwal_validator.validate_schedule_item')
    def test_validate_jadwal_all_data(self, mock_validate_schedule_item, mock_check_url_cover_validity):
        # Setup mocks
        mock_check_url_cover_validity.return_value = True
        mock_validate_schedule_item.return_value = (True, {
            "title": "Example Title",
            "url": "https://example.com",
            "anime_slug": "example-slug",
            "cover_url": "https://example.com/image.jpg",
            "type": "TV",
            "score": "N/A",
            "genres": ["Anime"],
            "release_time": "N/A"
        })
        
        # Test valid data
        data = {
            "Monday": [
                {
                    "title": "Example Title",
                    "url": "https://example.com",
                    "anime_slug": "example-slug",
                    "cover_url": "https://example.com/image.jpg"
                }
            ],
            "Tuesday": [
                {
                    "title": "Example Title",
                    "url": "https://example.com",
                    "anime_slug": "example-slug",
                    "cover_url": "https://example.com/image.jpg"
                }
            ]
        }
        
        result = validate_jadwal_all_data(data)
        self.assertGreaterEqual(result["confidence_score"], 0.8)
        self.assertEqual(len(result["Monday"]), 1)
        self.assertEqual(len(result["Tuesday"]), 1)
        
        # Test invalid data (URL/cover not valid)
        mock_check_url_cover_validity.return_value = False
        
        result = validate_jadwal_all_data(data)
        self.assertEqual(result["confidence_score"], 0.0)
        
        # Reset mock
        mock_check_url_cover_validity.return_value = True
        
        # Test invalid data (no valid items)
        mock_validate_schedule_item.return_value = (False, {})
        
        result = validate_jadwal_all_data(data)
        self.assertEqual(result["confidence_score"], 0.0)

if __name__ == '__main__':
    unittest.main()