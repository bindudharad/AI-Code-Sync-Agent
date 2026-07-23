from
 typing 
import
 List
,
 Dict
,
 Any
,
 Optional

from
 datetime 
import
 datetime
,
 timedelta


class
 
ContextWindow
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
max_tokens 
=
 config
[
"memory"
]
.
get
(
"context_window_tokens"
,
 
8000
)

        self
.
max_messages 
=
 config
[
"memory"
]
.
get
(
"context_window_messages"
,
 
50
)

        
        self
.
messages
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
token_count 
=
 
0

    
    
def
 
add_message
(
self
,
 role
:
 
str
,
 content
:
 
str
,
 tokens
:
 Optional
[
int
]
 
=
 
None
)
:

        
"""Add message to context window."""

        
if
 tokens 
is
 
None
:

            tokens 
=
 
len
(
content
.
split
(
)
)
 
*
 
1.3
  
# Rough estimate

        
        message 
=
 
{

            
"role"
:
 role
,

            
"content"
:
 content
,

            
"tokens"
:
 tokens
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

        
        self
.
messages
.
append
(
message
)

        self
.
token_count 
+=
 tokens
        
        
# Trim if over limits

        self
.
_trim_window
(
)

    
    
def
 
get_messages
(
self
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

        
"""Get all messages in window."""

        
return
 self
.
messages
.
copy
(
)

    
    
def
 
get_formatted_messages
(
self
)
 
-
>
 List
[
Dict
[
str
,
 
str
]
]
:

        
"""Get messages formatted for LLM API."""

        
return
 
[

            
{
"role"
:
 msg
[
"role"
]
,
 
"content"
:
 msg
[
"content"
]
}

            
for
 msg 
in
 self
.
messages
        
]

    
    
def
 
clear
(
self
)
:

        
"""Clear context window."""

        self
.
messages
.
clear
(
)

        self
.
token_count 
=
 
0

    
    
def
 
_trim_window
(
self
)
:

        
"""Trim window to fit within limits."""

        
# Trim by token count

        
while
 self
.
token_count 
>
 self
.
max_tokens 
and
 
len
(
self
.
messages
)
 
>
 
2
:

            removed 
=
 self
.
messages
.
pop
(
0
)

            self
.
token_count 
-=
 removed
[
"tokens"
]

        
        
# Trim by message count

        
while
 
len
(
self
.
messages
)
 
>
 self
.
max_messages
:

            removed 
=
 self
.
messages
.
pop
(
0
)

            self
.
token_count 
-=
 removed
[
"tokens"
]

    
    
def
 
get_summary
(
self
)
 
-
>
 
str
:

        
"""Get summary of context window."""

        
return
 
f"Context: 
{
len
(
self
.
messages
)
}
 messages, 
{
self
.
token_count
:
.0f
}
 tokens"



### tools/prompt_builder.py