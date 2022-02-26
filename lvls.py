from pymongo import MongoClient
import discord
client = MongoClient('mongodb://mongo:4tuf0leqvNuG020Vb7WK@containers-us-west-29.railway.app:5998')
db = client['Levels']
xpcollection = db['users']
async def addxp(message, member: discord.Member):
	id = member.id
	member2 = xpcollection.find_one({'user': id})
	print(member2)
	if member2 == None:
		data = {'user': id, 'lvls': 0, 'dolevel' : 0}
		memberid = xpcollection.insert_one(data).inserted_id
		return
	a = member2["user"]
	b = member2['lvls']
	c = member2['dolevel']
	try:
		opit = member2['xp']
		
	except:
		pass
	
	print(member2)
	#id['xp'] =+ 5
	
	#levelstable = [1000,2000,3000,4000,5000,6000,7000,8000,9000,10000,11000,12000,13000,14000,15000,16000,17000,18000,19000,20000,21000,22000,23000,24000,25000,26000,27000,28000,29000,30000,31000,32000,33000,34000,35000,36000,37000,38000,39000,40000,41000,42000,43000,44000,45000,46000,47000,48,49,50,51,52,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97000,98000,99000]
	
	if member2['dolevel'] / 1000 >= 1: 
		if member2['dolevel'] == 0:
			xpcollection.update_one({
  			'user': a
			},{
  				'$set': {
    			'lvls': member2['lvls'] + 1,
    			'dolevel': member2['dolevel'] + 1
  			}
			}, upsert=False)
			print('Registred user id: ' + str(a) + '!')
			return
		
		xpcollection.update_one({
  		'user': a
		},{
  			'$set': {
    		'lvls': member2['lvls'] + 1,
    		'dolevel': member2['dolevel'] - 1000
  		}
		}, upsert=False)
		await message.channel.send('Поздравляем у вас ' + str(member2['lvls']) + ' уровень!')
		if member2['dolevel'] >= 1000:
			xpcollection.update_one({
  			'user': a
			},{
  				'$set': {
    			'dolevel': member2['dolevel'] - 1000
  			}
			}, upsert=False)
			
	xpcollection.update_one({
  	'user': a
	},{
  		'$set': {
    	'dolevel': member2['dolevel'] + 5
  	}
	}, upsert=False)
	a = None
def open_user(member: discord.Member):
	id = member
	member2 = xpcollection.find_one({'user': id})
	return member2
