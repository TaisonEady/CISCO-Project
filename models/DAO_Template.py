class tableName(Resource)
    def post(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('fieldName', type=str, help='')
			#add additional argument here for each field
            args = parser.parse_args()

            _fieldName = args['fieldName']
			#add additional variables for each field

            db = get_db()
            cursor = db.execute('INSERT INTO tableName (fieldName, ...) values (?,...)',
                [_feildName, ...])
            data = cursor.fetchall()

            if len(data) is 0:
                db.commit()
                return {'tableName': {'fieldName': _fieldName, ...}}
            else:
                return {'Status Code': '1000', 'Message': str(data[0])}

        except Exception as e:
            return {'error': str(e)}

    def get(self):
        try:
            db = get_db()
            cursor = db.execute('SELECT fieldName, ... FROM tableName ORDER BY fieldName')
            data = cursor.fetchall()
	
            tableName_list = []
            for tableName in data:
                i = {
                    'fieldName': tableName[0],
					#add additional items here for each field
                }
                tableName_list.append(i)
	
            return {'Status Code': '200', 'tableName': tableName_list}
	
        except Exception as e:
            return {'error': str(e)}
