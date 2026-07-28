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
 List
,
 Any
,
 Optional

import
 subprocess


class
 
DependencyManager
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
 
install_dependencies
(
self
,
 project_path
:
 
str
,
 dependencies
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
)
:

        
"""Install project dependencies."""

        logs 
=
 
[
]

        
        
# Python dependencies

        
if
 
"python"
 
in
 dependencies
:

            req_file 
=
 Path
(
project_path
)
 
/
 
"requirements.txt"

            req_file
.
write_text
(
"\n"
.
join
(
dependencies
[
"python"
]
)
)

            
            result 
=
 subprocess
.
run
(

                
[
sys
.
executable
,
 
"-m"
,
 
"pip"
,
 
"install"
,
 
"-r"
,
 
"requirements.txt"
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

                logs
.
append
(
"Python dependencies installed"
)

            
else
:

                logs
.
append
(
f"Python install failed: 
{
result
.
stderr
}
"
)

        
        
# Node.js dependencies

        
if
 
"node"
 
in
 dependencies
:

            package_json 
=
 
{

                
"dependencies"
:
 
{
}
,

                
"devDependencies"
:
 
{
}

            
}

            
            
for
 dep 
in
 dependencies
[
"node"
]
:

                
if
 
"eslint"
 
in
 dep 
or
 
"prettier"
 
in
 dep
:

                    package_json
[
"devDependencies"
]
[
dep
.
split
(
"@"
)
[
0
]
]
 
=
 dep
.
split
(
"@"
)
[
-
1
]

                
else
:

                    name 
=
 dep
.
split
(
"@"
)
[
0
]
 
if
 
"@"
 
in
 dep 
else
 dep
                    version 
=
 dep
.
split
(
"@"
)
[
-
1
]
 
if
 
"@"
 
in
 dep 
else
 
"latest"

                    package_json
[
"dependencies"
]
[
name
]
 
=
 version
            
            Path
(
project_path
,
 
"package.json"
)
.
write_text
(

                json
.
dumps
(
package_json
,
 indent
=
2
)

            
)

            
            result 
=
 subprocess
.
run
(

                
[
"npm"
,
 
"install"
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

                logs
.
append
(
"Node dependencies installed"
)

            
else
:

                logs
.
append
(
f"Node install failed: 
{
result
.
stderr
}
"
)

        
        
return
 logs
    
    
async
 
def
 
check_vulnerabilities
(
self
,
 project_path
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

        
"""Check for vulnerable dependencies."""

        vulnerabilities 
=
 
[
]

        
        
# Check Python dependencies

        
if
 Path
(
project_path
,
 
"requirements.txt"
)
.
exists
(
)
:

            
# This would use safety or similar in production

            
pass

        
        
# Check Node dependencies

        
if
 Path
(
project_path
,
 
"package.json"
)
.
exists
(
)
:

            result 
=
 subprocess
.
run
(

                
[
"npm"
,
 
"audit"
,
 
"--json"
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
!=
 
0
:

                
try
:

                    audit_data 
=
 json
.
loads
(
result
.
stdout
)

                    vulnerabilities
.
extend
(
audit_data
.
get
(
"vulnerabilities"
,
 
[
]
)
)

                
except
:

                    
pass

        
        
return
 vulnerabilities


### tools/lint_runner.py