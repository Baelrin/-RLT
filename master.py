import logging

from motor.motor_asyncio import AsyncIOMotorClient

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_mongo_client():
    try:
        return AsyncIOMotorClient('mongodb://localhost:27017')
    except Exception as e:
        logger.error(f"Error connecting to MongoDB: {e}")
        return None


async def aggregate_salaries(dt_from, dt_upto, group_type):
    client = await get_mongo_client()
    if client is None:
        return {"error": "Failed to connect to MongoDB"}

    db = client.salary_data
    collection = db.salaries

    # MongoDB aggregation pipeline
    pipeline = [
        {"$match": {"date": {"$gte": dt_from, "$lte": dt_upto}}},
        {"$group": {
            "_id": {},
            "total_salary": {"$sum": "$salary"}
        }}
    ]

    # Adjusting the pipeline based on the group_type
    if group_type == "hour":
        pipeline[1]["_id"]["hour"] = {"$hour": "$date"}
    elif group_type == "day":
        pipeline[1]["_id"]["day"] = {"$dayOfMonth": "$date"}
    elif group_type == "month":
        pipeline[1]["_id"]["month"] = {"$month": "$date"}
    elif group_type == "week":
        pipeline[1]["_id"]["week"] = {"$week": "$date"}

    # Execute the aggregation
    try:
        cursor = collection.aggregate(pipeline)
        result = await cursor.to_list(length=None)
    except Exception as e:
        logger.error(f"Error executing aggregation: {e}")
        return {"error": "Failed to execute aggregation"}

    # Format the result
    dataset = [item['total_salary'] for item in result]
    labels = [str(item['_id']) for item in result]

    return {"dataset": dataset, "labels": labels}
