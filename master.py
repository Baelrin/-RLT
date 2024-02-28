import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

# MongoDB connection setup


async def get_mongo_client():
    try:
        return AsyncIOMotorClient('mongodb://localhost:27017')
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None


async def aggregate_salaries(dt_from, dt_upto, group_type):
    client = await get_mongo_client()
    if client is None:
        return {"error": "Failed to connect to MongoDB"}

    db = client.salary_data
    collection = db.salaries

    # Convert ISO format to datetime objects for MongoDB query
    dt_from_obj = datetime.fromisoformat(dt_from)
    dt_upto_obj = datetime.fromisoformat(dt_upto)

    # MongoDB aggregation pipeline
    pipeline = [
        {"$match": {"date": {"$gte": dt_from_obj, "$lte": dt_upto_obj}}},
        {"$group": {
            "_id": {
                "year": {"$year": "$date"},
                "month": {"$month": "$date"},
                "day": {"$dayOfMonth": "$date"},
                "hour": {"$hour": "$date"}
            },
            "total_salary": {"$sum": "$salary"}
        }}
    ]

    # Adjusting the pipeline based on the group_type
    if group_type == "hour":
        pipeline[1] = {
            "$group": {
                "_id": {
                    "year": {"$year": "$date"},
                    "month": {"$month": "$date"},
                    "day": {"$dayOfMonth": "$date"},
                    "hour": {"$hour": "$date"}
                },
                "total_salary": {"$sum": "$salary"}
            }
        }
    elif group_type == "day":
        pipeline[1] = {
            "$group": {
                "_id": {
                    "year": {"$year": "$date"},
                    "month": {"$month": "$date"},
                    "day": {"$dayOfMonth": "$date"}
                },
                "total_salary": {"$sum": "$salary"}
            }
        }
    elif group_type == "month":
        pipeline[1] = {
            "$group": {
                "_id": {
                    "year": {"$year": "$date"},
                    "month": {"$month": "$date"}
                },
                "total_salary": {"$sum": "$salary"}
            }
        }
    elif group_type == "week":
        pipeline[1] = {
            "$group": {
                "_id": {
                    "year": {"$year": "$date"},
                    "week": {"$week": "$date"}
                },
                "total_salary": {"$sum": "$salary"}
            }
        }

    # Execute the aggregation
    try:
        cursor = collection.aggregate(pipeline)
        result = await cursor.to_list(length=None)
    except Exception as e:
        print(f"Error executing aggregation: {e}")
        return {"error": "Failed to execute aggregation"}

    # Format the result
    dataset = [item['total_salary'] for item in result]
    labels = [str(item['_id']) for item in result]

    return {"dataset": dataset, "labels": labels}

# Example usage


async def main():
    result = await aggregate_salaries("2022-09-01T00:00:00", "2022-12-31T23:59:00", "month")
    print(result)

# Run the example
asyncio.run(main())
