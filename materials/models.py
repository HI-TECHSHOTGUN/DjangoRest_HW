from django.db import models

# Create your models here.


class Course(models.Model):
    name = models.CharField(
        max_length=250,
        verbose_name="Название курса",
        help_text="Введите название курса",
    )
    preview = models.ImageField(
        upload_to="course_previews/",
        blank=True,
        null=True,
        verbose_name="Фото",
        help_text="Загрузите фото",
    )
    description = models.TextField(blank=True, null=True, verbose_name="Описание курса")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lessons(models.Model):
    name = models.CharField(
        max_length=250,
        verbose_name="Название урока",
        help_text="Введите название урока",
    )

    description = models.TextField(blank=True, null=True, verbose_name="Описание урока")

    preview = models.ImageField(
        upload_to="lesson_previews/",
        blank=True,
        null=True,
        verbose_name="Фото",
        help_text="Загрузите фото",
    )
    video_link = models.URLField(
        verbose_name="Ссылка на видео",
        blank=True,
        null=True,
    )

    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
