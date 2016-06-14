# API

Python Tornado Web. Configure api through config.json.

## Requirements

Requires Redis. Default configuration has Redis running on localhost:6389. 

Assumes you have a hashset named `users` with keys `email` and values being json with `email` and `password`.

users 
<br/>&nbsp;&nbsp;&nbsp;&nbsp;ryan@example.com 
<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{"email":"ryan@example.com","password":"sha256hashedpassword1"}
<br/>&nbsp;&nbsp;&nbsp;&nbsp;fred@example.com 
<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{"email":"fred@example.com","password":"sha256hashedpassword2"}

## Run

```
python apiServer.py
```

## Todo:

- [ ] Signup