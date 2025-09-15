import os

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'instance', 'db.sqlite')

try:
    with open(db_path, 'a') as f:
        f.write('\n-- test write --')
    print("✅ Flask puede escribir en la base de datos.")
except Exception as e:
    print("❌ Error al escribir en la base de datos:")
    print(e)
