### Create Session 
•menggunakan library telethon
•create session menggunakan proxy
•cek session active

### baca
•buat api id, api hash di https://my.telegram.org/auth

•beli proxy recindential 1GB 1$ di https://proxyscrape.com/purchase?type=new_residential&bandwidth=1&price_version=p1

•isi number.txt dengan nomor telegram yang mau di buat sessionsnya

•isi api id dan api hash telegram di config.json
•isi proxy di dalam scriptnya sesuaikan 

### install
```
git clone https://github.com/JerryM28/CreateSessions
```
```
cd CreateSessions
```
```
pip install -r requirements.txt
```
create sessions
```
python create.py
```
cek session active 
```
python ceksessions.py
