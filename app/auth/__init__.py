# -*- coding: utf-8 -*-
from flask import Blueprint

auth = Blueprint('auth', __name__) #两个变量:蓝本的名字和蓝本所在的包或模块

from . import views