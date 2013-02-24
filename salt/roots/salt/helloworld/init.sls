include:
  - nginx
  - python

helloworld:
  user.present:
    - shell: /bin/bash
  nginx_site.managed:
    - source: salt://helloworld/nginx.conf
    - enable: true
    - require:
      - service: nginx

/home/helloworld/.env:
  virtualenv.managed:
    - requirements: salt://helloworld/requirements.txt
    - require:
      - pip: virtualenv
      - user: helloworld

/home/helloworld/app.py:
  file.managed:
    - source: salt://helloworld/app.py
    - user: helloworld
    - group: helloworld
    - require:
      - user: helloworld

/etc/init/gunicorn.conf:
  file.managed:
    - source: salt://helloworld/gunicorn.conf

gunicorn:
  service.running:
    - watch:
      - file: /home/helloworld/app.py
      - virtualenv: /home/helloworld/.env
      - file: /etc/init/gunicorn.conf
