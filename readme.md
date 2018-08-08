docker-buckend-test
====
# what's this?
Run as web server (web-api).
Return test result for backend connectivity.

e.g.
```
http://0.0.0.0:5000/tcp/google.com:80

{"result": "OK", "message": "all ok."}

http://0.0.0.0:5000/tcp/google.coma:80

{"result": "NG", "message": "[Errno 8] nodename nor servname provided, or not known"}
```

# Run
`docker run -it -p 5000:5000 himaoka/docker-backend-test`

# Environments
`HC_URL` healthcheck URL (default '/'). Anytime return OK!  
`CONN_TIMEOUT` tcp connection timeout res = second. (default 10)  
`CONTAINER_PORT` Bind port @ container (for fargate)  
