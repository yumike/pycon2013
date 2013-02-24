nginx:
  apt_repository.ubuntu_ppa:
    - user: nginx
    - name: stable
    - key_id: C300EE8C
  pkg.installed:
    - require:
      - apt_repository: nginx
  service.running:
    - require:
      - pkg: nginx

default-site:
  nginx_site.absent:
    - name: default
    - require:
      - service: nginx
