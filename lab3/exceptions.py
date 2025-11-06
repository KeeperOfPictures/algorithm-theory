class ArtGalleryError(Exception):
    """Базовое исключение для галереи"""
    pass

class ValidationError(ArtGalleryError):
    """Ошибка валидации данных"""
    pass

class DatabaseError(ArtGalleryError):
    """Ошибка работы с базой данных"""
    pass