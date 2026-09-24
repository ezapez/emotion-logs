# EmotionLogs

**Web app in progress.**

EmotionLogs is a personal emotion journal where users can record how they felt on a specific date and write about the experience behind that emotion. The app is designed to keep this process simple, private, and easy to return to over time.

## What I am making

- A user account and login system
- A private journal for each user
- Emotion notes with a date, emotion, and personal experience
- A clean interface for writing, viewing, and editing notes
- A secure foundation that can later grow with features such as mood patterns and analytics

## What I am learning

Building this app is helping me learn how to:

- Build a full web application with Django
- Design database models and manage migrations
- Create forms and validate user input
- Work with authentication, sessions, and user permissions
- Protect private user data
- Create responsive interfaces with Bootstrap
- Organize a project into reusable apps, views, templates, and URLs
- Prepare an application for deployment and version control with Git and GitHub

## Project files

- [Django settings](emotion_tracker/emotion_tracker/settings.py)
- [Main project URLs](emotion_tracker/emotion_tracker/urls.py)
- [Emotion note model](emotion_tracker/emotion_logs/models.py)
- [Emotion note forms](emotion_tracker/emotion_logs/forms.py)
- [Emotion note views](emotion_tracker/emotion_logs/views.py)
- [Emotion note URLs](emotion_tracker/emotion_logs/urls.py)
- [Emotion note tests](emotion_tracker/emotion_logs/tests.py)
- [Shared page layout](emotion_tracker/emotion_logs/templates/emotion_logs/base.html)
- [Journal page](emotion_tracker/emotion_logs/templates/emotion_logs/topics.html)
- [New note page](emotion_tracker/emotion_logs/templates/emotion_logs/new_entry.html)
- [Login page](emotion_tracker/accounts/templates/registration/login.html)
- [Registration page](emotion_tracker/accounts/templates/registration/register.html)
- [Database migrations](emotion_tracker/emotion_logs/migrations/)
- [Project dependencies](emotion_tracker/requirements.txt)

More features and improvements will be added as I continue learning and building the app.
