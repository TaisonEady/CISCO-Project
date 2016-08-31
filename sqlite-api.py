from flask import Flask, g
from flask_restful import Resource, Api, reqparse
from flask_restful.utils import cors
import sqlite3
import os

#from models import *

app = Flask(__name__)
api = Api(app)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flask.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print 'Initialized the database.'


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  return response
  
class subscription(Resource):
    def post(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('subscriptionName', type=str, help='Subscription name to create subscription')
            parser.add_argument('destinationGroupName', type=str, help='Destination group to create subscription')
            parser.add_argument('sensorName', type=str, help='Sensor Name to create subscription')
            parser.add_argument('subscriptionInterval', type=float, help='Interval for the new subscription')
            args = parser.parse_args()

            _subscriptionName = args['subscriptionName']
            _destinationGroupName = args['destinationGroupName']
            _sensorName = args['sensorName']
            _subscriptionInterval = args['subscriptionInterval']

            db = get_db()
            cursor = db.execute('INSERT INTO subscription (subscriptionName, destinationGroupName, sensorName, subscriptionInterval) values (?, ?, ?, ?)',
                [_subscriptionName, _destinationGroupName, _sensorName, _subscriptionInterval])
            data = cursor.fetchall()

            if len(data) is 0:
                db.commit()
                return {'subscription': {'subscriptionName': _subscriptionName,'destinationGroupName': _destinationGroupName, 'sensorName': _sensorName, 'subscriptionInterval': _subscriptionInterval}}
            else:
                return {'Status Code': '1000', 'Message': str(data[0])}

        except Exception as e:
            return {'error': str(e)}

    def get(self):
        try:
            db = get_db()
            cursor = db.execute('SELECT subscriptionName, destinationGroupName, sensorName, subscriptionInterval FROM subscription ORDER BY subscriptionName desc')
            data = cursor.fetchall()
	
            subscription_list = []
            for subsciption in data:
                i = {
                    'subscriptionName': subsciption[0],
                    'destinationGroupName': subsciption[1],
                    'sensorName': subsciption[2],
                    'subscriptionInterval': subscription[3]
                }
                subscription_list.append(i)
	
            return {'Status Code': '200', 'subscription': subscription_list}
	
        except Exception as e:
            return {'error': str(e)}

class destinationGroup(Resource):
    def post(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('destinationGroupName', type=str, help='')
            parser.add_argument('destinationGroupAddress', type=str, help='')
            parser.add_argument('destinationGroupPort', type=str, help='')
            parser.add_argument('destinationGroupEncoding', type=str, help='')
            parser.add_argument('destinationGroupProtocol', type=str, help='')
            args = parser.parse_args()

            _destinationGroupName = args['destinationGroupName']
            _destinationGroupAddress = args['destinationGroupAddress']
            _destinationGroupPort = args['destinationGroupPort']
            _destinationGroupEncoding = args['destinationGroupEncoding']
            _destinationGroupProtocol = args['destinationGroupProtocol']

            db = get_db()
            cursor = db.execute('INSERT INTO destinationGroup (destinationGroupName, destinationGroupAddress, destinationGroupPort, destinationGroupEncoding, destinationGroupProtocol) values (?, ?, ?, ?, ?)',
                [_destinationGroupName, _destinationGroupAddress, _destinationGroupPort, _destinationGroupEncoding, _destinationGroupProtocol])
            data = cursor.fetchall()

            if len(data) is 0:
                db.commit()
                return {
					'destinationGroup': {
						'destinationGroupName': _destinationGroupName,
						'destinationGroupAddress': _destinationGroupAddress,
						'destinationGroupPort': _destinationGroupPort,
						'destinationGroupEncoding': _destinationGroupEncoding,
						'destinationGroupProtocol': _destinationGroupProtocol
						}}
            else:
                return {'Status Code': '1000', 'Message': str(data[0])}

        except Exception as e:
            return {'error': str(e)}

    def get(self):
        try:
            db = get_db()
            cursor = db.execute('SELECT destinationGroupName, destinationGroupAddress destinationGroupPort, destinationGroupEncoding, destinationGroupProtocol FROM destinationGroup ORDER BY destinationGroupName')
            data = cursor.fetchall()
	
            destinationGroup_list = []
            for destinationGroup in data:
                i = {
                    'destinationGroupName': destinationGroup[0],
                    'destinationGroupAddress': destinationGroup[1],
                    'destinationGroupPort': destinationGroup[2],
                    'destinationGroupEncoding': destinationGroup[3],
                    'destinationGroupProtocol': destinationGroup[4]
                }
                destinationGroup_list.append(i)
	
            return {'Status Code': '200', 'destinationGroup': destinationGroup_list}
	
        except Exception as e:
            return {'error': str(e)}
    
class sensor(Resource):
    def post(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('sensorName', type=str, help='Sensor Name and primary key')
            args = parser.parse_args()

            _sensorName = args['sensorName']

            db = get_db()
            cursor = db.execute('INSERT INTO sensor (sensorName) values (?)',
                [_sensorName])
            data = cursor.fetchall()

            if len(data) is 0:
                db.commit()
                return {'sensor': {'sensorName': _sensorName}}
            else:
                return {'Status Code': '1000', 'Message': str(data[0])}

        except Exception as e:
            return {'error': str(e)}

    def get(self):
        try:
            db = get_db()
            cursor = db.execute('SELECT sensorName FROM sensor ORDER BY sensorName')
            data = cursor.fetchall()
	
            sensor_list = []
            for sensor in data:
                i = {
                    'sensorName': sensor[0],
                }
                sensor_list.append(i)
	
            return {'Status Code': '200', 'sensor': sensor_list}
	
        except Exception as e:
            return {'error': str(e)}

class policyGroup(Resource):
    def post(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('policyGroupName', type=str, help='')

            args = parser.parse_args()

            _fieldName = args['policyGroupName']

            db = get_db()
            cursor = db.execute('INSERT INTO policyGroup (policyGroupName) values (?)',
                [_policyGroupName])
            data = cursor.fetchall()

            if len(data) is 0:
                db.commit()
                return {'tableName': {'policyGroupName': _policyGroupName}}
            else:
                return {'Status Code': '1000', 'Message': str(data[0])}

        except Exception as e:
            return {'error': str(e)}

    def get(self):
        try:
            db = get_db()
            cursor = db.execute('SELECT policyGroupName FROM policyGroup ORDER BY policyGroupName')
            data = cursor.fetchall()
	
            policyGroupName_list = []
            for policyGroupName in data:
                i = {
                    'policyGroupName': policyGroupName[0],
                }
                policyGroupName_list.append(i)
	
            return {'Status Code': '200', 'policyGroupName': policyGroupName_list}
	
        except Exception as e:
            return {'error': str(e)}

class policy(Resource):
    def post(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('policyName', type=str, help='')
            parser.add_argument('policyDescription', type=str, help='')
            parser.add_argument('policyComment', type=str, help='')
            parser.add_argument('policyIdentifier', type=str, help='')
            parser.add_argument('policyPeriod', type=str, help='')
            
            args = parser.parse_args()

            _fieldName = args['policyName']
            _fieldName = args['policyDescription']
            _fieldName = args['policyComment']
            _fieldName = args['policyIdentifier']
            _fieldName = args['policyPeriod']

            db = get_db()
            cursor = db.execute('INSERT INTO policy (policyName, policyDescription, policyComment, policyIdentifier, policyPeriod) values (?,?,?,?,?)',
                [_policyName, _policyDescription, _policyComment, _policyIdentifier, _policyPeriod])
            data = cursor.fetchall()

            if len(data) is 0:
                db.commit()
                return {'policy': {'policyName': _policyName, 'policyDescription': _policyDescription}} 
            else:
                return {'Status Code': '1000', 'Message': str(data[0])}

        except Exception as e:
            return {'error': str(e)}

    def get(self):
        try:
            db = get_db()
            cursor = db.execute('SELECT policyName, policyDescription, policyComment, policyIdentifier, policyPeriod FROM policy ORDER BY policyName')
            data = cursor.fetchall()
	
            policy_list = []
            for policy in data:
                i = {
                    'policyName': policy[0],
                    'policyDescription': policy[1],
                    'policyComment': policy[2],
                    'policyIdentifier': policy[3],
                    'policyPeriod': policy[4]
                }
                tableName_list.append(i)
	
            return {'Status Code': '200', 'policy': policy_list}
	
        except Exception as e:
            return {'error': str(e)}

class sensorPath(Resource):
    def post(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('sensorPathName', type=str, help='')
            parser.add_argument('sensorPath', type=str, help='')
            
            args = parser.parse_args()

            _sensorPathName = args['sensorPathName']
            _sensorPath = args['sensorPath']

            db = get_db()
            cursor = db.execute('INSERT INTO sensorPath (sensorPathName, sensorPath) values (?,?)',
                [_sensorPathName, _sensorPath])
            data = cursor.fetchall()

            if len(data) is 0:
                db.commit()
                return {'sensorPath': {'sensorPathName': _sensorPathName}}
            else:
                return {'Status Code': '1000', 'Message': str(data[0])}

        except Exception as e:
            return {'error': str(e)}

    def get(self):
        try:
            db = get_db()
            cursor = db.execute('SELECT sensorPathName, sensorPath FROM sensorPath ORDER BY sensorPathName')
            data = cursor.fetchall()
	
            sensorPath_list = []
            for sensorPath in data:
                i = {
                    'sensorPathName': sensorPath[0],
                    'sensorPath': sensorPath[1]
                }
                sensorPath_list.append(i)
	
            return {'Status Code': '200', 'sensorPath': sensorPath_list}
	
        except Exception as e:
            return {'error': str(e)}

class linkSensorPath(Resource):
    def post(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('sensorPathName', type=str, help='')
            parser.add_argument('sensorName', type=str, help='')
            
            args = parser.parse_args()

            _sensorPathName = args['sensorPathName']
            _sensorPath = args['sensorName']

            db = get_db()
            cursor = db.execute('INSERT INTO linkSensorPath (sensorPathName, sensorName) values (?,?)',
                [_sensorPathName, _sensorName])
            data = cursor.fetchall()

            if len(data) is 0:
                db.commit()
                return {'sensorPath': {'sensorPathName': _sensorPathName}}
            else:
                return {'Status Code': '1000', 'Message': str(data[0])}

        except Exception as e:
            return {'error': str(e)}

    def get(self):
        try:
            db = get_db()
            cursor = db.execute('SELECT sensorPathName, sensorName FROM linkSensorPath')
            data = cursor.fetchall()
	
            linkSensorPath_list = []
            for linkSensorPath in data:
                i = {
                    'sensorPathName': linkSensorPath[0],
                    'sensorName': linSensorPath[1]
                }
                linkSensorPath_list.append(i)
	
            return {'Status Code': '200', 'linkSensorPath': linkSensorPath_list}
	
        except Exception as e:
            return {'error': str(e)}

class policyPath(Resource):
    def post(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('policyPathName', type=str, help='')
            parser.add_argument('policyPath', type=str, help='')
            
            args = parser.parse_args()

            _policyPathName = args['policyPathName']
            _policyPath = args['policyPath']

            db = get_db()
            cursor = db.execute('INSERT INTO policyPath (policyPathName, policyPath) values (?,?)',
                [_policyPathName, _policyPath])
            data = cursor.fetchall()

            if len(data) is 0:
                db.commit()
                return {'policyPath': {'policyPathName': _policyPathName}}
            else:
                return {'Status Code': '1000', 'Message': str(data[0])}

        except Exception as e:
            return {'error': str(e)}

    def get(self):
        try:
            db = get_db()
            cursor = db.execute('SELECT policyPathName, policyPath FROM policyPath')
            data = cursor.fetchall()
	
            policyPath_list = []
            for policyPath in data:
                i = {
                    'policyPathName': sensorPath[0],
                    'policyPath': sensorPath[1]
                }
                sensorPath_list.append(i)
	
            return {'Status Code': '200', 'policyPath': policyPath_list}
	
        except Exception as e:
            return {'error': str(e)}

class linkPolicyPath(Resource):
    def post(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('policyPathName', type=str, help='')
            parser.add_argument('policyName', type=str, help='')
            
            args = parser.parse_args()

            _policyPathName = args['policyPathName']
            _policyPath = args['policyName']

            db = get_db()
            cursor = db.execute('INSERT INTO linkPolicyPath (policyPathName, policyName) values (?,?)',
                [_policyPathName, _policyName])
            data = cursor.fetchall()

            if len(data) is 0:
                db.commit()
                return {'policyPath': {'policyPathName': _policyPathName}}
            else:
                return {'Status Code': '1000', 'Message': str(data[0])}

        except Exception as e:
            return {'error': str(e)}

    def get(self):
        try:
            db = get_db()
            cursor = db.execute('SELECT policyPathName, policyName FROM linkPolicyPath')
            data = cursor.fetchall()
	
            linkPolicyPath_list = []
            for linkPolicyPath in data:
                i = {
                    'policyPathName': linkPolicyPath[0],
                    'policyName': linPolicyPath[1]
                }
                linkPolicyPath_list.append(i)
	
            return {'Status Code': '200', 'linkPolicyPath': linkPolicyPath_list}
	
        except Exception as e:
            return {'error': str(e)}

class collector(Resource):
    def post(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('collectorName', type=str, help='')
            parser.add_argument('collectorAddress', type=str, help='')
            parser.add_argument('collectorPort', type=str, help='')
            parser.add_argument('collectorEncoding', type=str, help='')
            parser.add_argument('collectorProtocol', type=str, help='')
            args = parser.parse_args()

            _collectorName = args['collectorName']
            _collectorAddress = args['collectorAddress']
            _collectorPort = args['collectorPort']
            _collectorEncoding = args['collectorEncoding']
            _collectorProtocol = args['collectorProtocol']

            db = get_db()
            cursor = db.execute('INSERT INTO collectorName (collectorName, collectorAddress, collectorPort, collectorEncoding, collectorProtocol) values (?, ?, ?, ?, ?)',
                [_collectorName, _collectorAddress, _collectorPort, _collectorEncoding, _collectorProtocol])
            data = cursor.fetchall()

            if len(data) is 0:
                db.commit()
                return {
					'collector': {
						'collectorName': _collectorName,
						'collectorAddress': _collectorAddress,
						'collectorPort': _collectorPort,
						'collectorEncoding': _collectorEncoding,
						'collectorProtocol': _collectorProtocol
						}}
            else:
                return {'Status Code': '1000', 'Message': str(data[0])}

        except Exception as e:
            return {'error': str(e)}

    def get(self):
        try:
            db = get_db()
            cursor = db.execute('SELECT collectorName, collectorAddress, collectorPort, collectorEncoding, collectorProtocol FROM collector ORDER BY collectorName')
            data = cursor.fetchall()
	
            destinationGroup_list = []
            for destinationGroup in data:
                i = {
                    'collectorName': collector[0],
                    'collectorAddress': collector[1],
                    'collectorPort': collector[2],
                    'collectorEncoding': collector[3],
                    'collectorProtocol': collector[4]
                }
                collector_list.append(i)
	
            return {'Status Code': '200', 'collector': collector_list}
	
        except Exception as e:
            return {'error': str(e)}

#~ #TODO
#~ class router(Resource)
    #~ def post(self):
        #~ try:
            #~ # Parse the arguments
            #~ parser = reqparse.RequestParser()
            #~ parser.add_argument('routerName', type=str, help='')
            #~ parser.add_argument('routerAddress', type=str, help='')
            #~ args = parser.parse_args()

            #~ _routerName = args['routerName']
			#~ _routerAddress = args['routerAddress']

            #~ db = get_db()
            #~ cursor = db.execute('INSERT INTO router (routerName, routerAddress) values (?,?)',
                #~ [_routerName, ...])
            #~ data = cursor.fetchall()

            #~ if len(data) is 0:
                #~ db.commit()
                #~ return {'tableName': {'fieldName': _fieldName, ...}}
            #~ else:
                #~ return {'Status Code': '1000', 'Message': str(data[0])}

        #~ except Exception as e:
            #~ return {'error': str(e)}

    #~ def get(self):
        #~ try:
            #~ db = get_db()
            #~ cursor = db.execute('SELECT fieldName, ... FROM tableName ORDER BY fieldName')
            #~ data = cursor.fetchall()
	
            #~ tableName_list = []
            #~ for tableName in data:
                #~ i = {
                    #~ 'fieldName': tableName[0],
					#~ #add additional items here for each field
                #~ }
                #~ tableName_list.append(i)
	
            #~ return {'Status Code': '200', 'tableName': tableName_list}
	
        #~ except Exception as e:
            #~ return {'error': str(e)}
#~ #TODO
#~ class linkPolicyRouter(Resource)
    #~ def post(self):
        #~ try:
            #~ # Parse the arguments
            #~ parser = reqparse.RequestParser()
            #~ parser.add_argument('fieldName', type=str, help='')
			#~ #add additional argument here for each field
            #~ args = parser.parse_args()

            #~ _fieldName = args['fieldName']
			#~ #add additional variables for each field

            #~ db = get_db()
            #~ cursor = db.execute('INSERT INTO tableName (fieldName, ...) values (?,...)',
                #~ [_feildName, ...])
            #~ data = cursor.fetchall()

            #~ if len(data) is 0:
                #~ db.commit()
                #~ return {'tableName': {'fieldName': _fieldName, ...}}
            #~ else:
                #~ return {'Status Code': '1000', 'Message': str(data[0])}

        #~ except Exception as e:
            #~ return {'error': str(e)}

    #~ def get(self):
        #~ try:
            #~ db = get_db()
            #~ cursor = db.execute('SELECT fieldName, ... FROM tableName ORDER BY fieldName')
            #~ data = cursor.fetchall()
	
            #~ tableName_list = []
            #~ for tableName in data:
                #~ i = {
                    #~ 'fieldName': tableName[0],
					#~ #add additional items here for each field
                #~ }
                #~ tableName_list.append(i)
	
            #~ return {'Status Code': '200', 'tableName': tableName_list}
	
        #~ except Exception as e:
            #~ return {'error': str(e)}
#~ #TODO
#~ class linkSubscriptionRouter(Resource)
    #~ def post(self):
        #~ try:
            #~ # Parse the arguments
            #~ parser = reqparse.RequestParser()
            #~ parser.add_argument('fieldName', type=str, help='')
			#~ #add additional argument here for each field
            #~ args = parser.parse_args()

            #~ _fieldName = args['fieldName']
			#~ #add additional variables for each field

            #~ db = get_db()
            #~ cursor = db.execute('INSERT INTO tableName (fieldName, ...) values (?,...)',
                #~ [_feildName, ...])
            #~ data = cursor.fetchall()

            #~ if len(data) is 0:
                #~ db.commit()
                #~ return {'tableName': {'fieldName': _fieldName, ...}}
            #~ else:
                #~ return {'Status Code': '1000', 'Message': str(data[0])}

        #~ except Exception as e:
            #~ return {'error': str(e)}

    #~ def get(self):
        #~ try:
            #~ db = get_db()
            #~ cursor = db.execute('SELECT fieldName, ... FROM tableName ORDER BY fieldName')
            #~ data = cursor.fetchall()
	
            #~ tableName_list = []
            #~ for tableName in data:
                #~ i = {
                    #~ 'fieldName': tableName[0],
					#~ #add additional items here for each field
                #~ }
                #~ tableName_list.append(i)
	
            #~ return {'Status Code': '200', 'tableName': tableName_list}
	
        #~ except Exception as e:
            #~ return {'error': str(e)}

api.add_resource(subscription, '/subscription')
api.add_resource(destinationGroup, '/destinationGroup')
api.add_resource(sensor, '/sensor')
api.add_resource(policyGroup, '/policyGroup')
api.add_resource(policy, '/policy')
api.add_resource(sensorPath, '/sensorPath')
api.add_resource(linkSensorPath, '/linkSensorPath')
api.add_resource(policyPath, '/policyPath')
api.add_resource(linkPolicyPath, '/linkPolicyPath')
api.add_resource(collector, '/collector')
#api.add_resource(router, '/router')
#api.add_resource(linkPolicyRouter, '/linkPolicyRouter')
#api.add_resource(linkSubscriptionRouter, '/linkSubscriptionRouter')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)

