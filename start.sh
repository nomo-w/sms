nohup python3 axflix_server.py > axflix_server.out &
nohup python3 balance_server.py > balance_server.out &
nohup python3 queue_api.py > queue_api.out &
nohup python3 sender.py > sender.out &
nohup python3 auto_telegram.py > auto_telegram.out &
nohup /usr/local/bin/gunicorn -w 20 -b 0.0.0.0:8888 web:app > web.out &
