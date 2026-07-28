from
 typing 
import
 List
,
 Any
,
 Optional

import
 asyncio


class
 
EmbeddingManager
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
model_name 
=
 config
[
"memory"
]
.
get
(
"embedding_model"
,
 
"sentence-transformers/all-mpnet-base-v2"
)

        self
.
model 
=
 
None

        self
.
load_model
(
)

    
    
def
 
load_model
(
self
)
:

        
"""Load embedding model."""

        
try
:

            
from
 sentence_transformers 
import
 SentenceTransformer
            self
.
model 
=
 SentenceTransformer
(
self
.
model_name
)

        
except
 ImportError
:

            
print
(
"sentence-transformers not installed. Using fallback."
)

            self
.
model 
=
 
None

    
    
async
 
def
 
generate_embeddings
(
self
,
 texts
:
 List
[
str
]
)
 
-
>
 List
[
List
[
float
]
]
:

        
"""Generate embeddings for texts."""

        
if
 self
.
model 
is
 
None
:

            
# Fallback to simple embedding

            
return
 
[
self
.
_simple_embedding
(
text
)
 
for
 text 
in
 texts
]

        
        
# Use proper embedding model

        embeddings 
=
 self
.
model
.
encode
(
texts
,
 convert_to_tensor
=
False
)

        
return
 embeddings
.
tolist
(
)

    
    
async
 
def
 
generate_embedding
(
self
,
 text
:
 
str
)
 
-
>
 List
[
float
]
:

        
"""Generate embedding for single text."""

        
return
 
(
await
 self
.
generate_embeddings
(
[
text
]
)
)
[
0
]

    
    
def
 
_simple_embedding
(
self
,
 text
:
 
str
)
 
-
>
 List
[
float
]
:

        
"""Simple fallback embedding."""

        
# Simple character n-gram embedding

        vector 
=
 
[
0.0
]
 
*
 
128

        
        
for
 i 
in
 
range
(
len
(
text
)
 
-
 
2
)
:

            ngram 
=
 text
[
i
:
i
+
3
]

            idx 
=
 
hash
(
ngram
)
 
%
 
128

            vector
[
idx
]
 
+=
 
1.0

        
        
# Normalize

        magnitude 
=
 
sum
(
x
**
2
 
for
 x 
in
 vector
)
 
**
 
0.5

        
if
 magnitude 
>
 
0
:

            vector 
=
 
[
x 
/
 magnitude 
for
 x 
in
 vector
]

        
        
return
 vector
    
    
async
 
def
 
similarity
(
self
,
 vec1
:
 List
[
float
]
,
 vec2
:
 List
[
float
]
)
 
-
>
 
float
:

        
"""Calculate cosine similarity."""

        dot_product 
=
 
sum
(
a 
*
 b 
for
 a
,
 b 
in
 
zip
(
vec1
,
 vec2
)
)

        magnitude1 
=
 
sum
(
a
**
2
 
for
 a 
in
 vec1
)
 
**
 
0.5

        magnitude2 
=
 
sum
(
b
**
2
 
for
 b 
in
 vec2
)
 
**
 
0.5

        
        
if
 magnitude1 
==
 
0
 
or
 magnitude2 
==
 
0
:

            
return
 
0.0

        
        
return
 dot_product 
/
 
(
magnitude1 
*
 magnitude2
)
# Rewritten version:



import
 asyncio

import
 hashlib

import
 numpy 
as
 np

from
 typing 
import
 List
,
 Union
,
 Optional
,
 Dict
,
 Any

from
 dataclasses 
import
 dataclass

import
 logging


@dataclass


class
 
EmbeddingConfig
:

    provider
:
 
str
  
# "sentence_transformers", "openai", "cohere", "custom"

    model_name
:
 
str

    dimension
:
 
int

    max_tokens
:
 
int

    batch_size
:
 
int



class
 
EmbeddingManager
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

        
        
# Load configuration with defaults

        embedding_cfg 
=
 config
.
get
(
"memory"
,
 
{
}
)
.
get
(
"embedding"
,
 
{
}
)

        self
.
provider 
=
 embedding_cfg
.
get
(
"provider"
,
 
"sentence_transformers"
)

        self
.
model_name 
=
 embedding_cfg
.
get
(
"model_name"
,
 
"all-MiniLM-L6-v2"
)

        self
.
dimension 
=
 embedding_cfg
.
get
(
"dimension"
,
 
384
)

        self
.
max_tokens 
=
 embedding_cfg
.
get
(
"max_tokens"
,
 
512
)

        self
.
batch_size 
=
 embedding_cfg
.
get
(
"batch_size"
,
 
32
)

        self
.
cache_enabled 
=
 embedding_cfg
.
get
(
"cache_enabled"
,
 
True
)

        
        
# Initialize components

        self
.
_model 
=
 
None

        self
.
_tokenizer 
=
 
None

        self
.
_cache
:
 Dict
[
str
,
 np
.
ndarray
]
 
=
 
{
}

        self
.
_semaphore 
=
 asyncio
.
Semaphore
(
embedding_cfg
.
get
(
"max_concurrent"
,
 
5
)
)

        
        
# Performance metrics

        self
.
_metrics 
=
 
{

            
"total_requests"
:
 
0
,

            
"total_tokens"
:
 
0
,

            
"cache_hits"
:
 
0
,

            
"cache_misses"
:
 
0
,

            
"total_time"
:
 
0.0

        
}

        
        
# Load model in background

        asyncio
.
create_task
(
self
.
_load_model_async
(
)
)

    
    
async
 
def
 
_load_model_async
(
self
)
:

        
"""Asynchronously load the embedding model."""

        
try
:

            
if
 self
.
provider 
==
 
"sentence_transformers"
:

                
await
 self
.
_load_sentence_transformers
(
)

            
elif
 self
.
provider 
==
 
"openai"
:

                
await
 self
.
_load_openai_client
(
)

            
elif
 self
.
provider 
==
 
"cohere"
:

                
await
 self
.
_load_cohere_client
(
)

            
elif
 self
.
provider 
==
 
"custom"
:

                
await
 self
.
_load_custom_model
(
)

            
else
:

                self
.
logger
.
warning
(
f"Unknown provider 
{
self
.
provider
}
, using fallback"
)

                self
.
_model 
=
 
"fallback"

            
            self
.
logger
.
info
(
f"Embedding model 
{
self
.
model_name
}
 loaded successfully"
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
f"Failed to load embedding model: 
{
e
}
"
)

            self
.
_model 
=
 
"fallback"

    
    
async
 
def
 
_load_sentence_transformers
(
self
)
:

        
"""Load SentenceTransformer model."""

        
try
:

            
from
 sentence_transformers 
import
 SentenceTransformer
            self
.
_model 
=
 SentenceTransformer
(
self
.
model_name
)

            self
.
dimension 
=
 self
.
_model
.
get_sentence_embedding_dimension
(
)

        
except
 ImportError
:

            self
.
logger
.
error
(
"sentence-transformers not installed"
)

            
raise

    
    
async
 
def
 
_load_openai_client
(
self
)
:

        
"""Load OpenAI client for embeddings."""

        
try
:

            
import
 openai
            self
.
_client 
=
 openai
.
AsyncOpenAI
(
api_key
=
self
.
config
[
"llm"
]
[
"openai_api_key"
]
)

            self
.
_model 
=
 
"openai"

            
# Verify model

            
await
 self
.
_client
.
embeddings
.
create
(
input
=
[
"test"
]
,
 model
=
self
.
model_name
)

        
except
 ImportError
:

            self
.
logger
.
error
(
"openai package not installed"
)

            
raise

    
    
async
 
def
 
_load_cohere_client
(
self
)
:

        
"""Load Cohere client."""

        
try
:

            
import
 cohere
            self
.
_client 
=
 cohere
.
AsyncClient
(
self
.
config
[
"llm"
]
[
"cohere_api_key"
]
)

            self
.
_model 
=
 
"cohere"

        
except
 ImportError
:

            self
.
logger
.
error
(
"cohere package not installed"
)

            
raise

    
    
async
 
def
 
_load_custom_model
(
self
)
:

        
"""Load custom embedding model."""

        
# Placeholder for custom implementations

        
raise
 NotImplementedError
(
"Custom model loading not implemented"
)

    
    
async
 
def
 
generate_embeddings
(

        self
,

        texts
:
 List
[
str
]
,

        show_progress
:
 
bool
 
=
 
False

    
)
 
-
>
 List
[
np
.
ndarray
]
:

        
"""Generate embeddings for a list of texts.
        
        Args:
            texts: List of strings to embed
            show_progress: Show progress bar
            
        Returns:
            List of embedding vectors as numpy arrays
        """

        
if
 
not
 texts
:

            
return
 
[
]

        
        
# Check cache first

        
if
 self
.
cache_enabled
:

            cached_results 
=
 
[
]

            uncached_texts 
=
 
[
]

            uncached_indices 
=
 
[
]

            
            
for
 i
,
 text 
in
 
enumerate
(
texts
)
:

                cache_key 
=
 self
.
_get_cache_key
(
text
)

                
if
 cache_key 
in
 self
.
_cache
:

                    cached_results
.
append
(
(
i
,
 self
.
_cache
[
cache_key
]
)
)

                    self
.
_metrics
[
"cache_hits"
]
 
+=
 
1

                
else
:

                    uncached_texts
.
append
(
text
)

                    uncached_indices
.
append
(
i
)

                    self
.
_metrics
[
"cache_misses"
]
 
+=
 
1

        
else
:

            uncached_texts 
=
 texts
            uncached_indices 
=
 
list
(
range
(
len
(
texts
)
)
)

            cached_results 
=
 
[
]

        
        
# Generate embeddings for uncached texts

        
if
 uncached_texts
:

            embeddings 
=
 
await
 self
.
_generate_embeddings_batch
(
uncached_texts
,
 show_progress
)

            
            
# Cache results

            
if
 self
.
cache_enabled
:

                
for
 idx
,
 text
,
 embedding 
in
 
zip
(
uncached_indices
,
 uncached_texts
,
 embeddings
)
:

                    cache_key 
=
 self
.
_get_cache_key
(
text
)

                    self
.
_cache
[
cache_key
]
 
=
 embedding
        
else
:

            embeddings 
=
 
[
]

        
        
# Combine cached and new results

        all_embeddings 
=
 
[
None
]
 
*
 
len
(
texts
)

        
        
# Place cached results

        
for
 idx
,
 embedding 
in
 cached_results
:

            all_embeddings
[
idx
]
 
=
 embedding
        
        
# Place new results

        
for
 i
,
 
(
idx
,
 text
)
 
in
 
enumerate
(
zip
(
uncached_indices
,
 uncached_texts
)
)
:

            all_embeddings
[
idx
]
 
=
 embeddings
[
i
]

        
        
# Update metrics

        self
.
_metrics
[
"total_requests"
]
 
+=
 
len
(
texts
)

        self
.
_metrics
[
"total_tokens"
]
 
+=
 
sum
(
len
(
t
.
split
(
)
)
 
for
 t 
in
 texts
)

        
        
return
 all_embeddings
    
    
async
 
def
 
generate_embedding
(
self
,
 text
:
 
str
)
 
-
>
 np
.
ndarray
:

        
"""Generate embedding for a single text."""

        embeddings 
=
 
await
 self
.
generate_embeddings
(
[
text
]
)

        
return
 embeddings
[
0
]

    
    
async
 
def
 
_generate_embeddings_batch
(

        self
,

        texts
:
 List
[
str
]
,

        show_progress
:
 
bool

    
)
 
-
>
 List
[
np
.
ndarray
]
:

        
"""Generate embeddings in batches with concurrency control."""

        
if
 self
.
_model 
==
 
"fallback"
:

            
return
 
[
self
.
_fallback_embedding
(
text
)
 
for
 text 
in
 texts
]

        
        results 
=
 
[
]

        
        
# Process in batches

        
for
 i 
in
 
range
(
0
,
 
len
(
texts
)
,
 self
.
batch_size
)
:

            batch 
=
 texts
[
i
:
i 
+
 self
.
batch_size
]

            
            
if
 self
.
_model 
is
 
not
 
None
:

                
async
 
with
 self
.
_semaphore
:

                    embeddings 
=
 
await
 self
.
_call_embedding_api
(
batch
)

                    results
.
extend
(
embeddings
)

            
else
:

                
# Model not loaded yet, use fallback

                results
.
extend
(
[
self
.
_fallback_embedding
(
text
)
 
for
 text 
in
 batch
]
)

        
        
return
 results
    
    
async
 
def
 
_call_embedding_api
(
self
,
 batch
:
 List
[
str
]
)
 
-
>
 List
[
np
.
ndarray
]
:

        
"""Call the appropriate embedding API."""

        
if
 self
.
provider 
==
 
"sentence_transformers"
:

            
return
 
await
 self
.
_call_sentence_transformers
(
batch
)

        
elif
 self
.
provider 
==
 
"openai"
:

            
return
 
await
 self
.
_call_openai_embeddings
(
batch
)

        
elif
 self
.
provider 
==
 
"cohere"
:

            
return
 
await
 self
.
_call_cohere_embeddings
(
batch
)

        
else
:

            
return
 
[
self
.
_fallback_embedding
(
text
)
 
for
 text 
in
 batch
]

    
    
async
 
def
 
_call_sentence_transformers
(
self
,
 batch
:
 List
[
str
]
)
 
-
>
 List
[
np
.
ndarray
]
:

        
"""Call SentenceTransformer model."""

        
try
:

            
# Run in thread pool to avoid blocking

            embeddings 
=
 
await
 asyncio
.
get_event_loop
(
)
.
run_in_executor
(

                
None
,

                self
.
_model
.
encode
,

                batch
,

                
True
  
# convert_to_tensor

            
)

            
            
return
 
[
emb
.
cpu
(
)
.
numpy
(
)
 
if
 
hasattr
(
emb
,
 
'cpu'
)
 
else
 emb 
                   
for
 emb 
in
 embeddings
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
f"SentenceTransformer error: 
{
e
}
"
)

            
return
 
[
self
.
_fallback_embedding
(
text
)
 
for
 text 
in
 batch
]

    
    
async
 
def
 
_call_openai_embeddings
(
self
,
 batch
:
 List
[
str
]
)
 
-
>
 List
[
np
.
ndarray
]
:

        
"""Call OpenAI embeddings API."""

        
try
:

            response 
=
 
await
 self
.
_client
.
embeddings
.
create
(

                
input
=
batch
,

                model
=
self
.
model_name
            
)

            
            
return
 
[

                np
.
array
(
data
.
embedding
,
 dtype
=
np
.
float32
)

                
for
 data 
in
 response
.
data
            
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
f"OpenAI embeddings error: 
{
e
}
"
)

            
return
 
[
self
.
_fallback_embedding
(
text
)
 
for
 text 
in
 batch
]

    
    
async
 
def
 
_call_cohere_embeddings
(
self
,
 batch
:
 List
[
str
]
)
 
-
>
 List
[
np
.
ndarray
]
:

        
"""Call Cohere embeddings API."""

        
try
:

            response 
=
 
await
 self
.
_client
.
embed
(

                texts
=
batch
,

                model
=
self
.
model_name
,

                input_type
=
"search_document"

            
)

            
            
return
 
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
 response
.
embeddings
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
f"Cohere embeddings error: 
{
e
}
"
)

            
return
 
[
self
.
_fallback_embedding
(
text
)
 
for
 text 
in
 batch
]

    
    
def
 
_fallback_embedding
(
self
,
 text
:
 
str
)
 
-
>
 np
.
ndarray
:

        
"""Generate a simple but effective fallback embedding."""

        
# Use character n-grams with position weighting

        vector 
=
 np
.
zeros
(
self
.
dimension
,
 dtype
=
np
.
float32
)

        
        
# Normalize text

        text 
=
 text
.
lower
(
)
.
strip
(
)

        
        
if
 
not
 text
:

            
return
 vector
        
        
# Generate n-grams (1, 2, 3)

        
for
 n 
in
 
range
(
1
,
 
4
)
:

            weight 
=
 n 
/
 
6.0
  
# Weight by n-gram size

            
            
for
 i 
in
 
range
(
len
(
text
)
 
-
 n 
+
 
1
)
:

                ngram 
=
 text
[
i
:
i
+
n
]

                
                
# Hash n-gram to vector position

                hash_val 
=
 
int
(
hashlib
.
md5
(
ngram
.
encode
(
)
)
.
hexdigest
(
)
[
:
8
]
,
 
16
)

                idx 
=
 hash_val 
%
 self
.
dimension
                
                
# Add weighted value

                vector
[
idx
]
 
+=
 weight
        
        
# Apply TF-IDF style normalization

        vector 
=
 np
.
sqrt
(
vector
)
  
# Square root normalization

        
        
# Normalize to unit vector

        magnitude 
=
 np
.
linalg
.
norm
(
vector
)

        
if
 magnitude 
>
 
0
:

            vector 
=
 vector 
/
 magnitude
        
        
return
 vector
    
    
def
 
_get_cache_key
(
self
,
 text
:
 
str
)
 
-
>
 
str
:

        
"""Generate cache key for text."""

        
return
 hashlib
.
md5
(
text
.
encode
(
)
)
.
hexdigest
(
)

    
    
def
 
clear_cache
(
self
)
:

        
"""Clear embedding cache."""

        self
.
_cache
.
clear
(
)

        self
.
logger
.
info
(
"Embedding cache cleared"
)

    
    
def
 
get_cache_stats
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

        
"""Get cache statistics."""

        
return
 
{

            
"size"
:
 
len
(
self
.
_cache
)
,

            
"hits"
:
 self
.
_metrics
[
"cache_hits"
]
,

            
"misses"
:
 self
.
_metrics
[
"cache_misses"
]
,

            
"hit_rate"
:
 self
.
_metrics
[
"cache_hits"
]
 
/
 
max
(

                self
.
_metrics
[
"cache_hits"
]
 
+
 self
.
_metrics
[
"cache_misses"
]
,
 
1

            
)

        
}

    
    
def
 
get_metrics
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

        
"""Get performance metrics."""

        total_requests 
=
 self
.
_metrics
[
"total_requests"
]

        avg_time 
=
 self
.
_metrics
[
"total_time"
]
 
/
 
max
(
total_requests
,
 
1
)

        
        
return
 
{

            
**
self
.
_metrics
,

            
"average_time_per_request"
:
 avg_time
,

            
"cache_stats"
:
 self
.
get_cache_stats
(
)

        
}

    
    
async
 
def
 
find_similar
(

        self
,

        query
:
 
str
,

        candidates
:
 List
[
str
]
,

        threshold
:
 
float
 
=
 
0.7

    
)
 
-
>
 List
[
Tuple
[
str
,
 
float
]
]
:

        
"""Find similar strings to query."""

        query_embedding 
=
 
await
 self
.
generate_embedding
(
query
)

        candidate_embeddings 
=
 
await
 self
.
generate_embeddings
(
candidates
)

        
        similarities 
=
 
[
]

        
for
 text
,
 embedding 
in
 
zip
(
candidates
,
 candidate_embeddings
)
:

            sim 
=
 self
.
_cosine_similarity
(
query_embedding
,
 embedding
)

            
if
 sim 
>=
 threshold
:

                similarities
.
append
(
(
text
,
 sim
)
)

        
        
# Sort by similarity

        similarities
.
sort
(
key
=
lambda
 x
:
 x
[
1
]
,
 reverse
=
True
)

        
        
return
 similarities
    
    
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

        dot_product 
=
 np
.
dot
(
vec1
,
 vec2
)

        magnitude1 
=
 np
.
linalg
.
norm
(
vec1
)

        magnitude2 
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
 magnitude1 
==
 
0
 
or
 magnitude2 
==
 
0
:

            
return
 
0.0

        
        
return
 dot_product 
/
 
(
magnitude1 
*
 magnitude2
)

    
    
async
 
def
 
close
(
self
)
:

        
"""Close resources."""

        
if
 
hasattr
(
self
,
 
'_client'
)
:

            
await
 self
.
_client
.
close
(
)