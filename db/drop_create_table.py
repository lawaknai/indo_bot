import sqlite3

# Membuat koneksi dengan database SQLite
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Menghapus tabel 'bots' jika sudah ada
drop_table_query = """
    DROP TABLE IF EXISTS data
"""
cursor.execute(drop_table_query)

# Membuat tabel 'bots' barussss
create_table_query = """
    CREATE TABLE data (
        content_type TEXT,
        short_token TEXT,
        file_id TEXT,
        from_id TEXT
    )
"""
cursor.execute(create_table_query)

# Menyimpan perubahan dan menutup koneksi
conn.commit()
conn.close()



## COLLECT_USERDATA
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Menghapus tabel 'bots' jika sudah ada
drop_table_query = """
    DROP TABLE IF EXISTS user
"""
cursor.execute(drop_table_query)

# Membuat tabel 'bots' barussss
create_table_query = """
    CREATE TABLE user (
        user_id TEXT,
        first_name TEXT,
        last_name TEXT,
        username TEXT,
        file_id TEXT
    )
"""
cursor.execute(create_table_query)

# Menyimpan perubahan dan menutup koneksi
conn.commit()
conn.close()
