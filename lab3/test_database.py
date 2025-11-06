import pytest
import tempfile
import os
import sqlite3
from database import DatabaseManager
from models import Artwork

class TestDatabaseAddition:
    
    def test_add_artwork_to_database(self):
        fd, db_path = tempfile.mkstemp(suffix='.db')
        try:
            os.close(fd)
            
            db = DatabaseManager(db_path)
            
            test_artwork = Artwork(
                id=None,
                title="Звездная ночь",
                artist="Винсент Ван Гог",
                year=1889,
                style="Постимпрессионизм",
                price=100000000.0,
                created_at=""
            )
            
            artwork_id = db.add_artwork(test_artwork)
            
            assert artwork_id is not None
            assert artwork_id > 0
            
            artworks = db.get_all_artworks()
            assert len(artworks) == 1
            
            saved_artwork = artworks[0]
            assert saved_artwork.id == artwork_id
            assert saved_artwork.title == test_artwork.title
            assert saved_artwork.artist == test_artwork.artist
            assert saved_artwork.year == test_artwork.year
            assert saved_artwork.style == test_artwork.style
            assert saved_artwork.price == test_artwork.price
            assert saved_artwork.created_at is not None
            
        finally:
            try:
                if os.path.exists(db_path):
                    os.unlink(db_path)
            except PermissionError:
                pass