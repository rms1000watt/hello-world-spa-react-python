import os
import json
import redis
import datetime
import tornado.web
import tornado.ioloop

ENABLE_LOGGING = True
SCRIPT_LOG_DESCRIPTION = 'AS'
CWD = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE =  CWD + '/config.json'

FailureMessages = {
	'UNABLE_CONTACT_DATASTORE':{'success':False,
		'data':'',
		'error':'UNABLE_CONTACT_DATASTORE'},
	'USER_NOT_EXIST':{'success':False,
		'data':'',
		'error':'USER_NOT_EXIST'},
	'USER_EXISTS':{'success':False,
		'data':'',
		'error':'USER_EXISTS'},
	'USER_NOT_AUTHORIZED':{'success':False,
		'data':'',
		'error':'USER_NOT_AUTHORIZED'},
	'BAD_PAYLOAD':{'success':False,
		'data':'',
		'error':'BAD_PAYLOAD'},
	'INTERNAL_ERROR':{'success':False,
		'data':'',
		'error':'INTERNAL_ERROR'},
	'WRONG_PASSWORD':{'success':False,
		'data':'',
		'error':'WRONG_PASSWORD'},
	'BAD_LOGIN_DATA':{'success':False,
		'data':'',
		'error':'BAD_LOGIN_DATA'},
	'NO_STATS':{'success':False,
		'data':'',
		'error':'NO_STATS'},
	'NOT_CONNECT_DATASTORE':{'success':False,
		'data':'',
		'error':'NOT_CONNECT_DATASTORE'},
	'DASHBOARD_NOT_READY':{'success':False,
		'data':'',
		'error':'DASHBOARD_NOT_READY'},
	'CONTACT_NOT_RECEIVED':{'success':False,
		'data':'',
		'error':'CONTACT_NOT_RECEIVED'},
}

SuccessMessages = {
	'CONTACT_RECEIVED':{'success':True,
		'data':'CONTACT_RECEIVED',
		'error':''},
	'BLANK_SUCCESS':{'success':True,
		'data':'',
		'error':''},
}

def main():
	with open(CONFIG_FILE) as configFile:
		config = json.load(configFile)

	if config:
		startServer(config)
	else:
		log('FAILURE: Cannot load config')


def startServer(config):
	autoReload = True if config['env'] == 'dev' or config['env'] == 'local' else False
	# TODO: xsrf
	settings = {
		'xsrf_cookies': False,
		'cookie_secret': {
			1: "SECRET_KEY_NUMBER_1",
			2: "SECRET_KEY_NUMBER_2",
			3: "SECRET_KEY_NUMBER_3"
		},
		'key_version': 2,
		'login_url': 'http://127.0.0.1:3000/login',
		'debug': True
	}
	application = tornado.web.Application([
		(r'/ping', PingHandler, dict(config=config)),
		(r'/login', LoginHandler, dict(config=config)),
		(r'/signup', SignUpHandler, dict(config=config)),
		(r'/dashboard', DashboardHandler, dict(config=config)),
		], autoreload=autoReload, **settings)

	application.listen(int(config['apiServer']['port']), config['apiServer']['ip'])
	log('Listening on %s:%s' %(config['apiServer']['ip'], config['apiServer']['port']))
	
	mainLoop = tornado.ioloop.IOLoop.instance()
	mainLoop.start()


class BaseHandler(tornado.web.RequestHandler):
	def initialize(self, config=None):
		self.config = config
		# TODO: Use global connection instead
		self.r = redis.Redis(host=config['redis']['ip'], port=config['redis']['port'], socket_timeout=10)

	def get_current_user(self):
		# TODO: Validate that user is still authenticated with DB
		return self.get_secure_cookie("web_user")

	def set_default_headers(self):
		# ADDED: Set specific origins so you can use Cookies with CORS
		# TODO: Generate list dynamically from config.json
		self.set_header('Access-Control-Allow-Origin', 'http://127.0.0.1:3000')
		self.set_header('Access-Control-Allow-Credentials', 'true')
		
	def options(self, *args, **kwargs):
		if 'Access-Control-Request-Method' in self.request.headers:
			self.set_header('Access-Control-Allow-Methods', self.request.headers['Access-Control-Request-Method'])

		if 'Access-Control-Request-Headers' in self.request.headers:
			self.set_header('Access-Control-Allow-Headers', self.request.headers['Access-Control-Request-Headers'])


class PingHandler(BaseHandler):
	def post(self):
		self.write('pong')

	def get(self):
		self.write('pong')


class LoginHandler(BaseHandler):
	def post(self):
		try: 
			payload = json.loads(self.request.body)
			email = payload['email'].lower()
			password = payload['password']
		except Exception as e: 
			log('LOGIN: FAILURE: BAD_PAYLOAD')
			self.write(json.dumps(FailureMessages['BAD_PAYLOAD']))
			return

		try: val = self.r.hget('users', email)
		except Exception as e:
			log('LOGIN: FAILURE: NOT_CONNECT_DATASTORE')
			self.write(json.dumps(FailureMessages['NOT_CONNECT_DATASTORE']))
			return

		if type(val) == type(None):
			log('LOGIN: FAILURE: BAD_LOGIN_DATA: %s' %(email))
			self.write(json.dumps(FailureMessages['BAD_LOGIN_DATA']))
			return

		try: user = json.loads(val)
		except Exception as e:
			log('LOGIN: FAILURE: BAD_DATA_DATASTORE: %s' %(val))
			self.write(json.dumps(FailureMessages['INTERNAL_ERROR']))
			return

		if user['password'] == password:
			log('LOGIN: SUCCESS: %s' %(email))
			# TODO: JWT?
			self.set_secure_cookie("web_user", json.dumps(user), expires_days=7, version=2)
			self.write(json.dumps(SuccessMessages['BLANK_SUCCESS']))
		else:
			log('LOGIN: FAILURE: BAD_LOGIN_DATA: PASSWORD: %s' %(email))
			self.write(json.dumps(FailureMessages['BAD_LOGIN_DATA']))


class SignUpHandler(BaseHandler):
	@tornado.web.asynchronous
	def post(self):
		try: 
			payload = json.loads(self.request.body)
			fname = payload['fname'] if 'fname' in payload else ''
			lname = payload['lname'] if 'lname' in payload else ''
			email = payload['email'].lower()
			password = payload['password']
		except Exception as e: 
			log('SIGNUP: FAILURE: BAD_PAYLOAD')
			self.write(json.dumps(FailureMessages['BAD_PAYLOAD']))
			self.finish()
			return

		try: val = self.r.hget('users', email)
		except Exception as e:
			log('SIGNUP: FAILURE: NOT_CONNECT_DATASTORE')
			self.write(json.dumps(FailureMessages['NOT_CONNECT_DATASTORE']))
			self.finish()
			return

		if type(val) != type(None):
			log('SIGNUP: FAILURE: USER_EXISTS: %s' %(email))
			self.write(json.dumps(FailureMessages['USER_EXISTS']))
			self.finish()
			return

		user = {'fname': fname, 'lname': lname, 'email': email, 'password': password}
		val = self.r.hset('users', email, json.dumps(user))
		if type(val) == type(None):
			log('SIGNUP: FAILURE: INTERNAL_ERROR')
			self.write(json.dumps(FailureMessages['INTERNAL_ERROR']))
			self.finish()
			return

		log('SIGNUP: SUCCESS: %s' %(email))
		self.set_secure_cookie("web_user", json.dumps(user), expires_days=7, version=2)
		self.write(json.dumps(SuccessMessages['BLANK_SUCCESS']))
		self.finish()


class DashboardHandler(BaseHandler):
	@tornado.web.authenticated
	def post(self):
		try: 
			payload = json.loads(self.request.body)
		except Exception as e: 
			log('DASHBOARD: FAILURE: Bad Payload: %s: %s' %(self.request.method, self.request.path))
			self.write(json.dumps(FailureMessages['BAD_PAYLOAD']))
			self.finish()
			return

		self.write(json.dumps(SuccessMessages['BLANK_SUCCESS']))
		self.finish()


def log(msg, toFile=False):
	line = '[%s] %s: %s' %(getDate(), SCRIPT_LOG_DESCRIPTION, msg)
	if ENABLE_LOGGING:
		print line
	if toFile:
		fp = '%s\%s.log' %(CWD, SCRIPT_LOG_DESCRIPTION) 
		with open(fp, 'a') as f:
			f.write(line)
			f.write('\r\n')


def getDate():
	return datetime.datetime.now().strftime('%H:%M:%S')


if __name__ == '__main__':
	main()