from datetime import date

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from applications.models import Application
from companies.models import Company
from opportunities.models import Opportunity

from .models import Profile


class AuthViewsTests(TestCase):
    def test_login_page_loads(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)

    def test_register_page_loads(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)

    def test_student_profile_page_contains_form_fields_for_logged_in_user(self):
        User = get_user_model()
        user = User.objects.create_user(username='studentuser', password='secret123')
        self.client.login(username='studentuser', password='secret123')

        response = self.client.get(reverse('student_profile'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Student ID')
        self.assertContains(response, 'University')

    def test_company_profile_page_contains_form_fields_for_logged_in_user(self):
        User = get_user_model()
        user = User.objects.create_user(username='companyuser', password='secret123')
        Profile.objects.filter(user=user).update(role='Company')
        self.client.login(username='companyuser', password='secret123')

        response = self.client.get(reverse('company_profile'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id_company_name')
        self.assertContains(response, 'id_address')

    def test_student_can_open_own_profile_and_opportunities(self):
        User = get_user_model()
        user = User.objects.create_user(username='flowstudent', password='secret123')
        self.client.login(username='flowstudent', password='secret123')

        profile_response = self.client.get(reverse('student_profile'))
        opportunities_response = self.client.get(reverse('opportunity_list'))

        self.assertEqual(profile_response.status_code, 200)
        self.assertEqual(opportunities_response.status_code, 200)

    def test_company_cannot_open_student_profile(self):
        User = get_user_model()
        user = User.objects.create_user(username='flowcompany', password='secret123')
        Profile.objects.filter(user=user).update(role='Company')
        self.client.login(username='flowcompany', password='secret123')

        response = self.client.get(reverse('student_profile'))

        self.assertEqual(response.status_code, 403)

    def test_student_profile_save_redirects_to_opportunities_and_can_apply(self):
        User = get_user_model()
        company_user = User.objects.create_user(
            username='flowjobcompany',
            password='secret123',
        )
        Profile.objects.filter(user=company_user).update(role='Company')
        company = Company.objects.create(
            user=company_user,
            company_name='Flow Jobs Ltd',
            phone='555-0100',
            email='jobs@example.com',
            address='123 Main Street',
        )
        opportunity = Opportunity.objects.create(
            company=company,
            title='Django Intern',
            description='Build useful web features.',
            opportunity_type='Internship',
            category='IT',
            location='Remote',
            requirements='Python basics',
            deadline=date(2027, 1, 1),
        )

        student_user = User.objects.create_user(
            username='flowjobstudent',
            password='secret123',
        )
        self.client.login(username='flowjobstudent', password='secret123')

        profile_response = self.client.post(reverse('student_profile'), {
            'student_id': 'FLOW-001',
            'phone': '555-0101',
            'university': 'Example University',
            'program': 'Computer Science',
            'year_of_study': 3,
            'skills': 'Python, Django',
            'bio': 'Student developer',
        })

        self.assertRedirects(profile_response, reverse('opportunity_list'))
        self.assertContains(self.client.get(reverse('opportunity_list')), opportunity.title)

        application_response = self.client.post(
            reverse('application_create') + f'?opportunity={opportunity.pk}',
            {
                'opportunity': opportunity.pk,
                'cover_letter': 'I would like to apply.',
                'cv': SimpleUploadedFile(
                    'resume.pdf',
                    b'%PDF-1.4 student resume',
                    content_type='application/pdf',
                ),
            },
        )

        self.assertRedirects(application_response, reverse('application_list'))
        self.assertTrue(
            Application.objects.filter(
                student__user=student_user,
                opportunity=opportunity,
            ).exists()
        )
