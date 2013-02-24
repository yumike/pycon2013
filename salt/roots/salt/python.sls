include:
  - curl

python:
  pkg.installed:
    - names:
      - python
      - python-dev

distribute:
  cmd.run:
    - name: curl http://python-distribute.org/distribute_setup.py | python
    - unless: which easy_install
    - require:
      - pkg: curl
      - pkg: python

pip:
  cmd.run:
    - name: curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python
    - unless: which pip
    - require:
      - cmd: distribute

virtualenv:
  pip.installed:
    - require:
      - cmd: pip
