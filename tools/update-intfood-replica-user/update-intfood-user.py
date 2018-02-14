#!/usr/bin/python
import MySQLdb

admin_creds = {
  'ml': ('dboperator',''),
  'at': ('dboperator',''),
  'au': ('dboperator',''),
  'be': ('dboperator',''),
  'ca': ('intfood_ca_admin',''),
  'ch': ('dboperator',''),
  'de': ('dboperator',''),
  'gb': ('dboperator',''),
  'lu': ('dboperator',''),
  'us': ('dboperator',''),
  'nl': ('dboperator','')
}

user_to_change = 'biuser'
new_password = ''

for country in admin_creds.keys():
  hostname = 'intfood-db-{}001.live.bi.hellofresh.io'.format(country)
  db = MySQLdb.connect(host=hostname,
                       user=admin_creds[country][0],
                       passwd=admin_creds[country][1])

  cur = db.cursor()
  cur.execute("SELECT User, Host FROM mysql.user where user='{}'".format(user_to_change))

  for row in cur.fetchall():
      full_username = "'{}'@'{}'".format(row[0],row[1])
      print("Updating {} replica: {}".format(country, full_username))
      cur = db.cursor()
      cur.execute("SET PASSWORD FOR {} = PASSWORD('{}')".format(full_username, new_password))

  cur = db.cursor()
  cur.execute("FLUSH PRIVILEGES")
  db.close()
