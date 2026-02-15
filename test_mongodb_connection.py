#!/usr/bin/env python3
"""Test MongoDB connection"""

import sys
sys.path.insert(0, 'src')

from dotenv import load_dotenv
load_dotenv()

from persona.db import MongoDB

print('Testing MongoDB connection...')
try:
    db = MongoDB.connect()
    if db is not None:
        print('✅ MongoDB connected successfully!')
        print(f'   Database: {db.name}')

        # Try to create a test collection
        test_coll = db['test_collection']
        result = test_coll.insert_one({'test': 'data'})
        print(f'✅ Test write successful! ID: {result.inserted_id}')

        # Clean up
        test_coll.delete_one({'_id': result.inserted_id})
        print('✅ MongoDB is fully working!')
    else:
        print('❌ MongoDB connection returned None')
except Exception as e:
    print(f'❌ MongoDB error: {e}')
    import traceback
    traceback.print_exc()

