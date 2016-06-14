import './styles.less';
import React from 'react';
import sha256 from 'sha256';
import Paper from 'material-ui/Paper';
import { browserHistory } from 'react-router';
import TextField from 'material-ui/TextField';
import RaisedButton from 'material-ui/RaisedButton';
import BasicFooter from '../../components/basic-footer';
import { PORT, setAuthenticated, ajax } from '../../globals';

class Signup extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			'errorCode': '',
		}
	}

	onEnter = (e) => {
		if (e.keyCode == 13) { this.onSignup() }
	}

	onSignup = () => {
		// TODO: validate first
		this._onSignup(
			this.refs.fname.getValue(),
			this.refs.lname.getValue(),
			this.refs.email.getValue(), 
			this.refs.password.getValue()); 
	}

	_onSignup = (_fname, _lname, _email, _password) => {
		let url = 'http://'+ location.hostname + ':' + PORT +'/signup';
		let payload = {
			fname: _fname,
			lname: _lname,
			email: _email,
			password: sha256(_password),
		};

		ajax('POST', url, payload, this.completeSignup, this.completeSignup)
	}

	completeSignup = (data) => {
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
		let errorText = this.state.errorCode == 'BAD_PAYLOAD'				?	'Bad data sent to server' 					:
						this.state.errorCode == 'BAD_LOGIN_DATA'			?	'Email address or password is incorrect'	:
						this.state.errorCode == 'INTERNAL_ERROR'			?	'Internal error. Please try again'			:
						this.state.errorCode == 'USER_EXISTS'				?	'User already exists with this email'		:
						this.state.errorCode == 'NOT_CONNECT_TO_SERVER'		?	'Cannot connect to server'					:
										                                    	''                  						;
		return(
			<div className="signup-container">
				<div className="header-text">Omnicron</div>
				<div className="header-detail">Sign up for an Omnicron Account</div>
				<Paper className="signup-paper">
					<div className="signup-avatar">
						<img src="/assets/images/noProfile.png"/>
					</div>
					<TextField
						className="signup-fname"
						hintText="First Name"
						floatingLabelText="First Name"
						ref="fname"
						onKeyDown={this.onEnter}/>
					<TextField
						className="signup-lname"
						hintText="Last Name"
						floatingLabelText="Last Name"
						ref="lname"
						onKeyDown={this.onEnter}/>
					<TextField
						className="signup-email"
						hintText="Email Address"
						floatingLabelText="Email"
						ref="email"
						onKeyDown={this.onEnter}/>
					<TextField
						className="signup-password"
						hintText="Password"
						floatingLabelText="Password"
						type="password"
						ref="password"
						onKeyDown={this.onEnter}/>
					<RaisedButton 
						className="signup-button" 
						label="Sign Up" 
						secondary={true} 
						onClick={this.onSignup}/>
					<div className="signup-error"><span>{errorText}</span></div>
				</Paper>
				<BasicFooter threshold={821} height={40}/>
			</div>
		)
	}
};

export default Signup;