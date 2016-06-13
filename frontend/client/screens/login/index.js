import './styles.less';
import React from 'react';
import sha256 from 'sha256';
import Paper from 'material-ui/Paper';
import { browserHistory } from 'react-router';
import TextField from 'material-ui/TextField';
import RaisedButton from 'material-ui/RaisedButton';
import BasicFooter from '../../components/basic-footer';
import { PORT, setAuthenticated, ajax } from '../../globals';

class Login extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			'errorCode': '',
		}
	}

	onEnter = (e) => {
		if (e.keyCode == 13) { this.onLogin() }
	}

	onLogin = () => {
		// TODO: validate first
		this._onLogin(this.refs.email.getValue(), this.refs.password.getValue()); 
	}

	_onLogin = (_email, _password) => {
		let url = 'http://'+ location.hostname + ':' + PORT +'/login';
		let payload = {
			email: _email,
			password: sha256(_password),
		};

		ajax(payload, url, this.completeLogin, this.completeLogin)
	}

	completeLogin = (data) => {
		if (data.success) {
			this.setState({
				errorCode: '',
			})
			setAuthenticated(true);
			browserHistory.push('/dashboard');
		}
		else {
			this.setState({
				errorCode: data.error ? data.error : 'NOT_CONNECT_TO_SERVER',
			})
		}
	}

	render() {
		let errorText = this.state.errorCode == 'BAD_PAYLOAD'			      ? 	'Bad data sent to server' 					      :
										this.state.errorCode == 'BAD_LOGIN_DATA'		    ? 	'Email address or password is incorrect'  :
										this.state.errorCode == 'INTERNAL_ERROR'		    ? 	'Internal error. Please try again'			  :
										this.state.errorCode == 'NOT_CONNECT_TO_SERVER'	? 	'Cannot connect to server'					      :
										                                              			''                  											;
		return(
			<div className="login-container">
				<div className="header-text">Omnicron</div>
				<div className="header-detail">Sign in with your Omnicron Account</div>
				<Paper className="login-paper">
					<div className="login-avatar">
						<img src="/assets/images/noProfile.png"/>
					</div>
					<TextField
						className="login-email"
						hintText="Email Address"
						floatingLabelText="Email"
						ref="email"
						onKeyDown={this.onEnter}/>
					<TextField
						className="login-password"
						hintText="Password"
						floatingLabelText="Password"
						type="password"
						ref="password"
						onKeyDown={this.onEnter}/>
					<RaisedButton 
						className="login-signin" 
						label="Sign In" 
						secondary={true} 
						onClick={this.onLogin}/>
					<div className="login-error"><span>{errorText}</span></div>
				</Paper>
				<BasicFooter/>
			</div>
		)
	}
};

export default Login;