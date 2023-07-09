import logging

# Konfigurasi logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Buat FileHandler untuk menulis log ke file
file_handler = logging.FileHandler('app.log')

# Tentukan format log yang diinginkan
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Tambahkan FileHandler ke logger
logger.addHandler(file_handler)