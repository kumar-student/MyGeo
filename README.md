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

The Django abstract user model (AbstractUser) is a pre-built user model provided by Django with essential fields and functionalities for authentication, including email, password, and permissions.

Extending the Django abstract user model allows you to customize the user model according to the specific requirements of your project.

In ```'settings.py'``` file add ```'users'``` app name to INSTALLED_APPS

```python
# settings.py

INSTALLED_APPS = [
    # ... default django apps

    'users',
]
```

### Customizing the user model

Follow below steps to custome user model

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
        first_name = kwargs.pop('first_name', None)
        if not first_name:
            raise ValueError(_('First name must be provided'))
        last_name = kwargs.pop('last_name', None)
        user = self.model(email=email, **kwargs)
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
    username = None
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

### Configure database

Installing postgresql
```shell
sudo apt install libpq-dev postgresql postgresql-contrib postgis
```

Creating a Database

By default, Postgres uses an authentication schema called peer authentication for local connections.

During the Postgres installation, an operating system user name postgres was created to correspond to the postgres PostgreSQL administrative user.

Log into the interactive Postgre session to create database and databse user.
```shell
sudo -u postgres psql
```

After login you will be prompted to SQL prompt ```postgres=#```

Crete a database with the name ```mygeo``` for the project
```shell
CREATE DATABASE mygeo;
```

Now create a database user that will connect to an interact with the database.
```shell
CREATE USER mygeo_user WITH PASSWORD 'Abcd@123';
```

Set the default encoding to UTF-8. This will speed up database operations.
```shell
ALTER ROLE mygeo_user SET client_encoding to 'utf8';
```

Then, set the default transaction isolation schema to ```read committed```, which blocks reads from uncommitted transactions.
```shell
ALTER ROLE mygeo_user SET default_transaction_isolation TO 'read committed';
```

Set the timezone.
```shell
ALTER ROLE mygeo_user SET timezone TO 'UTC';
```

Now grant all privileges to mygeo_user.
```
GRANT ALL PRIVILEGES ON DATABASE mygeo TO mygeo_user;
```

PostGIS is a free, open-source extension that adds spacial data capabilities to PostgreSQL databases.

Connect to your ```mygeo``` database.
```shell
\c mygeo
```

Enable ```postgis``` extension in your database by creating postgis extension.
```shell
CREATE EXTENSION postgis;
```

Exit the SQL prompt.
```shell
\q
```
Restart the postgresql server to detected postgis extension.
```shell
sudo systemctl restart postgresql
# or
sudo systemctl restart postgresql.service
```


Install PostgreSQL adapter ```psycopg2``` in virtual environment for python.

Add ```psycopg2-binary==2.9.6``` to requirements.txt and install requirements.
```shell
pip install -r requirements.txt
```

Configure the connection to the PostgreSQL and PostGIS spacial database.
```shell
# settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'mygeo',
        'USER': 'mygeo_user',
        'PASSWORD': 'Abcd@123',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}

```

In Django, ```django.contrib.gis``` is a built-in Django application that provides geographic information system (GIS) functionalities and tools. Include it in INSTALLED_APPS
```shell
# settings.py

INSTALLED_APPS = [
    # ...
    'django.contrib.gis',

    # ...
]
```

### Adding more fields to the user model
Require fields: ```address```, ```phone``` and ```location```

For storing phone number install a django library which intefaces with python-phonenumbers to validate, pretty print and convert phone numbers.

Add ```django-phonenumber-field==7.1.0``` and ```phonenumberslite==8.13.16``` to requirements.txt
```shell
pip install -r requirements.txt
```

Update the user model
```shell
# users/models.py
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField as BasePhoneField

class PhoneField(BasePhoneField):
    pass


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
        first_name = kwargs.pop('first_name', None)
        if not first_name:
            raise ValueError(_('First name must be provided'))
        last_name = kwargs.pop('last_name', None)
        if not last_name:
            raise ValueError(_('Last name must be provided'))
        address = kwargs.pop('address', None)
        if not address:
            raise ValueError(_('Address must be provided'))
        phone = kwargs.pop('phone', None)
        if not phone:
            raise ValueError(_('Phone number must be provided'))
        location = kwargs.pop('location', None)
        if not location:
            raise ValueError(_('location must be provided'))
        user = self.model(email=email, **kwargs)
        user.first_name = first_name
        user.last_name = last_name
        user.address = address
        user.phone = phone
        user.location = location
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password=None, **kwargs):
        kwargs.setdefault('is_superuser', False)
        kwargs.setdefault('is_staff', False)
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password=None, **kwargs):
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('location', Point(0.0, 0.0))
        if kwargs.get("is_staff") is not True:
            raise ValueError(_('Superuser must have is_staff=True'))
        if kwargs.get("is_superuser") is not True:
            raise ValueError(_('Superuser must have is_superuser=True'))
        return self._create_user(email, password, **kwargs)


class User(AbstractUser, PermissionsMixin):
    """
    Custom user model
    """
    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.TextField(max_length=255)
    phone = PhoneField()
    location = models.PointField()
    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = [
        'first_name',
        'last_name',
        'address',
        'phone'
    ]

    def __str__(self):
        return str(self.email)
```

Create custom UserCreationForm and UserChangeForm classes to ensure that the admin interface works correctly with your custom user model.
```shell
# users/forms.py

from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm, \
    UserChangeForm as BaseUserChangeForm

from django.contrib.auth import get_user_model


class UserCreationForm(BaseUserCreationForm):
    class Meta(BaseUserCreationForm.Meta):
        model = get_user_model()
        fields = (
            'email', 
            'first_name', 
            'last_name', 
            'address', 
            'phone', 
            'location',
            'is_staff', 
            'is_superuser', 
            'groups',
            'user_permissions',
            'is_active'
        )


class UserChangeForm(BaseUserChangeForm):
    class Meta(BaseUserChangeForm.Meta):
        model = get_user_model()
        fields = (
            'email', 
            'first_name', 
            'last_name', 
            'address', 
            'phone', 
            'location',
            'is_staff', 
            'is_superuser', 
            'groups',
            'user_permissions',
            'is_active'
        )
```

Update admin interface
```shell
# users/admin.py

from django.contrib.gis import admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .forms import UserCreationForm, UserChangeForm


class UserAdmin(admin.OSMGeoAdmin):
    """
    User admin interface
    """
    model = get_user_model()
    add_form = UserCreationForm
    form = UserChangeForm
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser','groups', 'user_permissions')}),
        (_('More fields'), {'fields': ('address', 'phone', 'location')})
    )
    add_fieldsets = (
        (
            None,
            {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
            }
        )
    )


    def remove_fields(superset, subset):
        if len(subset) > 0:
            return [element for element in superset if element not in subset]
        return []

    def get_readonly_fields(self, request, obj=None):
        is_superuser = request.user.is_superuser
        # If user is not a super user return fields based on object ownership
        if not is_superuser:
            if not obj:     # If there is no user object no fild are marked as read only
                return []
            elif obj.pk == request.pk:      # If the object belongs to requested user no fields are marked as read only
                 return []
            else:       # If the object does not belogns to requested user few fieds marked as read only
                return [
                    'email',
                    'first_name',
                    'last_name',
                    'address',
                    'phone',
                    'location'
                ]
        # If user is super user, no fields are marked as read only fields
        return []

    def get_form(self, request, obj=None, **kwargs):
        form = self.form
        is_superuser = request.user.is_superuser

        disabled_fields = []
        all_fields = [field.name for field in self.model._meta.fields]

        if not is_superuser:
            fields_to_remove = []
            if not obj:
                disabled_fields = self.remove_fields(all_fields, fields_to_remove)
            elif obj and obj.pk == request.user.pk:
                fields_to_remove = [
                    'is_superuser', 
                    'is_staff', 
                    'user_permissions', 
                    'groups', 
                    'is_active'
                ]
                disabled_fields = self.remove_fields(all_fields, fields_to_remove)
            else:
                fields_to_remove = [
                    'is_superuser', 
                    'is_staff', 
                    'user_permissions', 
                    'groups', 
                    'is_active'
                ]
                disabled_fields = self.remove_fields(all_fields, fields_to_remove)

        for field in disabled_fields:
            if field in form.base_fields:
                form.base_fields[field].disabled = True
        
        return form

# Register the default User model with a custom ModelAdmin
admin.site.register(get_user_model(), UserAdmin)
```

### Running migrations
Django, migrations are a way to manage and synchronize changes in your models' schema with the database schema. They allow you to evolve the database schema over time without losing data.

When you make changes to your models, such as adding a new field, modifying existing fields, or creating new models, Django uses migrations to track these changes and generate migration files. These migration files contain the Python code that represents the changes to be applied to the database schema.

Here is how to ```makemigrations```
```shell
python manage.py makemigrations
```

By running migrate, you ensure that any changes to your models are reflected in the database schema, and your project's database is up-to-date with the latest changes.
Here is how to apply migrations
```shell
python manage.py migrate
```

### Create an admin user
Create superuser by running this command and fill the details.
```shell
python manage.py createsuperuser
``` 
