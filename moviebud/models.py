from py2neo import Graph, Node, Relationship, authenticate
#from passlib.hash import bcrypt
from datetime import datetime
import os
import uuid

graph = Graph()

class User:
    def __init__(self, login):
        self.login = login

    def find(self):
        user = graph.find_one("User", "login", self.login)
        return user
        
    def get_name(self):
    	query = """MATCH(n:User) WHERE n.login = {log}
		return n.name""" 
	return graph.cypher.execute(query, log=self.login)
	
    def register(self, password):
        if not self.find():
            user = Node("User", login=self.login, password=password, roles="ROLE_USER", name=self.login)
            graph.create(user)
            return True
        else:
            return False
            
    def verify_password(self, password):
        user = self.find()
        if user:
            return password == user['password']
        else:
            return False
            
    def get_mutual_friends(self):
    	query = """MATCH (n:User)-[:FRIEND*2..2]->(mut:User) 
    		WHERE n.login={param} AND NOT (n)-[:FRIEND]-(mut:User) 
    		RETURN mut.name, count(*), mut.login"""
    		
    	return graph.cypher.execute(query, param=self.login)
    	
    def movie_pref(self):
    	query = """match(n:User)-[r:RATED]->(m:Movie)<-[x:RATED]-(them:User)
		WHERE r.stars>=3 AND x.stars>=3 AND n.login = {log}
		return them.name, m.title, them.login"""
	
	return graph.cypher.execute(query, log = self.login)
	
    def add_friend(self, friendtoadd):
	query = """MATCH (a:User),(b:User)
		WHERE a.login = {me} AND b.login = {friendtoadd} 
		CREATE (a)-[r:FRIEND]->(b) RETURN r"""
		
	return graph.cypher.execute(query, me = self.login, friendtoadd = friendtoadd)
	
    def friend_recommendation(self):
    	query = """match(n:User)-[r:RATED]->(m:Movie), (you:User)
		WHERE r.stars>=3 AND (you)-[:FRIEND]-(n) AND you.login={you}
		return m.title, n.name, r.comment"""
		
	return graph.cypher.execute(query, you = self.login)
    
    def genre_recommendation(self):
	query1 = """match(n:User)-[r:RATED]->(m:Movie)
		WHERE r.stars>=3 AND n.login={you}
		return m.genre, count(*)
		ORDER by count(*) DESC limit 1"""
		
	genre = graph.cypher.execute(query1, you = self.login)
	
	query2 = "match(m:Movie) WHERE m.genre={param} return m.title, m.genre limit 5"
	
	return graph.cypher.execute(query2, param = genre[0][0])

    def moviedetails(self, title):
    	query = "MATCH(m:Movie) WHERE m.title={param} RETURN m.studio, m.genre, m.trailer, m.imdbId, m.title, m.description, m.tagline LIMIT 1"
    	
    	return graph.cypher.execute(query, param=title)
    	
    def rate(self, title, rating):
    	query = "MATCH (a:User),(b:Movie) WHERE a.login={param1} AND b.title={param2} CREATE (a)-[r:RATED {stars:{param3}}]->(b) RETURN r"
    	
    	return graph.cypher.execute(query, param1=self.login, param2=title, param3=rating)
