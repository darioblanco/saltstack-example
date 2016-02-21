# Ensure nginx is installed and running
nginx:
  pkg:
    - installed
  service.running:
    - watch:  # Reload automatically under certain conditions
      - pkg: nginx
      - file: /etc/nginx/nginx.conf
      - file: /etc/nginx/sites-available/default

# Manage nginx configuration file
/etc/nginx/nginx.conf:
  file.managed:
    - source: salt://nginx/files/etc/nginx/nginx.conf
    - user: root
    - group: root
    - mode: 640

# Manage default nginx site as a template
/etc/nginx/sites-available/default:
  file.managed:
    - source: salt://nginx/files/etc/nginx/sites-available/default.jinja
    - template: jinja
    - user: root
    - group: root
    - mode: 640

# Symlink site-available file to site-enabled
/etc/nginx/sites-enabled/default:
  file.symlink:
    - target: /etc/nginx/sites-available/default
    - require:
      - file: /etc/nginx/sites-available/default

# Example html page
/usr/share/nginx/www/index.html:
  file.managed:
    - source: salt://nginx/files/usr/share/nginx/www/index.html.jinja
    - template: jinja
    - user: root
    - group: root
    - mode: 644
