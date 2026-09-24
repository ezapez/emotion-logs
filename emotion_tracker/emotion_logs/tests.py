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
