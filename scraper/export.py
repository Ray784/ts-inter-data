import pymongo
file = open('num.txt', 'w')
client = pymongo.MongoClient("mongodb://RayMaster:GZX52SC7Rb9dXAuZ@cluster0-shard-00-00-arpax.mongodb.net:27017,cluster0-shard-00-01-arpax.mongodb.net:27017,cluster0-shard-00-02-arpax.mongodb.net:27017/db_3454?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.db_3454
collection = db.Results
for i in range(30, 65):
	file1 = open('data/data'+str(i)+'.txt', 'r')
	data = file1.read().split("\n\n")
	n = len(data)
	file.write(str(n)+"\n")
	ins_arr = []
	j = 0

	while j < n:
		obj = data[j]
		if obj.strip() != '':
			arr_data = obj.split("\n")
			hallticket = arr_data[1].split(':')[1].strip()
			exp_data = {
				'hallticket': hallticket, 
				'district': arr_data[2].split(':')[1].strip(), 
				'name': arr_data[3].split(':')[1].strip(), 
				'father': arr_data[4].split(':')[1].strip(), 
				'marks': '<br>'.join(arr_data[5:-4]), 
				'result': '<br>'.join(arr_data[-3:-1])
			}
			print(j, n, hallticket)
			ins_arr.append(exp_data)
			if(j % 100 == 0):
				print("inserting")
				collection.insert_many(ins_arr)
				ins_arr = []
				print("Done")
		j += 1

	print("inserting")
	collection.insert_many(ins_arr)
	print("Done")
	file1.close()
client.close()

