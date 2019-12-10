import requests
import shutil
import json
import os
import time
import sys
from datetime import datetime

# MASUKKAN ID INSTAGRAM YANG MAU DI-CRAWL
daftar_userid = [
  "viratandia"
]
num_of_ids = len(daftar_userid)
id_num = 0

# MASUKKAN BERAPA POSTS YANG MAU DIDOWNLOAD
post_qty = 5

# MASUKKAN BERAPA DETIK SEBELUM CRAWLING TIAP ID
timer = 60

# SET LOKASI DOWNLOAD
path = os.getcwd()
download_path = 'image-downloads/'

# BIKIN DIRECTORY DOWNLOAD BARU
try:
    os.mkdir(download_path)
except OSError:
    pass

# MULAI PROSES MENGUMPULKAN LINK GAMBAR
for userid in daftar_userid:
    id_num = id_num + 1

    # MENJALANKAN SCRIPT CRAWLING INSTAGRAM UNTUK MENDAPATKAN LINK KE IMAGENYA
    print("Downloading for " + userid)
    os.system('python crawler.py posts_full -u' + userid + ' -n ' + str(post_qty) + ' -o ./output')

    # SET IMAGE PATH UNTUK MENYIMPAN IMAGE / FOTO INSTAGRAM
    img_path = download_path + userid + '/'

    # MULAI PROSES DOWNLOAD GAMBAR DARI LINK YANG SUDAH DIKUMPULKAN
    try:
        # MEMBACA FILE OUTPUT DIMANA ADA LIST LINK KE IMAGE
        with open('output') as json_file:
            instagram_id = json.load(json_file)

            for index, p in enumerate(instagram_id):
            
                img_urls = p['img_urls']

                try:
                    os.mkdir(img_path)
                except:
                    pass

                for index, img_url in enumerate(img_urls):

                    now = datetime.now()
                    timestamp = datetime.timestamp(now)

                    resp = requests.get(img_url, stream=True)

                    img_name =  img_path + str(timestamp) + '.jpg'
                    local_file = open(img_name, 'wb')

                    resp.raw.decode_content = True

                    shutil.copyfileobj(resp.raw, local_file)

                    del resp

        os.remove("output")
    
    except:
        print('Failed to download for ' + userid)

    if id_num == num_of_ids:
        break

    # FUNGSI COUNTDOWN UNTUK MEMBERI DELAY ANTARA CRAWLING
    def countdown(n):

        sys.stdout.write("[%s]" % (" " * n))
        sys.stdout.flush()
        sys.stdout.write("\b" * (n+1))

        print("Next download in " + str(n) + " seconds")

        for i in range(n):
            time.sleep(1)

            sys.stdout.write(str(i))
            sys.stdout.flush()

        sys.stdout.write("]\n")

    print("Checking download queue")
    countdown(timer)

print('FINISHED CRAWLING')