from flask import jsonify, request, make_response
from flask_restful import Resource, Api, abort,reqparse
from shared import mongo
from pymongo import errors as pyErr
from pymongo import ReturnDocument
import schemas
from bson.objectid import ObjectId
import os,json

class InsertRecord(Resource):
    def post(self,uuid=None):
        schema = schemas.RecordRequest()
        data, errors = schema.load(request.json)
        if errors:
            abort(401, message=str(errors))
#---------------------------------------------------------------
        if uuid is None:
            schema = schemas.Record()
            record,errors = schema.dump(data['record'])
            if errors:
                abort(401, message=str(errors))
            if 'parent_id' in record:
                if(record['parent_id'] == "None"):
                    del record['parent_id']
                elif mongo.db.record.find_one({'_id': ObjectId(record['parent_id'])}) is None:
                    abort(401, message="parent_id is invalid")
            try:
                uuid = str(mongo.db.record.insert(record))
            except pyErr.DuplicateKeyError:
                abort(401, message="DuplicateKeyError")
#---------------------------------------------------------------
        if 'accelerometres' in data:
            schema = schemas.Sensor(many=True)
            accelerometres,errors = schema.dump(data['accelerometres'])
            if errors:
                abort(401, message=str(errors))
            for datum in accelerometres:
                datum['ref'] = uuid

            mongo.db.accelerometres.insert(accelerometres)
#---------------------------------------------------------------
        if 'gyrometres' in data:
            schema = schemas.Sensor(many=True)
            gyrometres,errors = schema.dump(data['gyrometres'])
            if errors:
                abort(401, message=str(errors))
            for datum in gyrometres:
                datum['ref'] = uuid

            mongo.db.gyrometres.insert(gyrometres)
#---------------------------------------------------------------
        if 'magnetometres' in data:
            schema = schemas.Sensor(many=True)
            magnetometres,errors = schema.dump(data['magnetometres'])
            if errors:
                abort(401, message=str(errors))
            for datum in magnetometres:
                datum['ref'] = uuid

            mongo.db.magnetometres.insert(magnetometres)
#---------------------------------------------------------------
        jsonresult = dict(valeuruuid=uuid)
        schema = schemas.Uuid()
        return schema.dump(jsonresult)

class InsertAlgorithmResults(Resource):
    def post(self):
        print request.json
        schema = schemas.AlgorithmResults()
        data, errors = schema.load(request.json)
        if errors:
            print("There was an error.")
            print(str(errors))
            abort(401, message=str(errors))
        else:
            print("Json loaded, about to insert into Mongo.")
            mongo.db.algorithmResults.insert(data)
        return request.json

class getRecords(Resource):
    def get(self):
        print 'getRecords'
        schema = schemas.Record(many=True)
        return schema.dump(mongo.db.record.find())

class getAlgorithmResults(Resource):
    def get(self):
        print 'getAlgorithmResults'
        schema = schemas.AlgorithmResults(many=True)
        return schema.dump(mongo.db.algorithmResults.find())

class renameRecord(Resource):
    def post(self,uuid):
        name = request.args.get('name')
        schema = schemas.Record()
        return schema.dump(
        mongo.db.record.find_one_and_update(
        {'_id': ObjectId(uuid)},
        {'$set': {'name': name}},
        return_document=ReturnDocument.AFTER)
        )

class getDataWithOptions(Resource):
    def get(self):
        schemaDataRequestWithOptions = schemas.DataRequestWithOptions()
        dataRequestWithOptions, dataRequestWithOptionsErrors = schemaDataRequestWithOptions.load(request.json)
        if dataRequestWithOptionsErrors:
            abort(401, message=str(dataRequestWithOptionsErrors))

        # Retrieve Filter
        timeFilterSchema = schemas.TimeFilter()
        timeFilterData, timeFilterErrors = timeFilterSchema.load(dataRequestWithOptions['timeFilter'])
        if timeFilterErrors:
            abort(401, message=str(timeFilterErrors))

        # Retrieve Sort
        sortSchema = schemas.DataSort()
        sortData, sortErrors = sortSchema.load(dataRequestWithOptions['sort'])
        if sortErrors:
            abort(401, message=str(sortErrors))


        # Retrieve UUID
        uuidData, uuidErrors = schemaDataRequestWithOptions.load(dataRequestWithOptions['recordId'])
        if uuidErrors:
            abort(401, message='enter valid uuid')
            return

        recordSchema = schemas.Record()

        # Retrieve Samples for preview
        nbSamples = schemas.samples()
        if(nbSamples > 0):
            return recordSchema.dump(mongo.db.record.find({}, {'name': 1, '_id': uuidData}))

        # Build request
        #  No filter, no sort. Just return all the record matching the UUID
        if (timeFilterData is None) & (sortData is None):
            return recordSchema.dump(mongo.db.record.find({}, {'name': 1, '_id': uuidData}))

        # Filter and Sort the record that matches the UUID
        if (timeFilterData is not None) & (sortData is not None):
            start = timeFilterData['beginDateTime']
            end = timeFilterData['endDateTime']
            if sortData['sortedDirection'] == 1:
                return recordSchema.dump(
                    mongo.db.record.find({}, {'_id': uuidData, 'date':{'$lt': end, '$gte': start}}).sort(sortData['sortedColumn'], mongo.ASCENDING))
            elif sortData['sortedDirection'] == 2:
                return recordSchema.dump(
                    mongo.db.record.find({}, {'_id': uuidData, 'date':{'$lt': end, '$gte': start}}).sort(sortData['sortedColumn'], mongo.DESCENDING))
            else:
                return recordSchema.dump(mongo.db.record.find({'_id': uuidData, 'date':{'$lt': end, '$gte': start}}))

        # Filter only the record that matches the UUID
        if (timeFilterData is not None) & (sortData is None):
            start = timeFilterData['beginDateTime']
            end = timeFilterData['endDateTime']
            return recordSchema.dump(mongo.db.record.find({'_id': uuidData, 'date':{'$lt': end, '$gte': start}}))

        # Sort only the record that matches the UUID
        if (timeFilterData is None) & (sortData is not None):
            if sortData['sortedDirection'] == 1:
                return recordSchema.dump(mongo.db.record.find({'_id': uuidData}).sort(sortData['sortedColumn'], mongo.ASCENDING))
            elif sortData['sortedDirection'] == 2:
                return recordSchema.dump(mongo.db.record.find({'_id': uuidData}).sort(sortData['sortedColumn'], mongo.DESCENDING))
            else:
                return recordSchema.dump(mongo.db.record.find({'_id': uuidData}))

class GetData(Resource):
    def get(self):
        uuid = request.args.get('uuid')
        if uuid is None:
            abort(401,message='enter valid uuid')
            return
        schema = schemas.Record()
        record,errors = schema.dump(mongo.db.record.find_one({'_id': ObjectId(uuid)}))
        #if errors:
        #    abort(401, message=str(errors))
#--------------------------------------------------------------
        schema = schemas.Sensor(many=True)
        accelerometres,errors = schema.dump(mongo.db.accelerometres.find({'ref': uuid}))
        if errors:
            abort(401, message=str(errors))
#--------------------------------------------------------------
        schema = schemas.Sensor(many=True)
        magnetometres,errors = schema.dump(mongo.db.magnetometres.find({'ref': uuid}))
        if errors:
            abort(401, message=str(errors))
#--------------------------------------------------------------
        schema = schemas.Sensor(many=True)
        gyrometres,errors = schema.dump(mongo.db.gyrometres.find({'ref': uuid}))
        if errors:
            abort(401, message=str(errors))
#--------------------------------------------------------------
        schema = schemas.RecordRequest()
        result,errors = schema.load(dict([('record', record), ('accelerometres', accelerometres), ('magnetometres', magnetometres), ('gyrometres',gyrometres)]))
        #if errors:
            #abort(401, message=str(errors))
        return result

class DeleteData(Resource):
    def get(self):
        uuid = request.args.get('uuid')
        if uuid is None:
            abort(401,message='enter valid uuid')
        res1 = mongo.db.accelerometres.delete_many({'ref':uuid})
        res2 = mongo.db.gyrometres.delete_many({'ref':uuid})
        res3 = mongo.db.magnetometres.delete_many({'ref':uuid})
        res4 = mongo.db.record.delete_many({'_id':ObjectId(uuid)})
        result = res1.deleted_count+res2.deleted_count+res3.deleted_count+res4.deleted_count
        return 'Affected ' + str(result)     + ' entries.'


class Algo(Resource):
    def get(self):
        modulename = 'algos.'+request.args.get('filename')

        my_module = __import__(modulename, globals(), locals(), [request.args.get('filename')], -1)
        my_class = getattr(my_module,request.args.get('filename'))
        instance = my_class()
        instance.database = mongo
        instance.load(request.args)
        instance.before_run()
        instance.run()
        instance.after_run()
        return dict(instance.output)

class AlgoList(Resource):
    def get(self):
        jsondict = {}
        content = []
        algo = {}
        id = 0
        for file in os.listdir("../lib/algos"):
            if (file.endswith(".py") and not file.startswith('__') and not file.startswith("template")):
                filename = os.path.splitext(file)[0]
                id = id + 1
                modulename = 'algos.' + filename
                my_module = __import__(modulename, globals(), locals(), [filename], -1)
                my_class = getattr(my_module, os.path.splitext(file)[0])
                instance = my_class()

                params = []
                param = {}
                for keys in instance.params.keys():
                    param['name'] =  keys
                    try :
                        param['info'] = instance.infos[keys]
                        param['possible_values'] = instance.possible[keys]
                    except:
                        pass

                    param['default'] = instance.params[keys]
                    params.append(param.copy())

                algo['id'] = id
                algo['filename'] = filename
                algo['name'] = instance.name
                algo['params'] = params
                algo['author'] = instance.author
                algo['description'] = instance.description
                algo['details'] = instance.details

                content.append(algo.copy())

        jsondict['algorithms'] = content
        return (jsondict)

class Position(Resource):
    def get(self):
        schema = schemas.Position(many=True)
        positions,errors = schema.dump(mongo.db.position.find())
        if errors:
            abort(401, message=str(errors))
        return positions

    def post(self):
        schema = schemas.Position()
        position, errors = schema.load(request.json)
        if errors:
            abort(401, message=str(errors))
        mongo.db.position.insert(position)
        return

    def delete(self):
        name = request.args.get('pos')
        if name is None:
            abort(401,message='enter valid name')
        res = mongo.db.position.delete_many({'name':name})
        return 'Affected ' + str(res.deleted_count) + ' entries.'


class TestInsert(Resource):
    def get(self):
        import numpy
        snaps = []
        amp = 100
        fs = 20

        uuid = ObjectId('57ed3f20e0034625e8fa61f1')
        dict = [
            {'x': int(amp*numpy.sin (2*numpy.pi*r/fs)),
             'y': int(amp*numpy.sin (2*numpy.pi*r/fs)),
             'z': int(amp*numpy.sin (2*numpy.pi*r/fs)),
             't': r,
             '_id': uuid
            } for r in range(1, fs)]
        schema = schemas.Sensor(many=True)
        result, _ = schema.load(dict)

        mongo.db.accelerometres.insert(result)
