import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Tambahkan path ke PYTHONPATH agar dapat mengimpor modul dari app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.utils.validator import validate_url, validate_image_url, validate_slug, validate_title, validate_item, validate_home_data

class TestHomeValidator(unittest.TestCase):
    def test_validate_url(self):
        # Test valid URLs
        self.assertTrue(validate_url("https://example.com"))
        self.assertTrue(validate_url("https://example.com/path"))
        self.assertTrue(validate_url("https://sub.example.com/path"))
        
        # Test invalid URLs
        self.assertFalse(validate_url(""))
        self.assertFalse(validate_url("N/A"))
        self.assertFalse(validate_url("-"))
        self.assertFalse(validate_url("example.com"))  # Missing https://
    
    def test_validate_image_url(self):
        # Test valid image URLs
        self.assertTrue(validate_image_url("https://example.com/image.jpg"))
        self.assertTrue(validate_image_url("https://example.com/image.jpeg"))
        self.assertTrue(validate_image_url("https://example.com/image.png"))
        self.assertTrue(validate_image_url("https://example.com/image.webp"))
        
        # Test invalid image URLs
        self.assertFalse(validate_image_url(""))
        self.assertFalse(validate_image_url("N/A"))
        self.assertFalse(validate_image_url("-"))
        self.assertFalse(validate_image_url("https://example.com/image"))  # Missing extension
        self.assertFalse(validate_image_url("example.com/image.jpg"))  # Missing https://
    
    def test_validate_slug(self):
        # Test valid slugs
        self.assertTrue(validate_slug("example"))
        self.assertTrue(validate_slug("example-slug"))
        self.assertTrue(validate_slug("example-slug-123"))
        
        # Test invalid slugs
        self.assertFalse(validate_slug(""))
        self.assertFalse(validate_slug("N/A"))
        self.assertFalse(validate_slug("-"))
        self.assertFalse(validate_slug("Example"))  # Contains uppercase
        self.assertFalse(validate_slug("example slug"))  # Contains space
        self.assertFalse(validate_slug("example_slug"))  # Contains underscore
    
    def test_validate_title(self):
        # Test valid titles
        self.assertTrue(validate_title("Example Title"))
        self.assertTrue(validate_title("Example"))
        self.assertTrue(validate_title("Example 123"))
        
        # Test invalid titles
        self.assertFalse(validate_title(""))
        self.assertFalse(validate_title("N/A"))
        self.assertFalse(validate_title("-"))
        self.assertFalse(validate_title("a"))  # Too short
        self.assertFalse(validate_title("example"))  # No uppercase
        self.assertFalse(validate_title("<div>Example</div>"))  # Contains HTML tags
    
    @patch('app.utils.validator.validate_title')
    @patch('app.utils.validator.validate_url')
    @patch('app.utils.validator.validate_slug')
    @patch('app.utils.validator.validate_image_url')
    def test_validate_item(self, mock_validate_image_url, mock_validate_slug, mock_validate_url, mock_validate_title):
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
        is_valid, validated_item = validate_item(item)
        self.assertTrue(is_valid)
        self.assertEqual(validated_item["judul"], "Example Title")
        self.assertEqual(validated_item["url"], "https://example.com")
        self.assertEqual(validated_item["anime_slug"], "example-slug")
        self.assertEqual(validated_item["cover"], "https://example.com/image.jpg")
        
        # Test invalid item (missing title)
        mock_validate_title.return_value = False
        is_valid, validated_item = validate_item(item)
        self.assertFalse(is_valid)
        
        # Reset mock
        mock_validate_title.return_value = True
        
        # Test invalid item (missing URL)
        mock_validate_url.return_value = False
        is_valid, validated_item = validate_item(item)
        self.assertFalse(is_valid)
        
        # Reset mock
        mock_validate_url.return_value = True
        
        # Test invalid item (missing slug)
        mock_validate_slug.return_value = False
        is_valid, validated_item = validate_item(item)
        self.assertFalse(is_valid)
        
        # Reset mock
        mock_validate_slug.return_value = True
        
        # Test invalid item (missing cover)
        mock_validate_image_url.return_value = False
        is_valid, validated_item = validate_item(item)
        self.assertFalse(is_valid)
    
    @patch('app.utils.validator.validate_item')
    def test_validate_home_data(self, mock_validate_item):
        # Setup mock
        mock_validate_item.return_value = (True, {"judul": "Example Title", "url": "https://example.com", "anime_slug": "example-slug", "cover": "https://example.com/image.jpg"})
        
        # Test valid data
        data = {
            "top10": [{"judul": "Example Title", "url": "https://example.com", "anime_slug": "example-slug", "cover": "https://example.com/image.jpg"}],
            "new_eps": [{"judul": "Example Title", "url": "https://example.com", "anime_slug": "example-slug", "cover": "https://example.com/image.jpg"}],
            "movies": [{"judul": "Example Title", "url": "https://example.com", "anime_slug": "example-slug", "cover": "https://example.com/image.jpg"}],
            "jadwal_rilis": {
                "Monday": [{"title": "Example Title", "url": "https://example.com", "anime_slug": "example-slug", "cover_url": "https://example.com/image.jpg"}]
            }
        }
        
        result = validate_home_data(data)
        self.assertGreaterEqual(result["confidence_score"], 0.8)
        self.assertEqual(len(result["top10"]), 1)
        self.assertEqual(len(result["new_eps"]), 1)
        self.assertEqual(len(result["movies"]), 1)
        self.assertEqual(len(result["jadwal_rilis"]), 1)
        
        # Test invalid data (missing top10)
        data = {
            "new_eps": [{"judul": "Example Title", "url": "https://example.com", "anime_slug": "example-slug", "cover": "https://example.com/image.jpg"}],
            "movies": [{"judul": "Example Title", "url": "https://example.com", "anime_slug": "example-slug", "cover": "https://example.com/image.jpg"}],
            "jadwal_rilis": {
                "Monday": [{"title": "Example Title", "url": "https://example.com", "anime_slug": "example-slug", "cover_url": "https://example.com/image.jpg"}]
            }
        }
        
        result = validate_home_data(data)
        self.assertEqual(result["confidence_score"], 0.0)
        
        # Test invalid data (empty top10)
        mock_validate_item.return_value = (False, {})
        
        data = {
            "top10": [{"judul": "Example Title", "url": "https://example.com", "anime_slug": "example-slug", "cover": "https://example.com/image.jpg"}],
            "new_eps": [{"judul": "Example Title", "url": "https://example.com", "anime_slug": "example-slug", "cover": "https://example.com/image.jpg"}],
            "movies": [{"judul": "Example Title", "url": "https://example.com", "anime_slug": "example-slug", "cover": "https://example.com/image.jpg"}],
            "jadwal_rilis": {
                "Monday": [{"title": "Example Title", "url": "https://example.com", "anime_slug": "example-slug", "cover_url": "https://example.com/image.jpg"}]
            }
        }
        
        result = validate_home_data(data)
        self.assertEqual(result["confidence_score"], 0.0)

if __name__ == '__main__':
    unittest.main()