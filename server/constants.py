import re

from flask import jsonify

email_pattern = re.compile('[\\w.]+@[\\w]+.[\\w]+', re.IGNORECASE)
json_tag = {'Content-Type': 'application/json'}
max_email_length = 255
max_password_length = 255
max_size = 48


def malformed_request(): return jsonify(
    error="Malformed request"), 422, json_tag


def internal_error(): return jsonify(error="Internal server error"), 500, json_tag
