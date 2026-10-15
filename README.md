# Fitness Hub

Django fitness platform by **Sagar shahi** — exercises, goals, progress tracking, diet, store, inspiration, chatbot, social, and achievements in one app.

## Quick start

**Requirements:** Python 3.11+

From the project root, run:

```bash
./start.sh
```

That single command:

1. Creates a virtual environment (`.venv`) if needed
2. Installs dependencies from `requirements.txt`
3. Creates `.env` from `.env.example` if missing
4. Runs database migrations
5. Seeds sample data (exercises, store products, inspiration, achievements)
6. Starts the development server at **http://127.0.0.1:8000**

Press **Ctrl+C** to stop the server.

Use a different port:

```bash
PORT=8080 ./start.sh
```

## Project structure

```
Fitness-Hub/
├── start.sh              # One-command setup and run
├── manage.py
├── requirements.txt
├── .env.example
├── fitness_hub/          # Django project (settings, urls)
├── core/
├── users/                # Auth, profile, settings
├── dashboard/
├── goals/
├── exercises/            # Home page + exercise library
├── progress/
├── store/                # Products, cart, checkout
├── diet/
├── inspiration/
├── chatbot/
├── social/
├── achievements/
├── templates/            # Shared HTML templates
└── static/               # CSS, JS, images
```

## Modules and URLs

All features run on one Django server — no separate services to start.

| Module | URL |
|--------|-----|
| Home / Exercises | http://127.0.0.1:8000/ |
| Store | http://127.0.0.1:8000/store/ |
| Dashboard | http://127.0.0.1:8000/dashboard/ |
| Goals | http://127.0.0.1:8000/goals/ |
| Progress | http://127.0.0.1:8000/progress/ |
| Diet | http://127.0.0.1:8000/diet/ |
| Inspiration | http://127.0.0.1:8000/inspiration/ |
| Chatbot | http://127.0.0.1:8000/chatbot/ |
| Social | http://127.0.0.1:8000/social/ |
| Achievements | http://127.0.0.1:8000/achievements/ |
| Users / Auth | http://127.0.0.1:8000/users/ |
| Admin | http://127.0.0.1:8000/admin/ |

## Seeded data

`start.sh` runs `python manage.py seed_all`, which loads:

- **36 exercises** across muscle groups and difficulty levels
- **12 store products** in 3 categories (Outfits, Gear, Supplements)
- **23 fitness icons** and motivation quotes
- **16 achievements**

To re-seed manually:

```bash
source .venv/bin/activate
python manage.py seed_all
```

Individual seed commands: `seed_exercises`, `seed_inspiration`, `seed_store`, `seed_achievements`.

## Environment variables

Copy `.env.example` to `.env` and edit as needed:

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | Groq API key for the AI chatbot (optional) |
| `GROQ_MODEL` | Groq model name (default: `llama-3.1-8b-instant`) |
| `STRIPE_SECRET_KEY` | Stripe test key for real checkout (optional) |

Without `GROQ_API_KEY`, the chatbot falls back to built-in responses.  
Without `STRIPE_SECRET_KEY`, checkout is simulated and orders are marked paid locally.

## Manual setup (optional)

If you prefer not to use `start.sh`:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py seed_all
python manage.py runserver
```

## Tests

```bash
source .venv/bin/activate
python manage.py test
```

With coverage:

```bash
coverage run --source='.' manage.py test
coverage report -m
```

## Features

- User registration, login, and profile management
- Dashboard with workout stats
- Goals CRUD with exercise recommendations
- Exercise library with completion tracking
- Progress logging and workout history
- Diet / nutrition records and meal suggestions
- Store with session cart and checkout (Stripe or simulated)
- Inspiration feed with fitness icons and quotes
- AI chatbot with Groq integration
- Social connections and messaging
- Achievement badges and unlocks

## CI

GitHub Actions runs migrations and tests on push/PR to `main` (see `.github/workflows/ci.yml`).
