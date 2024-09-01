import pymongo
def id():
    # Replace these with your MongoDB connection details
    mongodb_url = "MONGO_url"
    database_name = "ED2100"
    collection_name1 = "users"
    # Connect to MongoDB
    client = pymongo.MongoClient(mongodb_url)
    # Access the database and collection
    db = client[database_name]
    collection = db[collection_name1]
    # Query to retrieve one document from the collection
    query = {}
    # Projection to include only the '_id' field
    projection = {'_id': 1}
    # Retrieve one document from the collection with the specified projection
    document = collection.find_one(query, projection)
    if document:
        return document['_id']
    # Close the MongoDB connection
    client.close()
