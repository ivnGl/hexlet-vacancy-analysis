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
    )

    class Meta:
        verbose_name = "Platform"
        verbose_name_plural = "Platforms"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Company(models.Model):
    name = models.CharField(
        max_length=150,
        db_index=True,
        validators=[MinLengthValidator(1)],
    )

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class City(models.Model):
    name = models.CharField(
        max_length=50,
        db_index=True,
        validators=[MinLengthValidator(1)],
    )

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"
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
    )
    company = models.ForeignKey(
        Company,
        related_name="vacancies",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_index=True,
    )
    city = models.ForeignKey(
        City,
        related_name="vacancies",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_index=True,
    )
    platform_vacancy_id = models.CharField(
        max_length=25,
        null=True,
        blank=True,
        db_index=True,
    )
    title = models.CharField(
        max_length=255,
        db_index=True,
        validators=[MinLengthValidator(1)],
    )
    url = models.URLField(
        unique=True,
        blank=True,
        null=True,
    )
    salary = models.CharField(
        max_length=120,
        blank=True,
        null=True,
    )
    experience = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )
    employment = models.CharField(
        max_length=40,
        blank=True,
        null=True,
    )
    work_format = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    schedule = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    skills = models.TextField(
        blank=True,
        null=True,
    )
    description = models.TextField(
        blank=True,
        null=True,
    )
    education = models.CharField(
        max_length=30,
        blank=True,
        null=True,
    )
    contacts = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    published_at = models.DateTimeField(
        db_index=True,
    )

    class Meta:
        verbose_name = "Vacancy"
        verbose_name_plural = "Vacancies"
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
