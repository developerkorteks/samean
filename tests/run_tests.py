import unittest
import sys
import os

# Tambahkan path ke PYTHONPATH agar dapat mengimpor modul dari app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import semua test
from tests.test_home_validator import TestHomeValidator
from tests.test_jadwal_validator import TestJadwalValidator
from tests.test_movie_validator import TestMovieValidator
from tests.test_anime_terbaru_validator import TestAnimeTerbaruValidator
from tests.test_anime_detail_validator import TestAnimeDetailValidator
from tests.test_episode_detail_validator import TestEpisodeDetailValidator

def run_tests():
    # Buat test suite
    test_suite = unittest.TestSuite()
    
    # Tambahkan semua test ke test suite
    test_suite.addTest(unittest.makeSuite(TestHomeValidator))
    test_suite.addTest(unittest.makeSuite(TestJadwalValidator))
    test_suite.addTest(unittest.makeSuite(TestMovieValidator))
    test_suite.addTest(unittest.makeSuite(TestAnimeTerbaruValidator))
    test_suite.addTest(unittest.makeSuite(TestAnimeDetailValidator))
    test_suite.addTest(unittest.makeSuite(TestEpisodeDetailValidator))
    
    # Jalankan test
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(run_tests())