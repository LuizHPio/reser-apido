#!/bin/bash

watchmedo auto-restart --directory=./ --pattern="*.py;*.tpl;*.js" --recursive -- python route.py