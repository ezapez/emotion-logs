from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Entry


class EntryAccessTests(TestCase):
	def setUp(self):
		self.owner = User.objects.create_user(username='owner', password='test-password-123')
		self.other_user = User.objects.create_user(username='other', password='test-password-123')
		self.entry = Entry.objects.create(
			user=self.owner,
			date='2026-09-24',
			emotion='Calm',
			experience='A quiet day.',
		)

	def test_entries_require_login(self):
		response = self.client.get(reverse('emotion_logs:entries'))

		self.assertEqual(response.status_code, 302)
		self.assertIn('/accounts/login/', response.url)

	def test_user_sees_only_their_entries(self):
		self.client.force_login(self.other_user)

		response = self.client.get(reverse('emotion_logs:entries'))

		self.assertNotContains(response, 'A quiet day.')

	def test_personal_chart_data_contains_only_the_signed_in_users_entries(self):
		Entry.objects.create(
			user=self.other_user,
			date='2026-09-25',
			emotion='Angry',
			experience='This belongs to another account.',
		)
		self.client.force_login(self.owner)

		response = self.client.get(reverse('emotion_logs:entries'))
		chart_data = response.context['chart_data']

		self.assertEqual(chart_data['total_entries'], 1)
		calm_index = chart_data['emotion_labels'].index('Calm')
		angry_index = chart_data['emotion_labels'].index('Angry')
		self.assertEqual(chart_data['emotion_values'][calm_index], 1)
		self.assertEqual(chart_data['emotion_values'][angry_index], 0)
		self.assertNotContains(response, 'This belongs to another account.')

	def test_user_can_create_an_entry_for_themselves(self):
		self.client.force_login(self.owner)

		response = self.client.post(
			reverse('emotion_logs:new_entry'),
			{'date': '2026-09-25', 'emotion': 'Happy', 'experience': 'Good news today.'},
		)

		self.assertRedirects(response, reverse('emotion_logs:entries'))
		self.assertTrue(Entry.objects.filter(user=self.owner, emotion='Happy').exists())

	def test_user_cannot_edit_another_users_entry(self):
		self.client.force_login(self.other_user)

		response = self.client.get(reverse('emotion_logs:edit_entry', args=[self.entry.id]))

		self.assertEqual(response.status_code, 404)


class AdminDashboardTests(TestCase):
	def test_superuser_dashboard_shows_account_activity_but_not_notes(self):
		admin_user = User.objects.create_superuser(
			username='site-admin',
			email='admin@example.com',
			password='test-password-123',
		)
		new_user = User.objects.create_user(username='new-member', password='test-password-123')
		inactive_user = User.objects.create_user(
			username='inactive-member',
			password='test-password-123',
			is_active=False,
		)
		Entry.objects.create(
			user=new_user,
			date='2026-09-25',
			emotion='Calm',
						experience='Private emotion note content.',
		)
		self.client.force_login(admin_user)

		response = self.client.get(reverse('admin:index'))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Total users')
		self.assertContains(response, 'Active accounts')
		self.assertContains(response, 'Inactive accounts')
		self.assertContains(response, new_user.username)
		self.assertContains(response, inactive_user.username)
		self.assertNotContains(response, 'Recent emotion notes')
		self.assertNotContains(response, 'Private emotion note content.')
		self.assertContains(response, 'admin/css/dark_mode.css')
		self.assertContains(response, '#content-main .module caption')
		self.assertEqual(response.context['admin_analytics']['total_entries'], 1)
		self.assertContains(response, 'Emotion totals')

	def test_admin_charts_use_aggregates_after_five_contributors(self):
		admin_user = User.objects.create_superuser(
			username='analytics-admin',
			email='analytics@example.com',
			password='test-password-123',
		)
		for index in range(5):
			user = User.objects.create_user(username=f'member-{index}', password='test-password-123')
			Entry.objects.create(
				user=user,
				date='2026-09-25',
				emotion='Calm',
				experience=f'Private note text {index}.',
			)
		self.client.force_login(admin_user)

		response = self.client.get(reverse('admin:index'))
		analytics = response.context['admin_analytics']

		self.assertContains(response, 'Emotion totals')
		self.assertContains(response, 'Monthly logging activity')
		self.assertContains(response, 'all-emotions-chart')
		self.assertContains(response, 'chart.js@4.5.1')
		self.assertEqual(analytics['emotion_values'][4], 5)
		self.assertEqual(analytics['total_entries'], 5)
		self.assertEqual(set(analytics), {
			'total_entries', 'emotion_labels', 'emotion_values', 'month_labels', 'monthly_values',
		})
		for index in range(5):
			self.assertNotContains(response, f'Private note text {index}.')

	def test_non_superuser_cannot_access_admin(self):
		user = User.objects.create_user(username='regular-user', password='test-password-123')
		self.client.force_login(user)

		response = self.client.get(reverse('admin:index'))

		self.assertEqual(response.status_code, 404)
