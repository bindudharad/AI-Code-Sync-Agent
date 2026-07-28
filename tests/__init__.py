# Tests package
 
tests/test_core.py
Python
 
 
 
Copy
 
import
 pytest

from
 core
.
ai_brain 
import
 AIBrain

from
 core
.
goal_manager 
import
 GoalManager


@pytest
.
mark
.
asyncio


async
 
def
 
test_ai_brain_initialization
(
)
:

    
"""Test AI brain initialization."""

    config 
=
 
{
"paths"
:
 
{
"projects_root"
:
 
"./test_projects"
}
,
 
"agents"
:
 
{
"enabled"
:
 
[
]
}
}

    brain 
=
 AIBrain
(
config
)

    
    
await
 brain
.
initialize
(
)

    
assert
 brain
.
state
.
value 
==
 
"idle"



@pytest
.
mark
.
asyncio


async
 
def
 
test_goal_manager_create_goal
(
)
:

    
"""Test goal creation."""

    config 
=
 
{
"paths"
:
 
{
"projects_root"
:
 
"./test_projects"
}
}

    manager 
=
 GoalManager
(
config
)

    
await
 manager
.
initialize
(
)

    
    goal_id 
=
 
await
 manager
.
create_goal
(
"Test Goal"
,
 
"Test description"
)

    
assert
 goal_id 
is
 
not
 
None

    
    goal 
=
 manager
.
get_goal
(
goal_id
)

    
assert
 goal
.
title 
==
 
"Test Goal"



### tests/test_agents.py