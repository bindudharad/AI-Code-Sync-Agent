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
 pathlib 
import
 Path

import
 json

import
 re


from
 tools
.
prompt_builder 
import
 PromptBuilder


class
 
PromptEngineerAgent
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
prompt_builder 
=
 PromptBuilder
(
config
)

        self
.
skills 
=
 
[
"prompt_optimization"
,
 
"few_shot_generation"
,
 
"chain_of_thought"
,
 
"prompt_testing"
]

        
        
# Prompt engineering best practices

        self
.
best_practices 
=
 
[

            
"Be explicit and specific"
,

            
"Use clear examples"
,

            
"Specify output format"
,

            
"Break complex tasks into steps"
,

            
"Include context and constraints"

        
]

    
    
async
 
def
 
execute
(
self
,
 task
:
 Any
,
 goal
:
 Any
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

        
"""Execute prompt engineering tasks."""

        logs 
=
 
[
]

        files_generated 
=
 
[
]

        
        
try
:

            
if
 
"optimize prompt"
 
in
 task
.
title
.
lower
(
)
:

                result 
=
 
await
 self
.
_optimize_prompt
(
task
,
 goal
)

                files_generated
.
extend
(
result
[
"files"
]
)

                logs
.
extend
(
result
[
"logs"
]
)

            
            
elif
 
"few-shot"
 
in
 task
.
title
.
lower
(
)
:

                result 
=
 
await
 self
.
_generate_few_shot_examples
(
task
,
 goal
)

                files_generated
.
extend
(
result
[
"files"
]
)

                logs
.
extend
(
result
[
"logs"
]
)

            
            
elif
 
"chain"
 
in
 task
.
title
.
lower
(
)
:

                result 
=
 
await
 self
.
_generate_chain_of_thought
(
task
,
 goal
)

                files_generated
.
extend
(
result
[
"files"
]
)

                logs
.
extend
(
result
[
"logs"
]
)

            
            
elif
 
"test prompt"
 
in
 task
.
title
.
lower
(
)
:

                result 
=
 
await
 self
.
_test_prompt_quality
(
task
,
 goal
)

                logs
.
extend
(
result
[
"logs"
]
)

            
            
elif
 
"create template"
 
in
 task
.
title
.
lower
(
)
:

                result 
=
 
await
 self
.
_create_prompt_template
(
task
,
 goal
)

                files_generated
.
extend
(
result
[
"files"
]
)

                logs
.
extend
(
result
[
"logs"
]
)

            
            
return
 
{

                
"status"
:
 
"completed"
,

                
"files_generated"
:
 files_generated
,

                
"logs"
:
 logs
            
}

        
        
except
 Exception 
as
 e
:

            logs
.
append
(
f"Prompt engineering task failed: 
{
str
(
e
)
}
"
)

            
return
 
{

                
"status"
:
 
"failed"
,

                
"files_generated"
:
 files_generated
,

                
"logs"
:
 logs
,

                
"error"
:
 
str
(
e
)

            
}

    
    
async
 
def
 
_optimize_prompt
(
self
,
 task
:
 Any
,
 goal
:
 Any
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

        
"""Optimize existing prompts for better results."""

        logs 
=
 
[
]

        
        
# Parse existing prompt from task description

        existing_prompt 
=
 self
.
_extract_prompt_from_description
(
task
.
description
)

        
        
if
 
not
 existing_prompt
:

            logs
.
append
(
"❌ No existing prompt found to optimize"
)

            
return
 
{
"files"
:
 
[
]
,
 
"logs"
:
 logs
}

        
        logs
.
append
(
"🔍 Analyzing prompt structure..."
)

        
        
# Apply optimization techniques

        optimizations 
=
 
[

            self
.
_add_specificity
,

            self
.
_add_examples
,

            self
.
_add_output_format
,

            self
.
_add_constraints
,

            self
.
_decompose_complexity
        
]

        
        optimized_prompts 
=
 
{
}

        
        
for
 technique 
in
 optimizations
:

            optimized 
=
 technique
(
existing_prompt
)

            
if
 optimized 
!=
 existing_prompt
:

                optimized_prompts
[
technique
.
__name__
]
 
=
 optimized
        
        
# Evaluate which optimization works best

        project_name 
=
 goal
.
context
.
get
(
"project_name"
,
 
"app"
)

        optimize_file 
=
 Path
(
self
.
config
[
"paths"
]
[
"projects_root"
]
)
 
/
 project_name 
/
 
"docs"
 
/
 
"optimized_prompts.md"

        
        content 
=
 
f""
"
# Prompt Optimization Results



## Original Prompt
 
{existing_prompt}
plain
 
 
 
Copy
 

## Optimized Versions

{chr(10).join(f'### {name.replace("_", " ").title()}{chr(10)}