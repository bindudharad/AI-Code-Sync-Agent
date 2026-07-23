# Memory package
 
memory/short_term.py
Python
 
 
 
Copy
 
import
 json

import
 asyncio

from
 collections 
import
 deque

from
 datetime 
import
 datetime
,
 timedelta

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



class
 
ShortTermMemory
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
capacity 
=
 config
[
"memory"
]
[
"short_term_capacity"
]

        self
.
memory 
=
 deque
(
maxlen
=
self
.
capacity
)

        self
.
retention_minutes 
=
 
30

    
    
async
 
def
 
store
(
self
,
 event
:
 
str
,
 context
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
:

        
"""Store an event in short-term memory."""

        entry 
=
 
{

            
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
,

            
"event"
:
 event
,

            
"context"
:
 context 
or
 
{
}

        
}

        self
.
memory
.
append
(
entry
)

    
    
async
 
def
 
get_recent
(
self
,
 n
:
 
int
 
=
 
10
)
 
-
>
 List
[
Dict
[
str
,
 Any
]
]
:

        
"""Get recent n entries."""

        
return
 
list
(
self
.
memory
)
[
-
n
:
]

    
    
async
 
def
 
get_recent_context
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

        
"""Get context from recent events."""

        recent 
=
 
await
 self
.
get_recent
(
)

        context 
=
 
{
}

        
        
for
 entry 
in
 recent
:

            
if
 entry
[
"context"
]
:

                context
.
update
(
entry
[
"context"
]
)

        
        
return
 context
    
    
async
 
def
 
search
(
self
,
 keyword
:
 
str
)
 
-
>
 List
[
Dict
[
str
,
 Any
]
]
:

        
"""Search for events containing keyword."""

        results 
=
 
[
]

        
        
for
 entry 
in
 self
.
memory
:

            
if
 keyword
.
lower
(
)
 
in
 entry
[
"event"
]
.
lower
(
)
:

                results
.
append
(
entry
)

        
        
return
 results
    
    
async
 
def
 
clear
(
self
)
:

        
"""Clear all short-term memory."""

        self
.
memory
.
clear
(
)

    
    
def
 
get_task_context
(
self
,
 task_id
:
 
str
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

        
"""Get context for a specific task."""

        context 
=
 
{
}

        
        
for
 entry 
in
 self
.
memory
:

            
if
 entry
[
"context"
]
.
get
(
"task_id"
)
 
==
 task_id
:

                context
.
update
(
entry
[
"context"
]
)

        
        
return
 context
 
memory/long_term.py
Python
 
 
 
Copy
 
import
 json

import
 asyncio

from
 pathlib 
import
 Path

from
 datetime 
import
 datetime
,
 timedelta

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

import
 hashlib



class
 
LongTermMemory
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
memory_file 
=
 Path
(
config
[
"paths"
]
[
"memory_store"
]
)

        self
.
memory_file
.
parent
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
knowledge_base
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

        self
.
pattern_index
:
 Dict
[
str
,
 List
[
str
]
]
 
=
 
{
}

    
    
async
 
def
 
load
(
self
)
:

        
"""Load long-term memory from disk."""

        
if
 self
.
memory_file
.
exists
(
)
:

            
try
:

                data 
=
 json
.
loads
(
self
.
memory_file
.
read_text
(
)
)

                self
.
knowledge_base 
=
 data
.
get
(
"knowledge_base"
,
 
{
}
)

                self
.
pattern_index 
=
 data
.
get
(
"pattern_index"
,
 
{
}
)

            
except
 Exception 
as
 e
:

                
print
(
f"Error loading long-term memory: 
{
e
}
"
)

                self
.
knowledge_base 
=
 
{
}

                self
.
pattern_index 
=
 
{
}

        
else
:

            self
.
knowledge_base 
=
 
{
}

            self
.
pattern_index 
=
 
{
}

    
    
async
 
def
 
store
(
self
,
 pattern
:
 
str
,
 strategy
:
 
str
,
 context
:
 Dict
[
str
,
 Any
]
)
:

        
"""Store knowledge in long-term memory."""

        knowledge_id 
=
 hashlib
.
md5
(
f"
{
pattern
}
:
{
strategy
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
[
:
12
]

        
        entry 
=
 
{

            
"knowledge_id"
:
 knowledge_id
,

            
"pattern"
:
 pattern
,

            
"strategy"
:
 strategy
,

            
"context"
:
 context
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
,

            
"usage_count"
:
 
0
,

            
"success_rate"
:
 
0.0

        
}

        
        self
.
knowledge_base
[
knowledge_id
]
 
=
 entry
        
        
# Index by pattern

        
if
 pattern 
not
 
in
 self
.
pattern_index
:

            self
.
pattern_index
[
pattern
]
 
=
 
[
]

        self
.
pattern_index
[
pattern
]
.
append
(
knowledge_id
)

    
    
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
 limit
:
 
int
 
=
 
5
)
 
-
>
 List
[
Dict
[
str
,
 Any
]
]
:

        
"""Find similar knowledge entries."""

        query_lower 
=
 query
.
lower
(
)

        results 
=
 
[
]

        
        
for
 knowledge_id
,
 entry 
in
 self
.
knowledge_base
.
items
(
)
:

            
# Simple similarity matching (could use embeddings in production)

            pattern_score 
=
 self
.
_calculate_similarity
(
query_lower
,
 entry
[
"pattern"
]
.
lower
(
)
)

            context_score 
=
 self
.
_calculate_context_similarity
(
query_lower
,
 entry
[
"context"
]
)

            
            total_score 
=
 pattern_score 
*
 
0.7
 
+
 context_score 
*
 
0.3

            
            
if
 total_score 
>
 
0.3
:
  
# Threshold

                results
.
append
(
{

                    
"entry"
:
 entry
,

                    
"score"
:
 total_score
                
}
)

        
        
# Sort by score and return top results

        results
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
"score"
]
,
 reverse
=
True
)

        
        
return
 
[
r
[
"entry"
]
 
for
 r 
in
 results
[
:
limit
]
]

    
    
def
 
_calculate_similarity
(
self
,
 query
:
 
str
,
 pattern
:
 
str
)
 
-
>
 
float
:

        
"""Calculate similarity between query and pattern."""

        
# Simple overlap coefficient

        query_words 
=
 
set
(
query
.
split
(
)
)

        pattern_words 
=
 
set
(
pattern
.
split
(
)
)

        
        
if
 
not
 query_words 
or
 
not
 pattern_words
:

            
return
 
0.0

        
        overlap 
=
 
len
(
query_words 
&
 pattern_words
)

        
return
 overlap 
/
 
len
(
query_words
)

    
    
def
 
_calculate_context_similarity
(
self
,
 query
:
 
str
,
 context
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
 
float
:

        
"""Calculate similarity based on context."""

        context_str 
=
 json
.
dumps
(
context
)
.
lower
(
)

        query_words 
=
 
set
(
query
.
split
(
)
)

        context_words 
=
 
set
(
context_str
.
split
(
)
)

        
        overlap 
=
 
len
(
query_words 
&
 context_words
)

        
return
 overlap 
/
 
len
(
query_words
)
 
if
 query_words 
else
 
0.0

    
    
async
 
def
 
get_strategy
(
self
,
 pattern
:
 
str
)
 
-
>
 Optional
[
str
]
:

        
"""Get best strategy for a pattern."""

        similar 
=
 
await
 self
.
find_similar
(
pattern
,
 limit
=
1
)

        
        
if
 similar
:

            best_match 
=
 similar
[
0
]

            best_match
[
"usage_count"
]
 
+=
 
1

            
return
 best_match
[
"strategy"
]

        
        
return
 
None

    
    
async
 
def
 
update_success_rate
(
self
,
 knowledge_id
:
 
str
,
 success
:
 
bool
)
:

        
"""Update success rate for a knowledge entry."""

        
if
 knowledge_id 
in
 self
.
knowledge_base
:

            entry 
=
 self
.
knowledge_base
[
knowledge_id
]

            total_uses 
=
 entry
[
"usage_count"
]

            
            
if
 total_uses 
>
 
0
:

                current_rate 
=
 entry
[
"success_rate"
]

                new_rate 
=
 
(
current_rate 
*
 
(
total_uses 
-
 
1
)
 
+
 
(
1.0
 
if
 success 
else
 
0.0
)
)
 
/
 total_uses
                entry
[
"success_rate"
]
 
=
 new_rate
    
    
async
 
def
 
persist
(
self
)
:

        
"""Persist long-term memory to disk."""

        data 
=
 
{

            
"knowledge_base"
:
 self
.
knowledge_base
,

            
"pattern_index"
:
 self
.
pattern_index
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

        
        
try
:

            self
.
memory_file
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

            
print
(
f"Error persisting long-term memory: 
{
e
}
"
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

        
"""Get memory statistics."""

        
return
 
{

            
"total_entries"
:
 
len
(
self
.
knowledge_base
)
,

            
"indexed_patterns"
:
 
len
(
self
.
pattern_index
)
,

            
"avg_success_rate"
:
 
sum
(
e
[
"success_rate"
]
 
for
 e 
in
 self
.
knowledge_base
.
values
(
)
)
 
/
 
len
(
self
.
knowledge_base
)
 
if
 self
.
knowledge_base 
else
 
0.0

        
}
 
memory/experience_memory.py
Python
 
 
 
Copy
 
import
 json

import
 asyncio

from
 pathlib 
import
 Path

from
 datetime 
import
 datetime
,
 timedelta

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

import
 hashlib



class
 
ExperienceMemory
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
experience_file 
=
 Path
(
config
[
"paths"
]
[
"memory_store"
]
)
.
parent 
/
 
"experience.json"

        self
.
experience_file
.
parent
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
experiences
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
 
=
 
[
]

        self
.
retention_days 
=
 config
[
"memory"
]
.
get
(
"experience_retention_days"
,
 
90
)

    
    
async
 
def
 
load
(
self
)
:

        
"""Load experience memory from disk."""

        
if
 self
.
experience_file
.
exists
(
)
:

            
try
:

                data 
=
 json
.
loads
(
self
.
experience_file
.
read_text
(
)
)

                self
.
experiences 
=
 data
.
get
(
"experiences"
,
 
[
]
)

            
except
 Exception 
as
 e
:

                
print
(
f"Error loading experience memory: 
{
e
}
"
)

                self
.
experiences 
=
 
[
]

        
else
:

            self
.
experiences 
=
 
[
]

    
    
async
 
def
 
store_success
(
self
,
 goal
,
 quality_score
:
 
float
)
:

        
"""Store a successful experience."""

        experience 
=
 
{

            
"experience_id"
:
 hashlib
.
md5
(
f"
{
goal
.
goal_id
}
:success"
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
16
]
,

            
"goal_id"
:
 goal
.
goal_id
,

            
"goal_title"
:
 goal
.
title
,

            
"type"
:
 
"success"
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
,

            
"quality_score"
:
 quality_score
,

            
"plan"
:
 goal
.
plan
.
to_dict
(
)
 
if
 goal
.
plan 
else
 
None
,

            
"lessons"
:
 self
.
_extract_lessons
(
goal
,
 
True
)

        
}

        
        self
.
experiences
.
append
(
experience
)

        
        
# Remove old experiences if needed

        
await
 self
.
_cleanup_old_experiences
(
)

    
    
async
 
def
 
store_failure
(
self
,
 task
,
 error
:
 
str
,
 context
:
 Dict
[
str
,
 Any
]
)
:

        
"""Store a failure experience."""

        experience 
=
 
{

            
"experience_id"
:
 hashlib
.
md5
(
f"
{
task
.
task_id
}
:failure"
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
16
]
,

            
"goal_id"
:
 context
.
get
(
"goal_id"
)
,

            
"task_id"
:
 task
.
task_id
,

            
"task_title"
:
 task
.
title
,

            
"type"
:
 
"failure"
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
,

            
"error"
:
 error
,

            
"context"
:
 context
,

            
"mitigation"
:
 self
.
_suggest_mitigation
(
task
,
 error
)

        
}

        
        self
.
experiences
.
append
(
experience
)

        
        
await
 self
.
_cleanup_old_experiences
(
)

    
    
async
 
def
 
store_reflection
(
self
,
 goal_id
:
 
str
,
 quality_score
:
 
float
,
 learnings
:
 List
,
 issues
:
 List
)
:

        
"""Store reflection experience."""

        experience 
=
 
{

            
"experience_id"
:
 hashlib
.
md5
(
f"
{
goal_id
}
:reflection"
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
16
]
,

            
"goal_id"
:
 goal_id
,

            
"type"
:
 
"reflection"
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
,

            
"quality_score"
:
 quality_score
,

            
"learnings"
:
 
[
learning
.
__dict__ 
if
 
hasattr
(
learning
,
 
"__dict__"
)
 
else
 learning 
for
 learning 
in
 learnings
]
,

            
"issues"
:
 issues
        
}

        
        self
.
experiences
.
append
(
experience
)

    
    
def
 
_extract_lessons
(
self
,
 goal
,
 success
:
 
bool
)
 
-
>
 List
[
str
]
:

        
"""Extract lessons from a goal execution."""

        lessons 
=
 
[
]

        
        
if
 goal
.
plan
:

            
# Analyze task completion patterns

            completed_tasks 
=
 
[
t 
for
 t 
in
 goal
.
plan
.
tasks 
if
 t
.
status 
==
 
"completed"
]

            failed_tasks 
=
 
[
t 
for
 t 
in
 goal
.
plan
.
tasks 
if
 t
.
status 
==
 
"failed"
]

            
            
if
 
len
(
completed_tasks
)
 
>
 
len
(
failed_tasks
)
 
*
 
3
:

                lessons
.
append
(
"Breaking work into small tasks improves success rate"
)

            
            
# Analyze time estimates

            
for
 task 
in
 goal
.
plan
.
tasks
:

                
if
 task
.
result 
and
 task
.
result
.
get
(
"actual_hours"
)
:

                    variance 
=
 
abs
(
task
.
result
[
"actual_hours"
]
 
-
 task
.
estimated_hours
)
 
/
 task
.
estimated_hours
                    
if
 variance 
>
 
0.5
:

                        lessons
.
append
(
f"Task '
{
task
.
title
}
' had large time variance - improve estimation"
)

        
        
return
 lessons
    
    
def
 
_suggest_mitigation
(
self
,
 task
,
 error
:
 
str
)
 
-
>
 
str
:

        
"""Suggest mitigation for a failure."""

        error_lower 
=
 error
.
lower
(
)

        
        
if
 
"import"
 
in
 error_lower
:

            
return
 
"Add dependency installation step before this task"

        
elif
 
"syntax"
 
in
 error_lower
:

            
return
 
"Add code quality check before execution"

        
elif
 
"connection"
 
in
 error_lower
:

            
return
 
"Verify database/service is running before this task"

        
elif
 
"permission"
 
in
 error_lower
:

            
return
 
"Add permission check and request step"

        
else
:

            
return
 
"Add error handling and retry logic"

    
    
async
 
def
 
find_similar_plans
(
self
,
 features
:
 List
[
Dict
]
)
 
-
>
 List
[
Dict
[
str
,
 Any
]
]
:

        
"""Find similar successful plans."""

        similar 
=
 
[
]

        
        
for
 experience 
in
 self
.
experiences
:

            
if
 experience
[
"type"
]
 
!=
 
"success"
 
or
 
not
 experience
.
get
(
"plan"
)
:

                
continue

            
            
# Calculate similarity based on features

            plan_features 
=
 self
.
_extract_features_from_plan
(
experience
[
"plan"
]
)

            similarity 
=
 self
.
_calculate_features_similarity
(
features
,
 plan_features
)

            
            
if
 similarity 
>
 
0.6
:

                similar
.
append
(
{

                    
"experience"
:
 experience
,

                    
"similarity"
:
 similarity
,

                    
"plan"
:
 experience
[
"plan"
]

                
}
)

        
        similar
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
"similarity"
]
,
 reverse
=
True
)

        
return
 similar
[
:
3
]

    
    
def
 
_extract_features_from_plan
(
self
,
 plan
:
 Dict
)
 
-
>
 List
[
Dict
]
:

        
"""Extract features from a plan."""

        features 
=
 
[
]

        
        
for
 task 
in
 plan
.
get
(
"tasks"
,
 
[
]
)
:

            title 
=
 task
.
get
(
"title"
,
 
""
)
.
lower
(
)

            
if
 
"auth"
 
in
 title
:

                features
.
append
(
{
"name"
:
 
"authentication"
}
)

            
elif
 
"api"
 
in
 title
:

                features
.
append
(
{
"name"
:
 
"api"
}
)

            
elif
 
"database"
 
in
 title
:

                features
.
append
(
{
"name"
:
 
"database"
}
)

            
elif
 
"frontend"
 
in
 title
:

                features
.
append
(
{
"name"
:
 
"frontend"
}
)

        
        
return
 features
    
    
def
 
_calculate_features_similarity
(
self
,
 features1
:
 List
[
Dict
]
,
 features2
:
 List
[
Dict
]
)
 
-
>
 
float
:

        
"""Calculate similarity between two feature lists."""

        f1_names 
=
 
{
f
.
get
(
"name"
)
 
for
 f 
in
 features1
}

        f2_names 
=
 
{
f
.
get
(
"name"
)
 
for
 f 
in
 features2
}

        
        
if
 
not
 f1_names 
or
 
not
 f2_names
:

            
return
 
0.0

        
        intersection 
=
 f1_names 
&
 f2_names
        union 
=
 f1_names 
|
 f2_names
        
        
return
 
len
(
intersection
)
 
/
 
len
(
union
)

    
    
async
 
def
 
_cleanup_old_experiences
(
self
)
:

        
"""Remove experiences older than retention period."""

        cutoff_date 
=
 datetime
.
now
(
)
 
-
 timedelta
(
days
=
self
.
retention_days
)

        
        self
.
experiences 
=
 
[

            exp 
for
 exp 
in
 self
.
experiences
            
if
 datetime
.
fromisoformat
(
exp
[
"timestamp"
]
)
 
>
 cutoff_date
        
]

    
    
async
 
def
 
persist
(
self
)
:

        
"""Persist experience memory to disk."""

        data 
=
 
{

            
"experiences"
:
 self
.
experiences
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

        
        
try
:

            self
.
experience_file
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

            
print
(
f"Error persisting experience memory: 
{
e
}
"
)

    
    
def
 
get_failure_patterns
(
self
)
 
-
>
 Dict
[
str
,
 
int
]
:

        
"""Get most common failure patterns."""

        patterns 
=
 
{
}

        
        
for
 exp 
in
 self
.
experiences
:

            
if
 exp
[
"type"
]
 
==
 
"failure"
:

                error 
=
 exp
[
"error"
]

                
# Extract error type

                error_type 
=
 error
.
split
(
":"
)
[
0
]
 
if
 
":"
 
in
 error 
else
 error
[
:
50
]

                patterns
[
error_type
]
 
=
 patterns
.
get
(
error_type
,
 
0
)
 
+
 
1

        
        
return
 
dict
(
sorted
(
patterns
.
items
(
)
,
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
)
 
memory/user_preferences.py
Python
 
 
 
Copy
 
import
 json

from
 pathlib 
import
 Path

from
 typing 
import
 Dict
,
 Any
,
 Optional



class
 
UserPreferences
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
prefs_file 
=
 Path
(
config
[
"paths"
]
[
"memory_store"
]
)
.
parent 
/
 
"user_preferences.json"

        self
.
prefs_file
.
parent
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
preferences
:
 Dict
[
str
,
 Any
]
 
=
 
{
}

        self
.
load
(
)

    
    
def
 
load
(
self
)
:

        
"""Load user preferences from disk."""

        
if
 self
.
prefs_file
.
exists
(
)
:

            
try
:

                self
.
preferences 
=
 json
.
loads
(
self
.
prefs_file
.
read_text
(
)
)

            
except
 Exception 
as
 e
:

                
print
(
f"Error loading user preferences: 
{
e
}
"
)

                self
.
preferences 
=
 
{
}

        
else
:

            self
.
preferences 
=
 
{

                
"preferred_tech_stack"
:
 
{

                    
"frontend"
:
 
"react"
,

                    
"backend"
:
 
"fastapi"
,

                    
"database"
:
 
"postgresql"

                
}
,

                
"coding_style"
:
 
{

                    
"indent_size"
:
 
4
,

                    
"quote_style"
:
 
"double"
,

                    
"naming_convention"
:
 
"snake_case"

                
}
,

                
"deployment_preference"
:
 
"docker"

            
}

            
            self
.
_save
(
)

    
    
def
 
get_preferences
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

        
"""Get all user preferences."""

        
return
 self
.
preferences
    
    
def
 
get
(
self
,
 key
:
 
str
,
 default
:
 Any 
=
 
None
)
 
-
>
 Any
:

        
"""Get a specific preference."""

        
return
 self
.
preferences
.
get
(
key
,
 default
)

    
    
def
 
update
(
self
,
 key
:
 
str
,
 value
:
 Any
)
:

        
"""Update a preference."""

        self
.
preferences
[
key
]
 
=
 value
        self
.
_save
(
)

    
    
def
 
update_tech_stack
(
self
,
 frontend
:
 Optional
[
str
]
 
=
 
None
,
 backend
:
 Optional
[
str
]
 
=
 
None
,
 database
:
 Optional
[
str
]
 
=
 
None
)
:

        
"""Update technology stack preferences."""

        
if
 
"preferred_tech_stack"
 
not
 
in
 self
.
preferences
:

            self
.
preferences
[
"preferred_tech_stack"
]
 
=
 
{
}

        
        
if
 frontend
:

            self
.
preferences
[
"preferred_tech_stack"
]
[
"frontend"
]
 
=
 frontend
        
if
 backend
:

            self
.
preferences
[
"preferred_tech_stack"
]
[
"backend"
]
 
=
 backend
        
if
 database
:

            self
.
preferences
[
"preferred_tech_stack"
]
[
"database"
]
 
=
 database
        
        self
.
_save
(
)

    
    
def
 
_save
(
self
)
:

        
"""Save preferences to disk."""

        
try
:

            self
.
prefs_file
.
write_text
(
json
.
dumps
(
self
.
preferences
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

            
print
(
f"Error saving user preferences: 
{
e
}
"
)
 
Now I'll continue with the tools directory:
tools/
init
.py
Python
 
 
 
Copy
 
# Tools package
 
tools/file_tool.py
Python
 
 
 
Copy
 
import
 os

import
 shutil

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



class
 
FileTool
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
allowed_extensions 
=
 config
[
"tools"
]
[
"file_tool"
]
[
"allowed_extensions"
]

        self
.
max_file_size_mb 
=
 config
[
"tools"
]
[
"file_tool"
]
[
"max_file_size_mb"
]

    
    
async
 
def
 
write_file
(
self
,
 file_path
:
 
str
,
 content
:
 
str
)
 
-
>
 
bool
:

        
"""Write content to a file safely."""

        path 
=
 Path
(
file_path
)

        
        
# Check extension

        
if
 path
.
suffix
.
lower
(
)
 
not
 
in
 self
.
allowed_extensions
:

            
raise
 ValueError
(
f"File extension 
{
path
.
suffix
}
 not allowed"
)

        
        
# Check size

        content_size_mb 
=
 
len
(
content
.
encode
(
'utf-8'
)
)
 
/
 
(
1024
 
*
 
1024
)

        
if
 content_size_mb 
>
 self
.
max_file_size_mb
:

            
raise
 ValueError
(
f"Content size 
{
content_size_mb
:
.1f
}
MB exceeds limit 
{
self
.
max_file_size_mb
}
MB"
)

        
        
# Create directory if needed

        path
.
parent
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

        
        
# Write file

        
try
:

            path
.
write_text
(
content
,
 encoding
=
'utf-8'
)

            
return
 
True

        
except
 Exception 
as
 e
:

            
print
(
f"Error writing file 
{
file_path
}
: 
{
e
}
"
)

            
return
 
False

    
    
async
 
def
 
read_file
(
self
,
 file_path
:
 
str
)
 
-
>
 Optional
[
str
]
:

        
"""Read file content."""

        path 
=
 Path
(
file_path
)

        
        
if
 
not
 path
.
exists
(
)
:

            
return
 
None

        
        
try
:

            
return
 path
.
read_text
(
encoding
=
'utf-8'
)

        
except
 Exception 
as
 e
:

            
print
(
f"Error reading file 
{
file_path
}
: 
{
e
}
"
)

            
return
 
None

    
    
async
 
def
 
delete_file
(
self
,
 file_path
:
 
str
)
 
-
>
 
bool
:

        
"""Delete a file."""

        path 
=
 Path
(
file_path
)

        
        
if
 
not
 path
.
exists
(
)
:

            
return
 
False

        
        
try
:

            path
.
unlink
(
)

            
return
 
True

        
except
 Exception 
as
 e
:

            
print
(
f"Error deleting file 
{
file_path
}
: 
{
e
}
"
)

            
return
 
False

    
    
async
 
def
 
copy_file
(
self
,
 src
:
 
str
,
 dest
:
 
str
)
 
-
>
 
bool
:

        
"""Copy a file."""

        
try
:

            shutil
.
copy2
(
src
,
 dest
)

            
return
 
True

        
except
 Exception 
as
 e
:

            
print
(
f"Error copying file 
{
src
}
 to 
{
dest
}
: 
{
e
}
"
)

            
return
 
False

    
    
async
 
def
 
move_file
(
self
,
 src
:
 
str
,
 dest
:
 
str
)
 
-
>
 
bool
:

        
"""Move a file."""

        
try
:

            shutil
.
move
(
src
,
 dest
)

            
return
 
True

        
except
 Exception 
as
 e
:

            
print
(
f"Error moving file 
{
src
}
 to 
{
dest
}
: 
{
e
}
"
)

            
return
 
False

    
    
async
 
def
 
create_directory
(
self
,
 dir_path
:
 
str
)
 
-
>
 
bool
:

        
"""Create a directory."""

        path 
=
 Path
(
dir_path
)

        
        
try
:

            path
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

            
return
 
True

        
except
 Exception 
as
 e
:

            
print
(
f"Error creating directory 
{
dir_path
}
: 
{
e
}
"
)

            
return
 
False

    
    
async
 
def
 
delete_directory
(
self
,
 dir_path
:
 
str
)
 
-
>
 
bool
:

        
"""Delete a directory and its contents."""

        path 
=
 Path
(
dir_path
)

        
        
if
 
not
 path
.
exists
(
)
:

            
return
 
False

        
        
try
:

            shutil
.
rmtree
(
path
)

            
return
 
True

        
except
 Exception 
as
 e
:

            
print
(
f"Error deleting directory 
{
dir_path
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
 
list_files
(
self
,
 dir_path
:
 
str
,
 pattern
:
 
str
 
=
 
"*"
)
 
-
>
 List
[
str
]
:

        
"""List files in a directory matching pattern."""

        path 
=
 Path
(
dir_path
)

        
        
if
 
not
 path
.
exists
(
)
:

            
return
 
[
]

        
        
try
:

            
return
 
[
str
(
f
)
 
for
 f 
in
 path
.
glob
(
pattern
)
]

        
except
 Exception 
as
 e
:

            
print
(
f"Error listing files in 
{
dir_path
}
: 
{
e
}
"
)

            
return
 
[
]

    
    
def
 
file_exists
(
self
,
 file_path
:
 
str
)
 
-
>
 
bool
:

        
"""Check if file exists."""

        
return
 Path
(
file_path
)
.
exists
(
)

    
    
def
 
get_file_size
(
self
,
 file_path
:
 
str
)
 
-
>
 
int
:

        
"""Get file size in bytes."""

        path 
=
 Path
(
file_path
)

        
        
if
 
not
 path
.
exists
(
)
:

            
return
 
0

        
        
try
:

            
return
 path
.
stat
(
)
.
st_size
        
except
 Exception
:

            
return
 
0

    
    
async
 
def
 
append_to_file
(
self
,
 file_path
:
 
str
,
 content
:
 
str
)
 
-
>
 
bool
:

        
"""Append content to a file."""

        path 
=
 Path
(
file_path
)

        
        
if
 
not
 path
.
exists
(
)
:

            
return
 
await
 self
.
write_file
(
file_path
,
 content
)

        
        
try
:

            
with
 
open
(
path
,
 
'a'
,
 encoding
=
'utf-8'
)
 
as
 f
:

                f
.
write
(
content
)

            
return
 
True

        
except
 Exception 
as
 e
:

            
print
(
f"Error appending to file 
{
file_path
}
: 
{
e
}
"
)

            
return
 
False
 
tools/code_generator.py
Python
 
 
 
Copy
 
import
 ast

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



class
 
CodeGenerator
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
user_preferences 
=
 
None
  
# Will be set later

    
    
def
 
set_user_preferences
(
self
,
 user_preferences
)
:

        
"""Set user preferences for code style."""

        self
.
user_preferences 
=
 user_preferences
    
    
def
 
generate_function
(

        self
,

        name
:
 
str
,

        params
:
 List
[
str
]
,

        body
:
 
str
,

        return_type
:
 Optional
[
str
]
 
=
 
None
,

        docstring
:
 Optional
[
str
]
 
=
 
None

    
)
 
-
>
 
str
:

        
"""Generate a function."""

        indent 
=
 
" "
 
*
 self
.
_get_indent_size
(
)

        
        code 
=
 
[
]

        
        
if
 docstring
:

            code
.
extend
(
self
.
_generate_docstring
(
docstring
,
 indent
)
)

        
        
# Function signature

        params_str 
=
 
", "
.
join
(
params
)

        func_def 
=
 
f"def 
{
name
}
(
{
params_str
}
)"

        
        
if
 return_type
:

            func_def 
+=
 
f" -> 
{
return_type
}
"

        
        func_def 
+=
 
":"

        code
.
append
(
func_def
)

        
        
# Function body

        
for
 line 
in
 body
.
splitlines
(
)
:

            code
.
append
(
f"
{
indent
}
{
line
}
"
)

        
        
return
 
"\n"
.
join
(
code
)

    
    
def
 
generate_class
(

        self
,

        name
:
 
str
,

        methods
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

        base_classes
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

        docstring
:
 Optional
[
str
]
 
=
 
None

    
)
 
-
>
 
str
:

        
"""Generate a class."""

        indent 
=
 
" "
 
*
 self
.
_get_indent_size
(
)

        
        code 
=
 
[
]

        
        
if
 docstring
:

            code
.
extend
(
self
.
_generate_docstring
(
docstring
,
 
""
)
)

        
        
# Class definition

        base_str 
=
 
f"(
{
', '
.
join
(
base_classes
)
}
)"
 
if
 base_classes 
else
 
""

        code
.
append
(
f"class 
{
name
}
{
base_str
}
:"
)

        
        
if
 methods
:

            
for
 method 
in
 methods
:

                method_code 
=
 self
.
generate_function
(

                    name
=
method
[
"name"
]
,

                    params
=
[
"self"
]
 
+
 method
.
get
(
"params"
,
 
[
]
)
,

                    body
=
method
.
get
(
"body"
,
 
"pass"
)
,

                    return_type
=
method
.
get
(
"return_type"
)
,

                    docstring
=
method
.
get
(
"docstring"
)

                
)

                
                
# Indent method code

                
for
 line 
in
 method_code
.
splitlines
(
)
:

                    code
.
append
(
f"
{
indent
}
{
line
}
"
)

                code
.
append
(
""
)
  
# Blank line between methods

        
else
:

            code
.
append
(
f"
{
indent
}
pass"
)

        
        
return
 
"\n"
.
join
(
code
)

    
    
def
 
generate_api_endpoint
(

        self
,

        method
:
 
str
,

        path
:
 
str
,

        handler_name
:
 
str
,

        params
:
 List
[
Dict
[
str
,
 
str
]
]
,

        return_type
:
 
str
,

        body
:
 Optional
[
str
]
 
=
 
None

    
)
 
-
>
 
str
:

        
"""Generate a FastAPI endpoint."""

        indent 
=
 
" "
 
*
 self
.
_get_indent_size
(
)

        
        code 
=
 
[
]

        
        
# Decorator

        code
.
append
(
f'@app.
{
method
.
lower
(
)
}
("
{
path
}
")'
)

        
        
# Function signature

        func_params 
=
 
[
]

        
for
 param 
in
 params
:

            param_str 
=
 param
[
"name"
]

            
if
 param
.
get
(
"type"
)
:

                param_str 
+=
 
f': 
{
param
[
"type"
]
}
'

            
if
 param
.
get
(
"default"
)
:

                param_str 
+=
 
f' = 
{
param
[
"default"
]
}
'

            func_params
.
append
(
param_str
)

        
        params_str 
=
 
", "
.
join
(
func_params
)

        func_def 
=
 
f"async def 
{
handler_name
}
(
{
params_str
}
) -> 
{
return_type
}
:"

        code
.
append
(
func_def
)

        
        
# Body

        
if
 body
:

            
for
 line 
in
 body
.
splitlines
(
)
:

                code
.
append
(
f"
{
indent
}
{
line
}
"
)

        
else
:

            code
.
append
(
f"
{
indent
}
# TODO: Implement endpoint logic"
)

            code
.
append
(
f"
{
indent
}
return {{{{}}}"
)

        
        
return
 
"\n"
.
join
(
code
)

    
    
def
 
generate_react_component
(

        self
,

        name
:
 
str
,

        props
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

        state
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

        jsx
:
 Optional
[
str
]
 
=
 
None
,

        hooks
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

    
)
 
-
>
 
str
:

        
"""Generate a React component."""

        code 
=
 
[
]

        
        
# Imports

        code
.
append
(
"import React from 'react';"
)

        
        
if
 hooks
:

            
for
 hook 
in
 hooks
:

                
if
 hook 
==
 
"useState"
:

                    code
.
append
(
"import { useState } from 'react';"
)

                
elif
 hook 
==
 
"useEffect"
:

                    code
.
append
(
"import { useEffect } from 'react';"
)

        
        code
.
append
(
""
)

        
        
# Component

        props_str 
=
 
f"{{ 
{
', '
.
join
(
props
)
}
 }}"
 
if
 props 
else
 
""

        code
.
append
(
f"function 
{
name
}
(
{
props_str
}
) {{"
)

        
        
# State

        
if
 state
:

            
for
 var_name
,
 initial_value 
in
 state
.
items
(
)
:

                code
.
append
(
f"  const [
{
var_name
}
, set
{
var_name
.
capitalize
(
)
}
] = useState(
{
initial_value
}
);"
)

            code
.
append
(
""
)

        
        
# Hooks

        
if
 hooks
:

            
for
 hook 
in
 hooks
:

                
if
 hook
.
startswith
(
"useEffect"
)
:

                    code
.
append
(
"  useEffect(() => {"
)

                    code
.
append
(
"    // TODO: Add effect logic"
)

                    code
.
append
(
"  }, []);"
)

                    code
.
append
(
""
)

        
        
# JSX return

        code
.
append
(
"  return ("
)

        code
.
append
(
"    <div>"
)

        
        
if
 jsx
:

            
for
 line 
in
 jsx
.
splitlines
(
)
:

                code
.
append
(
f"      
{
line
}
"
)

        
else
:

            code
.
append
(
f"      <h1>
{
name
}
 Component</h1>"
)

        
        code
.
append
(
"    </div>"
)

        code
.
append
(
"  );"
)

        code
.
append
(
"}"
)

        code
.
append
(
""
)

        code
.
append
(
f"export default 
{
name
}
;"
)

        
        
return
 
"\n"
.
join
(
code
)

    
    
def
 
generate_test_function
(

        self
,

        test_name
:
 
str
,

        function_name
:
 
str
,

        test_cases
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

    
)
 
-
>
 
str
:

        
"""Generate a test function."""

        code 
=
 
[
]

        
        code
.
append
(
f"def test_
{
test_name
}
():"
)

        code
.
append
(
f'    """Test 
{
function_name
}
 function."""'
)

        code
.
append
(
""
)

        
        
for
 i
,
 
case
 
in
 
enumerate
(
test_cases
)
:

            code
.
append
(
f"    # Test case 
{
i 
+
 
1
}
: 
{
case
.
get
(
'description'
,
 
''
)
}
"
)

            
            args 
=
 
", "
.
join
(
map
(
str
,
 
case
.
get
(
"args"
,
 
[
]
)
)
)

            expected 
=
 
case
.
get
(
"expected"
)

            
            code
.
append
(
f"    result = 
{
function_name
}
(
{
args
}
)"
)

            code
.
append
(
f"    assert result == 
{
expected
}
"
)

            code
.
append
(
""
)

        
        
return
 
"\n"
.
join
(
code
)

    
    
def
 
_get_indent_size
(
self
)
 
-
>
 
int
:

        
"""Get indent size from preferences."""

        
if
 self
.
user_preferences
:

            
return
 self
.
user_preferences
.
get
(
"coding_style"
,
 
{
}
)
.
get
(
"indent_size"
,
 
4
)

        
return
 
4

    
    
def
 
_generate_docstring
(
self
,
 text
:
 
str
,
 indent
:
 
str
)
 
-
>
 List
[
str
]
:

        
"""Generate a docstring."""

        quote_style 
=
 self
.
_get_quote_style
(
)

        
        
return
 
[

            
f'
{
indent
}
{
quote_style
}
{
text
}
{
quote_style
}
'

        
]

    
    
def
 
_get_quote_style
(
self
)
 
-
>
 
str
:

        
"""Get quote style from preferences."""

        
if
 self
.
user_preferences
:

            style 
=
 self
.
user_preferences
.
get
(
"coding_style"
,
 
{
}
)
.
get
(
"quote_style"
,
 
"double"
)

            
return
 
'"'
 
if
 style 
==
 
"double"
 
else
 
"'"

        
return
 
'"'

    
    
def
 
generate_sql_table
(

        self
,

        table_name
:
 
str
,

        columns
:
 List
[
Dict
[
str
,
 
str
]
]
,

        indexes
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

    
)
 
-
>
 
str
:

        
"""Generate SQL CREATE TABLE statement."""

        code 
=
 
[
f"CREATE TABLE 
{
table_name
}
 ("
]

        
        column_defs 
=
 
[
]

        
for
 col 
in
 columns
:

            col_def 
=
 
f"    
{
col
[
'name'
]
}
 
{
col
[
'type'
]
}
"

            
if
 col
.
get
(
"primary_key"
)
:

                col_def 
+=
 
" PRIMARY KEY"

            
if
 col
.
get
(
"unique"
)
:

                col_def 
+=
 
" UNIQUE"

            
if
 col
.
get
(
"nullable"
)
 
is
 
False
:

                col_def 
+=
 
" NOT NULL"

            column_defs
.
append
(
col_def
)

        
        code
.
append
(
",\n"
.
join
(
column_defs
)
)

        code
.
append
(
");"
)

        
        
# Add indexes

        
if
 indexes
:

            
for
 idx 
in
 indexes
:

                code
.
append
(
f"CREATE INDEX idx_
{
table_name
}
_
{
idx
}
 ON 
{
table_name
}
 (
{
idx
}
);"
)

        
        
return
 
"\n"
.
join
(
code
)
 
tools/code_editor.py
Python
 
 
 
Copy
 
import
 re

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



class
 
CodeEditor
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
    
    
def
 
insert_code
(

        self
,

        file_path
:
 
str
,

        code
:
 
str
,

        after
:
 Optional
[
str
]
 
=
 
None
,

        before
:
 Optional
[
str
]
 
=
 
None
,

        at_line
:
 Optional
[
int
]
 
=
 
None

    
)
 
-
>
 
bool
:

        
"""Insert code into a file."""

        path 
=
 Path
(
file_path
)

        
        
if
 
not
 path
.
exists
(
)
:

            
return
 
False

        
        content 
=
 path
.
read_text
(
)

        lines 
=
 content
.
splitlines
(
)

        
        
if
 at_line 
is
 
not
 
None
:

            
# Insert at specific line

            lines
.
insert
(
at_line
,
 code
)

        
elif
 after
:

            
# Insert after pattern

            
for
 i
,
 line 
in
 
enumerate
(
lines
)
:

                
if
 after 
in
 line
:

                    lines
.
insert
(
i 
+
 
1
,
 code
)

                    
break

        
elif
 before
:

            
# Insert before pattern

            
for
 i
,
 line 
in
 
enumerate
(
lines
)
:

                
if
 before 
in
 line
:

                    lines
.
insert
(
i
,
 code
)

                    
break

        
else
:

            
# Append to end

            lines
.
append
(
code
)

        
        path
.
write_text
(
"\n"
.
join
(
lines
)
)

        
return
 
True

    
    
def
 
replace_code
(

        self
,

        file_path
:
 
str
,

        old_code
:
 
str
,

        new_code
:
 
str

    
)
 
-
>
 
bool
:

        
"""Replace code in a file."""

        path 
=
 Path
(
file_path
)

        
        
if
 
not
 path
.
exists
(
)
:

            
return
 
False

        
        content 
=
 path
.
read_text
(
)

        
        
if
 old_code 
not
 
in
 content
:

            
return
 
False

        
        new_content 
=
 content
.
replace
(
old_code
,
 new_code
)

        path
.
write_text
(
new_content
)

        
return
 
True

    
    
def
 
find_code
(

        self
,

        file_path
:
 
str
,

        pattern
:
 
str
,

        context_lines
:
 
int
 
=
 
2

    
)
 
-
>
 List
[
Dict
[
str
,
 Any
]
]
:

        
"""Find code matching a pattern."""

        path 
=
 Path
(
file_path
)

        
        
if
 
not
 path
.
exists
(
)
:

            
return
 
[
]

        
        content 
=
 path
.
read_text
(
)

        lines 
=
 content
.
splitlines
(
)

        
        results 
=
 
[
]

        
        
for
 i
,
 line 
in
 
enumerate
(
lines
)
:

            
if
 pattern 
in
 line
:

                start 
=
 
max
(
0
,
 i 
-
 context_lines
)

                end 
=
 
min
(
len
(
lines
)
,
 i 
+
 context_lines 
+
 
1
)

                
                context 
=
 
"\n"
.
join
(
lines
[
start
:
end
]
)

                
                results
.
append
(
{

                    
"line_number"
:
 i
,

                    
"line_content"
:
 line
,

                    
"context"
:
 context
,

                    
"start"
:
 start
,

                    
"end"
:
 end
                
}
)

        
        
return
 results
    
    
def
 
add_import
(

        self
,

        file_path
:
 
str
,

        import_statement
:
 
str

    
)
 
-
>
 
bool
:

        
"""Add an import statement to a file."""

        path 
=
 Path
(
file_path
)

        
        
if
 
not
 path
.
exists
(
)
:

            
return
 
False

        
        content 
=
 path
.
read_text
(
)

        
        
# Check if import already exists

        
if
 import_statement 
in
 content
:

            
return
 
True

        
        
# Find insertion point (after existing imports)

        lines 
=
 content
.
splitlines
(
)

        insert_line 
=
 
0

        
        
for
 i
,
 line 
in
 
enumerate
(
lines
)
:

            
if
 line
.
startswith
(
"import "
)
 
or
 line
.
startswith
(
"from "
)
:

                insert_line 
=
 i 
+
 
1

            
elif
 line
.
strip
(
)
 
==
 
""
 
and
 insert_line 
>
 
0
:

                
continue

            
else
:

                
break

        
        lines
.
insert
(
insert_line
,
 import_statement
)

        path
.
write_text
(
"\n"
.
join
(
lines
)
)

        
return
 
True

    
    
def
 
refactor_function
(

        self
,

        file_path
:
 
str
,

        old_func_name
:
 
str
,

        new_func_name
:
 
str
,

        update_references
:
 
bool
 
=
 
True

    
)
 
-
>
 Tuple
[
bool
,
 List
[
str
]
]
:

        
"""Rename a function and optionally update references."""

        path 
=
 Path
(
file_path
)

        
        
if
 
not
 path
.
exists
(
)
:

            
return
 
False
,
 
[
]

        
        content 
=
 path
.
read_text
(
)

        
        
# Simple regex for function definition

        func_pattern 
=
 
rf'def\s+
{
old_func_name
}
\s*\('

        
        
if
 
not
 re
.
search
(
func_pattern
,
 content
)
:

            
return
 
False
,
 
[
]

        
        
# Rename function

        new_content 
=
 re
.
sub
(
func_pattern
,
 
f'def 
{
new_func_name
}
('
,
 content
)

        
        
# Update references if requested

        files_modified 
=
 
[
]

        
        
if
 update_references
:

            
# For simplicity, only update in the same file

            reference_pattern 
=
 
rf'\b
{
old_func_name
}
\s*\('

            new_content 
=
 re
.
sub
(
reference_pattern
,
 
f'
{
new_func_name
}
('
,
 new_content
)

            files_modified
.
append
(
file_path
)

        
        path
.
write_text
(
new_content
)

        
return
 
True
,
 files_modified
    
    
def
 
extract_method
(

        self
,

        file_path
:
 
str
,

        start_line
:
 
int
,

        end_line
:
 
int
,

        new_method_name
:
 
str

    
)
 
-
>
 
bool
:

        
"""Extract code into a new method."""

        path 
=
 Path
(
file_path
)

        
        
if
 
not
 path
.
exists
(
)
:

            
return
 
False

        
        lines 
=
 path
.
read_text
(
)
.
splitlines
(
)

        
        
if
 start_line 
<
 
0
 
or
 end_line 
>
 
len
(
lines
)
 
or
 start_line 
>=
 end_line
:

            
return
 
False

        
        
# Extract code

        extracted_lines 
=
 lines
[
start_line
:
end_line
]

        indent 
=
 
len
(
extracted_lines
[
0
]
)
 
-
 
len
(
extracted_lines
[
0
]
.
lstrip
(
)
)

        
        
# Create method

        method_lines 
=
 
[

            
f"def 
{
new_method_name
}
(self):"
,

            
"    \"\"\"Extracted method.\"\"\""

        
]

        
        
for
 line 
in
 extracted_lines
:

            
if
 line
.
strip
(
)
:

                method_lines
.
append
(
"    "
 
+
 line
[
indent
:
]
)

        
        
# Insert method before the extracted code

        lines
[
start_line
:
end_line
]
 
=
 method_lines 
+
 
[
f"
{
extracted_lines
[
0
]
[
:
indent]
}
self.
{
new_method_name
}
()"
]

        
        path
.
write_text
(
"\n"
.
join
(
lines
)
)

        
return
 
True
 
tools/command_runner.py
Python
 
 
 
Copy
 
import
 asyncio

import
 subprocess

from
 dataclasses 
import
 dataclass

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



@dataclass


class
 
CommandResult
:

    returncode
:
 
int

    stdout
:
 
str

    stderr
:
 
str

    execution_time
:
 
float




class
 
CommandRunner
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
allowed_commands 
=
 config
[
"tools"
]
[
"command_runner"
]
[
"allowed_commands"
]

        self
.
sandbox_mode 
=
 config
[
"tools"
]
[
"command_runner"
]
[
"sandbox_mode"
]

        self
.
timeout 
=
 config
[
"limits"
]
[
"execution_timeout"
]

    
    
async
 
def
 
run_command
(

        self
,

        command
:
 List
[
str
]
,

        cwd
:
 Optional
[
str
]
 
=
 
None
,

        env
:
 Optional
[
Dict
[
str
,
 
str
]
]
 
=
 
None
,

        timeout
:
 Optional
[
int
]
 
=
 
None

    
)
 
-
>
 CommandResult
:

        
"""Run a command with safety checks."""

        
        
# Check if command is allowed

        command_name 
=
 command
[
0
]

        
if
 command_name 
not
 
in
 self
.
allowed_commands
:

            
return
 CommandResult
(

                returncode
=
1
,

                stdout
=
""
,

                stderr
=
f"Command '
{
command_name
}
' not allowed"
,

                execution_time
=
0.0

            
)

        
        
# Set timeout

        exec_timeout 
=
 timeout 
or
 self
.
timeout
        
        
try
:

            start_time 
=
 asyncio
.
get_event_loop
(
)
.
time
(
)

            
            
# Run command

            process 
=
 
await
 asyncio
.
create_subprocess_exec
(

                
*
command
,

                cwd
=
cwd
,

                env
=
env
,

                stdout
=
asyncio
.
subprocess
.
PIPE
,

                stderr
=
asyncio
.
subprocess
.
PIPE
            
)

            
            
try
:

                stdout
,
 stderr 
=
 
await
 asyncio
.
wait_for
(

                    process
.
communicate
(
)
,

                    timeout
=
exec_timeout
                
)

                
                execution_time 
=
 asyncio
.
get_event_loop
(
)
.
time
(
)
 
-
 start_time
                
                
return
 CommandResult
(

                    returncode
=
process
.
returncode
,

                    stdout
=
stdout
.
decode
(
'utf-8'
,
 errors
=
'ignore'
)
,

                    stderr
=
stderr
.
decode
(
'utf-8'
,
 errors
=
'ignore'
)
,

                    execution_time
=
execution_time
                
)

                
            
except
 asyncio
.
TimeoutError
:

                process
.
kill
(
)

                
await
 process
.
communicate
(
)

                
                
return
 CommandResult
(

                    returncode
=
1
,

                    stdout
=
""
,

                    stderr
=
f"Command timed out after 
{
exec_timeout
}
 seconds"
,

                    execution_time
=
exec_timeout
                
)

        
        
except
 Exception 
as
 e
:

            
return
 CommandResult
(

                returncode
=
1
,

                stdout
=
""
,

                stderr
=
f"Error running command: 
{
str
(
e
)
}
"
,

                execution_time
=
0.0

            
)

    
    
async
 
def
 
run_shell_command
(

        self
,

        command
:
 
str
,

        cwd
:
 Optional
[
str
]
 
=
 
None
,

        env
:
 Optional
[
Dict
[
str
,
 
str
]
]
 
=
 
None
,

        timeout
:
 Optional
[
int
]
 
=
 
None

    
)
 
-
>
 CommandResult
:

        
"""Run a shell command (more flexible but less safe)."""

        
        
# In sandbox mode, only allow simple commands

        
if
 self
.
sandbox_mode 
and
 
any
 dangerous 
in
 command 
for
 dangerous 
in
 
[
"rm -rf"
,
 
">"
,
 
"|"
,
 
"&&"
,
 
"||"
]
)
:

            
return
 CommandResult
(

                returncode
=
1
,

                stdout
=
""
,

                stderr
=
"Dangerous command pattern detected in sandbox mode"
,

                execution_time
=
0.0

            
)

        
        
try
:

            start_time 
=
 asyncio
.
get_event_loop
(
)
.
time
(
)

            
            process 
=
 
await
 asyncio
.
create_subprocess_shell
(

                command
,

                cwd
=
cwd
,

                env
=
env
,

                stdout
=
asyncio
.
subprocess
.
PIPE
,

                stderr
=
asyncio
.
subprocess
.
PIPE
            
)

            
            
try
:

                stdout
,
 stderr 
=
 
await
 asyncio
.
wait_for
(

                    process
.
communicate
(
)
,

                    timeout
=
timeout 
or
 self
.
timeout
                
)

                
                execution_time 
=
 asyncio
.
get_event_loop
(
)
.
time
(
)
 
-
 start_time
                
                
return
 CommandResult
(

                    returncode
=
process
.
returncode
,

                    stdout
=
stdout
.
decode
(
'utf-8'
,
 errors
=
'ignore'
)
,

                    stderr
=
stderr
.
decode
(
'utf-8'
,
 errors
=
'ignore'
)
,

                    execution_time
=
execution_time
                
)

                
            
except
 asyncio
.
TimeoutError
:

                process
.
kill
(
)

                
await
 process
.
communicate
(
)

                
                
return
 CommandResult
(

                    returncode
=
1
,

                    stdout
=
""
,

                    stderr
=
"Command timed out"
,

                    execution_time
=
timeout 
or
 self
.
timeout
                
)

        
        
except
 Exception 
as
 e
:

            
return
 CommandResult
(

                returncode
=
1
,

                stdout
=
""
,

                stderr
=
f"Error: 
{
str
(
e
)
}
"
,

                execution_time
=
0.0

            
)

    
    
def
 
validate_command
(
self
,
 command
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

        
"""Validate if a command is safe to run."""

        
if
 
not
 command
:

            
return
 
False

        
        command_name 
=
 command
[
0
]

        
        
if
 command_name 
not
 
in
 self
.
allowed_commands
:

            
return
 
False

        
        
# Additional validation for specific commands

        
if
 command_name 
==
 
"rm"
:

            
# Prevent dangerous rm commands

            
if
 
"-rf"
 
in
 command 
or
 
"*"
 
in
 
" "
.
join
(
command
)
:

                
return
 
False

        
        
return
 
True
 
tools/test_runner.py
Python
 
 
 
Copy
 
import
 json

import
 asyncio

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

from
 dataclasses 
import
 dataclass



@dataclass


class
 
TestRunResult
:

    test_type
:
 
str

    passed
:
 
bool

    coverage
:
 
float

    failures
:
 List
[
str
]

    execution_time
:
 
float




class
 
TestRunner
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
coverage_threshold 
=
 config
[
"testing"
]
[
"coverage_threshold"
]

    
    
async
 
def
 
run_test_suite
(
self
,
 project_path
:
 
str
,
 test_config
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
 TestRunResult
:

        
"""Run a test suite based on configuration."""

        test_type 
=
 test_config
.
get
(
"type"
,
 
"unit"
)

        
        
if
 test_type 
==
 
"unit"
:

            
return
 
await
 self
.
run_unit_tests
(
project_path
)

        
elif
 test_type 
==
 
"integration"
:

            
return
 
await
 self
.
run_integration_tests
(
project_path
)

        
elif
 test_type 
==
 
"api"
:

            
return
 
await
 self
.
run_api_tests
(
project_path
)

        
elif
 test_type 
==
 
"ui"
:

            
return
 
await
 self
.
run_ui_tests
(
project_path
)

        
else
:

            
return
 TestRunResult
(

                test_type
=
test_type
,

                passed
=
False
,

                coverage
=
0.0
,

                failures
=
[
f"Unknown test type: 
{
test_type
}
"
]
,

                execution_time
=
0.0

            
)

    
    
async
 
def
 
run_unit_tests
(
self
,
 project_path
:
 
str
)
 
-
>
 TestRunResult
:

        
"""Run unit tests using pytest."""

        
import
 sys
        
        start_time 
=
 asyncio
.
get_event_loop
(
)
.
time
(
)

        
        
# Find test files

        test_files 
=
 
list
(
Path
(
project_path
)
.
glob
(
"**/test_*.py"
)
)

        test_files
.
extend
(
list
(
Path
(
project_path
)
.
glob
(
"**/*_test.py"
)
)
)

        
        
if
 
not
 test_files
:

            
return
 TestRunResult
(

                test_type
=
"unit"
,

                passed
=
True
,

                coverage
=
0.0
,

                failures
=
[
]
,

                execution_time
=
0.0

            
)

        
        
# Run pytest

        
import
 subprocess
        
        
try
:

            result 
=
 
await
 asyncio
.
create_subprocess_exec
(

                sys
.
executable
,
 
"-m"
,
 
"pytest"
,
 
"--tb=short"
,

                
*
[
str
(
f
)
 
for
 f 
in
 test_files
]
,

                cwd
=
project_path
,

                stdout
=
asyncio
.
subprocess
.
PIPE
,

                stderr
=
asyncio
.
subprocess
.
PIPE
            
)

            
            stdout
,
 stderr 
=
 
await
 result
.
communicate
(
)

            execution_time 
=
 asyncio
.
get_event_loop
(
)
.
time
(
)
 
-
 start_time
            
            passed 
=
 result
.
returncode 
==
 
0

            
            
return
 TestRunResult
(

                test_type
=
"unit"
,

                passed
=
passed
,

                coverage
=
0.0
,
  
# Could extract from coverage plugin

                failures
=
self
.
_parse_pytest_failures
(
stderr
.
decode
(
)
)
,

                execution_time
=
execution_time
            
)

        
        
except
 Exception 
as
 e
:

            
return
 TestRunResult
(

                test_type
=
"unit"
,

                passed
=
False
,

                coverage
=
0.0
,

                failures
=
[
str
(
e
)
]
,

                execution_time
=
0.0

            
)

    
    
async
 
def
 
run_integration_tests
(
self
,
 project_path
:
 
str
)
 
-
>
 TestRunResult
:

        
"""Run integration tests."""

        start_time 
=
 asyncio
.
get_event_loop
(
)
.
time
(
)

        
        
# Look for integration test files

        integration_files 
=
 
list
(
Path
(
project_path
)
.
glob
(
"**/integration/test_*.py"
)
)

        
        
if
 
not
 integration_files
:

            
return
 TestRunResult
(

                test_type
=
"integration"
,

                passed
=
True
,

                coverage
=
0.0
,

                failures
=
[
]
,

                execution_time
=
0.0

            
)

        
        
# Run integration tests

        result 
=
 
await
 self
.
run_unit_tests
(
str
(
integration_files
[
0
]
.
parent
)
)

        result
.
test_type 
=
 
"integration"

        result
.
execution_time 
=
 asyncio
.
get_event_loop
(
)
.
time
(
)
 
-
 start_time
        
        
return
 result
    
    
async
 
def
 
run_api_tests
(
self
,
 project_path
:
 
str
)
 
-
>
 TestRunResult
:

        
"""Run API tests."""

        start_time 
=
 asyncio
.
get_event_loop
(
)
.
time
(
)

        
        
# Check if FastAPI app exists

        main_app 
=
 Path
(
project_path
)
 
/
 
"main.py"

        app_app 
=
 Path
(
project_path
)
 
/
 
"app.py"

        
        
if
 
not
 main_app
.
exists
(
)
 
and
 
not
 app_app
.
exists
(
)
:

            
return
 TestRunResult
(

                test_type
=
"api"
,

                passed
=
False
,

                coverage
=
0.0
,

                failures
=
[
"No main application file found"
]
,

                execution_time
=
0.0

            
)

        
        
# Run simple health check test

        
import
 sys
        
        test_code 
=
 
f'''
import sys
sys.path.insert(0, "
{
project_path
}
")

try:
    from fastapi.testclient import TestClient
    try:
        from main import app
    except ImportError:
        from app import app
    
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    print("API test passed")
except Exception as e:
    print(f"API test failed: {{e}}")
    sys.exit(1)
'''

        
        
try
:

            result 
=
 
await
 asyncio
.
create_subprocess_exec
(

                sys
.
executable
,
 
"-c"
,
 test_code
,

                stdout
=
asyncio
.
subprocess
.
PIPE
,

                stderr
=
asyncio
.
subprocess
.
PIPE
            
)

            
            stdout
,
 stderr 
=
 
await
 result
.
communicate
(
)

            execution_time 
=
 asyncio
.
get_event_loop
(
)
.
time
(
)
 
-
 start_time
            
            passed 
=
 result
.
returncode 
==
 
0

            
            
return
 TestRunResult
(

                test_type
=
"api"
,

                passed
=
passed
,

                coverage
=
0.0
,

                failures
=
[
]
 
if
 passed 
else
 
[
stderr
.
decode
(
)
]
,

                execution_time
=
execution_time
            
)

        
        
except
 Exception 
as
 e
:

            
return
 TestRunResult
(

                test_type
=
"api"
,

                passed
=
False
,

                coverage
=
0.0
,

                failures
=
[
str
(
e
)
]
,

                execution_time
=
0.0

            
)

    
    
async
 
def
 
run_ui_tests
(
self
,
 project_path
:
 
str
)
 
-
>
 TestRunResult
:

        
"""Run UI tests."""

        start_time 
=
 asyncio
.
get_event_loop
(
)
.
time
(
)

        
        
# Check for Playwright

        package_json 
=
 Path
(
project_path
)
 
/
 
"package.json"

        
        
if
 
not
 package_json
.
exists
(
)
:

            
return
 TestRunResult
(

                test_type
=
"ui"
,

                passed
=
False
,

                coverage
=
0.0
,

                failures
=
[
"No package.json found - not a Node.js project"
]
,

                execution_time
=
0.0

            
)

        
        
# Try to run Playwright tests

        
try
:

            result 
=
 
await
 asyncio
.
create_subprocess_exec
(

                
"npx"
,
 
"playwright"
,
 
"test"
,

                cwd
=
project_path
,

                stdout
=
asyncio
.
subprocess
.
PIPE
,

                stderr
=
asyncio
.
subprocess
.
PIPE
            
)

            
            stdout
,
 stderr 
=
 
await
 result
.
communicate
(
)

            execution_time 
=
 asyncio
.
get_event_loop
(
)
.
time
(
)
 
-
 start_time
            
            passed 
=
 result
.
returncode 
==
 
0

            
            
return
 TestRunResult
(

                test_type
=
"ui"
,

                passed
=
passed
,

                coverage
=
0.0
,

                failures
=
[
]
 
if
 passed 
else
 
[
stderr
.
decode
(
)
]
,

                execution_time
=
execution_time
            
)

        
        
except
 Exception 
as
 e
:

            
return
 TestRunResult
(

                test_type
=
"ui"
,

                passed
=
False
,

                coverage
=
0.0
,

                failures
=
[
f"Playwright not available: 
{
str
(
e
)
}
"
]
,

                execution_time
=
0.0

            
)

    
    
def
 
_parse_pytest_failures
(
self
,
 stderr
:
 
str
)
 
-
>
 List
[
str
]
:

        
"""Parse pytest failures from output."""

        failures 
=
 
[
]

        lines 
=
 stderr
.
splitlines
(
)

        
        in_failure 
=
 
False

        current_failure 
=
 
[
]

        
        
for
 line 
in
 lines
:

            
if
 
"FAILED"
 
in
 line 
or
 
"ERROR"
 
in
 line
:

                in_failure 
=
 
True

                current_failure 
=
 
[
line
]

            
elif
 in_failure 
and
 line
.
strip
(
)
 
and
 
not
 line
.
startswith
(
"="
)
:

                current_failure
.
append
(
line
)

            
elif
 in_failure 
and
 line
.
startswith
(
"="
)
:

                
if
 current_failure
:

                    failures
.
append
(
"\n"
.
join
(
current_failure
)
)

                in_failure 
=
 
False

                current_failure 
=
 
[
]

        
        
if
 current_failure
:

            failures
.
append
(
"\n"
.
join
(
current_failure
)
)

        
        
return
 failures
[
:
5
]
  
# Limit to first 5 failures

    
    
def
 
generate_test_template
(
self
,
 description
:
 
str
,
 requirements
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
 
str
:

        
"""Generate a test template based on description."""

        
if
 
"api"
 
in
 description
.
lower
(
)
:

            
return
 self
.
_generate_api_test_template
(
requirements
)

        
elif
 
"database"
 
in
 description
.
lower
(
)
:

            
return
 self
.
_generate_database_test_template
(
requirements
)

        
else
:

            
return
 self
.
_generate_unit_test_template
(
requirements
)

    
    
def
 
_generate_api_test_template
(
self
,
 requirements
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
 
str
:

        
"""Generate API test template."""

        
return
 
'''import pytest
from fastapi.testclient import TestClient

def test_health_endpoint():
    """Test health check endpoint."""
    # TODO: Import app
    # client = TestClient(app)
    # response = client.get("/health")
    # assert response.status_code == 200
    pass

def test_api_endpoints():
    """Test API endpoints."""
    # TODO: Add endpoint tests
    pass
'''

    
    
def
 
_generate_database_test_template
(
self
,
 requirements
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
 
str
:

        
"""Generate database test template."""

        
return
 
'''import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def test_database_connection():
    """Test database connection."""
    # TODO: Add connection test
    pass

def test_models():
    """Test database models."""
    # TODO: Add model tests
    pass
'''

    
    
def
 
_generate_unit_test_template
(
self
,
 requirements
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
 
str
:

        
"""Generate unit test template."""

        
return
 
'''import pytest

def test_functionality():
    """Test main functionality."""
    # TODO: Add unit tests
    assert True
'''
 
tools/browser_tool.py
Python
 
 
 
Copy
 
import
 asyncio

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

from
 dataclasses 
import
 dataclass

import
 json



@dataclass


class
 
BrowserAction
:

    action
:
 
str
  
# goto, click, fill, screenshot, evaluate

    selector
:
 Optional
[
str
]
 
=
 
None

    value
:
 Optional
[
str
]
 
=
 
None

    url
:
 Optional
[
str
]
 
=
 
None

    script
:
 Optional
[
str
]
 
=
 
None




@dataclass


class
 
BrowserResult
:

    success
:
 
bool

    data
:
 Optional
[
str
]
 
=
 
None

    error
:
 Optional
[
str
]
 
=
 
None

    screenshot
:
 Optional
[
bytes
]
 
=
 
None




class
 
BrowserTool
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
headless 
=
 config
[
"tools"
]
[
"browser_tool"
]
[
"headless"
]

        self
.
timeout 
=
 config
[
"tools"
]
[
"browser_tool"
]
[
"timeout"
]

        self
.
browser 
=
 
None

        self
.
page 
=
 
None

    
    
async
 
def
 
initialize
(
self
)
:

        
"""Initialize browser instance."""

        
try
:

            
from
 playwright
.
async_api 
import
 async_playwright
            
            self
.
playwright 
=
 
await
 async_playwright
(
)
.
start
(
)

            self
.
browser 
=
 
await
 self
.
playwright
.
chromium
.
launch
(

                headless
=
self
.
headless
            
)

            
        
except
 ImportError
:

            
print
(
"Playwright not installed. Run: pip install playwright"
)

            self
.
browser 
=
 
None

    
    
async
 
def
 
execute_action
(
self
,
 action
:
 BrowserAction
)
 
-
>
 BrowserResult
:

        
"""Execute a browser action."""

        
if
 
not
 self
.
browser
:

            
return
 BrowserResult
(

                success
=
False
,

                error
=
"Browser not initialized"

            
)

        
        
try
:

            
if
 
not
 self
.
page
:

                self
.
page 
=
 
await
 self
.
browser
.
new_page
(
)

                self
.
page
.
set_default_timeout
(
self
.
timeout 
*
 
1000
)

            
            
if
 action
.
action 
==
 
"goto"
:

                
await
 self
.
page
.
goto
(
action
.
url
)

                
return
 BrowserResult
(
success
=
True
)

            
            
elif
 action
.
action 
==
 
"click"
:

                
await
 self
.
page
.
click
(
action
.
selector
)

                
return
 BrowserResult
(
success
=
True
)

            
            
elif
 action
.
action 
==
 
"fill"
:

                
await
 self
.
page
.
fill
(
action
.
selector
,
 action
.
value
)

                
return
 BrowserResult
(
success
=
True
)

            
            
elif
 action
.
action 
==
 
"screenshot"
:

                screenshot 
=
 
await
 self
.
page
.
screenshot
(
)

                
return
 BrowserResult
(
success
=
True
,
 screenshot
=
screenshot
)

            
            
elif
 action
.
action 
==
 
"evaluate"
:

                result 
=
 
await
 self
.
page
.
evaluate
(
action
.
script
)

                
return
 BrowserResult
(

                    success
=
True
,

                    data
=
json
.
dumps
(
result
)

                
)

            
            
elif
 action
.
action 
==
 
"text"
:

                text 
=
 
await
 self
.
page
.
inner_text
(
action
.
selector
)

                
return
 BrowserResult
(
success
=
True
,
 data
=
text
)

            
            
else
:

                
return
 BrowserResult
(

                    success
=
False
,

                    error
=
f"Unknown action: 
{
action
.
action
}
"

                
)

        
        
except
 Exception 
as
 e
:

            
return
 BrowserResult
(

                success
=
False
,

                error
=
str
(
e
)

            
)

    
    
async
 
def
 
run_test_sequence
(
self
,
 actions
:
 List
[
BrowserAction
]
)
 
-
>
 List
[
BrowserResult
]
:

        
"""Run a sequence of browser actions."""

        results 
=
 
[
]

        
        
for
 action 
in
 actions
:

            result 
=
 
await
 self
.
execute_action
(
action
)

            results
.
append
(
result
)

            
            
if
 
not
 result
.
success
:

                
break

        
        
return
 results
    
    
async
 
def
 
test_ui_flow
(
self
,
 project_path
:
 
str
,
 user_flow
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
 Dict
[
str
,
 Any
]
:

        
"""Test a UI flow."""

        actions 
=
 user_flow
.
get
(
"steps"
,
 
[
]
)

        browser_actions 
=
 
[
]

        
        
for
 step 
in
 actions
:

            
if
 step
[
"action"
]
 
==
 
"visit"
:

                browser_actions
.
append
(
BrowserAction
(

                    action
=
"goto"
,

                    url
=
step
.
get
(
"url"
,
 
"http://localhost:3000"
)

                
)
)

            
elif
 step
[
"action"
]
 
==
 
"click"
:

                browser_actions
.
append
(
BrowserAction
(

                    action
=
"click"
,

                    selector
=
step
.
get
(
"selector"
)

                
)
)

            
elif
 step
[
"action"
]
 
==
 
"fill"
:

                browser_actions
.
append
(
BrowserAction
(

                    action
=
"fill"
,

                    selector
=
step
.
get
(
"selector"
)
,

                    value
=
step
.
get
(
"value"
)

                
)
)

        
        results 
=
 
await
 self
.
run_test_sequence
(
browser_actions
)

        
        
# Take final screenshot

        screenshot_action 
=
 BrowserAction
(
action
=
"screenshot"
)

        screenshot_result 
=
 
await
 self
.
execute_action
(
screenshot_action
)

        
        
return
 
{

            
"passed"
:
 
all
(
r
.
success 
for
 r 
in
 results
)
,

            
"results"
:
 results
,

            
"final_screenshot"
:
 screenshot_result
.
screenshot
        
}

    
    
async
 
def
 
close
(
self
)
:

        
"""Close browser instance."""

        
if
 self
.
page
:

            
await
 self
.
page
.
close
(
)

            self
.
page 
=
 
None

        
        
if
 self
.
browser
:

            
await
 self
.
browser
.
close
(
)

            self
.
browser 
=
 
None

        
        
if
 
hasattr
(
self
,
 
'playwright'
)
:

            
await
 self
.
playwright
.
stop
(
)
 
Let me continue with the web intelligence modules and remaining components in the next batch.
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 Next
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
Edit
 
 
Copy
 
 
Share
 
 
 
 
 
 
 
 
 
 
 
 
 
Autonomous AI Web Developer System Production Ready Safe Extensible
 
 
 
 
The user wants me to continue generating the code for the autonomous AI web developer system. I've already created:
main.py
config/
core/ (ai_brain, goal_manager, requirement_engine, planner, reflection_engine, code_quality_engine, metrics_engine, testing_engine)
agents/ (manager, architect, backend, frontend, database, qa, reviewer, devops)
memory/ (short_term, long_term, experience_memory, user_preferences)
tools/ (file_tool, code_generator, code_editor, command_runner, test_runner, browser_tool)
Now I need to create:
web_intelligence/ (frontend_intel, backend_intel, database_intel, auth_intel, api_designer)
execution/ (sandbox, error_handler)
versioning/ (git_manager, diff_engine)
interface/ (cli, dashboard - though dashboard may be optional, cli is mandatory)
Let me continue systematically.
web_intelligence/frontend_intel.py
Python
 
 
 
Copy
 
"""
Frontend intelligence module for generating React/Next.js code.
"""


import
 json

from
 typing 
import
 Dict
,
 List
,
 Any



class
 
FrontendIntel
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
framework 
=
 
"react"
  
# Default

    
    
def
 
generate_login_component
(
self
)
 
-
>
 
str
:

        
"""Generate a React login component."""

        
return
 
'''import React, { useState } from 'react';
import { authService } from '../services/auth';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    try {
      await authService.login(email, password);
      window.location.href = '/dashboard';
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="login-container">
      <h2>Login</h2>
      {error && <div className="error">{error}</div>}
      <form onSubmit={handleSubmit}>
        <div>
          <label>Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default Login;
'''

    
    
def
 
generate_register_component
(
self
)
 
-
>
 
str
:

        
"""Generate a React register component."""

        
return
 
'''import React, { useState } from 'react';
import { authService } from '../services/auth';

function Register() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    try {
      await authService.register({ name, email, password });
      window.location.href = '/login';
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="register-container">
      <h2>Register</h2>
      {error && <div className="error">{error}</div>}
      <form onSubmit={handleSubmit}>
        <div>
          <label>Name:</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Register</button>
      </form>
    </div>
  );
}

export default Register;
'''

    
    
def
 
generate_auth_service
(
self
)
 
-
>
 
str
:

        
"""Generate authentication service."""

        
return
 
'''import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

class AuthService {
  async login(email, password) {
    const response = await axios.post(`${API_URL}/auth/login`, {
      email,
      password
    });
    
    if (response.data.token) {
      localStorage.setItem('token', response.data.token);
    }
    
    return response.data;
  }

  async register(userData) {
    const response = await axios.post(`${API_URL}/auth/register`, userData);
    return response.data;
  }

  logout() {
    localStorage.removeItem('token');
  }

  getToken() {
    return localStorage.getItem('token');
  }

  getAuthHeader() {
    const token = this.getToken();
    return token ? { Authorization: `Bearer ${token}` } : {};
  }
}

export const authService = new AuthService();
'''

    
    
def
 
generate_list_component
(
self
,
 entity
:
 
str
)
 
-
>
 
str
:

        
"""Generate a list component for an entity."""

        entity_cap 
=
 entity
.
capitalize
(
)

        
        
return
 
f'''import React, {{ useState, useEffect }} from 'react';
import {{ 
{
entity_cap
}
API }} from '../services/
{
entity
}
API';

function 
{
entity_cap
}
List() {{
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {{
    fetchItems();
  }}, []);

  const fetchItems = async () => {{
    try {{
      setLoading(true);
      const data = await 
{
entity_cap
}
API.getAll();
      setItems(data);
    }} catch (err) {{
      setError(err.message);
    }} finally {{
      setLoading(false);
    }}
  }};

  const handleDelete = async (id) => {{
    if (window.confirm('Are you sure you want to delete this item?')) {{
      try {{
        await 
{
entity_cap
}
API.delete(id);
        fetchItems();
      }} catch (err) {{
        setError(err.message);
      }}
    }}
  }};

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {{error}}</div>;

  return (
    <div className="
{
entity
}
-list">
      <h2>
{
entity_cap
}
s</h2>
      <button onClick={{() => window.location.href = '/
{
entity
}
s/new'}}>
        Add New
      </button>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {{items.map(item => (
            <tr key={{item.id}}>
              <td>{{item.id}}</td>
              <td>{{item.name || item.title}}</td>
              <td>
                <button onClick={{() => window.location.href = '/
{
entity
}
s/{{item.id}}/edit'}}>
                  Edit
                </button>
                <button onClick={{() => handleDelete(item.id)}}>
                  Delete
                </button>
              </td>
            </tr>
          ))}}
        </tbody>
      </table>
    </div>
  );
}}

export default 
{
entity_cap
}
List;
'''

    
    
def
 
generate_form_component
(
self
,
 entity
:
 
str
)
 
-
>
 
str
:

        
"""Generate a form component for an entity."""

        entity_cap 
=
 entity
.
capitalize
(
)

        
        
return
 
f'''import React, {{ useState }} from 'react';
import {{ useNavigate, useParams }} from 'react-router-dom';
import {{ 
{
entity_cap
}
API }} from '../services/
{
entity
}
API';

function 
{
entity_cap
}
Form() {{
  const [formData, setFormData] = useState({{
    name: '',
    description: ''
  }});
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const {{ id }} = useParams();

  useEffect(() => {{
    if (id) {{
      fetchItem(id);
    }}
  }}, [id]);

  const fetchItem = async (itemId) => {{
    try {{
      const item = await 
{
entity_cap
}
API.getById(itemId);
      setFormData(item);
    }} catch (err) {{
      setError(err.message);
    }}
  }};

  const handleChange = (e) => {{
    setFormData({{
      ...formData,
      [e.target.name]: e.target.value
    }});
  }};

  const handleSubmit = async (e) => {{
    e.preventDefault();
    setError(null);

    try {{
      if (id) {{
        await 
{
entity_cap
}
API.update(id, formData);
      }} else {{
        await 
{
entity_cap
}
API.create(formData);
      }}
      navigate('/
{
entity
}
s');
    }} catch (err) {{
      setError(err.message);
    }}
  }};

  return (
    <div className="
{
entity
}
-form">
      <h2>{{id ? 'Edit' : 'Create'}} 
{
entity_cap
}
</h2>
      {{error && <div className="error">{{error}}</div>}}
      <form onSubmit={{handleSubmit}}>
        <div>
          <label>Name:</label>
          <input
            type="text"
            name="name"
            value={{formData.name}}
            onChange={{handleChange}}
            required
          />
        </div>
        <div>
          <label>Description:</label>
          <textarea
            name="description"
            value={{formData.description}}
            onChange={{handleChange}}
          />
        </div>
        <button type="submit">Save</button>
        <button type="button" onClick={{() => navigate('/
{
entity
}
s')}}>
          Cancel
        </button>
      </form>
    </div>
  );
}}

export default 
{
entity_cap
}
Form;
'''

    
    
def
 
generate_api_service
(
self
,
 entity
:
 
str
)
 
-
>
 
str
:

        
"""Generate API service for an entity."""

        entity_cap 
=
 entity
.
capitalize
(
)

        
        
return
 
f'''import axios from 'axios';
import {{ authService }} from './auth';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

class 
{
entity_cap
}
API {{
  async getAll() {{
    const response = await axios.get(`${{API_URL}}/
{
entity
}
s`, {{
      headers: authService.getAuthHeader()
    }});
    return response.data;
  }}

  async getById(id) {{
    const response = await axios.get(`${{API_URL}}/
{
entity
}
s/${{id}}`, {{
      headers: authService.getAuthHeader()
    }});
    return response.data;
  }}

  async create(data) {{
    const response = await axios.post(`${{API_URL}}/
{
entity
}
s`, data, {{
      headers: authService.getAuthHeader()
    }});
    return response.data;
  }}

  async update(id, data) {{
    const response = await axios.put(`${{API_URL}}/
{
entity
}
s/${{id}}`, data, {{
      headers: authService.getAuthHeader()
    }});
    return response.data;
  }}

  async delete(id) {{
    await axios.delete(`${{API_URL}}/
{
entity
}
s/${{id}}`, {{
      headers: authService.getAuthHeader()
    }});
  }}
}}

export const 
{
entity_cap
}
API = new 
{
entity_cap
}
API();
'''

    
    
def
 
generate_navigation_component
(
self
)
 
-
>
 
str
:

        
"""Generate navigation component."""

        
return
 
'''import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { authService } from '../services/auth';

function Navigation() {
  const navigate = useNavigate();
  const isLoggedIn = !!authService.getToken();

  const handleLogout = () => {
    authService.logout();
    navigate('/login');
  };

  return (
    <nav className="navigation">
      <div className="nav-left">
        <Link to="/">Home</Link>
        {isLoggedIn && <Link to="/dashboard">Dashboard</Link>}
      </div>
      <div className="nav-right">
        {isLoggedIn ? (
          <button onClick={handleLogout}>Logout</button>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>
          </>
        )}
      </div>
    </nav>
  );
}

export default Navigation;
'''

    
    
def
 
generate_layout_component
(
self
)
 
-
>
 
str
:

        
"""Generate layout component."""

        
return
 
'''import React from 'react';
import Navigation from './Navigation';

function Layout({ children }) {
  return (
    <div className="layout">
      <Navigation />
      <main className="main-content">
        {children}
      </main>
      <footer className="footer">
        <p>&copy; 2024 AutonomousAI Generated App</p>
      </footer>
    </div>
  );
}

export default Layout;
'''

    
    
def
 
generate_react_app
(
self
)
 
-
>
 
str
:

        
"""Generate main App.js."""

        
return
 
'''import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/layout/Layout';
import Login from './components/auth/Login';
import Register from './components/auth/Register';
import Dashboard from './pages/Dashboard';
import './App.css';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
'''

    
    
def
 
generate_app_css
(
self
)
 
-
>
 
str
:

        
"""Generate App.css with basic styling."""

        
return
 
'''* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.navigation {
  background: #333;
  color: white;
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navigation a {
  color: white;
  text-decoration: none;
  margin-right: 1rem;
}

.navigation button {
  background: #555;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  cursor: pointer;
}

.main-content {
  flex: 1;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.footer {
  background: #f5f5f5;
  padding: 1rem;
  text-align: center;
}

.login-container, .register-container {
  max-width: 400px;
  margin: 2rem auto;
  padding: 2rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.login-container h2, .register-container h2 {
  margin-bottom: 1rem;
}

.login-container form div,
.register-container form div {
  margin-bottom: 1rem;
}

.login-container label,
.register-container label {
  display: block;
  margin-bottom: 0.5rem;
}

.login-container input,
.register-container input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.error {
  background: #fee;
  color: #c33;
  padding: 0.5rem;
  margin-bottom: 1rem;
  border-radius: 4px;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

table th, table td {
  border: 1px solid #ddd;
  padding: 0.5rem;
  text-align: left;
}

table th {
  background: #f5f5f5;
}
'''

    
    
def
 
generate_frontend_module
(
self
,
 description
:
 
str
)
 
-
>
 
str
:

        
"""Generate a generic frontend module."""

        
return
 
f'''// Generated frontend module
// Description: 
{
description
}


import React from 'react';

function GeneratedComponent() {{
  return (
    <div>
      <h2>Generated Component</h2>
      <p>This component was generated based on: {{description}}</p>
    </div>
  );
}}

export default GeneratedComponent;
'''



### web_intelligence/backend_intel.py