# CALOME - Fitness and Nutrition Tracking App

CALOME is a comprehensive fitness and nutrition tracking application built with Django. It helps users monitor their daily food intake, track nutritional information, and manage their fitness goals.

## Features

- User authentication (register, login, logout)
- Food diary with nutritional information tracking
- Automatic food lookup using USDA Food Data Central API
- Track calories, protein, carbs, fat, and fiber
- Daily nutritional totals
- Responsive design with Bootstrap

## Prerequisites

- Python 3.12 or higher
- pip (Python package installer)
- Git

## Installation

1. Clone the repository:
```bash
git clone https://github.com/JivSTuban/wewew.git
cd wewew
```

2. Create a virtual environment:
```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
.\venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Apply database migrations:
```bash
python manage.py migrate
```

5. Create a superuser (admin) account:
```bash
python manage.py createsuperuser
```

## Running the Application

1. Start the development server:
```bash
python manage.py runserver
```

2. Open your web browser and navigate to:
```
http://127.0.0.1:8000/
```

## Usage

1. Register a new account or log in with existing credentials
2. Navigate to the Food Diary section
3. Add food entries:
   - Enter food name and use the "Look up" button for automatic nutritional info
   - Or manually enter nutritional information
4. View your daily totals and track your nutrition goals

## Project Structure

```
fitness_tracker/
├── fitness_tracker/    # Project settings
├── tracker/           # Main application
│   ├── models.py      # Database models
│   ├── views.py       # View logic
│   ├── forms.py       # Form definitions
│   └── templates/     # HTML templates
└── manage.py         # Django management script
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
