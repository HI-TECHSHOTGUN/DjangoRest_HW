from rest_framework.exceptions import ValidationError


class YouTubeValidator:
    """Проверка, на ютуб ли ведет ссылка"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        url = value.get(self.field)

        if url and "youtube.com" not in url:
            raise ValidationError("Ссылка должна вести на youtube.com")
