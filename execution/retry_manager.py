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


class
 
RetryManager
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
max_retries 
=
 config
[
"execution"
]
.
get
(
"max_retries"
,
 
3
)

        self
.
backoff_factor 
=
 config
[
"execution"
]
.
get
(
"backoff_factor"
,
 
2.0
)

        self
.
retry_on_errors 
=
 config
[
"execution"
]
.
get
(
"retry_on_errors"
,
 
[
"timeout"
,
 
"connection"
]
)

    
    
async
 
def
 
execute_with_retry
(

        self
,

        func
,

        
*
args
,

        
**
kwargs
    
)
 
-
>
 Any
:

        
"""Execute function with retry logic."""

        last_error 
=
 
None

        
        
for
 attempt 
in
 
range
(
self
.
max_retries 
+
 
1
)
:

            
try
:

                result 
=
 
await
 func
(
*
args
,
 
**
kwargs
)

                
return
 result
            
            
except
 Exception 
as
 e
:

                last_error 
=
 e
                
                
if
 attempt 
>=
 self
.
max_retries
:

                    
break

                
                
if
 
not
 self
.
_should_retry
(
e
)
:

                    
break

                
                
# Calculate backoff

                backoff 
=
 self
.
backoff_factor 
**
 attempt
                
await
 asyncio
.
sleep
(
backoff
)

        
        
raise
 last_error
    
    
def
 
_should_retry
(
self
,
 error
:
 Exception
)
 
-
>
 
bool
:

        
"""Check if error should trigger retry."""

        error_str 
=
 
str
(
error
)
.
lower
(
)

        
        
return
 
any
(

            retry_error 
in
 error_str
            
for
 retry_error 
in
 self
.
retry_on_errors
        
)



### execution/rollback_manager.py