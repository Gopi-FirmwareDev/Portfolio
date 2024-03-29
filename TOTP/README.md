# TOTP (Time-based One-Time Password) Generator

This project implements a TOTP generator, providing a secure way to enable two-factor authentication (2FA) in your applications.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Login](#login)
    - [TOTP Verification](#totp-verification)
- [Contributing](#contributing)
- [License](#license)

## Introduction
TOTP, or Time-based One-Time Password, is a widely used method for implementing two-factor authentication (2FA). This project provides a simple TOTP generator that allows users to enhance the security of their accounts by requiring a time-sensitive one-time password in addition to a regular password.

## Features
- User authentication with a username and password.
- Generation of TOTP based on the current time.
- QR code provisioning for TOTP with support for popular authenticator apps.

## Getting Started
### Prerequisites
Make sure you have the following installed:
- Python (version 3.x)
- Flask
- pyotp
- qrcode
- io
  
### Usage
#### Login
1. Run the main code.
2. Access the login page by navigating to http://127.0.0.1:5000/login in your web browser.
3. Enter the provided username and password to log in; for example, the code uses Username: Gopi, Password: 12345.

#### TOTP Verification
- After login, you will be redirected to the TOTP verification page.
- Obtain the TOTP access by scanning the QR code. Click "Lost TOTP access using authenticator app" if not already done.
- Enter the TOTP generated by your authenticator app.
- Click "Submit TOTP" to verify.

## Contributing
Contributions are welcome! If you have any suggestions, improvements, or issues, feel free to open an issue or create a pull request.

## License
This project is licensed under the MIT License.
