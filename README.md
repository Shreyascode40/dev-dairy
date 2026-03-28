# Dev Dairy - Blog Platform

A modern blog platform built with Django where users can create profiles, write blogs, like, comment, and connect with other users.

## Features

- **User Authentication**
  - Registration and Login
  - Profile management with customizable bio
  - Profile picture upload

- **Blog Management**
  - Create, edit, and delete blogs
  - Categories and tags
  - Cover images
  - Blog views counter

- **Social Features**
  - Like and comment on blogs
  - User search functionality
  - View other user profiles

- **Profile Customization**
  - Profile picture
  - Bio/About section
  - Social media links:
    - GitHub
    - Instagram
    - Facebook
    - Twitter/X
    - LinkedIn
    - Website

## Tech Stack

- **Backend**: Django 5.2
- **Database**: Postgresql
- **Frontend**: HTML, CSS, JavaScript
- **Icons**: SVG

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Shreyascode40/dev-dairy.git
cd dev-dairy
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install django
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Start the server:
```bash
python manage.py runserver
```

6. Open browser and visit:
```
http://127.0.0.1:8000
```

## Project Structure

```
dev_dairy/
├── blog/
│   ├── migrations/
│   ├── templates/blog/
│   │   ├── blog_detail.html
│   │   ├── create_blog.html
│   │   ├── home.html
│   │   └── update_blog.html
│   ├── admin.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── user/
│   ├── migrations/
│   ├── templates/user/
│   │   ├── edit_profile.html
│   │   ├── login.html
│   │   ├── profile.html
│   │   ├── register.html
│   │   ├── search.html
│   │   └── view_user.html
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── dev_dairy/
│   ├── settings.py
│   └── urls.py
├── manage.py
└── README.md
```

## Usage

1. **Register** a new account
2. **Login** with your credentials
3. **Edit Profile** - Add bio, profile picture, and social links
4. **Create Blog** - Write your first blog post
5. **Browse** - View other blogs and users
6. **Interact** - Like and comment on posts

## Screenshots

The app features:
- Modern sidebar navigation
- Responsive design
- Gradient backgrounds
- Clean typography

## License

MIT License


##Author

Shreyas More