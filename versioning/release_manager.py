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

import
 subprocess


class
 
ReleaseManager
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
    
    
async
 
def
 
create_release
(
self
,
 project_path
:
 
str
,
 version
:
 
str
)
 
-
>
 
bool
:

        
"""Create a new release."""

        
try
:

            
# Tag in git

            result 
=
 subprocess
.
run
(

                
[
"git"
,
 
"tag"
,
 
f"v
{
version
}
"
]
,

                cwd
=
project_path
,

                capture_output
=
True

            
)

            
            
if
 result
.
returncode 
!=
 
0
:

                
return
 
False

            
            
# Push tag

            result 
=
 subprocess
.
run
(

                
[
"git"
,
 
"push"
,
 
"origin"
,
 
f"v
{
version
}
"
]
,

                cwd
=
project_path
,

                capture_output
=
True

            
)

            
            
return
 result
.
returncode 
==
 
0

        
        
except
 Exception 
as
 e
:

            
print
(
f"Release creation failed: 
{
e
}
"
)

            
return
 
False

    
    
async
 
def
 
get_version
(
self
,
 project_path
:
 
str
)
 
-
>
 
str
:

        
"""Get current version from git tags."""

        
try
:

            result 
=
 subprocess
.
run
(

                
[
"git"
,
 
"describe"
,
 
"--tags"
,
 
"--abbrev=0"
]
,

                cwd
=
project_path
,

                capture_output
=
True
,

                text
=
True

            
)

            
            
if
 result
.
returncode 
==
 
0
:

                
return
 result
.
stdout
.
strip
(
)

            
            
return
 
"0.1.0"

        
        
except
:

            
return
 
"0.1.0"



### versioning/changelog_generator.py