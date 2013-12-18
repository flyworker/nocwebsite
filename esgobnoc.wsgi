import sys,os,logging
import newrelic.agent
newrelic.agent.initialize('/var/www/esgobnoc/newrelic.ini')
dir = os.path.dirname(__file__)
sys.path.insert(0, dir)
logging.basicConfig(stream=sys.stderr)
from main import app as application

#application = main.WSGIHandler()
#application = newrelic.agent.WSGIApplicationWrapper(application)