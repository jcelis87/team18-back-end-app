# Ubuntu server

To run the backend, type the following commands on the terminal.

```
cd ~/team18-back-end-app
pipenv shell
nohup python app.py &
deactivate
```

To run the frontend, type the following commands on the terminal.

```
cd ~/team18front-end-app
pipenv shell
nohup gunicorn -w 3 -b 0.0.0.0:8050 index:server &
deactivate
```

To check what processes are running on the server:
```
ps -x
```

To stop a process from the terminal:
```
kill [PID]
```