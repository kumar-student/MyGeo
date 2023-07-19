# MyGeo
The MyGeo Application is a web-based platform that aims to provide an interactive interface for display registered user's profile and geo locations.

Additionally, users can update and maintain their profiles, which include thier own profile and location information.

## Key Features:
1. Sign up
2. Sign in
3. Profile Management
4. Dashboard
5. Access Control

## Use case diagram

![Use case diagram](<MyGeo Use case diagram.png>)


## Class diagram
| User                      |
|---------------------------|
| id: int                   |
| username: string          |
| email: string             |
| first_name: string        |
| last_name: string         |
| country: string           |
| address: string           |
| phone: string             |
| location: string(pointer) |
| is_active: boolean        |
|                           |
| users()                   |
| my_profile()              |
| update_profile()          |
|

##  Technical requirements
1. python3
2. libraries for handling spacial data
3. virtual environment
4. django
5. postgresql database
6. leaflet

**python3** as main programming language for the project.

**GEOS, PROJ.4, and GDAL** are the libraries that provide geospatial functionalities.

**virtual environment** to handle all project dependencies.

**Django** as the web framework for the project.

**PostgreSQL** is commonly used as the database for handling spatial data and offers advanced geospatial features through the PostGIS extension

**Leaflet** is a popular JavaScript library that allows you to create interactive and customizable maps on web applications.

## Initial setup on Linux
Add python respository
```shell
sudo add-apt-repository ppa:deadsnakes/ppa
```
Install specific python version and virtual environment
```shell
sudo apt update
sudo apt install python3.10 python3.10-dev python3.10-distutils python3.10-venv
```

### Installing Geospatial libraries
**GEOS** stands for Geometry Engine Open Source is a C++ library that is used for performing geometric operations and handling spatial data. It provides the necessary functionalities for working with geographic information such as points, polygons, and distances.

**PROJ.4** is a library used for cartographic projections and coordinate system transformations. It is commonly used in conjunction with PostGIS, which is an extension for the PostgreSQL database that adds support for spatial data and spatial queries.

**GDAL** (Geospatial Data Abstraction Library) is a open-source library used in geospatial applications. provides the necessary functionality to read, write, and convert data between different formats including vector formats (e.g., Shapefile, GeoJSON) and raster formats (e.g., GeoTIFF, JPEG2000). It provides functions which are useful in performing spatial calculations and generating derived data. Django's GIS module and PostGIS leverage GDAL for handling geospatial data.

Installing binary utils
```shell
sudo apt install binutils
```
Binary utils offer offer various operations on binary files thare are going to used in the project.

Install GEOS libraries
```shell
sudo apt install libgeos-dev
```

Install Proj.4 libraries
```shell
sudo apt install libproj-dev
```

Install GDAL libraries
```shell
sudo apt install gdal-bin libgdal-dev python3-gdal
```

<!-- Install GeoIP libraries
```shell
sudo apt install libgeoip-dev
``` -->

### Crate and activate virtual environment
Navigate to a working directory
```shell
cd ~/workspace
mkdir MyGeo
cd MyGeo
```
Create virtual environment with the name .venv
```shell
python3.10 -m venv .venv
```

Activate virtual environment
```shell
source .venv/bin/activate
```

### Install project dependencies
**requirements.txt** lists the packages and their respective versions that need to be installed for the project to run correctly.

Create requirements.txt 
```shell
touch requirements.txt
```

requirements.txt
```
django==4.2
```

**pip** is a package management system for Python. It is used to install, upgrade, and manage Python packages and their dependencies.

pip can read the requirements.txt file and automatically install all the packages and their versions specified in the file.

To install the packages listed in a requirements.txt file, you can use the following command
```shell
pip install -r requirements.txt
```

### Initialize the project
```
django-admin startproject project .
```

Create users app to store user details
```shell
python manage.py startapp users
```

The Django abstract user model (AbstractUser) is a pre-built user model provided by Django with essential fields and functionalities for authentication, including username, email, password, and permissions.

Extending the Django abstract user model allows you to customize the user model according to the specific requirements of your project.

Follow below steps to customize user

In ```'settings.py'``` file add ```'users'``` app name to INSTALLED_APPS

```python
# settings.py

INSTALLED_APPS = [
    # ... default django apps

    'users',
]
```

Customize the user model
```python
# users/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    Custom manager for Custom User model
    """

    def get_by_natural_key(self, email):
        return super().get_by_natural_key(email)

    def _create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError(_('Email must be provided'))
        email = self.normalize_email(email)
        username = kwargs.get('username', None)
        if not username:
            username = email
        first_name = kwargs.pop('first_name', None)
        if not first_name:
            raise ValueError(_('First name must be provided'))
        last_name = kwargs.pop('last_name', None)
        user = self.model(email=email, **kwargs)
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        user.save()
        return user

    def create_user(self, emial, password=None, **kwargs):
        kwargs.setdefault('is_superuser', False)
        kwargs.setdefault('is_staff', False)
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password=None, **kwargs):
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_staff', True)
        return self._create_user(email, password, **kwargs)


class User(AbstractUser):
    """
    Custom user model
    """
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    objects = UserManager()

    def __str__(self):
        return str(self.email)
```

Register user model with admin interface
```python
# users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


class UserAdmin(BaseUserAdmin):
    """
    User admin interface
    """
    pass

# Register the default User model with a custom ModelAdmin
admin.site.register(User, UserAdmin)
```

To use this custom user model, you need to inform about it to Django
```python
# settings.py

AUTH_USER_MODEL = 'users.User'
```
