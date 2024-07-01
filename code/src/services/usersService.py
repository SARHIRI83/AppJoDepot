import datetime
from flask import Flask, current_app, render_template, request, jsonify, make_response, redirect, url_for
from flask_session import Session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import psycopg2
import psycopg2.extras
import os
import hashlib
import random
import string
import json
import logging
import urllib.parse
import qrcode
from datetime import date, datetime
from . import databaseService as db
from . import utilsService as utils
from . import offersService as offers
from . import ordersService as orders