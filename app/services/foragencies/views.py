from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views import View
from inertia import render as inertia_render

from .models import AgencyPricingPlan, CompanyInquiry


class AgencyView(View):
    def get(self, request):
        plans = AgencyPricingPlan.objects.filter(is_active=True)
        props = {
            'plans': [
                {
                    'id': plan.id,
                    'name': plan.name,
                    'price': float(plan.price),
                    'currency': plan.currency,
                    'period': plan.period,
                    'description': plan.description,
                    'features': [
                        {'name': feature.name, 'description': feature.description}
                        for feature in plan.features.all()
                    ]
                }
                for plan in plans
            ]
        }
        return inertia_render(request, 'AgencyPricingPage', props)

    def post(self, request):
        data = request.POST or request.json()
        try:
            if not all(key in data for key in ['company_name', 'email']):
                raise ValidationError('Обязательные поля: company_name и email')
            if not data.get('email', '').count('@'):
                raise ValueError('Invalid email')

            CompanyInquiry.objects.create(
                company_name=data.get('company_name'),
                email=data.get('email'),
                phone=data.get('phone', ''),
                message=data.get('message', ''),
            )
            return JsonResponse({'success': True, 'message': 'Заявка отправлена'})

        except ValidationError as e:
            return JsonResponse(
                {'success': False, 'error': str(e)},
                status=400
            )
        except ValueError as e:
            return JsonResponse(
                {'success': False, 'error': f'Validation error: {str(e)}'},
                status=400
            )
        except Exception:
            return JsonResponse(
                {'success': False, 'error': 'Internal error'},
                status=500
            )