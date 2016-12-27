from neo4jrestclient.client import GraphDatabase
from neo4jrestclient import client

CONNECTION_STRING = 'bolt://localhost'


def start_up():
    db = GraphDatabase("http://localhost:7474", username="neo4j", password="neo4j")
    user = db.labels.create("User")
    u1 = db.nodes.create(name="Arthur")
    u2 = db.nodes.create(name="Bob")
    u3 = db.nodes.create(name="Alex")
    u4 = db.nodes.create(name="Strucinsky")
    u5 = db.nodes.create(name="Alice")
    u6 = db.nodes.create(name="Carol")
    user.add(u1, u2, u3, u4, u5, u6)

    interest = db.labels.create("Interests")
    i1 = db.nodes.create(name="Startups")
    i2 = db.nodes.create(name="Programming")
    interest.add(i1, i2)

    u1.relationships.create("likes", i1)
    u2.relationships.create("likes", i1)
    u3.relationships.create("likes", i2)
    u4.relationships.create("likes", i2)


def common_interests_count(first_user_name, second_user_name):
    db = GraphDatabase("http://localhost:7474", username="neo4j", password="neo4j")
    q = """MATCH (u:User { name: {first_user_name} })
           MATCH (o:User { name: {second_user_name} })
           OPTIONAL MATCH (u)-[r:likes]->(d)<-[:likes]-(o)
           RETURN count(r) as c
    """
    params = {
        "first_user_name": first_user_name,
        "second_user_name": second_user_name
    }
    return db.query(q, params=params, returns=int)[0]


def without_interests():
    db = GraphDatabase("http://localhost:7474", username="neo4j", password="neo4j")
    q = """MATCH (u:User)
           WHERE NOT (u)-[:likes]->(:Interests)
           RETURN u
    """
    return db.query(q, returns=client.Node)


if __name__ == "__main__":
    print(common_interests_count("Alex", "Strucinsky"))
    for n in without_interests():
        print(n[0]["name"])
