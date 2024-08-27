# AuthTokenCache

## Overview

`AuthTokenCache` is a Python class designed to cache authentication tokens in Redis. This class allows you to store, retrieve, and manage tokens in an in-memory data store, minimizing the need for repeated requests to a third-party authentication service. By using Redis as the underlying cache store, the system ensures high performance, scalability, and persistence across distributed environments.

## Features

- **Redis Backend**: Utilizes Redis for storing tokens, ensuring quick access and persistence.
- **FIFO Eviction**: Implements a First-In-First-Out (FIFO) eviction policy when the cache exceeds its maximum size.
- **Thread Safety**: Uses threading locks to ensure safe concurrent access.

## Requirements

- Python 3.x
- Redis Server
- `redis` Python package (`pip install redis`)


2. **Install Python Dependencies**:
   - Install the `redis` Python package:
     ```bash
     pip install redis
     ```

## Usage

### Initialization

```python
from auth_token_cache import AuthTokenCache

# Initialize the AuthTokenCache with a maximum size of 100 tokens
cache = AuthTokenCache(max_size=100)
