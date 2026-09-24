# emotion-logs
### Emotion log app is a digital tool that helps you track and monitor your emotions. By recording and analyzing your mood changes over time, you can gain valuable insights into your emotional well-being.

## Run locally

From `emotion_tracker`, activate your virtual environment and run:

```powershell
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Google sign-in

Google sign-in is optional. Create a Web application OAuth client in Google Cloud, then add this authorized redirect URI:

```text
http://127.0.0.1:8000/accounts/google/login/callback/
```

Set the credentials in the terminal before starting Django. Do not commit them or place real values in `.env.example`:

```powershell
$env:DJANGO_SECRET_KEY = 'replace-with-a-long-random-secret'
$env:GOOGLE_CLIENT_ID = 'your-client-id'
$env:GOOGLE_CLIENT_SECRET = 'your-client-secret'
python manage.py runserver
```

The Google button appears on the login page only when both variables are set. Production should use the HTTPS callback URL for its deployed domain.
