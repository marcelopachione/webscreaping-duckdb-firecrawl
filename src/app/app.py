# Import packages
import os
import json
import duckdb
import logging
import datetime

from firecrawl import FirecrawlApp
from dotenv import load_dotenv
from bs4 import BeautifulSoup