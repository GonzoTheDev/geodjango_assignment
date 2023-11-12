# GeoDjango Fishing Mark Map

A fishing mark locations map application, showing fishing locations around Dublin and the types of fish you can catch there.

Website: https://geodjango.shanewilson.ie


# Steps to Deploy to cloud

Create Postgres GIS database container in docker:
```docker create --name geodjango_assignment_postgis --network geodjango_assignment_network --network-alias geodjango-assignment-postgis -t -v geodjango_assignment_postgis_data:/var/lib/postgresql -e 'POSTGRES_USER=c20703429' -e 'POSTGRES_PASS=c20703429' kartoza/postgis```

Create PGAdmin4 database frontend management system container in docker:
```docker create --name geodjango_assignment_pgadmin4 --network geodjango_assignment_network --network-alias geodjango-assignment-pgadmin4 -t -v geodjango_assignment_pgadmin_data:/var/lib/pgadmin -e 'PGADMIN_DEFAULT_EMAIL=YOURNAME@tudublin.ie' -p 20080:80 -e 'PGADMIN_DEFAULT_PASSWORD=YOURPASSWORD' dpage/pgadmin4```

Pull the Django application container from DockerHub:
```docker pull drgonzo19929/geodjango_assignment```

Create the Django application container from the image:
```docker create --name geodjango_assignment --network geodjango_assignment_network --network-alias geodjango_assignment -t -p 8001:8001 drgonzo19929/geodjango_assignment```

Start the Django application:
```docker start geodjango_assignment```

Run the migrations:
```docker exec geodjango_assignment bash -c "conda run -n geodjango_assignment python manage.py migrate"```

Import the map locations data:
```docker exec geodjango_assignment bash -c "conda run -n geodjango_assignment python manage.py import_fishing_marks"```

Create a superuser to be able to setup users etc. :
```docker exec geodjango_assignment bash -c "conda run -n geodjango_assignment python manage.py createsuperuser"```

