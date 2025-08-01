import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Tambahkan path ke PYTHONPATH agar dapat mengimpor modul dari app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.utils.anime_detail_validator import validate_episode_item, validate_recommendation_item, validate_anime_detail

class TestAnimeDetailValidator(unittest.TestCase):
    def test_validate_episode_item(self):
        # Test valid episode item
        episode = {
            "episode": "1",
            "title": "Example Episode",
            "url": "https://example.com/episode/1",
            "episode_slug": "example-episode-1"
        }
        
        with patch('app.utils.anime_detail_validator.validate_title', return_value=True), \
             patch('app.utils.anime_detail_validator.validate_url', return_value=True), \
             patch('app.utils.anime_detail_validator.validate_slug', return_value=True):
            self.assertTrue(validate_episode_item(episode))
        
        # Test invalid episode item (missing episode)
        episode = {
            "title": "Example Episode",
            "url": "https://example.com/episode/1",
            "episode_slug": "example-episode-1"
        }
        
        with patch('app.utils.anime_detail_validator.validate_title', return_value=True), \
             patch('app.utils.anime_detail_validator.validate_url', return_value=True), \
             patch('app.utils.anime_detail_validator.validate_slug', return_value=True):
            self.assertFalse(validate_episode_item(episode))
        
        # Test invalid episode item (invalid title)
        episode = {
            "episode": "1",
            "title": "Example Episode",
            "url": "https://example.com/episode/1",
            "episode_slug": "example-episode-1"
        }
        
        with patch('app.utils.anime_detail_validator.validate_title', return_value=False), \
             patch('app.utils.anime_detail_validator.validate_url', return_value=True), \
             patch('app.utils.anime_detail_validator.validate_slug', return_value=True):
            self.assertFalse(validate_episode_item(episode))
        
        # Test invalid episode item (invalid URL)
        episode = {
            "episode": "1",
            "title": "Example Episode",
            "url": "https://example.com/episode/1",
            "episode_slug": "example-episode-1"
        }
        
        with patch('app.utils.anime_detail_validator.validate_title', return_value=True), \
             patch('app.utils.anime_detail_validator.validate_url', return_value=False), \
             patch('app.utils.anime_detail_validator.validate_slug', return_value=True):
            self.assertFalse(validate_episode_item(episode))
        
        # Test invalid episode item (invalid slug)
        episode = {
            "episode": "1",
            "title": "Example Episode",
            "url": "https://example.com/episode/1",
            "episode_slug": "example-episode-1"
        }
        
        with patch('app.utils.anime_detail_validator.validate_title', return_value=True), \
             patch('app.utils.anime_detail_validator.validate_url', return_value=True), \
             patch('app.utils.anime_detail_validator.validate_slug', return_value=False):
            self.assertFalse(validate_episode_item(episode))
    
    def test_validate_recommendation_item(self):
        # Test valid recommendation item
        recommendation = {
            "title": "Example Recommendation",
            "url": "https://example.com/anime/example",
            "anime_slug": "example",
            "cover_url": "https://example.com/image.jpg"
        }
        
        with patch('app.utils.anime_detail_validator.validate_title', return_value=True), \
             patch('app.utils.anime_detail_validator.validate_url', return_value=True), \
             patch('app.utils.anime_detail_validator.validate_slug', return_value=True), \
             patch('app.utils.anime_detail_validator.validate_image_url', return_value=True):
            self.assertTrue(validate_recommendation_item(recommendation))
        
        # Test invalid recommendation item (invalid title)
        recommendation = {
            "title": "Example Recommendation",
            "url": "https://example.com/anime/example",
            "anime_slug": "example",
            "cover_url": "https://example.com/image.jpg"
        }
        
        with patch('app.utils.anime_detail_validator.validate_title', return_value=False), \
             patch('app.utils.anime_detail_validator.validate_url', return_value=True), \
             patch('app.utils.anime_detail_validator.validate_slug', return_value=True), \
             patch('app.utils.anime_detail_validator.validate_image_url', return_value=True):
            self.assertFalse(validate_recommendation_item(recommendation))
        
        # Test invalid recommendation item (invalid URL)
        recommendation = {
            "title": "Example Recommendation",
            "url": "https://example.com/anime/example",
            "anime_slug": "example",
            "cover_url": "https://example.com/image.jpg"
        }
        
        with patch('app.utils.anime_detail_validator.validate_title', return_value=True), \
             patch('app.utils.anime_detail_validator.validate_url', return_value=False), \
             patch('app.utils.anime_detail_validator.validate_slug', return_value=True), \
             patch('app.utils.anime_detail_validator.validate_image_url', return_value=True):
            self.assertFalse(validate_recommendation_item(recommendation))
        
        # Test invalid recommendation item (invalid slug)
        recommendation = {
            "title": "Example Recommendation",
            "url": "https://example.com/anime/example",
            "anime_slug": "example",
            "cover_url": "https://example.com/image.jpg"
        }
        
        with patch('app.utils.anime_detail_validator.validate_title', return_value=True), \
             patch('app.utils.anime_detail_validator.validate_url', return_value=True), \
             patch('app.utils.anime_detail_validator.validate_slug', return_value=False), \
             patch('app.utils.anime_detail_validator.validate_image_url', return_value=True):
            self.assertFalse(validate_recommendation_item(recommendation))
        
        # Test invalid recommendation item (invalid cover_url)
        recommendation = {
            "title": "Example Recommendation",
            "url": "https://example.com/anime/example",
            "anime_slug": "example",
            "cover_url": "https://example.com/image.jpg"
        }
        
        with patch('app.utils.anime_detail_validator.validate_title', return_value=True), \
             patch('app.utils.anime_detail_validator.validate_url', return_value=True), \
             patch('app.utils.anime_detail_validator.validate_slug', return_value=True), \
             patch('app.utils.anime_detail_validator.validate_image_url', return_value=False):
            self.assertFalse(validate_recommendation_item(recommendation))
    
    def test_validate_anime_detail(self):
        # Test valid anime detail
        anime_detail = {
            "judul": "Example Anime",
            "url_anime": "https://example.com/anime/example",
            "anime_slug": "example",
            "url_cover": "https://example.com/image.jpg",
            "episode_list": [
                {
                    "episode": "1",
                    "title": "Example Episode",
                    "url": "https://example.com/episode/1",
                    "episode_slug": "example-episode-1"
                }
            ],
            "recommendations": [
                {
                    "title": "Example Recommendation",
                    "url": "https://example.com/anime/recommendation",
                    "anime_slug": "recommendation",
                    "cover_url": "https://example.com/image2.jpg"
                }
            ]
        }
        
        with patch('app.utils.anime_detail_validator.validate_title', return_value=True), \
             patch('app.utils.anime_detail_validator.validate_url', return_value=True), \
             patch('app.utils.anime_detail_validator.validate_slug', return_value=True), \
             patch('app.utils.anime_detail_validator.validate_image_url', return_value=True), \
             patch('app.utils.anime_detail_validator.validate_episode_item', return_value=True), \
             patch('app.utils.anime_detail_validator.validate_recommendation_item', return_value=True), \
             patch('app.utils.anime_detail_validator.fill_optional_episode_fields', return_value={"episode": "1", "title": "Example Episode", "url": "https://example.com/episode/1", "episode_slug": "example-episode-1", "release_date": "N/A"}), \
             patch('app.utils.anime_detail_validator.fill_optional_recommendation_fields', return_value={"title": "Example Recommendation", "url": "https://example.com/anime/recommendation", "anime_slug": "recommendation", "cover_url": "https://example.com/image2.jpg", "rating": "N/A", "episode": "N/A"}):
            
            result = validate_anime_detail(anime_detail)
            self.assertEqual(result["confidence_score"], 1.0)
            self.assertEqual(result["judul"], "Example Anime")
            self.assertEqual(result["url_anime"], "https://example.com/anime/example")
            self.assertEqual(result["anime_slug"], "example")
            self.assertEqual(result["url_cover"], "https://example.com/image.jpg")
            self.assertEqual(len(result["episode_list"]), 1)
            self.assertEqual(len(result["recommendations"]), 1)
        
        # Test invalid anime detail (invalid judul)
        with patch('app.utils.anime_detail_validator.validate_title', return_value=False), \
             patch('app.utils.anime_detail_validator.validate_url', return_value=True), \
             patch('app.utils.anime_detail_validator.validate_slug', return_value=True), \
             patch('app.utils.anime_detail_validator.validate_image_url', return_value=True):
            
            result = validate_anime_detail(anime_detail)
            self.assertEqual(result["confidence_score"], 0.0)
        
        # Test invalid anime detail (invalid url_anime)
        with patch('app.utils.anime_detail_validator.validate_title', return_value=True), \
             patch('app.utils.anime_detail_validator.validate_url', return_value=False), \
             patch('app.utils.anime_detail_validator.validate_slug', return_value=True), \
             patch('app.utils.anime_detail_validator.validate_image_url', return_value=True):
            
            result = validate_anime_detail(anime_detail)
            self.assertEqual(result["confidence_score"], 0.0)
        
        # Test invalid anime detail (invalid anime_slug)
        with patch('app.utils.anime_detail_validator.validate_title', return_value=True), \
             patch('app.utils.anime_detail_validator.validate_url', return_value=True), \
             patch('app.utils.anime_detail_validator.validate_slug', return_value=False), \
             patch('app.utils.anime_detail_validator.validate_image_url', return_value=True):
            
            result = validate_anime_detail(anime_detail)
            self.assertEqual(result["confidence_score"], 0.0)
        
        # Test invalid anime detail (invalid url_cover)
        with patch('app.utils.anime_detail_validator.validate_title', return_value=True), \
             patch('app.utils.anime_detail_validator.validate_url', return_value=True), \
             patch('app.utils.anime_detail_validator.validate_slug', return_value=True), \
             patch('app.utils.anime_detail_validator.validate_image_url', return_value=False):
            
            result = validate_anime_detail(anime_detail)
            self.assertEqual(result["confidence_score"], 0.0)
        
        # Test invalid anime detail (no valid episodes)
        with patch('app.utils.anime_detail_validator.validate_title', return_value=True), \
             patch('app.utils.anime_detail_validator.validate_url', return_value=True), \
             patch('app.utils.anime_detail_validator.validate_slug', return_value=True), \
             patch('app.utils.anime_detail_validator.validate_image_url', return_value=True), \
             patch('app.utils.anime_detail_validator.validate_episode_item', return_value=False):
            
            result = validate_anime_detail(anime_detail)
            self.assertEqual(result["confidence_score"], 0.0)

if __name__ == '__main__':
    unittest.main()