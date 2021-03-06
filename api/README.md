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

Go to `http://127.0.0.1:3000/signup` to add users.

## Install

#### Install Redis (as datastore)
```
brew install redis
```

#### Install Python requirements
```
sudo pip install -r requirements.txt
```

## Run

```
redis-server
```

```
python apiServer.py
```

## Todo:

- [ ] SQLAlchemy
- [ ] Async DB requests