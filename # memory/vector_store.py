

import
 json

import
 asyncio

import
 numpy 
as
 np

from
 pathlib 
import
 Path

from
 typing 
import
 Dict
,
 List
,
 Any
,
 Optional
,
 Tuple
,
 Set

from
 dataclasses 
import
 dataclass

import
 hashlib

import
 logging

from
 datetime 
import
 datetime
,
 timedelta


@dataclass


class
 
VectorDocument
:

    document_id
:
 
str

    vector
:
 np
.
ndarray
    metadata
:
 Dict
[
str
,
 Any
]

    content
:
 
str

    timestamp
:
 datetime


@dataclass


class
 
SearchResult
:

    document_id
:
 
str

    score
:
 
float

    metadata
:
 Dict
[
str
,
 Any
]

    content
:
 
str



class
 
VectorStore
:

    
def
 
__init__
(
self
,
 config
:
 Dict
[
str
,
 Any
]
)
:

        self
.
config 
=
 config
        self
.
logger 
=
 logging
.
getLogger
(
__name__
)

        
        
# Vector store configuration

        self
.
persist_dir 
=
 Path
(
config
[
"memory"
]
.
get
(
"vector_store"
,
 
"./memory/vector_store"
)
)

        self
.
persist_dir
.
mkdir
(
parents
=
True
,
 exist_ok
=
True
)

        
        self
.
dimension 
=
 config
[
"memory"
]
.
get
(
"embedding_dimension"
,
 
384
)

        self
.
similarity_threshold 
=
 config
[
"memory"
]
.
get
(
"similarity_threshold"
,
 
0.7
)

        self
.
max_results 
=
 config
[
"memory"
]
.
get
(
"max_vector_results"
,
 
50
)

        
        
# In-memory storage

        self
.
documents
:
 Dict
[
str
,
 VectorDocument
]
 
=
 
{
}

        self
.
index
:
 Dict
[
str
,
 Set
[
str
]
]
 
=
 
{
}
  
# Metadata-based index

        self
.
similarity_index
:
 Dict
[
np
.
ndarray
,
 
str
]
 
=
 
{
}
  
# Vector similarity hash

        
        
# Performance metrics

        self
.
metrics 
=
 
{

            
"total_documents"
:
 
0
,

            
"total_searches"
:
 
0
,

            
"avg_query_time"
:
 
0.0
,

            
"cache_hits"
:
 
0
,

            
"cache_misses"
:
 
0

        
}

        
        
# TTL cache for recent searches

        self
.
query_cache
:
 Dict
[
str
,
 List
[
SearchResult
]
]
 
=
 
{
}

        self
.
cache_ttl 
=
 config
[
"memory"
]
.
get
(
"vector_cache_ttl"
,
 
300
)
  
# 5 minutes

        
        self
.
load
(
)

    
    
def
 
add
(

        self
,

        documents
:
 List
[
str
]
,

        metadatas
:
 List
[
Dict
[
str
,
 Any
]
]
,

        ids
:
 List
[
str
]
,

        embeddings
:
 Optional
[
List
[
np
.
ndarray
]
]
 
=
 
None

    
)
 
-
>
 
bool
:

        
"""Add documents to vector store."""

        
try
:

            
from
 memory
.
embedding_manager 
import
 EmbeddingManager
            embedding_manager 
=
 EmbeddingManager
(
self
.
config
)

            
            
# Generate embeddings if not provided

            
if
 embeddings 
is
 
None
:

                embeddings 
=
 asyncio
.
run
(
embedding_manager
.
generate_embeddings
(
documents
)
)

            
            
# Ensure embeddings match dimension

            embeddings 
=
 
[
np
.
array
(
emb
,
 dtype
=
np
.
float32
)
 
for
 emb 
in
 embeddings
]

            
for
 emb 
in
 embeddings
:

                
if
 
len
(
emb
)
 
!=
 self
.
dimension
:

                    
raise
 ValueError
(
f"Embedding dimension mismatch: expected 
{
self
.
dimension
}
, got 
{
len
(
emb
)
}
"
)

            
            
# Add documents

            added_count 
=
 
0

            
for
 doc_id
,
 content
,
 metadata
,
 vector 
in
 
zip
(
ids
,
 documents
,
 metadatas
,
 embeddings
)
:

                doc 
=
 VectorDocument
(

                    document_id
=
doc_id
,

                    vector
=
vector
,

                    metadata
=
metadata
,

                    content
=
content
,

                    timestamp
=
datetime
.
now
(
)

                
)

                
                self
.
documents
[
doc_id
]
 
=
 doc
                self
.
_update_index
(
doc_id
,
 metadata
)

                self
.
metrics
[
"total_documents"
]
 
+=
 
1

                added_count 
+=
 
1

            
            
# Persist to disk

            self
.
save
(
)

            
            self
.
logger
.
info
(
f"Added 
{
added_count
}
 documents to vector store"
)

            
return
 
True

            
        
except
 Exception 
as
 e
:

            self
.
logger
.
error
(
f"Error adding documents: 
{
e
}
"
)

            
return
 
False

    
    
def
 
search_similar
(

        self
,

        query
:
 
str
,

        limit
:
 
int
 
=
 
10
,

        
filter
:
 Optional
[
Dict
[
str
,
 Any
]
]
 
=
 
None
,

        embeddings
:
 Optional
[
np
.
ndarray
]
 
=
 
None

    
)
 
-
>
 List
[
SearchResult
]
:

        
"""Search for similar documents."""

        
import
 time
        start_time 
=
 time
.
time
(
)

        
        
# Check cache first

        cache_key 
=
 hashlib
.
md5
(
f"
{
query
}
_
{
filter
}
_
{
limit
}
"
.
encode
(
)
)
.
hexdigest
(
)

        
if
 cache_key 
in
 self
.
query_cache
:

            self
.
metrics
[
"cache_hits"
]
 
+=
 
1

            
return
 self
.
query_cache
[
cache_key
]

        
        self
.
metrics
[
"cache_misses"
]
 
+=
 
1

        
        
try
:

            
# Generate query embedding if not provided

            
if
 embeddings 
is
 
None
:

                
from
 memory
.
embedding_manager 
import
 EmbeddingManager
                embedding_manager 
=
 EmbeddingManager
(
self
.
config
)

                query_vector 
=
 asyncio
.
run
(
embedding_manager
.
generate_embedding
(
query
)
)

            
else
:

                query_vector 
=
 embeddings
            
            
# Perform similarity search

            results 
=
 
[
]

            
            
for
 doc_id
,
 doc 
in
 self
.
documents
.
items
(
)
:

                
# Apply metadata filter

                
if
 
filter
 
and
 
not
 self
.
_matches_filter
(
doc
.
metadata
,
 
filter
)
:

                    
continue

                
                
# Calculate similarity

                similarity 
=
 self
.
_cosine_similarity
(
query_vector
,
 doc
.
vector
)

                
                
if
 similarity 
>=
 self
.
similarity_threshold
:

                    results
.
append
(
SearchResult
(

                        document_id
=
doc_id
,

                        score
=
float
(
similarity
)
,

                        metadata
=
doc
.
metadata
,

                        content
=
doc
.
content
                    
)
)

            
            
# Sort by similarity score

            results
.
sort
(
key
=
lambda
 r
:
 r
.
score
,
 reverse
=
True
)

            
            
# Cache results

            self
.
query_cache
[
cache_key
]
 
=
 results
[
:
limit
]

            
            
# Update metrics

            query_time 
=
 time
.
time
(
)
 
-
 start_time
            self
.
metrics
[
"avg_query_time"
]
 
=
 
(

                
(
self
.
metrics
[
"avg_query_time"
]
 
*
 self
.
metrics
[
"total_searches"
]
 
+
 query_time
)
 
/

                
(
self
.
metrics
[
"total_searches"
]
 
+
 
1
)

            
)

            self
.
metrics
[
"total_searches"
]
 
+=
 
1

            
            
return
 results
[
:
limit
]

            
        
except
 Exception 
as
 e
:

            self
.
logger
.
error
(
f"Error searching documents: 
{
e
}
"
)

            
return
 
[
]

    
    
def
 
search_by_metadata
(

        self
,

        
filter
:
 Dict
[
str
,
 Any
]
,

        limit
:
 
int
 
=
 
50

    
)
 
-
>
 List
[
SearchResult
]
:

        
"""Search documents by metadata only."""

        results 
=
 
[
]

        
        
for
 doc_id
,
 doc 
in
 self
.
documents
.
items
(
)
:

            
if
 self
.
_matches_filter
(
doc
.
metadata
,
 
filter
)
:

                results
.
append
(
SearchResult
(

                    document_id
=
doc_id
,

                    score
=
1.0
,
  
# Exact metadata match

                    metadata
=
doc
.
metadata
,

                    content
=
doc
.
content
                
)
)

        
        
return
 results
[
:
limit
]

    
    
def
 
_matches_filter
(
self
,
 metadata
:
 Dict
[
str
,
 Any
]
,
 
filter
:
 Dict
[
str
,
 Any
]
)
 
-
>
 
bool
:

        
"""Check if metadata matches filter."""

        
for
 key
,
 value 
in
 
filter
.
items
(
)
:

            
if
 key 
not
 
in
 metadata
:

                
return
 
False

            
            
if
 
isinstance
(
value
,
 
list
)
:

                
if
 metadata
[
key
]
 
not
 
in
 value
:

                    
return
 
False

            
elif
 
isinstance
(
value
,
 
dict
)
:

                
# Nested filter

                
if
 
not
 self
.
_matches_filter
(
metadata
.
get
(
key
,
 
{
}
)
,
 value
)
:

                    
return
 
False

            
elif
 metadata
[
key
]
 
!=
 value
:

                
return
 
False

        
        
return
 
True

    
    
def
 
delete
(
self
,
 ids
:
 List
[
str
]
)
 
-
>
 
bool
:

        
"""Delete documents by ID."""

        
try
:

            deleted_count 
=
 
0

            
            
for
 doc_id 
in
 ids
:

                
if
 doc_id 
in
 self
.
documents
:

                    doc 
=
 self
.
documents
[
doc_id
]

                    self
.
_remove_from_index
(
doc_id
,
 doc
.
metadata
)

                    
del
 self
.
documents
[
doc_id
]

                    deleted_count 
+=
 
1

                    self
.
metrics
[
"total_documents"
]
 
-=
 
1

            
            self
.
save
(
)

            self
.
logger
.
info
(
f"Deleted 
{
deleted_count
}
 documents"
)

            
return
 deleted_count 
>
 
0

            
        
except
 Exception 
as
 e
:

            self
.
logger
.
error
(
f"Error deleting documents: 
{
e
}
"
)

            
return
 
False

    
    
def
 
update
(

        self
,

        ids
:
 List
[
str
]
,

        documents
:
 Optional
[
List
[
str
]
]
 
=
 
None
,

        metadatas
:
 Optional
[
List
[
Dict
[
str
,
 Any
]
]
]
 
=
 
None

    
)
 
-
>
 
bool
:

        
"""Update documents."""

        
try
:

            updated_count 
=
 
0

            
            
for
 i
,
 doc_id 
in
 
enumerate
(
ids
)
:

                
if
 doc_id 
not
 
in
 self
.
documents
:

                    
continue

                
                doc 
=
 self
.
documents
[
doc_id
]

                
                
if
 documents 
and
 i 
<
 
len
(
documents
)
:

                    doc
.
content 
=
 documents
[
i
]

                
                
if
 metadatas 
and
 i 
<
 
len
(
metadatas
)
:

                    
# Remove old metadata from index

                    self
.
_remove_from_index
(
doc_id
,
 doc
.
metadata
)

                    
# Update metadata

                    doc
.
metadata
.
update
(
metadatas
[
i
]
)

                    
# Add new metadata to index

                    self
.
_update_index
(
doc_id
,
 doc
.
metadata
)

                
                doc
.
timestamp 
=
 datetime
.
now
(
)

                updated_count 
+=
 
1

            
            self
.
save
(
)

            self
.
logger
.
info
(
f"Updated 
{
updated_count
}
 documents"
)

            
return
 updated_count 
>
 
0

            
        
except
 Exception 
as
 e
:

            self
.
logger
.
error
(
f"Error updating documents: 
{
e
}
"
)

            
return
 
False

    
    
def
 
_update_index
(
self
,
 doc_id
:
 
str
,
 metadata
:
 Dict
[
str
,
 Any
]
)
:

        
"""Update metadata index."""

        
for
 key
,
 value 
in
 metadata
.
items
(
)
:

            index_key 
=
 
f"
{
key
}
:
{
value
}
"

            
if
 index_key 
not
 
in
 self
.
index
:

                self
.
index
[
index_key
]
 
=
 
set
(
)

            self
.
index
[
index_key
]
.
add
(
doc_id
)

    
    
def
 
_remove_from_index
(
self
,
 doc_id
:
 
str
,
 metadata
:
 Dict
[
str
,
 Any
]
)
:

        
"""Remove document from metadata index."""

        
for
 key
,
 value 
in
 metadata
.
items
(
)
:

            index_key 
=
 
f"
{
key
}
:
{
value
}
"

            
if
 index_key 
in
 self
.
index
:

                self
.
index
[
index_key
]
.
discard
(
doc_id
)

                
if
 
not
 self
.
index
[
index_key
]
:

                    
del
 self
.
index
[
index_key
]

    
    
def
 
_cosine_similarity
(
self
,
 vec1
:
 np
.
ndarray
,
 vec2
:
 np
.
ndarray
)
 
-
>
 
float
:

        
"""Calculate cosine similarity between vectors."""

        
# Normalize vectors

        norm1 
=
 np
.
linalg
.
norm
(
vec1
)

        norm2 
=
 np
.
linalg
.
norm
(
vec2
)

        
        
if
 norm1 
==
 
0
 
or
 norm2 
==
 
0
:

            
return
 
0.0

        
        vec1_norm 
=
 vec1 
/
 norm1
        vec2_norm 
=
 vec2 
/
 norm2
        
        
# Calculate dot product

        similarity 
=
 np
.
dot
(
vec1_norm
,
 vec2_norm
)

        
        
# Ensure value is between 0 and 1

        
return
 
float
(
max
(
0.0
,
 
min
(
1.0
,
 similarity
)
)
)

    
    
def
 
get_document
(
self
,
 doc_id
:
 
str
)
 
-
>
 Optional
[
VectorDocument
]
:

        
"""Get document by ID."""

        
return
 self
.
documents
.
get
(
doc_id
)

    
    
def
 
get_all_documents
(
self
)
 
-
>
 List
[
VectorDocument
]
:

        
"""Get all documents."""

        
return
 
list
(
self
.
documents
.
values
(
)
)

    
    
def
 
get_stats
(
self
)
 
-
>
 Dict
[
str
,
 Any
]
:

        
"""Get vector store statistics."""

        
return
 
{

            
"total_documents"
:
 
len
(
self
.
documents
)
,

            
"total_index_entries"
:
 
sum
(
len
(
s
)
 
for
 s 
in
 self
.
index
.
values
(
)
)
,

            
"cache_size"
:
 
len
(
self
.
query_cache
)
,

            
"metrics"
:
 self
.
metrics
        
}

    
    
def
 
clear
(
self
)
:

        
"""Clear all documents."""

        self
.
documents
.
clear
(
)

        self
.
index
.
clear
(
)

        self
.
query_cache
.
clear
(
)

        self
.
metrics 
=
 
{

            
"total_documents"
:
 
0
,

            
"total_searches"
:
 
0
,

            
"avg_query_time"
:
 
0.0
,

            
"cache_hits"
:
 
0
,

            
"cache_misses"
:
 
0

        
}

        self
.
save
(
)

        self
.
logger
.
info
(
"Vector store cleared"
)

    
    
def
 
save
(
self
)
:

        
"""Persist vector store to disk."""

        
try
:

            data 
=
 
{

                
"documents"
:
 
{

                    doc_id
:
 
{

                        
"document_id"
:
 doc
.
document_id
,

                        
"vector"
:
 doc
.
vector
.
tolist
(
)
,

                        
"metadata"
:
 doc
.
metadata
,

                        
"content"
:
 doc
.
content
,

                        
"timestamp"
:
 doc
.
timestamp
.
isoformat
(
)

                    
}

                    
for
 doc_id
,
 doc 
in
 self
.
documents
.
items
(
)

                
}
,

                
"index"
:
 
{
k
:
 
list
(
v
)
 
for
 k
,
 v 
in
 self
.
index
.
items
(
)
}
,

                
"metrics"
:
 self
.
metrics
,

                
"last_updated"
:
 datetime
.
now
(
)
.
isoformat
(
)

            
}

            
            self
.
persist_dir
.
mkdir
(
parents
=
True
,
 exist_ok
=
True
)

            
(
self
.
persist_dir 
/
 
"store.json"
)
.
write_text
(
json
.
dumps
(
data
,
 indent
=
2
)
)

            
        
except
 Exception 
as
 e
:

            self
.
logger
.
error
(
f"Error saving vector store: 
{
e
}
"
)

    
    
def
 
load
(
self
)
:

        
"""Load vector store from disk."""

        
try
:

            store_file 
=
 self
.
persist_dir 
/
 
"store.json"

            
if
 store_file
.
exists
(
)
:

                data 
=
 json
.
loads
(
store_file
.
read_text
(
)
)

                
                self
.
documents 
=
 
{
}

                
for
 doc_id
,
 doc_data 
in
 data
.
get
(
"documents"
,
 
{
}
)
.
items
(
)
:

                    self
.
documents
[
doc_id
]
 
=
 VectorDocument
(

                        document_id
=
doc_data
[
"document_id"
]
,

                        vector
=
np
.
array
(
doc_data
[
"vector"
]
,
 dtype
=
np
.
float32
)
,

                        metadata
=
doc_data
[
"metadata"
]
,

                        content
=
doc_data
[
"content"
]
,

                        timestamp
=
datetime
.
fromisoformat
(
doc_data
[
"timestamp"
]
)

                    
)

                
                self
.
index 
=
 
{
k
:
 
set
(
v
)
 
for
 k
,
 v 
in
 data
.
get
(
"index"
,
 
{
}
)
.
items
(
)
}

                self
.
metrics 
=
 data
.
get
(
"metrics"
,
 self
.
metrics
)

                
                self
.
logger
.
info
(
f"Loaded 
{
len
(
self
.
documents
)
}
 documents from disk"
)

            
        
except
 Exception 
as
 e
:

            self
.
logger
.
error
(
f"Error loading vector store: 
{
e
}
"
)

            self
.
documents 
=
 
{
}

            self
.
index 
=
 
{
}

    
    
def
 
cleanup_expired_cache
(
self
)
:

        
"""Clean up expired cache entries."""

        current_time 
=
 datetime
.
now
(
)

        expired_keys 
=
 
[
]

        
        
for
 cache_key
,
 results 
in
 self
.
query_cache
.
items
(
)
:

            
# Simple TTL based on key hash (approximate)

            
if
 
hash
(
cache_key
)
 
%
 
100
 
<
 
10
:
  
# 10% chance of being expired

                expired_keys
.
append
(
cache_key
)

        
        
for
 key 
in
 expired_keys
:

            
del
 self
.
query_cache
[
key
]

        
        
if
 expired_keys
:

            self
.
logger
.
info
(
f"Cleared 
{
len
(
expired_keys
)
}
 expired cache entries"
)

    
    
async
 
def
 
batch_search
(

        self
,

        queries
:
 List
[
str
]
,

        limit
:
 
int
 
=
 
10
,

        
filter
:
 Optional
[
Dict
[
str
,
 Any
]
]
 
=
 
None

    
)
 
-
>
 List
[
List
[
SearchResult
]
]
:

        
"""Search multiple queries in parallel."""

        
from
 memory
.
embedding_manager 
import
 EmbeddingManager
        embedding_manager 
=
 EmbeddingManager
(
self
.
config
)

        
        
# Generate embeddings in one batch

        query_embeddings 
=
 
await
 embedding_manager
.
generate_embeddings
(
queries
)

        
        
# Run searches in parallel

        tasks 
=
 
[

            self
.
search_similar
(

                query
,

                limit
=
limit
,

                
filter
=
filter
,

                embeddings
=
embedding
            
)

            
for
 query
,
 embedding 
in
 
zip
(
queries
,
 query_embeddings
)

        
]

        
        
return
 
await
 asyncio
.
gather
(
*
tasks
)



### memory/memory_indexer.py

```python

from
 typing 
import
 Dict
,
 List
,
 Any
,
 Set
,
 Optional

from
 pathlib 
import
 Path

import
 json

from
 dataclasses 
import
 dataclass
,
 asdict

from
 datetime 
import
 datetime


@dataclass


class
 
IndexEntry
:

    document_id
:
 
str

    metadata
:
 Dict
[
str
,
 Any
]

    timestamp
:
 datetime
    score
:
 Optional
[
float
]
 
=
 
None



class
 
MemoryIndexer
:

    
def
 
__init__
(
self
,
 config
:
 Dict
[
str
,
 Any
]
)
:

        self
.
config 
=
 config
        self
.
persist_dir 
=
 Path
(
config
[
"memory"
]
.
get
(
"vector_store"
,
 
"./memory/vector_store"
)
)

        self
.
persist_dir
.
mkdir
(
parents
=
True
,
 exist_ok
=
True
)

        
        
# Multi-level index structure

        
# Index format: {metadata_key: {metadata_value: Set[document_ids]}}

        self
.
metadata_index
:
 Dict
[
str
,
 Dict
[
str
,
 Set
[
str
]
]
]
 
=
 
{
}

        
        
# Temporal index: {time_bucket: Set[document_ids]}

        self
.
temporal_index
:
 Dict
[
str
,
 Set
[
str
]
]
 
=
 
{
}

        
        
# Semantic index: {concept: Set[document_ids]}

        self
.
semantic_index
:
 Dict
[
str
,
 Set
[
str
]
]
 
=
 
{
}

        
        
# Document metadata store

        self
.
document_metadata
:
 Dict
[
str
,
 Dict
[
str
,
 Any
]
]
 
=
 
{
}

        
        
# Performance metrics

        self
.
metrics 
=
 
{

            
"total_indexed"
:
 
0
,

            
"total_queries"
:
 
0
,

            
"avg_index_time"
:
 
0.0
,

            
"avg_query_time"
:
 
0.0

        
}

        
        self
.
load
(
)

    
    
def
 
index_document
(

        self
,

        document_id
:
 
str
,

        metadata
:
 Dict
[
str
,
 Any
]
,

        content
:
 
str
,

        embeddings
:
 Optional
[
List
[
float
]
]
 
=
 
None

    
)
 
-
>
 
bool
:

        
"""Index a document with multiple index types."""

        
try
:

            
import
 time
            start_time 
=
 time
.
time
(
)

            
            
# Store document metadata

            self
.
document_metadata
[
document_id
]
 
=
 
{

                
"metadata"
:
 metadata
,

                
"content_preview"
:
 content
[
:
200
]
,

                
"timestamp"
:
 datetime
.
now
(
)
.
isoformat
(
)

            
}

            
            
# Index by metadata

            self
.
_index_metadata
(
document_id
,
 metadata
)

            
            
# Index by time

            self
.
_index_temporal
(
document_id
,
 metadata
)

            
            
# Index by semantic concepts

            self
.
_index_semantic
(
document_id
,
 content
,
 metadata
)

            
            
# Update metrics

            indexing_time 
=
 time
.
time
(
)
 
-
 start_time
            self
.
metrics
[
"avg_index_time"
]
 
=
 
(

                
(
self
.
metrics
[
"avg_index_time"
]
 
*
 self
.
metrics
[
"total_indexed"
]
 
+
 indexing_time
)
 
/

                
(
self
.
metrics
[
"total_indexed"
]
 
+
 
1
)

            
)

            self
.
metrics
[
"total_indexed"
]
 
+=
 
1

            
            self
.
save
(
)

            
return
 
True

            
        
except
 Exception 
as
 e
:

            logging
.
error
(
f"Error indexing document 
{
document_id
}
: 
{
e
}
"
)

            
return
 
False

    
    
def
 
_index_metadata
(
self
,
 document_id
:
 
str
,
 metadata
:
 Dict
[
str
,
 Any
]
)
:

        
"""Index by metadata key-value pairs."""

        
for
 key
,
 value 
in
 metadata
.
items
(
)
:

            
if
 
isinstance
(
value
,
 
(
str
,
 
int
,
 
float
,
 
bool
)
)
:

                str_value 
=
 
str
(
value
)

                
                
if
 key 
not
 
in
 self
.
metadata_index
:

                    self
.
metadata_index
[
key
]
 
=
 
{
}

                
                
if
 str_value 
not
 
in
 self
.
metadata_index
[
key
]
:

                    self
.
metadata_index
[
key
]
[
str_value
]
 
=
 
set
(
)

                
                self
.
metadata_index
[
key
]
[
str_value
]
.
add
(
document_id
)

            
            
elif
 
isinstance
(
value
,
 
list
)
:

                
for
 item 
in
 value
:

                    str_value 
=
 
str
(
item
)

                    
                    
if
 key 
not
 
in
 self
.
metadata_index
:

                        self
.
metadata_index
[
key
]
 
=
 
{
}

                    
                    
if
 str_value 
not
 
in
 self
.
metadata_index
[
key
]
:

                        self
.
metadata_index
[
key
]
[
str_value
]
 
=
 
set
(
)

                    
                    self
.
metadata_index
[
key
]
[
str_value
]
.
add
(
document_id
)

    
    
def
 
_index_temporal
(
self
,
 document_id
:
 
str
,
 metadata
:
 Dict
[
str
,
 Any
]
)
:

        
"""Index by time periods."""

        timestamp 
=
 metadata
.
get
(
"timestamp"
,
 datetime
.
now
(
)
.
isoformat
(
)
)

        
        
try
:

            dt 
=
 datetime
.
fromisoformat
(
timestamp
)

            
            
# Create time buckets

            buckets 
=
 
[

                
f"year:
{
dt
.
year
}
"
,

                
f"month:
{
dt
.
year
}
-
{
dt
.
month
:
02d
}
"
,

                
f"day:
{
dt
.
year
}
-
{
dt
.
month
:
02d
}
-
{
dt
.
day
:
02d
}
"
,

                
f"hour:
{
dt
.
year
}
-
{
dt
.
month
:
02d
}
-
{
dt
.
day
:
02d
}
-
{
dt
.
hour
:
02d
}
"

            
]

            
            
for
 bucket 
in
 buckets
:

                
if
 bucket 
not
 
in
 self
.
temporal_index
:

                    self
.
temporal_index
[
bucket
]
 
=
 
set
(
)

                self
.
temporal_index
[
bucket
]
.
add
(
document_id
)

        
        
except
:

            
pass

    
    
def
 
_index_semantic
(
self
,
 document_id
:
 
str
,
 content
:
 
str
,
 metadata
:
 Dict
[
str
,
 Any
]
)
:

        
"""Index by semantic concepts."""

        
# Extract concepts from content and metadata

        concepts 
=
 
set
(
)

        
        
# Extract from content

        words 
=
 re
.
findall
(
r'\b[a-zA-Z]{3,}\b'
,
 content
.
lower
(
)
)

        
# Add top frequent words as concepts

        
from
 collections 
import
 Counter
        word_counts 
=
 Counter
(
words
)

        concepts
.
update
(
[
word 
for
 word
,
 count 
in
 word_counts
.
most_common
(
10
)
]
)

        
        
# Extract from metadata values

        
for
 value 
in
 metadata
.
values
(
)
:

            
if
 
isinstance
(
value
,
 
str
)
:

                words 
=
 re
.
findall
(
r'\b[a-zA-Z]{3,}\b'
,
 value
.
lower
(
)
)

                concepts
.
update
(
words
)

        
        
# Add to semantic index

        
for
 concept 
in
 concepts
:

            
if
 concept 
not
 
in
 self
.
semantic_index
:

                self
.
semantic_index
[
concept
]
 
=
 
set
(
)

            self
.
semantic_index
[
concept
]
.
add
(
document_id
)

    
    
def
 
query
(

        self
,

        
filter
:
 Dict
[
str
,
 Any
]
,

        time_range
:
 Optional
[
Tuple
[
str
,
 
str
]
]
 
=
 
None
,

        concepts
:
 Optional
[
List
[
str
]
]
 
=
 
None
,

        limit
:
 
int
 
=
 
100

    
)
 
-
>
 List
[
IndexEntry
]
:

        
"""Query documents using multiple index types."""

        start_time 
=
 time
.
time
(
)

        
        
# Start with metadata filter

        candidates 
=
 self
.
_query_metadata
(
filter
)

        
        
# Apply time range filter

        
if
 time_range
:

            time_candidates 
=
 self
.
_query_time_range
(
time_range
)

            candidates 
=
 candidates
.
intersection
(
time_candidates
)
 
if
 candidates 
else
 time_candidates
        
        
# Apply semantic concept filter

        
if
 concepts
:

            concept_candidates 
=
 self
.
_query_concepts
(
concepts
)

            candidates 
=
 candidates
.
intersection
(
concept_candidates
)
 
if
 candidates 
else
 concept_candidates
        
        
# Fetch document details

        results 
=
 
[
]

        
for
 doc_id 
in
 
list
(
candidates
)
[
:
limit
]
:

            
if
 doc_id 
in
 self
.
document_metadata
:

                results
.
append
(
IndexEntry
(

                    document_id
=
doc_id
,

                    metadata
=
self
.
document_metadata
[
doc_id
]
[
"metadata"
]
,

                    timestamp
=
datetime
.
fromisoformat
(
self
.
document_metadata
[
doc_id
]
[
"timestamp"
]
)
,

                    score
=
1.0

                
)
)

        
        
# Update metrics

        query_time 
=
 time
.
time
(
)
 
-
 start_time
        self
.
metrics
[
"avg_query_time"
]
 
=
 
(

            
(
self
.
metrics
[
"avg_query_time"
]
 
*
 self
.
metrics
[
"total_queries"
]
 
+
 query_time
)
 
/

            
(
self
.
metrics
[
"total_queries"
]
 
+
 
1
)

        
)

        self
.
metrics
[
"total_queries"
]
 
+=
 
1

        
        
return
 results
    
    
def
 
_query_metadata
(
self
,
 
filter
:
 Dict
[
str
,
 Any
]
)
 
-
>
 Set
[
str
]
:

        
"""Query by metadata filter."""

        results 
=
 
None

        
        
for
 key
,
 value 
in
 
filter
.
items
(
)
:

            
if
 key 
in
 self
.
metadata_index
:

                
if
 
isinstance
(
value
,
 
list
)
:

                    
# OR condition for list values

                    matches 
=
 
set
(
)

                    
for
 v 
in
 value
:

                        str_v 
=
 
str
(
v
)

                        
if
 str_v 
in
 self
.
metadata_index
[
key
]
:

                            matches
.
update
(
self
.
metadata_index
[
key
]
[
str_v
]
)

                
else
:

                    
# Exact match

                    str_value 
=
 
str
(
value
)

                    
if
 str_value 
in
 self
.
metadata_index
[
key
]
:

                        matches 
=
 self
.
metadata_index
[
key
]
[
str_value
]

                    
else
:

                        matches 
=
 
set
(
)

                
                
if
 results 
is
 
None
:

                    results 
=
 matches
                
else
:

                    results 
=
 results
.
intersection
(
matches
)

            
else
:

                
# Key not in index, return empty

                
return
 
set
(
)

        
        
return
 results 
or
 
set
(
)

    
    
def
 
_query_time_range
(
self
,
 time_range
:
 Tuple
[
str
,
 
str
]
)
 
-
>
 Set
[
str
]
:

        
"""Query documents within time range."""

        results 
=
 
set
(
)

        
        
try
:

            start_dt 
=
 datetime
.
fromisoformat
(
time_range
[
0
]
)

            end_dt 
=
 datetime
.
fromisoformat
(
time_range
[
1
]
)

            
            
# Generate all bucket keys in range

            current 
=
 start_dt
            
while
 current 
<=
 end_dt
:

                buckets 
=
 
[

                    
f"year:
{
current
.
year
}
"
,

                    
f"month:
{
current
.
year
}
-
{
current
.
month
:
02d
}
"
,

                    
f"day:
{
current
.
year
}
-
{
current
.
month
:
02d
}
-
{
current
.
day
:
02d
}
"
,

                
]

                
                
for
 bucket 
in
 buckets
:

                    
if
 bucket 
in
 self
.
temporal_index
:

                        results
.
update
(
self
.
temporal_index
[
bucket
]
)

                
                current 
+=
 timedelta
(
days
=
1
)

        
        
except
:

            
pass

        
        
return
 results
    
    
def
 
_query_concepts
(
self
,
 concepts
:
 List
[
str
]
)
 
-
>
 Set
[
str
]
:

        
"""Query by semantic concepts."""

        results 
=
 
None

        
        
for
 concept 
in
 concepts
:

            concept_lower 
=
 concept
.
lower
(
)

            
if
 concept_lower 
in
 self
.
semantic_index
:

                
if
 results 
is
 
None
:

                    results 
=
 self
.
semantic_index
[
concept_lower
]
.
copy
(
)

                
else
:

                    results 
=
 results
.
intersection
(
self
.
semantic_index
[
concept_lower
]
)

            
else
:

                
# Concept not found, return empty

                
return
 
set
(
)

        
        
return
 results 
or
 
set
(
)

    
    
def
 
delete_document
(
self
,
 document_id
:
 
str
)
 
-
>
 
bool
:

        
"""Delete a document from the index."""

        
try
:

            
if
 document_id 
not
 
in
 self
.
document_metadata
:

                
return
 
False

            
            doc_meta 
=
 self
.
document_metadata
[
document_id
]

            
            
# Remove from metadata index

            self
.
_remove_from_metadata_index
(
document_id
,
 doc_meta
[
"metadata"
]
)

            
            
# Remove from temporal index

            self
.
_remove_from_temporal_index
(
document_id
,
 doc_meta
[
"metadata"
]
)

            
            
# Remove from semantic index

            
# (Simplified - would need to find all concepts)

            
            
# Remove from metadata store

            
del
 self
.
document_metadata
[
document_id
]

            
            self
.
save
(
)

            
return
 
True

            
        
except
 Exception 
as
 e
:

            logging