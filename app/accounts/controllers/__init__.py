from functools import wraps
from flask import request, jsonify, abort
import os

# Import module models
from ..models.user import *
from ..models.session import *
from ..models.search_terms import *