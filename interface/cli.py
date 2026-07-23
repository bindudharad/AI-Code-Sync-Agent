import
 asyncio

import
 sys

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
 argparse


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

from
 core
.
metrics_engine 
import
 MetricsEngine

from
 memory
.
user_preferences 
import
 UserPreferences


class
 
CLIInterface
:

    
def
 
__init__
(
self
)
:

        self
.
brain 
=
 
None

        self
.
goal_manager 
=
 
None

        self
.
metrics_engine 
=
 
None

        self
.
user_preferences 
=
 
None

        
        
# Commands registry

        self
.
commands
:
 Dict
[
str
,
 
callable
]
 
=
 
{

            
"help"
:
 self
.
cmd_help
,

            
"create"
:
 self
.
cmd_create
,

            
"list"
:
 self
.
cmd_list
,

            
"start"
:
 self
.
cmd_start
,

            
"pause"
:
 self
.
cmd_pause
,

            
"resume"
:
 self
.
cmd_resume
,

            
"cancel"
:
 self
.
cmd_cancel
,

            
"status"
:
 self
.
cmd_status
,

            
"inspect"
:
 self
.
cmd_inspect
,

            
"config"
:
 self
.
cmd_config
,

            
"metrics"
:
 self
.
cmd_metrics
,

            
"clear"
:
 self
.
cmd_clear
,

            
"exit"
:
 self
.
cmd_exit
        
}

    
    
async
 
def
 
start_interactive_mode
(
self
,
 brain
:
 AIBrain
,
 goal_manager
:
 GoalManager
)
:

        
"""Start interactive CLI mode."""

        self
.
brain 
=
 brain
        self
.
goal_manager 
=
 goal_manager
        self
.
metrics_engine 
=
 MetricsEngine
(
brain
.
config
)

        self
.
user_preferences 
=
 UserPreferences
(
brain
.
config
)

        
        
print
(
"🚀 Autonomous AI Web Developer"
)

        
print
(
"Type 'help' for available commands or 'exit' to quit."
)

        
print
(
)

        
        
while
 
True
:

            
try
:

                command 
=
 
await
 self
.
_get_input
(
"> "
)

                
await
 self
.
_execute_command
(
command
)

                
            
except
 KeyboardInterrupt
:

                
print
(
"\nUse 'exit' to quit."
)

            
except
 EOFError
:

                
await
 self
.
cmd_exit
(
[
]
)

                
break

            
except
 Exception 
as
 e
:

                
print
(
f"Error: 
{
str
(
e
)
}
"
)

    
    
async
 
def
 
_get_input
(
self
,
 prompt
:
 
str
)
 
-
>
 
str
:

        
"""Get user input asynchronously."""

        loop 
=
 asyncio
.
get_event_loop
(
)

        
return
 
await
 loop
.
run_in_executor
(
None
,
 
input
,
 prompt
)

    
    
async
 
def
 
_execute_command
(
self
,
 command
:
 
str
)
:

        
"""Parse and execute command."""

        parts 
=
 command
.
strip
(
)
.
split
(
)

        
if
 
not
 parts
:

            
return

        
        cmd_name 
=
 parts
[
0
]
.
lower
(
)

        args 
=
 parts
[
1
:
]

        
        
if
 cmd_name 
in
 self
.
commands
:

            
await
 self
.
commands
[
cmd_name
]
(
args
)

        
else
:

            
print
(
f"Unknown command: 
{
cmd_name
}
"
)

            
print
(
"Type 'help' for available commands."
)

    
    
async
 
def
 
cmd_help
(
self
,
 args
:
 List
[
str
]
)
:

        
"""Display help information."""

        help_text 
=
 
"""
Available Commands:

Goal Management:
  create <title> <description> [priority]  - Create a new goal
  list [status]                           - List goals (all, pending, active, completed)
  start [goal_id]                         - Start processing goals or a specific goal
  pause <goal_id>                         - Pause a goal
  resume <goal_id>                        - Resume a paused goal
  cancel <goal_id>                        - Cancel a goal
  status <goal_id>                        - Show detailed status of a goal

Inspection:
  inspect memory                          - Inspect memory contents
  inspect agents                          - Show agent status
  metrics                                 - Show system metrics
  config show                             - Show current configuration
  config set <key> <value>                - Update configuration

System:
  clear                                   - Clear screen
  exit                                    - Exit the application
  help                                    - Show this help message

Examples:
  > create "Build Todo App" "Create a simple todo application with React and FastAPI" 1.0
  > list pending
  > start
  > status 123e4567-e89b-12d3-a456-426614174000
"""

        
print
(
help_text
)

    
    
async
 
def
 
cmd_create
(
self
,
 args
:
 List
[
str
]
)
:

        
"""Create a new goal."""

        
if
 
len
(
args
)
 
<
 
2
:

            
print
(
"Usage: create <title> <description> [priority]"
)

            
return

        
        title 
=
 args
[
0
]

        description 
=
 args
[
1
]

        priority 
=
 
float
(
args
[
2
]
)
 
if
 
len
(
args
)
 
>
 
2
 
else
 
1.0

        
        goal_id 
=
 
await
 self
.
goal_manager
.
create_goal
(
title
,
 description
,
 priority
)

        
print
(
f"✅ Goal created: 
{
goal_id
}
"
)

        
print
(
f"   Title: 
{
title
}
"
)

        
print
(
f"   Description: 
{
description
}
"
)

        
print
(
f"   Priority: 
{
priority
}
"
)

    
    
async
 
def
 
cmd_list
(
self
,
 args
:
 List
[
str
]
)
:

        
"""List goals."""

        status_filter 
=
 args
[
0
]
.
upper
(
)
 
if
 args 
else
 
None

        
        
if
 status_filter 
and
 status_filter 
not
 
in
 
[
"PENDING"
,
 
"ACTIVE"
,
 
"COMPLETED"
,
 
"FAILED"
]
:

            
print
(
"Invalid status. Use: pending, active, completed, failed"
)

            
return

        
        goals 
=
 self
.
goal_manager
.
get_pending_goals
(
)

        
        
if
 
not
 goals
:

            
print
(
"No goals found."
)

            
return

        
        
print
(
"\n📋 Goals:"
)

        
print
(
"-"
 
*
 
80
)

        
        
for
 goal 
in
 goals
:

            
if
 
not
 status_filter 
or
 goal
.
status
.
value 
==
 status_filter
:

                progress 
=
 goal
.
progress_percentage
                
print
(
f"ID: 
{
goal
.
goal_id
}
"
)

                
print
(
f"Title: 
{
goal
.
title
}
"
)

                
print
(
f"Status: 
{
goal
.
status
.
value
}
"
)

                
print
(
f"Priority: 
{
goal
.
priority
}
"
)

                
print
(
f"Progress: 
{
progress
:
.1f
}
%"
)

                
print
(
f"Created: 
{
goal
.
created_at
.
strftime
(
'%Y-%m-%d %H:%M'
)
}
"
)

                
if
 goal
.
plan
:

                    total_tasks 
=
 
len
(
goal
.
plan
.
tasks
)

                    completed 
=
 
sum
(
1
 
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
)

                    
print
(
f"Tasks: 
{
completed
}
/
{
total_tasks
}
"
)

                
print
(
"-"
 
*
 
80
)

    
    
async
 
def
 
cmd_start
(
self
,
 args
:
 List
[
str
]
)
:

        
"""Start processing goals."""

        
if
 args
:

            
# Start specific goal

            goal_id 
=
 args
[
0
]

            goal 
=
 self
.
goal_manager
.
get_goal
(
goal_id
)

            
if
 goal
:

                
await
 self
.
goal_manager
.
resume_goal
(
goal_id
)

                
print
(
f"🚀 Resumed goal: 
{
goal_id
}
"
)

            
else
:

                
print
(
f"Goal not found: 
{
goal_id
}
"
)

        
else
:

            
# Start autonomous processing

            
print
(
"Starting autonomous mode..."
)

            
await
 self
.
brain
.
start
(
"autonomous"
)

    
    
async
 
def
 
cmd_pause
(
self
,
 args
:
 List
[
str
]
)
:

        
"""Pause a goal."""

        
if
 
not
 args
:

            
print
(
"Usage: pause <goal_id>"
)

            
return

        
        goal_id 
=
 args
[
0
]

        
await
 self
.
goal_manager
.
pause_goal
(
goal_id
)

        
print
(
f"⏸️  Paused goal: 
{
goal_id
}
"
)

    
    
async
 
def
 
cmd_resume
(
self
,
 args
:
 List
[
str
]
)
:

        
"""Resume a paused goal."""

        
if
 
not
 args
:

            
print
(
"Usage: resume <goal_id>"
)

            
return

        
        goal_id 
=
 args
[
0
]

        
await
 self
.
goal_manager
.
resume_goal
(
goal_id
)

        
print
(
f"▶️  Resumed goal: 
{
goal_id
}
"
)

    
    
async
 
def
 
cmd_cancel
(
self
,
 args
:
 List
[
str
]
)
:

        
"""Cancel a goal."""

        
if
 
not
 args
:

            
print
(
"Usage: cancel <goal_id>"
)

            
return

        
        goal_id 
=
 args
[
0
]

        
await
 self
.
goal_manager
.
cancel_goal
(
goal_id
)

        
print
(
f"❌ Cancelled goal: 
{
goal_id
}
"
)

    
    
async
 
def
 
cmd_status
(
self
,
 args
:
 List
[
str
]
)
:

        
"""Show detailed status of a goal."""

        
if
 
not
 args
:

            
print
(
"Usage: status <goal_id>"
)

            
return

        
        goal_id 
=
 args
[
0
]

        goal 
=
 self
.
goal_manager
.
get_goal
(
goal_id
)

        
        
if
 
not
 goal
:

            
print
(
f"Goal not found: 
{
goal_id
}
"
)

            
return

        
        
print
(
f"\n📊 Goal Status: 
{
goal_id
}
"
)

        
print
(
"-"
 
*
 
50
)

        
print
(
f"Title: 
{
goal
.
title
}
"
)

        
print
(
f"Status: 
{
goal
.
status
.
value
}
"
)

        
print
(
f"Priority: 
{
goal
.
priority
}
"
)

        
print
(
f"Progress: 
{
goal
.
progress_percentage
:
.1f
}
%"
)

        
print
(
f"Created: 
{
goal
.
created_at
}
"
)

        
print
(
f"Updated: 
{
goal
.
updated_at
}
"
)

        
        
if
 goal
.
analyzed_requirements
:

            
print
(
f"\nRequirements:"
)

            
print
(
f"  Features: 
{
len
(
goal
.
analyzed_requirements
.
get
(
'features'
,
 
[
]
)
)
}
"
)

            
print
(
f"  APIs: {len(goal.analyzed_requirements.get('api_contracts', {}).get('endpoints', []))}"
)

        
        
if
 goal
.
plan
:

            
print
(
f"\nPlan:"
)

            
print
(
f"  Total tasks: 
{
len
(
goal
.
plan
.
tasks
)
}
"
)

            
            
for
 task 
in
 goal
.
plan
.
tasks
:

                status_icon 
=
 
"✅"
 
if
 task
.
status 
==
 
"completed"
 
else
 
"⏳"
 
if
 task
.
status 
==
 
"in_progress"
 
else
 
"⭕"

                
print
(
f"  
{
status_icon
}
 [
{
task
.
priority
}
] 
{
task
.
title
}
 (
{
task
.
agent_type
}
)"
)

        
        
if
 goal
.
revision_history
:

            
print
(
f"\nRevisions: 
{
len
(
goal
.
revision_history
)
}
"
)

    
    
async
 
def
 
cmd_inspect
(
self
,
 args
:
 List
[
str
]
)
:

        
"""Inspect system components."""

        
if
 
not
 args
:

            
print
(
"Usage: inspect <memory|agents>"
)

            
return

        
        component 
=
 args
[
0
]
.
lower
(
)

        
        
if
 component 
==
 
"memory"
:

            
await
 self
.
_inspect_memory
(
)

        
elif
 component 
==
 
"agents"
:

            
await
 self
.
_inspect_agents
(
)

        
else
:

            
print
(
"Unknown component. Use: memory, agents"
)

    
    
async
 
def
 
_inspect_memory
(
self
)
:

        
"""Inspect memory contents."""

        
print
(
"\n🧠 Memory Inspection"
)

        
print
(
"-"
 
*
 
30
)

        
        
from
 memory
.
short_term 
import
 ShortTermMemory
        
from
 memory
.
long_term 
import
 LongTermMemory
        
        short_term 
=
 ShortTermMemory
(
self
.
brain
.
config
)

        recent 
=
 
await
 short_term
.
get_recent
(
10
)

        
        
print
(
"\nShort-term memory (last 10 entries):"
)

        
for
 entry 
in
 recent
:

            
print
(
f"  - 
{
entry
[
'event'
]
[
:
60]
}
..."
)

        
        long_term 
=
 LongTermMemory
(
self
.
brain
.
config
)

        
print
(
f"\nLong-term memory: 
{
len
(
long_term
.
knowledge_base
)
}
 entries"
)

        
        experience 
=
 self
.
brain
.
experience_memory
        
print
(
f"Experience memory: 
{
len
(
experience
.
experiences
)
}
 entries"
)

        
print
(
f"Success rate: 
{
experience
.
get_success_rate
(
)
:
.1%
}
"
)

    
    
async
 
def
 
_inspect_agents
(
self
)
:

        
"""Inspect agent status."""

        
print
(
"\n🤖 Agent Status"
)

        
print
(
"-"
 
*
 
30
)

        
        status 
=
 
await
 self
.
brain
.
state_manager
.
get_system_health
(
)

        
        
print
(
f"System state: 
{
status
[
'system_state'
]
}
"
)

        
print
(
f"System health: 
{
status
[
'system_health'
]
}
"
)

        
print
(
f"Active agents: 
{
status
[
'active_agents'
]
}
"
)

        
print
(
f"Total agents: 
{
status
[
'total_agents'
]
}
"
)

        
        
for
 agent_id
,
 agent_state 
in
 self
.
brain
.
state_manager
.
get_all_agent_states
(
)
.
items
(
)
:

            
print
(
f"\nAgent: 
{
agent_id
}
"
)

            
print
(
f"  Type: 
{
agent_state
.
agent_type
}
"
)

            
print
(
f"  State: 
{
agent_state
.
state
.
value
}
"
)

            
print
(
f"  Tasks completed: 
{
agent_state
.
tasks_completed
}
"
)

            
print
(
f"  Performance: 
{
agent_state
.
performance_score
:
.2f
}
"
)

    
    
async
 
def
 
cmd_metrics
(
self
,
 args
:
 List
[
str
]
)
:

        
"""Show system metrics."""

        
print
(
"\n📊 System Metrics"
)

        
print
(
"-"
 
*
 
40
)

        
        report 
=
 self
.
metrics_engine
.
get_performance_report
(
)

        
        
if
 
"error"
 
in
 report
:

            
print
(
f"No metrics available yet"
)

            
return

        
        
print
(
f"Total goals: 
{
report
[
'total_goals'
]
}
"
)

        
print
(
f"Success rate: 
{
report
[
'success_rate'
]
:
.1%
}
"
)

        
print
(
f"Success rate (last 10): 
{
report
[
'success_rate_last_10'
]
:
.1%
}
"
)

        
print
(
f"Average duration: 
{
report
[
'average_duration_minutes'
]
:
.1f
}
 minutes"
)

        
print
(
f"Bug frequency: 
{
report
[
'bug_frequency_per_kloc'
]
:
.2f
}
 bugs/KLOC"
)

        
print
(
f"Learning improvement: 
{
report
[
'learning_improvement'
]
:
+.1%
}
"
)

        
print
(
f"Throughput: 
{
report
[
'goal_throughput_per_day'
]
:
.2f
}
 goals/day"
)

    
    
async
 
def
 
cmd_config
(
self
,
 args
:
 List
[
str
]
)
:

        
"""Show or update configuration."""

        
if
 
not
 args
:

            
print
(
"Usage: config <show|set> [key] [value]"
)

            
return

        
        action 
=
 args
[
0
]
.
lower
(
)

        
        
if
 action 
==
 
"show"
:

            
if
 
len
(
args
)
 
>
 
1
:

                key 
=
 args
[
1
]

                value 
=
 self
.
_get_nested_config
(
key
)

                
print
(
f"
{
key
}
: 
{
value
}
"
)

            
else
:

                
print
(
"\n⚙️  Configuration"
)

                
print
(
"-"
 
*
 
30
)

                
print
(
f"Mode: 
{
self
.
brain
.
config
[
'system'
]
[
'mode'
]
}
"
)

                
print
(
f"Max concurrent goals: 
{
self
.
brain
.
config
[
'limits'
]
[
'max_concurrent_goals'
]
}
"
)

                
print
(
f"LLM Provider: 
{
self
.
brain
.
config
[
'llm'
]
[
'provider'
]
}
"
)

                
print
(
f"Model: 
{
self
.
brain
.
config
[
'llm'
]
[
'model'
]
}
"
)

        
        
elif
 action 
==
 
"set"
:

            
if
 
len
(
args
)
 
<
 
3
:

                
print
(
"Usage: config set <key> <value>"
)

                
return

            
            key 
=
 args
[
1
]

            value 
=
 args
[
2
]

            self
.
_set_nested_config
(
key
,
 value
)

            
print
(
f"✅ Configuration updated: 
{
key
}
 = 
{
value
}
"
)

    
    
def
 
_get_nested_config
(
self
,
 key
:
 
str
)
 
-
>
 Any
:

        
"""Get nested configuration value."""

        keys 
=
 key
.
split
(
"."
)

        value 
=
 self
.
brain
.
config
        
        
for
 k 
in
 keys
:

            
if
 
isinstance
(
value
,
 
dict
)
 
and
 k 
in
 value
:

                value 
=
 value
[
k
]

            
else
:

                
return
 
None

        
        
return
 value
    
    
def
 
_set_nested_config
(
self
,
 key
:
 
str
,
 value
:
 
str
)
:

        
"""Set nested configuration value."""

        keys 
=
 key
.
split
(
"."
)

        cfg 
=
 self
.
brain
.
config
        
        
for
 k 
in
 keys
[
:
-
1
]
:

            cfg 
=
 cfg
.
setdefault
(
k
,
 
{
}
)

        
        
# Try to convert value to appropriate type

        cfg
[
keys
[
-
1
]
]
 
=
 self
.
_convert_value
(
value
)

    
    
def
 
_convert_value
(
self
,
 value
:
 
str
)
 
-
>
 Any
:

        
"""Convert string value to appropriate type."""

        
if
 value
.
lower
(
)
 
in
 
[
"true"
,
 
"false"
]
:

            
return
 value
.
lower
(
)
 
==
 
"true"

        
        
try
:

            
if
 
"."
 
in
 value
:

                
return
 
float
(
value
)

            
return
 
int
(
value
)

        
except
:

            
return
 value
    
    
async
 
def
 
cmd_clear
(
self
,
 args
:
 List
[
str
]
)
:

        
"""Clear screen."""

        
print
(
"\033[H\033[J"
)

    
    
async
 
def
 
cmd_exit
(
self
,
 args
:
 List
[
str
]
)
:

        
"""Exit the application."""

        
print
(
"\n👋 Shutting down Autonomous AI..."
)

        
await
 self
.
brain
.
shutdown
(
)

        sys
.
exit
(
0
)



### interface/dashboard.py