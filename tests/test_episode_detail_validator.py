import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Tambahkan path ke PYTHONPATH agar dapat mengimpor modul dari app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.utils.episode_detail_validator import validate_streaming_server, validate_episode_detail

class TestEpisodeDetailValidator(unittest.TestCase):
    def test_validate_streaming_server(self):
        # Test valid streaming server
        server = {
            "server_name": "Example Server",
            "streaming_url": "https://example.com/stream/1"
        }
        
        with patch('app.utils.episode_detail_validator.validate_url', return_value=True):
            self.assertTrue(validate_streaming_server(server))
        
        # Test invalid streaming server (missing server_name)
        server = {
            "streaming_url": "https://example.com/stream/1"
        }
        
        with patch('app.utils.episode_detail_validator.validate_url', return_value=True):
            self.assertFalse(validate_streaming_server(server))
        
        # Test invalid streaming server (invalid streaming_url)
        server = {
            "server_name": "Example Server",
            "streaming_url": "https://example.com/stream/1"
        }
        
        with patch('app.utils.episode_detail_validator.validate_url', return_value=False):
            self.assertFalse(validate_streaming_server(server))
    
    def test_validate_episode_detail(self):
        # Test valid episode detail
        episode_detail = {
            "title": "Example Episode",
            "thumbnail_url": "https://example.com/image.jpg",
            "streaming_servers": [
                {
                    "server_name": "Example Server",
                    "streaming_url": "https://example.com/stream/1"
                }
            ],
            "release_info": "Released on 2025-08-01",
            "download_links": {
                "480p": {
                    "GDrive": [
                        {
                            "provider": "GDrive",
                            "url": "https://example.com/download/1"
                        }
                    ]
                }
            },
            "navigation": {
                "previous_episode_url": "https://example.com/episode/0",
                "next_episode_url": "https://example.com/episode/2",
                "all_episodes_url": "https://example.com/anime/example"
            },
            "anime_info": {
                "title": "Example Anime",
                "thumbnail_url": "https://example.com/image2.jpg"
            },
            "other_episodes": [
                {
                    "title": "Example Episode 2",
                    "url": "https://example.com/episode/2",
                    "thumbnail_url": "https://example.com/image3.jpg",
                    "release_date": "2025-08-02"
                }
            ]
        }
        
        with patch('app.utils.episode_detail_validator.validate_title', return_value=True), \
             patch('app.utils.episode_detail_validator.validate_image_url', return_value=True), \
             patch('app.utils.episode_detail_validator.validate_streaming_server', return_value=True), \
             patch('app.utils.episode_detail_validator.fill_optional_streaming_server_fields', return_value={"server_name": "Example Server", "streaming_url": "https://example.com/stream/1"}):
            
            result = validate_episode_detail(episode_detail)
            self.assertEqual(result["confidence_score"], 1.0)
            self.assertEqual(result["title"], "Example Episode")
            self.assertEqual(result["thumbnail_url"], "https://example.com/image.jpg")
            self.assertEqual(len(result["streaming_servers"]), 1)
            self.assertEqual(result["release_info"], "Released on 2025-08-01")
            self.assertEqual(len(result["download_links"]), 1)
            self.assertEqual(result["navigation"]["previous_episode_url"], "https://example.com/episode/0")
            self.assertEqual(result["navigation"]["next_episode_url"], "https://example.com/episode/2")
            self.assertEqual(result["navigation"]["all_episodes_url"], "https://example.com/anime/example")
            self.assertEqual(result["anime_info"]["title"], "Example Anime")
            self.assertEqual(result["anime_info"]["thumbnail_url"], "https://example.com/image2.jpg")
            self.assertEqual(len(result["other_episodes"]), 1)
        
        # Test invalid episode detail (invalid title)
        with patch('app.utils.episode_detail_validator.validate_title', return_value=False), \
             patch('app.utils.episode_detail_validator.validate_image_url', return_value=True), \
             patch('app.utils.episode_detail_validator.validate_streaming_server', return_value=True):
            
            result = validate_episode_detail(episode_detail)
            self.assertEqual(result["confidence_score"], 0.0)
        
        # Test invalid episode detail (invalid thumbnail_url)
        with patch('app.utils.episode_detail_validator.validate_title', return_value=True), \
             patch('app.utils.episode_detail_validator.validate_image_url', return_value=False), \
             patch('app.utils.episode_detail_validator.validate_streaming_server', return_value=True):
            
            result = validate_episode_detail(episode_detail)
            self.assertEqual(result["confidence_score"], 0.0)
        
        # Test invalid episode detail (no valid streaming servers)
        with patch('app.utils.episode_detail_validator.validate_title', return_value=True), \
             patch('app.utils.episode_detail_validator.validate_image_url', return_value=True), \
             patch('app.utils.episode_detail_validator.validate_streaming_server', return_value=False):
            
            result = validate_episode_detail(episode_detail)
            self.assertEqual(result["confidence_score"], 0.0)
        
        # Test valid episode detail with thumbnail_url in anime_info
        episode_detail = {
            "title": "Example Episode",
            "streaming_servers": [
                {
                    "server_name": "Example Server",
                    "streaming_url": "https://example.com/stream/1"
                }
            ],
            "anime_info": {
                "title": "Example Anime",
                "thumbnail_url": "https://example.com/image2.jpg"
            }
        }
        
        with patch('app.utils.episode_detail_validator.validate_title', return_value=True), \
             patch('app.utils.episode_detail_validator.validate_image_url', side_effect=[False, True]), \
             patch('app.utils.episode_detail_validator.validate_streaming_server', return_value=True), \
             patch('app.utils.episode_detail_validator.fill_optional_streaming_server_fields', return_value={"server_name": "Example Server", "streaming_url": "https://example.com/stream/1"}):
            
            result = validate_episode_detail(episode_detail)
            self.assertEqual(result["confidence_score"], 1.0)
            self.assertEqual(result["title"], "Example Episode")
            self.assertEqual(result["thumbnail_url"], "https://example.com/image2.jpg")
            self.assertEqual(len(result["streaming_servers"]), 1)

if __name__ == '__main__':
    unittest.main()