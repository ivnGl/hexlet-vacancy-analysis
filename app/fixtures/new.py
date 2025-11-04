features = [
    PlanFeature.objects.get_or_create(name='Просмотр аналитики рынка')[0],
    PlanFeature.objects.get_or_create(name='Базовые отчеты')[0],
    PlanFeature.objects.get_or_create(name='50 запросов/месяц')[0],
    PlanFeature.objects.get_or_create(name='Доступ к вакансиям')[0],
    PlanFeature.objects.get_or_create(name='Email поддержка')[0],
    PlanFeature.objects.get_or_create(name='Все из Базового')[0],
    PlanFeature.objects.get_or_create(name='Безлимитные запросы')[0],
    PlanFeature.objects.get_or_create(name='Расширенная аналитика')[0],
    PlanFeature.objects.get_or_create(name='Персональные рекомендации')[0],
    PlanFeature.objects.get_or_create(name='Тота ИИ помощник')[0],
    PlanFeature.objects.get_or_create(name='Приоритетная поддержка')[0],
    PlanFeature.objects.get_or_create(name='Отчеты по карьерному росту')[0],
    PlanFeature.objects.get_or_create(name='Все из Профи')[0],
    PlanFeature.objects.get_or_create(name='AI карьерный консультант')[0],
    PlanFeature.objects.get_or_create(name='Индивидуальный план развития')[0],
    PlanFeature.objects.get_or_create(name='Прогноз зарплат')[0],
    PlanFeature.objects.get_or_create(name='Эксклюзивные вакансии')[0],
    PlanFeature.objects.get_or_create(name='Менторство от экспертов')[0],
    PlanFeature.objects.get_or_create(name='Приоритет в рекомендациях')[0],
    PlanFeature.objects.get_or_create(name='Персональный менеджер')[0],
]

basic = PricingPlan.objects.get_or_create(name='Базовый', price=0, period='навсегда', description='Для начинающих специалистов', order=1)[0]
basic.features.set(features[:5])

pro = PricingPlan.objects.get_or_create(name='Профи', price=490, description='Для активного поиска работы',order=2)[0]
pro.features.set(features[5:12])

premium = PricingPlan.objects.get_or_create(name='Премиум', price=990, description='Для профессионалов',order=3)[0]
premium.features.set(features[12:])