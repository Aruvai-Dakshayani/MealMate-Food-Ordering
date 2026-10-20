MealMate – Food Ordering Web Application

About the Project

MealMate is a web-based food ordering application developed using Python and Django. It allows users to explore restaurants, view menu items, add food items to their cart, and manage their orders through a simple and user-friendly interface.

Features

- Browse available restaurants
- View restaurant details and menus
- User registration and login
- Add food items to the cart
- Place and manage food orders
- User profile management
- Restaurant and menu management through Django Admin

Technologies Used

- Backend: Python, Django
- Frontend: HTML, CSS, JavaScript
- Database: SQLite
- Version Control: Git and GitHub

Project Structure

text
MealMate/
├── MealMate/
│   ├── manage.py
│   ├── MealMate/
│   └── delivery/
├── .gitignore
└── README.md

 Installation and Setup

1. Clone the Repository

bash
git clone https://github.com/Aruvai-Dakshayani/MealMate-Food-Ordering.git


2. Navigate to the Project Directory

bash
cd MealMate-Food-Ordering
Navigate to the inner `MealMate` directory containing `manage.py`.
3. Create a Virtual Environment
bash
python -m venv myenv
4. Activate the Virtual Environment

For Windows PowerShell:
powershell
..\myenv\Scripts\Activate.ps1

5. Install Django
bash
pip install django
If a `requirements.txt` file is available, install the project dependencies using:

bash
pip install -r requirements.txt

6. Apply Database Migrations
bash
python manage.py migrate

7. Run the Development Server
bash
python manage.py runserver

Open the following URL in your browser:

http://127.0.0.1:8000/

 Learning Outcomes

- Gained practical experience in Python and Django web development.
- Learned to connect frontend pages with backend views.
- Practiced working with database models and migrations.
- Developed an understanding of user authentication and order management.
- Gained experience using Git and GitHub for version control.

Author
Aruvai Dakshayani

GitHub Profile: https://github.com/Aruvai-Dakshayani

Project Repository: https://github.com/Aruvai-Dakshayani/MealMate-Food-Ordering
