from rest_framework.serializers import ValidationError

def youtube_url_validator(value):
    """
    Проверяет, что ссылка на видео ведет на youtube.com.
    """
    if 'youtube.com' not in value.lower():
        raise ValidationError('Разрешены ссылки только на youtube.com')