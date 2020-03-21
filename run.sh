#!/usr/bin/env bash

gunicorn --workers=4 -b 0.0.0.0:8080 -D wsgi:app
