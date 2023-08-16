from flask import Flask, render_template, flash
from config import Config
import os
app = Flask(__name__)
app.config.from_object(Config)
from . import routes