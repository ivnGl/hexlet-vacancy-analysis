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
        help_text="Name of the job search platform",
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
        help_text="Company name",
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
        help_text="City name",
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
        help_text="Platform where the vacancy was posted",
    )
    company = models.ForeignKey(
        Company,
        related_name="vacancies",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_index=True,
        help_text="Company offering the position",
    )
    city = models.ForeignKey(
        City,
        related_name="vacancies",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_index=True,
        help_text="City where the position is located",
    )
    platform_vacancy_id = models.CharField(
        max_length=25,
        null=True,
        blank=True,
        db_index=True,
        help_text="Unique identifier from the source platform",
    )
    title = models.CharField(
        max_length=255,
        db_index=True,
        help_text="Job title",
        validators=[MinLengthValidator(1)],
    )
    url = models.URLField(
        unique=True,
        blank=True,
        null=True,
        help_text="URL to the original vacancy posting",
    )
    salary = models.CharField(
        max_length=120,
        blank=True,
        null=True,
        help_text="Salary information",
    )
    experience = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Required experience level",
    )
    employment = models.CharField(
        max_length=40,
        blank=True,
        null=True,
        help_text="Employment type (full-time, part-time, etc.)",
    )
    work_format = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Work format (remote, office, hybrid, etc.)",
    )
    schedule = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Work schedule",
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Physical address of the workplace",
    )
    skills = models.TextField(
        blank=True,
        null=True,
        help_text="Required skills and qualifications",
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Detailed job description",
    )
    education = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        help_text="Required education level",
    )
    contacts = models.CharField(
        max_length=250,
        blank=True,
        null=True,
        help_text="Contact information",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the vacancy was added to the system",
    )
    published_at = models.DateTimeField(
        db_index=True,
        help_text="When the vacancy was published on the source platform",
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
