from flask import Flask, request, Response
import pymongo, re
app = Flask(__name__)

start_temp = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no"><link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous"><link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet"><title>Results</title><style>body{margin: 5px;overflow-x: hidden;overflow-y: scroll;padding-left: 30px;font-family: poppins;cursor: context-menu;}html {scroll-behavior: smooth;}.center{display: block;margin: auto;}.card-body{background-color: #F7F7F7;}.card{padding: 20px;margin: 10px;border-radius: 2px;background-color: white;box-shadow: 0 10px 16px 0 rgba(0,0,0,0.2);transition: 0.3s;}.card-title{text-decoration: underline;}.display{height: 300px;}</style></head><body><br><br><div class="container"><div class="row"><div class="card col-md">'
end_temp = '</div></div></div></div><script src="https://cdn.jsdelivr.net/gh/google/code-prettify@master/loader/run_prettify.js"></script><script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script><script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script><script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script></body></html>'
form_temp = '<h2 style="display: block; margin: 0 auto;">Intermediate First Year Results 2020</h2><form action="/" method = "POST"><small id="response-help" class="form-text text-muted">Enter either hallticket number or name</small><div class="form-group row"><label class="col-sm-2 col-form-label" for="input1">Hallticket number</label><div class="col-md-10"><input type="text" class="form-control" id="input1" name="hallticket"></div></div><div class="form-group row"><label class="col-sm-2 col-form-label" for="input1">Name</label><div class="col-md-10"><input type="text" class="form-control" id="input1" name="name"></div></div><button type="submit" class="btn btn-primary">Find</button></form>'
error_temp = '<div class="alert alert-danger" role="alert">Enter atleast one of the following</div>'

list_begin = '<ul class="list-group list-group-flush">'
list_item = '<li class="list-group-item">'

acc_link_begin_1 = '<h5 class="mb-0">'
acc_link_begin_2 = '<button class="btn btn-primary collapsed" style="margin-left: 10px;" type="button" data-toggle="collapse" data-target="#'
acc_link_begin_3 = '" aria-expanded="false">''Get</button></h5><div id="'
acc_link_begin_4 = '" class="collapse"><div class="card-body">'
acc_link_end = '</div></div>'

@app.route('/', methods = ['GET'])
def index():
	return start_temp + form_temp + end_temp

@app.route('/', methods = ['POST'])
def indexCandidates():
	name = request.form['name']
	hallticket = request.form['hallticket']
	if name.strip() != '':
		client = pymongo.MongoClient("mongodb://RayMaster:GZX52SC7Rb9dXAuZ@cluster0-shard-00-00-arpax.mongodb.net:27017,cluster0-shard-00-01-arpax.mongodb.net:27017,cluster0-shard-00-02-arpax.mongodb.net:27017/db_3454?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
		db = client.db_3454
		collection = db.Results
		candidate_temp = '<br>' + list_begin
		i = 0 
		chk = 0
		for document in collection.find({"name" : re.compile(".*"+name.upper()+" .*")}).sort("name"):
			chk = 1
			candidate_temp += list_item + acc_link_begin_1 + document['name'] + " : " + document['hallticket'] + acc_link_begin_2 + "acc"+str(i) + acc_link_begin_3 + "acc"+str(i) + acc_link_begin_4 + getResult(document) + acc_link_end + '</li>'
			i += 1
		if chk == 0:
			candidate_temp += getResult(None)
		client.close()
		candidate_temp += '</ul>'
	elif hallticket.strip() != '':
		client = pymongo.MongoClient("mongodb://RayMaster:GZX52SC7Rb9dXAuZ@cluster0-shard-00-00-arpax.mongodb.net:27017,cluster0-shard-00-01-arpax.mongodb.net:27017,cluster0-shard-00-02-arpax.mongodb.net:27017/db_3454?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
		db = client.db_3454
		collection = db.Results
		candidate_temp = list_begin
		document = collection.find_one({"hallticket" : hallticket})
		candidate_temp += getResult(document)
		client.close()
	else:
		return start_temp + error_temp + form_temp + end_temp
	return start_temp + form_temp + candidate_temp + end_temp

def getResult(document):
	if document == None:
		return '<small  class="form-text text-muted"><font style="color:red">Enter a valid hallticket number or name</font></small>'
	return list_begin + list_item + '<b>Intermediate Public Examinations First Year March-2020</b></li>' + list_item + '<b>Hallticket Number: </b>' + document['hallticket'] + '</li>' + list_item + '<b>Name: </b>' + document['name'] + '</li>' + list_item + "<b>Father's Name: </b>" + document['father'] + '</li>' + list_item + '<b>District: </b>' + document['district'] + '</li>' + list_item + document['marks'] + '</li>' + list_item + document['result'] + '</li>' + '</ul>'