"""
MongoDB database configuration and connection management.
"""
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
import os
from dotenv import load_dotenv

load_dotenv()


class Database:
    """Database connection manager"""
    client: AsyncIOMotorClient = None
    db = None


db = Database()


async def connect_to_mongo():
    """Establish connection to MongoDB"""
    mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    database_name = os.getenv("MONGODB_DATABASE", "petshop")
    
    try:
        db.client = AsyncIOMotorClient(mongodb_uri)
        db.db = db.client[database_name]
        
        # Test the connection
        await db.client.admin.command('ping')
        print(f"✓ Connected to MongoDB: {database_name}")
        
        # Initialize collections with sample data if empty
        await initialize_sample_data()
        
    except ConnectionFailure as e:
        print(f"✗ Failed to connect to MongoDB: {e}")
        raise


async def close_mongo_connection():
    """Close MongoDB connection"""
    if db.client:
        db.client.close()
        print("✓ Closed MongoDB connection")


async def get_database():
    """Get database instance"""
    return db.db


async def initialize_sample_data():
    """Initialize the database with sample pet data if empty"""
    pets_collection = db.db.pets
    
    # Check if pets collection is empty
    count = await pets_collection.count_documents({})
    if count == 0:
        sample_pets = [
            {
                "id": "pet001",
                "name": "Golden Retriever Puppy",
                "type": "dog",
                "description": "Friendly and energetic Golden Retriever puppy, great with families and children. Well-socialized and vaccinated.",
                "price": 1200.00,
                "age_months": 3,
                "available": True,
                "image_url": "https://example.com/golden-retriever.jpg"
            },
            {
                "id": "pet002",
                "name": "British Shorthair Kitten",
                "type": "cat",
                "description": "Adorable British Shorthair kitten with beautiful blue-gray coat. Calm and affectionate temperament.",
                "price": 800.00,
                "age_months": 2,
                "available": True,
                "image_url": "https://example.com/british-shorthair.jpg"
            },
            {
                "id": "pet003",
                "name": "Beagle",
                "type": "dog",
                "description": "Playful Beagle with excellent hunting instincts. Friendly, curious, and great for active families.",
                "price": 950.00,
                "age_months": 6,
                "available": True,
                "image_url": "https://example.com/beagle.jpg"
            },
            {
                "id": "pet004",
                "name": "Siamese Cat",
                "type": "cat",
                "description": "Elegant Siamese cat with striking blue eyes. Vocal, intelligent, and social personality.",
                "price": 650.00,
                "age_months": 8,
                "available": True,
                "image_url": "https://example.com/siamese.jpg"
            },
            {
                "id": "pet005",
                "name": "Cockatiel",
                "type": "bird",
                "description": "Hand-tamed Cockatiel with yellow crest. Whistles and mimics sounds, very social bird.",
                "price": 150.00,
                "age_months": 4,
                "available": True,
                "image_url": "https://example.com/cockatiel.jpg"
            },
            {
                "id": "pet006",
                "name": "Betta Fish",
                "type": "fish",
                "description": "Beautiful Betta fish with vibrant blue and red coloring. Low maintenance and stunning to watch.",
                "price": 25.00,
                "age_months": 6,
                "available": True,
                "image_url": "https://example.com/betta.jpg"
            },
            {
                "id": "pet007",
                "name": "Holland Lop Rabbit",
                "type": "rabbit",
                "description": "Sweet Holland Lop rabbit with soft fur and floppy ears. Gentle and perfect for families.",
                "price": 300.00,
                "age_months": 5,
                "available": True,
                "image_url": "https://example.com/holland-lop.jpg"
            },
            {
                "id": "pet008",
                "name": "Syrian Hamster",
                "type": "hamster",
                "description": "Friendly Syrian hamster with golden brown fur. Active and entertaining, great starter pet.",
                "price": 45.00,
                "age_months": 2,
                "available": True,
                "image_url": "https://example.com/hamster.jpg"
            },
            {
                "id": "pet009",
                "name": "German Shepherd Puppy",
                "type": "dog",
                "description": "Intelligent German Shepherd puppy with excellent temperament. Loyal, trainable, and protective.",
                "price": 1500.00,
                "age_months": 4,
                "available": True,
                "image_url": "https://example.com/german-shepherd.jpg"
            },
            {
                "id": "pet010",
                "name": "Parakeet Pair",
                "type": "bird",
                "description": "Bonded pair of colorful parakeets (blue and green). Social, playful, and chatter together.",
                "price": 80.00,
                "age_months": 7,
                "available": True,
                "image_url": "https://example.com/parakeets.jpg"
            }
        ]
        
        await pets_collection.insert_many(sample_pets)
        print(f"✓ Initialized database with {len(sample_pets)} sample pets")
