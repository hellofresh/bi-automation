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

user_source = 'biuser'
user_target = 'dsuser'
password_target = ''

for country in admin_creds.keys():
  hostname = 'intfood-db-{}001.live.bi.hellofresh.io'.format(country)
  db = MySQLdb.connect(host=hostname,
                       user=admin_creds[country][0],
                       passwd=admin_creds[country][1])
  cur = db.cursor()
  cur.execute("SELECT Host FROM mysql.user where user='{}'".format(user_source))
  for row in cur.fetchall():
      host = row[0]
      full_source_username = "'{}'@'{}'".format(user_source,host)
      full_target_username = "'{}'@'{}'".format(user_target,host)
      cur = db.cursor()
      cur.execute("CREATE USER {} IDENTIFIED BY {}".format(full_target_username, password_target))

      cur = db.cursor()
      cur.execute("show grants for {}".format(full_source_username))
      for row in cur.fetchall():
          grant_command_source = row[0]
          # we won't need that
          splitted = grant_command_source.split("IDENTIFIED BY PASSWORD")
          grant_command_target = splitted[0].replace(user_source, user_target)
          cur = db.cursor()
          cur.execute(grant_command_target)

  cur = db.cursor()
  cur.execute("FLUSH PRIVILEGES")
  db.close()
