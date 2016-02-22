{%- set sites = ['default','monitoring'] -%}

# Ensure nginx is installed and reload when required
nginx:
  pkg:
    - installed
  service.running:
    - enable: True
    - restart: True
    - watch:  # Reload automatically under certain conditions
      - pkg: nginx
      - file: /etc/nginx/nginx.conf
      {% for site in sites %}
      - file: /etc/nginx/sites-enabled/{{ site }}
      {% endfor %}
    - require:
      - file: /etc/nginx/nginx.conf
      {% for site in sites %}
      - file: /etc/nginx/sites-enabled/{{ site }}
      {% endfor %}

# Manage nginx configuration file
/etc/nginx/nginx.conf:
  file.managed:
    - source: salt://nginx/files/etc/nginx/nginx.conf
    - user: root
    - group: root
    - mode: 640

# Manage nginx sites as templates and symlink them
{% for site in sites %}
/etc/nginx/sites-available/{{ site }}:
  file.managed:
    - source: salt://nginx/files/etc/nginx/sites-available/{{ site }}.jinja
    - template: jinja
    - user: root
    - group: root
    - mode: 640

/etc/nginx/sites-enabled/{{ site }}:
  file.symlink:
    - target: /etc/nginx/sites-available/{{ site }}
    - require:
      - file: /etc/nginx/sites-available/{{ site }}
{% endfor %}

# Example html page
/usr/share/nginx/www/index.html:
  file.managed:
    - source: salt://nginx/files/usr/share/nginx/www/index.html.jinja
    - template: jinja
    - user: root
    - group: root
    - mode: 644
