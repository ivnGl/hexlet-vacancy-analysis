from django.core.validators import MinLengthValidator
from django.db import models


class Platform(models.Model):
    HH = "HeadHunter"
    SUPER_JOB = "SuperJob"
    TELEGRAM = "Telegram"

    PLATFORM_NAME_CHOICES = [
        (HH, "HeadHunter"),
        (SUPER_JOB, "SuperJob"),
        (TELEGRAM, "Telegram"),
    ]

    name = models.CharField(
        max_length=50,
        choices=PLATFORM_NAME_CHOICES,
        unique=True,
        db_index=True,
        verbose_name="Платформа",
    )

    class Meta:
        verbose_name = "Платформа"
        verbose_name_plural = "Платформы"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Company(models.Model):
    name = models.CharField(
        max_length=150,
        db_index=True,
        validators=[MinLengthValidator(1)],
        verbose_name="Компания"
    )

    class Meta:
        verbose_name = "Компания"
        verbose_name_plural = "Компании"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class City(models.Model):
    name = models.CharField(
        max_length=50,
        db_index=True,
        validators=[MinLengthValidator(1)],
        verbose_name="Город",
    )

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Vacancy(models.Model):
    platform = models.ForeignKey(
        Platform,
        related_name="vacancies",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_index=True,
        verbose_name="Платформа",
    )
    company = models.ForeignKey(
        Company,
        related_name="vacancies",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_index=True,
        verbose_name="Компания",
    )
    city = models.ForeignKey(
        City,
        related_name="vacancies",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_index=True,
        verbose_name="Город",
    )
    platform_vacancy_id = models.CharField(
        max_length=25,
        null=True,
        blank=True,
        db_index=True,
        verbose_name="Идентификатор вакансии на платформе",
    )
    title = models.CharField(
        max_length=255,
        db_index=True,
        validators=[MinLengthValidator(1)],
        verbose_name="Заголовок",
    )
    url = models.URLField(
        unique=True,
        blank=True,
        null=True,
        verbose_name="Cсылка",
    )
    salary = models.CharField(
        max_length=120,
        blank=True,
        null=True,
        verbose_name="Зарплата",
    )
    experience = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Опыт работы",
    )
    employment = models.CharField(
        max_length=40,
        blank=True,
        null=True,
        verbose_name="Занятость",
    )
    work_format = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Формат работы",
    )
    schedule = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Расписание",
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Адрес",
    )
    skills = models.TextField(
        blank=True,
        null=True,
        verbose_name="Навыки",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание",
    )
    education = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name="Образование",
    )
    contacts = models.CharField(
        max_length=250,
        blank=True,
        null=True,
        verbose_name="Контакты",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создано",
    )
    published_at = models.DateTimeField(
        db_index=True,
        verbose_name="Опубликовано",
    )

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"
        ordering = ["-published_at"]
        indexes = [
            models.Index(fields=["-published_at", "platform"]),
            models.Index(fields=["title", "company"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["platform_vacancy_id"],
                name="unique_platform_vacancy_id",
                condition=models.Q(
                    platform__isnull=False, platform_vacancy_id__isnull=False
                ),
            ),
        ]

    def __str__(self) -> str:
        company_name = self.company.name if self.company else "Неизвестная компания"
        return f"{self.title} в {company_name}"
