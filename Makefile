devenv:
	virtualenv -p python2.7 `pwd`/.venv
	. .venv/bin/activate && pip install -r requirements/development.txt

clean:
	@(rm -rvf .venv .tox .coverage build django-safety* *.egg-info)

pep8:
	@(flake8 safety --ignore=E501,E127,E128,E124)

test:
	@(py.test -s --cov-report term --cov-config .coveragerc --cov=safety --color=yes safety/tests)

geoip:
	@(wget http://geolite.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz)
	@(wget http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.mmdb.gz)
	@(wget http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz)
	@(gunzip -d GeoIP.dat.gz && mv GeoIP.dat data/geoip/)
	@(gunzip -d GeoLite2-City.mmdb.gz && mv GeoLite2-City.mmdb data/geoip2/)
	@(gunzip -d GeoLiteCity.dat.gz && mv GeoLiteCity.dat data/geoip/)

migrate:
	@(ENV=example python manage.py makemigrations safety)

example-clean:
	@(rm -rf example.db)

example-migrate:
	@(ENV=example python manage.py migrate)

example-user:
	@(ENV=example python manage.py createsuperuser --username='johndoe' --email='johndoe@example.com')

example-serve:
	@(ENV=example python manage.py runserver)

delpyc:
	@(find . -name '*.pyc' -delete)

release:
	@(python setup.py sdist register upload -s)
