import datetime
from flask import Flask, json, send_file
from flask import request
from flask.helpers import make_response
from pymongo.common import validate_document_class
from flask_cors import CORS, cross_origin
from io import StringIO, BytesIO
import pandas as pd
import numpy as np
from sklearn import linear_model, svm
from sklearn.neighbors import KNeighborsRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn import tree
from flask import Flask, session
from flask import jsonify
from flask_session import Session
import pickle
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
import pymongo
from functools import wraps
from configparser import ConfigParser
import re