import json
from pathlib import Path
from typing import Dict, List, Any

from tools.code_generator import CodeGenerator
from tools.file_tool import FileTool
from web_intelligence.backend_intel import BackendIntel
from web_intelligence.api_designer import APIDesigner


class BackendAgent:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.code_generator = CodeGenerator(config)
        self.file_tool = FileTool(config)
        self.backend_intel = BackendIntel(config)
        self.api_designer = APIDesigner(config)
    
    async def execute(self, task, goal) -> Dict[str, Any]:
        """Execute backend development tasks."""
        logs = []
        files_generated = []
        
        try:
            if "authentication" in task.title.lower():
                result = await self._implement_authentication(goal)
                files_generated.extend(result["files"])
                logs.append("Implemented authentication system")
            
            elif any(x in task.title.lower() for x in ["api", "endpoint"]):
                entity = self._extract_entity(task.title)
                result = await self._implement_api_endpoints(goal, entity)
                files_generated.extend(result["files"])
                logs.append(f"Implemented {entity} API endpoints")
            
            elif "api documentation" in task.title.lower():
                result = await self._generate_api_docs(goal)
                files_generated.extend(result["files"])
                logs.append("Generated API documentation")
            
            else:
                # Generic backend task
                result = await self._implement_generic_backend(task, goal)
                files_generated.extend(result["files"])
                logs.append("Completed backend implementation")
            
            return {
                "status": "completed",
                "files_generated": files_generated,
                "logs": logs
            }
            
        except Exception as e:
            return {
                "status": "failed",
                "files_generated": files_generated,
                "logs": logs,
                "error": str(e)
            }
    
    async def _implement_authentication(self, goal) -> Dict[str, Any]:
        """Implement JWT authentication system."""
        project_name = goal.context.get("project_name", "app")
        base_path = Path(self.config["paths"]["projects_root"]) / project_name / "backend" / "app"
        
        files = []
        
        # JWT utility
        jwt_content = self.backend_intel.generate_jwt_handler()
        jwt_file = base_path / "auth" / "jwt_handler.py"
        jwt_file.parent.mkdir(exist_ok=True)
        
        await self.file_tool.write_file(str(jwt_file), jwt_content)
        files.append(str(jwt_file))
        
        # Auth endpoints
        auth_api_content = self.backend_intel.generate_auth_api()
        auth_api_file = base_path / "auth" / "auth_api.py"
        await self.file_tool.write_file(str(auth_api_file), auth_api_content)
        files.append(str(auth_api_file))
        
        # User model
        user_model_content = self.backend_intel.generate_user_model()
        user_model_file = base_path / "models" / "user.py"
        user_model_file.parent.mkdir(exist_ok=True)
        await self.file_tool.write_file(str(user_model_file), user_model_content)
        files.append(str(user_model_file))
        
        return {"files": files}
    
    async def _implement_api_endpoints(self, goal, entity: str) -> Dict[str, Any]:
        """Implement CRUD API endpoints for an entity."""
        project_name = goal.context.get("project_name", "app")
        base_path = Path(self.config["paths"]["projects_root"]) / project_name / "backend" / "app"
        
        # API file
        api_content = self.backend_intel.generate_crud_api(entity)
        api_file = base_path / f"{entity}_api.py"
        
        await self.file_tool.write_file(str(api_file), api_content)
        
        # Service file
        service_content = self.backend_intel.generate_service_layer(entity)
        service_file = base_path / f"{entity}_service.py"
        
        await self.file_tool.write_file(str(service_file), service_content)
        
        # Model file
        model_content = self.backend_intel.generate_model(entity)
        model_file = base_path / "models" / f"{entity}.py"
        model_file.parent.mkdir(exist_ok=True)
        
        await self.file_tool.write_file(str(model_file), model_content)
        
        return {
            "files": [str(api_file), str(service_file), str(model_file)]
        }
    
    async def _generate_api_docs(self, goal) -> Dict[str, Any]:
        """Generate OpenAPI documentation."""
        project_name = goal.context.get("project_name", "app")
        api_spec = self.api_designer.generate_openapi_spec(goal.analyzed_requirements)
        
        docs_path = Path(self.config["paths"]["projects_root"]) / project_name / "docs"
        docs_path.mkdir(parents=True, exist_ok=True)
        
        api_spec_file = docs_path / "openapi.json"
        await self.file_tool.write_file(
            str(api_spec_file),
            json.dumps(api_spec, indent=2)
        )
        
        return {"files": [str(api_spec_file)]}
    
    async def _implement_generic_backend(self, task, goal) -> Dict[str, Any]:
        """Implement generic backend functionality."""
        project_name = goal.context.get("project_name", "app")
        base_path = Path(self.config["paths"]["projects_root"]) / project_name / "backend"
        
        # Generate based on task description
        content = self.backend_intel.generate_backend_module(task.description)
        
        output_file = base_path / f"{task.task_id}.py"
        await self.file_tool.write_file(str(output_file), content)
        
        return {"files": [str(output_file)]}
    
    def _extract_entity(self, title: str) -> str:
        """Extract entity name from task title."""
        import re
        
        match = re.search(r'Implement (\w+) API', title)
        if match:
            return match.group(1).lower()
        
        return "generic"
 
agents/frontend_agent.py
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
 List
,
 Any


from
 tools
.
code_generator 
import
 CodeGenerator

from
 tools
.
file_tool 
import
 FileTool

from
 web_intelligence
.
frontend_intel 
import
 FrontendIntel



class
 
FrontendAgent
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
code_generator 
=
 CodeGenerator
(
config
)

        self
.
file_tool 
=
 FileTool
(
config
)

        self
.
frontend_intel 
=
 FrontendIntel
(
config
)

    
    
async
 
def
 
execute
(
self
,
 task
,
 goal
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

        
"""Execute frontend development tasks."""

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
 
"authentication"
 
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
_build_auth_ui
(
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
append
(
"Built authentication UI components"
)

            
            
elif
 
any
(
x 
in
 task
.
title
.
lower
(
)
 
for
 x 
in
 
[
"ui"
,
 
"page"
,
 
"component"
]
)
:

                entity 
=
 self
.
_extract_entity
(
task
.
title
)

                result 
=
 
await
 self
.
_build_management_ui
(
goal
,
 entity
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
append
(
f"Built 
{
entity
}
 management UI"
)

            
            
elif
 
"navigation"
 
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
_build_navigation
(
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
append
(
"Built navigation layout"
)

            
            
elif
 
"framework"
 
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
_setup_frontend_framework
(
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
append
(
"Set up frontend framework"
)

            
            
else
:

                result 
=
 
await
 self
.
_implement_generic_frontend
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
append
(
"Completed frontend implementation"
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
 
_build_auth_ui
(
self
,
 goal
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

        
"""Build authentication UI components."""

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

        tech_stack 
=
 goal
.
analyzed_requirements
.
get
(
"tech_stack"
,
 
{
}
)

        
        
if
 tech_stack
.
get
(
"frontend"
)
 
==
 
"react"
:

            
return
 
await
 self
.
_build_react_auth_ui
(
project_name
)

        
elif
 tech_stack
.
get
(
"frontend"
)
 
==
 
"nextjs"
:

            
return
 
await
 self
.
_build_nextjs_auth_ui
(
project_name
)

        
else
:

            
return
 
await
 self
.
_build_generic_auth_ui
(
project_name
)

    
    
async
 
def
 
_build_react_auth_ui
(
self
,
 project_name
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

        
"""Build React authentication components."""

        base_path 
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
 
"frontend"
 
/
 
"src"

        
        files 
=
 
[
]

        
        
# Login component

        login_content 
=
 self
.
frontend_intel
.
generate_login_component
(
)

        login_file 
=
 base_path 
/
 
"components"
 
/
 
"auth"
 
/
 
"Login.jsx"

        login_file
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

        
        
await
 self
.
file_tool
.
write_file
(
str
(
login_file
)
,
 login_content
)

        files
.
append
(
str
(
login_file
)
)

        
        
# Register component

        register_content 
=
 self
.
frontend_intel
.
generate_register_component
(
)

        register_file 
=
 base_path 
/
 
"components"
 
/
 
"auth"
 
/
 
"Register.jsx"

        
        
await
 self
.
file_tool
.
write_file
(
str
(
register_file
)
,
 register_content
)

        files
.
append
(
str
(
register_file
)
)

        
        
# Auth service

        auth_service_content 
=
 self
.
frontend_intel
.
generate_auth_service
(
)

        auth_service_file 
=
 base_path 
/
 
"services"
 
/
 
"auth.js"

        auth_service_file
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

        
        
await
 self
.
file_tool
.
write_file
(
str
(
auth_service_file
)
,
 auth_service_content
)

        files
.
append
(
str
(
auth_service_file
)
)

        
        
return
 
{
"files"
:
 files
}

    
    
async
 
def
 
_build_management_ui
(
self
,
 goal
,
 entity
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

        
"""Build management UI for an entity."""

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

        tech_stack 
=
 goal
.
analyzed_requirements
.
get
(
"tech_stack"
,
 
{
}
)

        
        
if
 tech_stack
.
get
(
"frontend"
)
 
==
 
"react"
:

            
return
 
await
 self
.
_build_react_management_ui
(
project_name
,
 entity
)

        
else
:

            
return
 
await
 self
.
_build_generic_management_ui
(
project_name
,
 entity
)

    
    
async
 
def
 
_build_react_management_ui
(
self
,
 project_name
:
 
str
,
 entity
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

        
"""Build React management components."""

        base_path 
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
 
"frontend"
 
/
 
"src"

        
        files 
=
 
[
]

        
        
# List component

        list_content 
=
 self
.
frontend_intel
.
generate_list_component
(
entity
)

        list_file 
=
 base_path 
/
 
"components"
 
/
 
f"
{
entity
.
capitalize
(
)
}
List.jsx"

        list_file
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

        
        
await
 self
.
file_tool
.
write_file
(
str
(
list_file
)
,
 list_content
)

        files
.
append
(
str
(
list_file
)
)

        
        
# Form component

        form_content 
=
 self
.
frontend_intel
.
generate_form_component
(
entity
)

        form_file 
=
 base_path 
/
 
"components"
 
/
 
f"
{
entity
.
capitalize
(
)
}
Form.jsx"

        
        
await
 self
.
file_tool
.
write_file
(
str
(
form_file
)
,
 form_content
)

        files
.
append
(
str
(
form_file
)
)

        
        
# API service

        api_service_content 
=
 self
.
frontend_intel
.
generate_api_service
(
entity
)

        api_service_file 
=
 base_path 
/
 
"services"
 
/
 
f"
{
entity
}
API.js"

        
        
await
 self
.
file_tool
.
write_file
(
str
(
api_service_file
)
,
 api_service_content
)

        files
.
append
(
str
(
api_service_file
)
)

        
        
return
 
{
"files"
:
 files
}

    
    
async
 
def
 
_build_navigation
(
self
,
 goal
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

        
"""Build navigation layout."""

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

        base_path 
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
 
"frontend"
 
/
 
"src"

        
        files 
=
 
[
]

        
        
# Navigation component

        nav_content 
=
 self
.
frontend_intel
.
generate_navigation_component
(
)

        nav_file 
=
 base_path 
/
 
"components"
 
/
 
"layout"
 
/
 
"Navigation.jsx"

        nav_file
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

        
        
await
 self
.
file_tool
.
write_file
(
str
(
nav_file
)
,
 nav_content
)

        files
.
append
(
str
(
nav_file
)
)

        
        
# Layout component

        layout_content 
=
 self
.
frontend_intel
.
generate_layout_component
(
)

        layout_file 
=
 base_path 
/
 
"components"
 
/
 
"layout"
 
/
 
"Layout.jsx"

        
        
await
 self
.
file_tool
.
write_file
(
str
(
layout_file
)
,
 layout_content
)

        files
.
append
(
str
(
layout_file
)
)

        
        
return
 
{
"files"
:
 files
}

    
    
async
 
def
 
_setup_frontend_framework
(
self
,
 goal
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

        
"""Setup frontend framework boilerplate."""

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

        tech_stack 
=
 goal
.
analyzed_requirements
.
get
(
"tech_stack"
,
 
{
}
)

        
        
if
 tech_stack
.
get
(
"frontend"
)
 
==
 
"react"
:

            
return
 
await
 self
.
_setup_react
(
project_name
)

        
else
:

            
return
 
{
"files"
:
 
[
]
}

    
    
async
 
def
 
_setup_react
(
self
,
 project_name
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

        
"""Setup React project."""

        base_path 
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
 
"frontend"

        
        files 
=
 
[
]

        
        
# App.js

        app_content 
=
 self
.
frontend_intel
.
generate_react_app
(
)

        app_file 
=
 base_path 
/
 
"src"
 
/
 
"App.js"

        app_file
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

        
        
await
 self
.
file_tool
.
write_file
(
str
(
app_file
)
,
 app_content
)

        files
.
append
(
str
(
app_file
)
)

        
        
# App.css

        css_content 
=
 self
.
frontend_intel
.
generate_app_css
(
)

        css_file 
=
 base_path 
/
 
"src"
 
/
 
"App.css"

        
        
await
 self
.
file_tool
.
write_file
(
str
(
css_file
)
,
 css_content
)

        files
.
append
(
str
(
css_file
)
)

        
        
return
 
{
"files"
:
 files
}

    
    
async
 
def
 
_implement_generic_frontend
(
self
,
 task
,
 goal
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

        
"""Implement generic frontend functionality."""

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

        base_path 
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
 
"frontend"

        
        content 
=
 self
.
frontend_intel
.
generate_frontend_module
(
task
.
description
)

        
        output_file 
=
 base_path 
/
 
f"
{
task
.
task_id
}
.jsx"

        
await
 self
.
file_tool
.
write_file
(
str
(
output_file
)
,
 content
)

        
        
return
 
{
"files"
:
 
[
str
(
output_file
)
]
}

    
    
def
 
_extract_entity
(
self
,
 title
:
 
str
)
 
-
>
 
str
:

        
"""Extract entity name from task title."""

        
import
 re
        
        
match
 
=
 re
.
search
(
r'Build (\w+) UI'
,
 title
)

        
if
 
match
:

            
return
 
match
.
group
(
1
)
.
lower
(
)

        
        
return
 
"generic"
 
Let me continue with the remaining agents and memory systems in the next response.
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 Next
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
Edit
 
 
Copy
 
 
Share
 
 
 
 
 
 
 
 
 
 
 
 
 
Expand System with Remaining Agents Memory Tools Intelligence Execution
 
 
 
 
The user wants me to continue generating the complete system. I have generated the core engines (ai_brain, goal_manager, requirement_engine, planner, reflection_engine, code_quality_engine, metrics_engine, testing_engine) and the initial agents (manager_agent, architect_agent, backend_agent, frontend_agent).
I need to continue with:
Remaining agents: database_agent, qa_agent, reviewer_agent, devops_agent
Memory system: short_term.py, long_term.py, experience_memory.py, user_preferences.py
Tools: file_tool.py, code_generator.py, code_editor.py, command_runner.py, test_runner.py, browser_tool.py
Web intelligence modules: frontend_intel.py, backend_intel.py, database_intel.py, auth_intel.py, api_designer.py
Execution modules: sandbox.py, error_handler.py
Versioning modules: git_manager.py, diff_engine.py
Interface modules: cli.py, dashboard.py
Final config and any remaining files
Let me continue systematically, ensuring each file is production-ready, complete, and follows the established patterns.
Next batch:
database_agent.py
qa_agent.py
reviewer_agent.py
devops_agent.py
memory/short_term.py
memory/long_term.py
memory/experience_memory.py
memory/user_preferences.py
I'll generate these now.
 
 
 
agents/database_agent.py
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
 List
,
 Any


from
 tools
.
file_tool 
import
 FileTool

from
 web_intelligence
.
database_intel 
import
 DatabaseIntel



class
 
DatabaseAgent
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
file_tool 
=
 FileTool
(
config
)

        self
.
database_intel 
=
 DatabaseIntel
(
config
)

    
    
async
 
def
 
execute
(
self
,
 task
,
 goal
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

        
"""Execute database-related tasks."""

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
 
"schema"
 
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
_design_database_schema
(
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
append
(
"Designed database schema"
)

            
            
elif
 
"connection"
 
in
 task
.
title
.
lower
(
)
 
or
 
"orm"
 
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
_setup_database_connection
(
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
append
(
"Set up database connection and ORM"
)

            
            
elif
 
"migration"
 
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
_create_migration
(
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
append
(
"Created database migration"
)

            
            
elif
 
"seed"
 
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
_create_seed_data
(
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
append
(
"Created seed data scripts"
)

            
            
else
:

                result 
=
 
await
 self
.
_implement_generic_database
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
append
(
"Completed database implementation"
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
 
_design_database_schema
(
self
,
 goal
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

        
"""Design database schema from requirements."""

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

        schema 
=
 goal
.
analyzed_requirements
.
get
(
"database_schema"
,
 
{
}
)

        
        tech_stack 
=
 goal
.
analyzed_requirements
.
get
(
"tech_stack"
,
 
{
}
)

        db_type 
=
 tech_stack
.
get
(
"database"
,
 
"postgresql"
)

        
        base_path 
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
        
        files 
=
 
[
]

        
        
if
 db_type 
==
 
"postgresql"
 
or
 db_type 
==
 
"mysql"
:

            
# SQL schema

            sql_schema 
=
 self
.
database_intel
.
generate_sql_schema
(
schema
)

            schema_file 
=
 base_path 
/
 
"database"
 
/
 
"schema.sql"

            schema_file
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

            
            
await
 self
.
file_tool
.
write_file
(
str
(
schema_file
)
,
 sql_schema
)

            files
.
append
(
str
(
schema_file
)
)

            
            
# Migration script

            migration_script 
=
 self
.
database_intel
.
generate_migration_script
(
schema
,
 db_type
)

            migration_file 
=
 base_path 
/
 
"database"
 
/
 
"migrations"
 
/
 
"001_initial.py"

            migration_file
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

            
            
await
 self
.
file_tool
.
write_file
(
str
(
migration_file
)
,
 migration_script
)

            files
.
append
(
str
(
migration_file
)
)

        
        
elif
 db_type 
==
 
"mongodb"
:

            
# MongoDB schema

            mongo_schema 
=
 self
.
database_intel
.
generate_mongodb_schema
(
schema
)

            schema_file 
=
 base_path 
/
 
"database"
 
/
 
"schema.js"

            schema_file
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

            
            
await
 self
.
file_tool
.
write_file
(
str
(
schema_file
)
,
 mongo_schema
)

            files
.
append
(
str
(
schema_file
)
)

        
        
return
 
{
"files"
:
 files
}

    
    
async
 
def
 
_setup_database_connection
(
self
,
 goal
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

        
"""Setup database connection and ORM."""

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

        tech_stack 
=
 goal
.
analyzed_requirements
.
get
(
"tech_stack"
,
 
{
}
)

        db_type 
=
 tech_stack
.
get
(
"database"
,
 
"postgresql"
)

        
        base_path 
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
 
"backend"
 
/
 
"app"

        
        files 
=
 
[
]

        
        
# Database config

        db_config 
=
 self
.
database_intel
.
generate_db_config
(
db_type
)

        config_file 
=
 base_path 
/
 
"database"
 
/
 
"config.py"

        config_file
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

        
        
await
 self
.
file_tool
.
write_file
(
str
(
config_file
)
,
 db_config
)

        files
.
append
(
str
(
config_file
)
)

        
        
# ORM models

        orm_models 
=
 self
.
database_intel
.
generate_orm_models
(

            goal
.
analyzed_requirements
.
get
(
"database_schema"
,
 
{
}
)
,

            db_type
        
)

        models_file 
=
 base_path 
/
 
"database"
 
/
 
"models.py"

        
        
await
 self
.
file_tool
.
write_file
(
str
(
models_file
)
,
 orm_models
)

        files
.
append
(
str
(
models_file
)
)

        
        
# Connection manager

        connection_manager 
=
 self
.
database_intel
.
generate_connection_manager
(
db_type
)

        manager_file 
=
 base_path 
/
 
"database"
 
/
 
"connection.py"

        
        
await
 self
.
file_tool
.
write_file
(
str
(
manager_file
)
,
 connection_manager
)

        files
.
append
(
str
(
manager_file
)
)

        
        
return
 
{
"files"
:
 files
}

    
    
async
 
def
 
_create_migration
(
self
,
 goal
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

        
"""Create database migration."""

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

        base_path 
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
        
        migration_content 
=
 self
.
database_intel
.
generate_migration
(

            goal
.
analyzed_requirements
.
get
(
"database_schema"
,
 
{
}
)

        
)

        
        migration_file 
=
 base_path 
/
 
"database"
 
/
 
"migrations"
 
/
 
f"migration_
{
int
(
asyncio
.
get_event_loop
(
)
.
time
(
)
)
}
.py"

        migration_file
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

        
        
await
 self
.
file_tool
.
write_file
(
str
(
migration_file
)
,
 migration_content
)

        
        
return
 
{
"files"
:
 
[
str
(
migration_file
)
]
}

    
    
async
 
def
 
_create_seed_data
(
self
,
 goal
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

        
"""Create seed data scripts."""

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

        base_path 
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
        
        seed_script 
=
 self
.
database_intel
.
generate_seed_script
(

            goal
.
analyzed_requirements
.
get
(
"database_schema"
,
 
{
}
)

        
)

        
        seed_file 
=
 base_path 
/
 
"database"
 
/
 
"seed.py"

        
        
await
 self
.
file_tool
.
write_file
(
str
(
seed_file
)
,
 seed_script
)

        
        
return
 
{
"files"
:
 
[
str
(
seed_file
)
]
}

    
    
async
 
def
 
_implement_generic_database
(
self
,
 task
,
 goal
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

        
"""Implement generic database functionality."""

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

        base_path 
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
        
        content 
=
 self
.
database_intel
.
generate_database_module
(
task
.
description
)

        
        output_file 
=
 base_path 
/
 
"database"
 
/
 
f"
{
task
.
task_id
}
.sql"

        output_file
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

        
        
await
 self
.
file_tool
.
write_file
(
str
(
output_file
)
,
 content
)

        
        
return
 
{
"files"
:
 
[
str
(
output_file
)
]
}
 
agents/qa_agent.py
Python
 
 
 
Copy
 
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


from
 core
.
testing_engine 
import
 TestingEngine



class
 
QAAgent
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
testing_engine 
=
 TestingEngine
(
config
)

    
    
async
 
def
 
execute
(
self
,
 task
,
 goal
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

        
"""Execute QA/testing tasks."""

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
 
"unit"
 
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
_run_unit_tests
(
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
 
"integration"
 
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
_run_integration_tests
(
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
 
"api"
 
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
_run_api_tests
(
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
 
"ui"
 
in
 task
.
title
.
lower
(
)
 
or
 
"browser"
 
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
_run_ui_tests
(
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
 
"regression"
 
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
_run_regression_tests
(
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
 
"test"
 
in
 task
.
title
.
lower
(
)
 
and
 
"write"
 
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
_write_tests
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
append
(
"Wrote test files"
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
 
_run_unit_tests
(
self
,
 goal
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

        
"""Run unit tests."""

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

        project_path 
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
        
        results 
=
 
await
 self
.
testing_engine
.
run_unit_tests
(
str
(
project_path
)
)

        
        logs 
=
 
[

            
f"Unit tests 
{
'passed'
 
if
 results
.
passed 
else
 
'failed'
}
"
,

            
f"Coverage: 
{
results
.
coverage
:
.1f
}
%"
,

            
f"Failures: 
{
len
(
results
.
failures
)
}
"

        
]

        
        
if
 
not
 results
.
passed
:

            logs
.
extend
(
[
f"FAIL: 
{
failure
}
"
 
for
 failure 
in
 results
.
failures
[
:
3
]
]
)

        
        
return
 
{
"logs"
:
 logs
}

    
    
async
 
def
 
_run_integration_tests
(
self
,
 goal
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

        
"""Run integration tests."""

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

        project_path 
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
        
        results 
=
 
await
 self
.
testing_engine
.
run_integration_tests
(
str
(
project_path
)
)

        
        logs 
=
 
[

            
f"Integration tests 
{
'passed'
 
if
 results
.
passed 
else
 
'failed'
}
"
,

            
f"Execution time: 
{
results
.
execution_time
:
.1f
}
s"

        
]

        
        
return
 
{
"logs"
:
 logs
}

    
    
async
 
def
 
_run_api_tests
(
self
,
 goal
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

        
"""Run API tests."""

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

        project_path 
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
        
        results 
=
 
await
 self
.
testing_engine
.
run_api_tests
(
str
(
project_path
)
)

        
        logs 
=
 
[

            
f"API tests 
{
'passed'
 
if
 results
.
passed 
else
 
'failed'
}
"
,

            
f"Files tested: 
{
len
(
results
.
files_tested
)
}
"

        
]

        
        
return
 
{
"logs"
:
 logs
}

    
    
async
 
def
 
_run_ui_tests
(
self
,
 goal
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

        
"""Run UI tests."""

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

        project_path 
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
        
        results 
=
 
await
 self
.
testing_engine
.
run_ui_tests
(
str
(
project_path
)
)

        
        logs 
=
 
[

            
f"UI tests 
{
'passed'
 
if
 results
.
passed 
else
 
'failed'
}
"
,

            
f"Execution time: 
{
results
.
execution_time
:
.1f
}
s"

        
]

        
        
return
 
{
"logs"
:
 logs
}

    
    
async
 
def
 
_run_regression_tests
(
self
,
 goal
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

        
"""Run regression tests."""

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

        project_path 
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
        
        results 
=
 
await
 self
.
testing_engine
.
run_regression_tests
(
str
(
project_path
)
)

        
        logs 
=
 
[

            
f"Regression tests 
{
'passed'
 
if
 results
.
passed 
else
 
'failed'
}
"
,

            
f"Critical paths tested: 
{
len
(
results
.
files_tested
)
}
"

        
]

        
        
return
 
{
"logs"
:
 logs
}

    
    
async
 
def
 
_write_tests
(
self
,
 task
,
 goal
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

        
"""Write test files."""

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

        base_path 
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
        
        test_content 
=
 self
.
testing_engine
.
generate_test_template
(

            task
.
description
,

            goal
.
analyzed_requirements
        
)

        
        test_file 
=
 base_path 
/
 
"tests"
 
/
 
f"test_
{
task
.
task_id
}
.py"

        test_file
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

        
        
await
 self
.
file_tool
.
write_file
(
str
(
test_file
)
,
 test_content
)

        
        
return
 
{
"files"
:
 
[
str
(
test_file
)
]
}
 
agents/reviewer_agent.py
Python
 
 
 
Copy
 
from
 typing 
import
 Dict
,
 List
,
 Any


from
 core
.
code_quality_engine 
import
 CodeQualityEngine



class
 
ReviewerAgent
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
code_quality_engine 
=
 CodeQualityEngine
(
config
)

    
    
async
 
def
 
execute
(
self
,
 task
,
 goal
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

        
"""Execute code review tasks."""

        
try
:

            review_result 
=
 
await
 self
.
code_quality_engine
.
review_goal
(
goal
)

            
            logs 
=
 
[

                
f"Quality score: 
{
review_result
.
quality_score
:
.2f
}
"
,

                
f"Issues found: 
{
len
(
review_result
.
issues
)
}
"
,

                
f"Security vulnerabilities: 
{
len
(
review_result
.
security_vulnerabilities
)
}
"

            
]

            
            
# Add critical issues to logs

            critical_issues 
=
 
[
i 
for
 i 
in
 review_result
.
issues 
if
 i
.
get
(
"severity"
)
 
==
 
"critical"
]

            
if
 critical_issues
:

                logs
.
extend
(
[
f"CRITICAL: 
{
issue
[
'description'
]
}
"
 
for
 issue 
in
 critical_issues
[
:
3
]
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
 
[
]
,

                
"logs"
:
 logs
,

                
"review_result"
:
 review_result
            
}

            
        
except
 Exception 
as
 e
:

            
return
 
{

                
"status"
:
 
"failed"
,

                
"files_generated"
:
 
[
]
,

                
"logs"
:
 
[
]
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
 
review_goal
(
self
,
 goal
,
 task_results
:
 List
[
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

        
"""Review a complete goal."""

        
return
 
await
 self
.
code_quality_engine
.
review_goal
(
goal
)
 
agents/devops_agent.py
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
 List
,
 Any


from
 tools
.
command_runner 
import
 CommandRunner

from
 tools
.
file_tool 
import
 FileTool



class
 
DevOpsAgent
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
command_runner 
=
 CommandRunner
(
config
)

        self
.
file_tool 
=
 FileTool
(
config
)

    
    
async
 
def
 
execute
(
self
,
 task
,
 goal
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

        
"""Execute DevOps tasks."""

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
 
"project structure"
 
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
_initialize_project_structure
(
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
append
(
"Initialized project structure"
)

            
            
elif
 
"docker"
 
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
_setup_docker
(
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
append
(
"Set up Docker configuration"
)

            
            
elif
 
"git"
 
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
_setup_git
(
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
 
"deploy"
 
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
_setup_deployment
(
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
append
(
"Set up deployment configuration"
)

            
            
elif
 
"install"
 
in
 task
.
title
.
lower
(
)
 
or
 
"dependency"
 
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
_install_dependencies
(
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

            
            
else
:

                result 
=
 
await
 self
.
_run_generic_devops
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
 
_initialize_project_structure
(
self
,
 goal
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

        
"""Initialize Git repository and basic structure."""

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

        base_path 
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
        
        
# Create README

        readme_content 
=
 
f""
"
# {project_name}


AI
-
generated web application
.



## Quick Start