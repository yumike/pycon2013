{% for user in ('alex', 'kennethreitz', 'mitsuhiko') %}
{{ user }}:
  user.present: []
{% endfor %}
