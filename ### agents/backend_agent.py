```python
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

```bash

# Install dependencies

npm install  
# or pip install -r requirements.txt



# Run development server

npm start    
# or python main.py
# Create .gitignore
    gitignore_content = self._get_gitignore_template()
    gitignore_file = base_path / ".gitignore"
    await self.file_tool.write_file(str(gitignore_file), gitignore_content)
    
    # Initialize git repo
    await self.command_runner.run_command(
        ["git", "init"],
        cwd=str(base_path)
    )
    
    return {
        "files": [str(readme_file), str(gitignore_file)]
    }

async def _setup_docker(self, goal) -> Dict[str, Any]:
    """Setup Docker configuration."""
    project_name = goal.context.get("project_name", "app")
    base_path = Path(self.config["paths"]["projects_root"]) / project_name
    
    tech_stack = goal.analyzed_requirements.get("tech_stack", {})
    
    files = []
    
    # Dockerfile
    if tech_stack.get("backend") == "fastapi":
        dockerfile_content = self._get_fastapi_dockerfile()
    else:
        dockerfile_content = self._get_generic_dockerfile()
    
    dockerfile = base_path / "Dockerfile"
    await self.file_tool.write_file(str(dockerfile), dockerfile_content)
    files.append(str(dockerfile))
    
    # docker-compose.yml
    compose_content = self._get_docker_compose_template(tech_stack)
    compose_file = base_path / "docker-compose.yml"
    await self.file_tool.write_file(str(compose_file), compose_content)
    files.append(str(compose_file))
    
    return {"files": files}

async def _setup_git(self, goal) -> Dict[str, Any]:
    """Setup Git and create initial commit."""
    project_name = goal.context.get("project_name", "app")
    base_path = Path(self.config["paths"]["projects_root"]) / project_name
    
    # Add all files
    await self.command_runner.run_command(
        ["git", "add", "."],
        cwd=str(base_path)
    )
    
    # Initial commit
    result = await self.command_runner.run_command(
        ["git", "commit", "-m", "Initial commit by AutonomousAI"],
        cwd=str(base_path)
    )
    
    return {
        "logs": [f"Git initial commit: {'success' if result.returncode == 0 else 'failed'}"]
    }

async def _setup_deployment(self, goal) -> Dict[str, Any]:
    """Setup deployment configuration."""
    project_name = goal.context.get("project_name", "app")
    base_path = Path(self.config["paths"]["projects_root"]) / project_name
    
    # GitHub Actions workflow
    workflow_content = self._get_github_workflow()
    workflow_file = base_path / ".github" / "workflows" / "deploy.yml"
    workflow_file.parent.mkdir(parents=True, exist_ok=True)
    
    await self.file_tool.write_file(str(workflow_file), workflow_content)
    
    return {"files": [str(workflow_file)]}

async def _install_dependencies(self, goal) -> Dict[str, Any]:
    """Install project dependencies."""
    project_name = goal.context.get("project_name", "app")
    base_path = Path(self.config["paths"]["projects_root"]) / project_name
    
    tech_stack = goal.analyzed_requirements.get("tech_stack", {})
    
    logs = []
    
    # Install backend dependencies
    if (base_path / "backend" / "requirements.txt").exists():
        result = await self.command_runner.run_command(
            ["pip", "install", "-r", "requirements.txt"],
            cwd=str(base_path / "backend")
        )
        logs.append(f"Backend dependencies: {'installed' if result.returncode == 0 else 'failed'}")
    
    # Install frontend dependencies
    if (base_path / "frontend" / "package.json").exists():
        result = await self.command_runner.run_command(
            ["npm", "install"],
            cwd=str(base_path / "frontend")
        )
        logs.append(f"Frontend dependencies: {'installed' if result.returncode == 0 else 'failed'}")
    
    return {"logs": logs}

async def _run_generic_devops(self, task, goal) -> Dict[str, Any]:
    """Run generic DevOps commands."""
    # Parse command from task description
    import re
    
    command_match = re.search(r'run\s+(.+)', task.description.lower())
    if command_match:
        command = command_match.group(1).split()
        
        project_name = goal.context.get("project_name", "app")
        base_path = Path(self.config["paths"]["projects_root"]) / project_name
        
        result = await self.command_runner.run_command(command, cwd=str(base_path))
        
        return {
            "logs": [f"Command '{' '.join(command)}': {'success' if result.returncode == 0 else 'failed'}"]
        }
    
    return {"logs": ["No command specified"]}

def _get_gitignore_template(self) -> str:
    return '''# Dependencies
def _get_fastapi_dockerfile(self) -> str:
    return '''FROM python:3.11-slim
def _get_generic_dockerfile(self) -> str:
    return '''FROM node:18-alpine
def _get_docker_compose_template(self, tech_stack: Dict[str, str]) -> str:
    return f'''version: '3.8'
def _get_github_workflow(self) -> str:
    return '''name: Deploy
steps:
- uses: actions/checkout@v3

- name: Setup Node.js
  uses: actions/setup-node@v3
  with:
    node-version: '18'

- name: Install dependencies
  run: npm ci

- name: Run tests
  run: npm test

- name: Build
  run: npm run build

- name: Deploy
  run: echo "Deployment would happen here"
Now I'll create the memory system:

### memory/__init__.py
```python
# Memory package
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
# Tools package
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

```python

"""
Backend intelligence module for generating FastAPI/Flask code.
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
 
BackendIntel
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
 
"fastapi"
  
# Default

    
    
def
 
generate_jwt_handler
(
self
)
 
-
>
 
str
:

        
"""Generate JWT authentication handler."""

        
return
 
'''from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = "your-secret-key-here"  # Use environment variable in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
'''

    
    
def
 
generate_auth_api
(
self
)
 
-
>
 
str
:

        
"""Generate authentication API endpoints."""

        
return
 
'''from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from jose import jwt

from ..database import get_db
from ..models.user import User
from .jwt_handler import (
    verify_password, create_access_token, get_password_hash, 
    verify_token, ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter(prefix="/auth", tags=["authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(User).filter(User.id == payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register")
def register(user_data: dict, db: Session = Depends(get_db)):
    # Check if user exists
    existing = db.query(User).filter(User.email == user_data["email"]).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = User(
        email=user_data["email"],
        name=user_data["name"],
        password_hash=get_password_hash(user_data["password"])
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name
    }
'''

    
    
def
 
generate_user_model
(
self
)
 
-
>
 
str
:

        
"""Generate User model."""

        
return
 
'''from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": str(self.id),
            "email": self.email,
            "name": self.name,
            "created_at": self.created_at.isoformat()
        }
'''

    
    
def
 
generate_crud_api
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

        
"""Generate CRUD API endpoints for an entity."""

        entity_cap 
=
 entity
.
capitalize
(
)

        
        
return
 
f'''from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models.
{
entity
}
 import 
{
entity_cap
}

from ..schemas.
{
entity
}
 import 
{
entity_cap
}
Create, 
{
entity_cap
}
Response

router = APIRouter(prefix="/
{
entity
}
s", tags=["
{
entity
}
s"])

@router.get("/", response_model=List[
{
entity_cap
}
Response])
def list_items(db: Session = Depends(get_db)):
    items = db.query(
{
entity_cap
}
).all()
    return items

@router.post("/", response_model=
{
entity_cap
}
Response)
def create_item(item: 
{
entity_cap
}
Create, db: Session = Depends(get_db)):
    db_item = 
{
entity_cap
}
(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/{{item_id}}", response_model=
{
entity_cap
}
Response)
def get_item(item_id: str, db: Session = Depends(get_db)):
    item = db.query(
{
entity_cap
}
).filter(
{
entity_cap
}
.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="
{
entity_cap
}
 not found")
    return item

@router.put("/{{item_id}}", response_model=
{
entity_cap
}
Response)
def update_item(item_id: str, item: 
{
entity_cap
}
Create, db: Session = Depends(get_db)):
    db_item = db.query(
{
entity_cap
}
).filter(
{
entity_cap
}
.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="
{
entity_cap
}
 not found")
    
    for key, value in item.dict().items():
        setattr(db_item, key, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/{{item_id}}")
def delete_item(item_id: str, db: Session = Depends(get_db)):
    item = db.query(
{
entity_cap
}
).filter(
{
entity_cap
}
.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="
{
entity_cap
}
 not found")
    
    db.delete(item)
    db.commit()
    return {{ "message": "
{
entity_cap
}
 deleted successfully" }}
'''

    
    
def
 
generate_service_layer
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

        
"""Generate service layer for an entity."""

        entity_cap 
=
 entity
.
capitalize
(
)

        
        
return
 
f'''from sqlalchemy.orm import Session
from typing import List, Optional

from ..models.
{
entity
}
 import 
{
entity_cap
}

from ..schemas.
{
entity
}
 import 
{
entity_cap
}
Create

class 
{
entity_cap
}
Service:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self) -> List[
{
entity_cap
}
]:
        return self.db.query(
{
entity_cap
}
).all()
    
    def get_by_id(self, item_id: str) -> Optional[
{
entity_cap
}
]:
        return self.db.query(
{
entity_cap
}
).filter(
{
entity_cap
}
.id == item_id).first()
    
    def create(self, item: 
{
entity_cap
}
Create) -> 
{
entity_cap
}
:
        db_item = 
{
entity_cap
}
(**item.dict())
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item
    
    def update(self, item_id: str, item: 
{
entity_cap
}
Create) -> Optional[
{
entity_cap
}
]:
        db_item = self.get_by_id(item_id)
        if not db_item:
            return None
        
        for key, value in item.dict().items():
            setattr(db_item, key, value)
        
        self.db.commit()
        self.db.refresh(db_item)
        return db_item
    
    def delete(self, item_id: str) -> bool:
        db_item = self.get_by_id(item_id)
        if not db_item:
            return False
        
        self.db.delete(db_item)
        self.db.commit()
        return True

def get_service(db: Session):
    return 
{
entity_cap
}
Service(db)
'''

    
    
def
 
generate_model
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

        
"""Generate SQLAlchemy model for an entity."""

        entity_cap 
=
 entity
.
capitalize
(
)

        
        
return
 
f'''from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
import uuid
from datetime import datetime

Base = declarative_base()

class 
{
entity_cap
}
(Base):
    __tablename__ = "
{
entity
}
s"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    user = relationship("User", back_populates="
{
entity
}
s")

    def to_dict(self):
        return {{
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "user_id": str(self.user_id)
        }}
'''

    
    
def
 
generate_backend_module
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

        
"""Generate a generic backend module."""

        
return
 
f'''"""
Generated backend module
Description: 
{
description
}

"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def read_root():
    return {{"message": "Generated endpoint for: 
{
description
}
"}}

@router.post("/")
def create_item(item: dict):
    return {{"message": "Item created", "data": item}}
'''

    
    
def
 
generate_jwt_middleware
(
self
)
 
-
>
 
str
:

        
"""Generate JWT authentication middleware."""

        
return
 
'''from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
    
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

def verify_jwt(jwtoken: str):
    try:
        payload = jwt.decode(jwtoken, "SECRET_KEY", algorithms=["HS256"])
        return payload
    except:
        return None
'''



### web_intelligence/database_intel.py

```python

"""
Database intelligence module for generating SQL/NoSQL schemas.
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
 
DatabaseIntel
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
preferred_db 
=
 config
.
get
(
"preferred_database"
,
 
"postgresql"
)

    
    
def
 
generate_sql_schema
(
self
,
 schema
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

        
"""Generate SQL schema from schema definition."""

        tables 
=
 schema
.
get
(
"tables"
,
 
[
]
)

        
        sql_statements 
=
 
[
]

        
        
for
 table 
in
 tables
:

            table_name 
=
 table
[
"name"
]

            columns 
=
 table
[
"columns"
]

            
            
# Generate CREATE TABLE

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

            
            create_table 
=
 
f"CREATE TABLE 
{
table_name
}
 (\n    "
 
+
 
",\n    "
.
join
(
column_defs
)
 
+
 
"\n);"

            sql_statements
.
append
(
create_table
)

            
            
# Add indexes

            indexes 
=
 table
.
get
(
"indexes"
,
 
[
]
)

            
for
 idx 
in
 indexes
:

                sql_statements
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

        
        
# Add relationships

        relationships 
=
 schema
.
get
(
"relationships"
,
 
[
]
)

        
for
 rel 
in
 relationships
:

            
if
 rel
[
"type"
]
 
==
 
"foreign_key"
:

                sql_statements
.
append
(

                    
f"ALTER TABLE 
{
rel
[
'from_table'
]
}
 "

                    
f"ADD CONSTRAINT fk_
{
rel
[
'from_table'
]
}
_
{
rel
[
'to_table'
]
}
 "

                    
f"FOREIGN KEY (
{
rel
[
'from_column'
]
}
) "

                    
f"REFERENCES 
{
rel
[
'to_table'
]
}
(
{
rel
[
'to_column'
]
}
);"

                
)

        
        
return
 
"\n\n"
.
join
(
sql_statements
)

    
    
def
 
generate_migration_script
(
self
,
 schema
:
 Dict
[
str
,
 Any
]
,
 db_type
:
 
str
 
=
 
"postgresql"
)
 
-
>
 
str
:

        
"""Generate database migration script."""

        
return
 
f'''"""
Database migration script
Generated by AutonomousAI
"""

from sqlalchemy import create_engine, MetaData, Table, Column
from sqlalchemy.dialects.postgresql import UUID
import uuid

def upgrade():
    """Upgrade database schema."""
    # TODO: Implement migration
    pass

def downgrade():
    """Downgrade database schema."""
    # TODO: Implement rollback
    pass

if __name__ == "__main__":
    upgrade()
'''

    
    
def
 
generate_mongodb_schema
(
self
,
 schema
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

        
"""Generate MongoDB schema."""

        collections 
=
 schema
.
get
(
"tables"
,
 
[
]
)

        
        js_statements 
=
 
[
]

        
        
for
 collection 
in
 collections
:

            collection_name 
=
 collection
[
"name"
]

            js_statements
.
append
(
f"// Collection: 
{
collection_name
}
"
)

            js_statements
.
append
(
f'db.createCollection("
{
collection_name
}
");'
)

            
            
# Add indexes

            indexes 
=
 collection
.
get
(
"indexes"
,
 
[
]
)

            
for
 idx 
in
 indexes
:

                js_statements
.
append
(
f'db.
{
collection_name
}
.createIndex({{ "
{
idx
}
": 1 }});'
)

        
        
return
 
"\n\n"
.
join
(
js_statements
)

    
    
def
 
generate_db_config
(
self
,
 db_type
:
 
str
)
 
-
>
 
str
:

        
"""Generate database configuration."""

        
if
 db_type 
==
 
"postgresql"
:

            
return
 
'''from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost:5432/app"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
'''

        
elif
 db_type 
==
 
"mongodb"
:

            
return
 
'''from pymongo import MongoClient
import os

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")

client = MongoClient(MONGODB_URL)
db = client.app

def get_db():
    return db
'''

        
else
:

            
return
 
f'# Database configuration for 
{
db_type
}
\n# TODO: Implement config\n'

    
    
def
 
generate_orm_models
(
self
,
 schema
:
 Dict
[
str
,
 Any
]
,
 db_type
:
 
str
)
 
-
>
 
str
:

        
"""Generate ORM models."""

        
if
 db_type 
==
 
"postgresql"
:

            
return
 self
.
_generate_sqlalchemy_models
(
schema
)

        
elif
 db_type 
==
 
"mongodb"
:

            
return
 self
.
_generate_mongoengine_models
(
schema
)

        
else
:

            
return
 
f'# ORM models for 
{
db_type
}
\n# TODO: Implement models\n'

    
    
def
 
_generate_sqlalchemy_models
(
self
,
 schema
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

        
"""Generate SQLAlchemy models."""

        tables 
=
 schema
.
get
(
"tables"
,
 
[
]
)

        
        code 
=
 
[

            
"from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean"
,

            
"from sqlalchemy.dialects.postgresql import UUID"
,

            
"from sqlalchemy.orm import declarative_base, relationship"
,

            
"import uuid"
,

            
"from datetime import datetime"
,

            
""
,

            
"Base = declarative_base()"
,

            
""

        
]

        
        
for
 table 
in
 tables
:

            table_name 
=
 table
[
"name"
]

            table_class 
=
 
''
.
join
(
word
.
capitalize
(
)
 
for
 word 
in
 table_name
.
rstrip
(
's'
)
.
split
(
'_'
)
)

            
            code
.
append
(
f"class 
{
table_class
}
(Base):"
)

            code
.
append
(
f'    __tablename__ = "
{
table_name
}
"'
)

            code
.
append
(
""
)

            
            
for
 col 
in
 table
[
"columns"
]
:

                col_def 
=
 
f'    
{
col
[
"name"
]
}
 = Column('

                
                col_type 
=
 col
[
"type"
]

                
if
 
"UUID"
 
in
 col_type
:

                    col_def 
+=
 
"UUID(as_uuid=True)"

                
elif
 
"VARCHAR"
 
in
 col_type
:

                    col_def 
+=
 
"String"

                
elif
 
"TIMESTAMP"
 
in
 col_type
:

                    col_def 
+=
 
"DateTime"

                
elif
 
"BOOLEAN"
 
in
 col_type
:

                    col_def 
+=
 
"Boolean"

                
elif
 
"INTEGER"
 
in
 col_type
:

                    col_def 
+=
 
"Integer"

                
else
:

                    col_def 
+=
 
"String"

                
                
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
 
", primary_key=True"

                
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
 
", unique=True"

                
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
 
", nullable=False"

                
if
 
"default"
 
in
 col
:

                    col_def 
+=
 
f', default=
{
col
[
"default"
]
}
'

                
                col_def 
+=
 
")"

                code
.
append
(
col_def
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
 
_generate_mongoengine_models
(
self
,
 schema
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

        
"""Generate MongoEngine models."""

        
return
 
'''from mongoengine import Document, StringField, DateTimeField, UUIDField
import uuid
from datetime import datetime

class BaseDocument(Document):
    meta = {'abstract': True}
    
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = DateTimeField(default=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "created_at": self.created_at.isoformat()
        }
'''

    
    
def
 
generate_connection_manager
(
self
,
 db_type
:
 
str
)
 
-
>
 
str
:

        
"""Generate database connection manager."""

        
if
 db_type 
==
 
"postgresql"
:

            
return
 
'''import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

class DatabaseManager:
    def __init__(self, database_url: str = None):
        self.database_url = database_url or os.getenv(
            "DATABASE_URL",
            "postgresql://user:password@localhost:5432/app"
        )
        self.engine = None
        self.session_factory = None
        self.session = None
    
    def connect(self):
        self.engine = create_engine(self.database_url, pool_pre_ping=True)
        self.session_factory = sessionmaker(bind=self.engine)
        self.session = scoped_session(self.session_factory)
    
    def disconnect(self):
        if self.session:
            self.session.remove()
        if self.engine:
            self.engine.dispose()
    
    def get_session(self):
        if not self.session:
            self.connect()
        return self.session()

db_manager = DatabaseManager()
'''

        
else
:

            
return
 
f'# Connection manager for 
{
db_type
}
\n# TODO: Implement\n'

    
    
def
 
generate_seed_script
(
self
,
 schema
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

        
"""Generate database seed script."""

        
return
 
'''"""
Seed script for database
"""

import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import get_db
from app.models.user import User
from app.core.security import get_password_hash

def seed():
    db = next(get_db())
    
    # Create admin user if not exists
    admin = db.query(User).filter(User.email == "admin@example.com").first()
    if not admin:
        admin = User(
            email="admin@example.com",
            name="Admin User",
            password_hash=get_password_hash("admin123")
        )
        db.add(admin)
        db.commit()
        print("Admin user created: admin@example.com / admin123")
    
    print("Database seeding completed!")

if __name__ == "__main__":
    seed()
'''

    
    
def
 
generate_database_module
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

        
"""Generate a generic database module."""

        
return
 
f'''"""
Generated database module
Description: 
{
description
}

"""

def setup_database():
    """Setup database tables."""
    # TODO: Implement
    pass

def migrate():
    """Run database migrations."""
    # TODO: Implement
    pass

if __name__ == "__main__":
    setup_database()
'''



### web_intelligence/auth_intel.py

```python

"""
Authentication intelligence module for JWT, OAuth, and security.
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
 
AuthIntel
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
 
generate_jwt_auth_system
(
self
)
 
-
>
 Dict
[
str
,
 
str
]
:

        
"""Generate complete JWT authentication system."""

        
return
 
{

            
"jwt_handler.py"
:
 self
.
_generate_jwt_handler
(
)
,

            
"auth_middleware.py"
:
 self
.
_generate_auth_middleware
(
)
,

            
"auth_routes.py"
:
 self
.
_generate_auth_routes
(
)
,

            
"user_model.py"
:
 self
.
_generate_user_model
(
)

        
}

    
    
def
 
_generate_jwt_handler
(
self
)
 
-
>
 
str
:

        
"""Generate JWT handler utility."""

        
return
 
'''"""
JWT Authentication Handler
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
import os

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)

def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    })
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Verify and decode a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def create_refresh_token(data: dict) -> str:
    """Create a long-lived refresh token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=30)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh"
    })
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
'''

    
    
def
 
_generate_auth_middleware
(
self
)
 
-
>
 
str
:

        
"""Generate authentication middleware."""

        
return
 
'''"""
FastAPI Authentication Middleware
"""

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt

from .jwt_handler import verify_token

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
    
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            
            payload = verify_token(credentials.credentials)
            if not payload:
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            
            return payload
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

def get_current_user(payload: dict = Depends(JWTBearer())):
    """Get current user from token payload."""
    return payload

def get_current_active_user(current_user: dict = Depends(get_current_user)):
    """Get current active user with additional checks."""
    # Could check if user is active, not deleted, etc.
    return current_user

def require_role(required_role: str):
    """Decorator to require specific role."""
    def role_checker(current_user: dict = Depends(get_current_user)):
        if current_user.get("role") != required_role:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return current_user
    return role_checker
'''

    
    
def
 
_generate_auth_routes
(
self
)
 
-
>
 
str
:

        
"""Generate authentication routes."""

        
return
 
'''"""
Authentication Routes
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from .jwt_handler import (
    create_access_token, create_refresh_token,
    get_password_hash, verify_password
)
from ..database import get_db
from ..models.user import User

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login endpoint."""
    user = db.query(User).filter(User.email == form_data.username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token = create_access_token(
        data={{"sub": str(user.id), "email": user.email}}
    )
    
    refresh_token = create_refresh_token(
        data={{"sub": str(user.id), "email": user.email}}
    )
    
    return {{
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": user.to_dict()
    }}

@router.post("/refresh")
def refresh_token(payload: dict = Depends(JWTBearer())):
    """Refresh access token."""
    access_token = create_access_token(
        data={{"sub": payload["sub"], "email": payload.get("email")}}
    )
    
    return {{
        "access_token": access_token,
        "token_type": "bearer"
    }}

@router.post("/logout")
def logout():
    """Logout endpoint (client-side token removal)."""
    return {{"message": "Successfully logged out"}}

@router.get("/me")
def get_current_user_info(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user information."""
    user = db.query(User).filter(User.id == current_user["sub"]).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user.to_dict()

@router.post("/register")
def register(user_data: dict, db: Session = Depends(get_db)):
    """User registration."""
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data["email"]).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    user = User(
        email=user_data["email"],
        name=user_data["name"],
        password_hash=get_password_hash(user_data["password"])
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Auto-login after registration
    access_token = create_access_token(
        data={{"sub": str(user.id), "email": user.email}}
    )
    
    return {{
        "access_token": access_token,
        "token_type": "bearer",
        "user": user.to_dict()
    }}
'''

    
    
def
 
_generate_user_model
(
self
)
 
-
>
 
str
:

        
"""Generate User model for authentication."""

        
return
 
'''"""
User Model
"""

from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
import uuid
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

    def to_dict(self):
        """Convert to dictionary, excluding sensitive fields."""
        return {
            "id": str(self.id),
            "email": self.email,
            "name": self.name,
            "is_active": self.is_active,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat(),
            "last_login": self.last_login.isoformat() if self.last_login else None
        }
'''

    
    
def
 
generate_oauth_integration
(
self
,
 provider
:
 
str
)
 
-
>
 
str
:

        
"""Generate OAuth integration for a provider."""

        
return
 
f'''"""
OAuth Integration for 
{
provider
}

"""

import os
from fastapi import APIRouter, HTTPException
from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request
from starlette.responses import RedirectResponse

router = APIRouter(prefix="/oauth/
{
provider
.
lower
(
)
}
", tags=["oauth"])

oauth = OAuth()

oauth.register(
    name="
{
provider
.
lower
(
)
}
",
    client_id=os.getenv("
{
provider
.
upper
(
)
}
_CLIENT_ID"),
    client_secret=os.getenv("
{
provider
.
upper
(
)
}
_CLIENT_SECRET"),
    access_token_url="
{
self
.
_get_oauth_token_url
(
provider
)
}
",
    authorize_url="
{
self
.
_get_oauth_auth_url
(
provider
)
}
",
    client_kwargs={{"scope": "openid email profile"}},
)

@router.get("/login")
async def login(request: Request):
    """Redirect to OAuth provider."""
    redirect_uri = request.url_for("auth_
{
provider
.
lower
(
)
}
_callback")
    return await oauth.
{
provider
.
lower
(
)
}
.authorize_redirect(request, redirect_uri)

@router.get("/callback")
async def callback(request: Request):
    """Handle OAuth callback."""
    try:
        token = await oauth.
{
provider
.
lower
(
)
}
.authorize_access_token(request)
        user_info = await oauth.
{
provider
.
lower
(
)
}
.userinfo(token=token)
        
        # TODO: Create/update user in database
        # TODO: Generate JWT token
        
        return {{"user": user_info, "token": token}}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
'''

    
    
def
 
_get_oauth_token_url
(
self
,
 provider
:
 
str
)
 
-
>
 
str
:

        
"""Get OAuth token URL for provider."""

        urls 
=
 
{

            
"google"
:
 
"https://accounts.google.com/o/oauth2/token"
,

            
"github"
:
 
"https://github.com/login/oauth/access_token"
,

            
"facebook"
:
 
"https://graph.facebook.com/v12.0/oauth/access_token"

        
}

        
return
 urls
.
get
(
provider
.
lower
(
)
,
 
""
)

    
    
def
 
_get_oauth_auth_url
(
self
,
 provider
:
 
str
)
 
-
>
 
str
:

        
"""Get OAuth authorization URL for provider."""

        urls 
=
 
{

            
"google"
:
 
"https://accounts.google.com/o/oauth2/auth"
,

            
"github"
:
 
"https://github.com/login/oauth/authorize"
,

            
"facebook"
:
 
"https://www.facebook.com/v12.0/dialog/oauth"

        
}

        
return
 urls
.
get
(
provider
.
lower
(
)
,
 
""
)

    
    
def
 
generate_password_reset_flow
(
self
)
 
-
>
 Dict
[
str
,
 
str
]
:

        
"""Generate password reset flow components."""

        
return
 
{

            
"reset_request.py"
:
 self
.
_generate_reset_request
(
)
,

            
"reset_token.py"
:
 self
.
_generate_reset_token_handler
(
)
,

            
"email_sender.py"
:
 self
.
_generate_email_sender
(
)

        
}

    
    
def
 
_generate_reset_request
(
self
)
 
-
>
 
str
:

        
"""Generate password reset request handler."""

        
return
 
'''"""
Password Reset Request
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import uuid
import os

from ..database import get_db
from ..models.user import User
from .email_sender import send_reset_email

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/reset-password-request")
def request_password_reset(email: str, db: Session = Depends(get_db)):
    """Request password reset email."""
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        # Don't reveal if user exists
        return {"message": "If the email exists, a reset link has been sent"}
    
    # Generate reset token
    reset_token = str(uuid.uuid4())
    
    # Store token with expiry (in Redis or database)
    # TODO: Implement token storage
    
    # Send reset email
    send_reset_email(user.email, reset_token)
    
    return {"message": "If the email exists, a reset link has been sent"}

@router.post("/reset-password")
def reset_password(token: str, new_password: str, db: Session = Depends(get_db)):
    """Reset password using token."""
    # TODO: Verify token and expiry
    
    # TODO: Update user password
    
    return {"message": "Password reset successfully"}
'''

    
    
def
 
_generate_reset_token_handler
(
self
)
 
-
>
 
str
:

        
"""Generate reset token handler."""

        
return
 
'''"""
Reset Token Handler
"""

import redis
import uuid
import os
from datetime import timedelta

class ResetTokenManager:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            db=0
        )
        self.token_expiry = timedelta(hours=1)
    
    def create_token(self, user_id: str) -> str:
        """Create a reset token for user."""
        token = str(uuid.uuid4())
        self.redis_client.setex(
            f"reset_token:{token}",
            int(self.token_expiry.total_seconds()),
            user_id
        )
        return token
    
    def verify_token(self, token: str) -> str:
        """Verify reset token and return user ID."""
        user_id = self.redis_client.get(f"reset_token:{token}")
        if user_id:
            return user_id.decode()
        return None
    
    def delete_token(self, token: str):
        """Delete reset token."""
        self.redis_client.delete(f"reset_token:{token}")

# Global instance
reset_token_manager = ResetTokenManager()
'''

    
    
def
 
_generate_email_sender
(
self
)
 
-
>
 
str
:

        
"""Generate email sender utility."""

        
return
 
'''"""
Email Sender for Authentication
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_reset_email(to_email: str, reset_token: str):
    """Send password reset email."""
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASSWORD")
    
    if not smtp_user or not smtp_pass:
        print("SMTP credentials not configured")
        return
    
    # Email content
    msg = MIMEMultipart()
    msg["From"] = smtp_user
    msg["To"] = to_email
    msg["Subject"] = "Password Reset Request"
    
    reset_link = f"{os.getenv('FRONTEND_URL', 'http://localhost:3000')}/reset-password?token={reset_token}"
    
    body = f"""
    Hello,
    
    You requested a password reset. Click the link below to reset your password:
    
    {reset_link}
    
    This link will expire in 1 hour.
    
    If you didn't request this, please ignore this email.
    """
    
    msg.attach(MIMEText(body, "plain"))
    
    # Send email
    try:
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)
        server.quit()
        print(f"Reset email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# For development: print to console
def send_reset_email_dev(to_email: str, reset_token: str):
    """Development version: print reset link to console."""
    reset_link = f"http://localhost:3000/reset-password?token={reset_token}"
    print(f"=== PASSWORD RESET LINK FOR {to_email} ===")
    print(reset_link)
    print("=" * 50)
'''



### web_intelligence/api_designer.py

```python

"""
API Designer module for creating RESTful and GraphQL APIs.
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
 
APIDesigner
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
 
design
(
self
,
 features
:
 List
[
Dict
]
,
 user_flows
:
 List
[
Dict
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

        
"""Design API based on features and user flows."""

        api_spec 
=
 
{

            
"openapi"
:
 
"3.0.0"
,

            
"info"
:
 
{

                
"title"
:
 
"AutonomousAI Generated API"
,

                
"version"
:
 
"1.0.0"

            
}
,

            
"paths"
:
 
{
}
,

            
"components"
:
 
{

                
"schemas"
:
 
{
}
,

                
"securitySchemes"
:
 
{

                    
"BearerAuth"
:
 
{

                        
"type"
:
 
"http"
,

                        
"scheme"
:
 
"bearer"
,

                        
"bearerFormat"
:
 
"JWT"

                    
}

                
}

            
}

        
}

        
        
# Design paths based on features

        
for
 feature 
in
 features
:

            feature_name 
=
 feature
[
"name"
]

            
if
 
"user"
 
in
 feature_name
:

                api_spec
[
"paths"
]
.
update
(
self
.
_generate_user_paths
(
)
)

            
elif
 
any
(
x 
in
 feature_name 
for
 x 
in
 
[
"product"
,
 
"post"
,
 
"article"
,
 
"order"
]
)
:

                entity 
=
 feature
.
get
(
"entity"
,
 feature_name
.
split
(
"_"
)
[
0
]
)

                api_spec
[
"paths"
]
.
update
(
self
.
_generate_crud_paths
(
entity
)
)

        
        
# Design paths based on user flows

        
for
 flow 
in
 user_flows
:

            flow_name 
=
 flow
[
"name"
]

            
if
 
"payment"
 
in
 flow_name
:

                api_spec
[
"paths"
]
.
update
(
self
.
_generate_payment_paths
(
)
)

            
elif
 
"search"
 
in
 flow_name
:

                api_spec
[
"paths"
]
.
update
(
self
.
_generate_search_paths
(
)
)

        
        
return
 api_spec
    
    
def
 
_generate_user_paths
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

        
"""Generate user-related API paths."""

        
return
 
{

            
"/auth/login"
:
 
{

                
"post"
:
 
{

                    
"summary"
:
 
"User login"
,

                    
"requestBody"
:
 
{

                        
"content"
:
 
{

                            
"application/json"
:
 
{

                                
"schema"
:
 
{

                                    
"type"
:
 
"object"
,

                                    
"required"
:
 
[
"email"
,
 
"password"
]
,

                                    
"properties"
:
 
{

                                        
"email"
:
 
{
"type"
:
 
"string"
,
 
"format"
:
 
"email"
}
,

                                        
"password"
:
 
{
"type"
:
 
"string"
,
 
"format"
:
 
"password"
}

                                    
}

                                
}

                            
}

                        
}

                    
}
,

                    
"responses"
:
 
{

                        
"200"
:
 
{

                            
"description"
:
 
"Login successful"
,

                            
"content"
:
 
{

                                
"application/json"
:
 
{

                                    
"schema"
:
 
{

                                        
"type"
:
 
"object"
,

                                        
"properties"
:
 
{

                                            
"access_token"
:
 
{
"type"
:
 
"string"
}
,

                                            
"token_type"
:
 
{
"type"
:
 
"string"
}

                                        
}

                                    
}

                                
}

                            
}

                        
}
,

                        
"401"
:
 
{
"description"
:
 
"Invalid credentials"
}

                    
}

                
}

            
}
,

            
"/auth/register"
:
 
{

                
"post"
:
 
{

                    
"summary"
:
 
"User registration"
,

                    
"requestBody"
:
 
{

                        
"content"
:
 
{

                            
"application/json"
:
 
{

                                
"schema"
:
 
{

                                    
"type"
:
 
"object"
,

                                    
"required"
:
 
[
"email"
,
 
"password"
,
 
"name"
]
,

                                    
"properties"
:
 
{

                                        
"email"
:
 
{
"type"
:
 
"string"
,
 
"format"
:
 
"email"
}
,

                                        
"password"
:
 
{
"type"
:
 
"string"
,
 
"format"
:
 
"password"
}
,

                                        
"name"
:
 
{
"type"
:
 
"string"
}

                                    
}

                                
}

                            
}

                        
}

                    
}
,

                    
"responses"
:
 
{

                        
"201"
:
 
{
"description"
:
 
"User created"
}
,

                        
"400"
:
 
{
"description"
:
 
"Email already exists"
}

                    
}

                
}

            
}

        
}

    
    
def
 
_generate_crud_paths
(
self
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

        
"""Generate CRUD paths for an entity."""

        base_path 
=
 
f"/
{
entity
}
s"

        entity_id_path 
=
 
f"/
{
entity
}
s/{{id}}"

        
        
return
 
{

            base_path
:
 
{

                
"get"
:
 
{

                    
"summary"
:
 
f"List 
{
entity
}
s"
,

                    
"security"
:
 
[
{
"BearerAuth"
:
 
[
]
}
]
,

                    
"responses"
:
 
{

                        
"200"
:
 
{

                            
"description"
:
 
f"List of 
{
entity
}
s"
,

                            
"content"
:
 
{

                                
"application/json"
:
 
{

                                    
"schema"
:
 
{

                                        
"type"
:
 
"array"
,

                                        
"items"
:
 
{
"$ref"
:
 
f"#/components/schemas/
{
entity
.
capitalize
(
)
}
"
}

                                    
}

                                
}

                            
}

                        
}

                    
}

                
}
,

                
"post"
:
 
{

                    
"summary"
:
 
f"Create 
{
entity
}
"
,

                    
"security"
:
 
[
{
"BearerAuth"
:
 
[
]
}
]
,

                    
"requestBody"
:
 
{

                        
"content"
:
 
{

                            
"application/json"
:
 
{

                                
"schema"
:
 
{
"$ref"
:
 
f"#/components/schemas/
{
entity
.
capitalize
(
)
}
Create"
}

                            
}

                        
}

                    
}
,

                    
"responses"
:
 
{

                        
"201"
:
 
{

                            
"description"
:
 
f"
{
entity
.
capitalize
(
)
}
 created"
,

                            
"content"
:
 
{

                                
"application/json"
:
 
{

                                    
"schema"
:
 
{
"$ref"
:
 
f"#/components/schemas/
{
entity
.
capitalize
(
)
}
"
}

                                
}

                            
}

                        
}

                    
}

                
}

            
}
,

            entity_id_path
:
 
{

                
"get"
:
 
{

                    
"summary"
:
 
f"Get 
{
entity
}
 by ID"
,

                    
"security"
:
 
[
{
"BearerAuth"
:
 
[
]
}
]
,

                    
"parameters"
:
 
[

                        
{

                            
"name"
:
 
"id"
,

                            
"in"
:
 
"path"
,

                            
"required"
:
 
True
,

                            
"schema"
:
 
{
"type"
:
 
"string"
}

                        
}

                    
]
,

                    
"responses"
:
 
{

                        
"200"
:
 
{

                            
"description"
:
 
f"
{
entity
.
capitalize
(
)
}
 details"
,

                            
"content"
:
 
{

                                
"application/json"
:
 
{

                                    
"schema"
:
 
{
"$ref"
:
 
f"#/components/schemas/
{
entity
.
capitalize
(
)
}
"
}

                                
}

                            
}

                        
}
,

                        
"404"
:
 
{
"description"
:
 
f"
{
entity
.
capitalize
(
)
}
 not found"
}

                    
}

                
}
,

                
"put"
:
 
{

                    
"summary"
:
 
f"Update 
{
entity
}
"
,

                    
"security"
:
 
[
{
"BearerAuth"
:
 
[
]
}
]
,

                    
"parameters"
:
 
[

                        
{

                            
"name"
:
 
"id"
,

                            
"in"
:
 
"path"
,

                            
"required"
:
 
True
,

                            
"schema"
:
 
{
"type"
:
 
"string"
}

                        
}

                    
]
,

                    
"requestBody"
:
 
{

                        
"content"
:
 
{

                            
"application/json"
:
 
{

                                
"schema"
:
 
{
"$ref"
:
 
f"#/components/schemas/
{
entity
.
capitalize
(
)
}
Create"
}

                            
}

                        
}

                    
}
,

                    
"responses"
:
 
{

                        
"200"
:
 
{

                            
"description"
:
 
f"
{
entity
.
capitalize
(
)
}
 updated"
,

                            
"content"
:
 
{

                                
"application/json"
:
 
{

                                    
"schema"
:
 
{
"$ref"
:
 
f"#/components/schemas/
{
entity
.
capitalize
(
)
}
"
}

                                
}

                            
}

                        
}

                    
}

                
}
,

                
"delete"
:
 
{

                    
"summary"
:
 
f"Delete 
{
entity
}
"
,

                    
"security"
:
 
[
{
"BearerAuth"
:
 
[
]
}
]
,

                    
"parameters"
:
 
[

                        
{

                            
"name"
:
 
"id"
,

                            
"in"
:
 
"path"
,

                            
"required"
:
 
True
,

                            
"schema"
:
 
{
"type"
:
 
"string"
}

                        
}

                    
]
,

                    
"responses"
:
 
{

                        
"204"
:
 
{
"description"
:
 
f"
{
entity
.
capitalize
(
)
}
 deleted"
}

                    
}

                
}

            
}

        
}

    
    
def
 
_generate_payment_paths
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

        
"""Generate payment API paths."""

        
return
 
{

            
"/payments/create"
:
 
{

                
"post"
:
 
{

                    
"summary"
:
 
"Create payment intent"
,

                    
"security"
:
 
[
{
"BearerAuth"
:
 
[
]
}
]
,

                    
"requestBody"
:
 
{

                        
"content"
:
 
{

                            
"application/json"
:
 
{

                                
"schema"
:
 
{

                                    
"type"
:
 
"object"
,

                                    
"required"
:
 
[
"amount"
,
 
"currency"
]
,

                                    
"properties"
:
 
{

                                        
"amount"
:
 
{
"type"
:
 
"number"
}
,

                                        
"currency"
:
 
{
"type"
:
 
"string"
,
 
"default"
:
 
"usd"
}

                                    
}

                                
}

                            
}

                        
}

                    
}
,

                    
"responses"
:
 
{

                        
"200"
:
 
{

                            
"description"
:
 
"Payment intent created"
,

                            
"content"
:
 
{

                                
"application/json"
:
 
{

                                    
"schema"
:
 
{

                                        
"type"
:
 
"object"
,

                                        
"properties"
:
 
{

                                            
"client_secret"
:
 
{
"type"
:
 
"string"
}

                                        
}

                                    
}

                                
}

                            
}

                        
}

                    
}

                
}

            
}
,

            
"/payments/confirm"
:
 
{

                
"post"
:
 
{

                    
"summary"
:
 
"Confirm payment"
,

                    
"security"
:
 
[
{
"BearerAuth"
:
 
[
]
}
]
,

                    
"requestBody"
:
 
{

                        
"content"
:
 
{

                            
"application/json"
:
 
{

                                
"schema"
:
 
{

                                    
"type"
:
 
"object"
,

                                    
"required"
:
 
[
"payment_intent_id"
]
,

                                    
"properties"
:
 
{

                                        
"payment_intent_id"
:
 
{
"type"
:
 
"string"
}

                                    
}

                                
}

                            
}

                        
}

                    
}
,

                    
"responses"
:
 
{

                        
"200"
:
 
{
"description"
:
 
"Payment confirmed"
}
,

                        
"400"
:
 
{
"description"
:
 
"Payment failed"
}

                    
}

                
}

            
}

        
}

    
    
def
 
_generate_search_paths
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

        
"""Generate search API paths."""

        
return
 
{

            
"/search"
:
 
{

                
"get"
:
 
{

                    
"summary"
:
 
"Search across resources"
,

                    
"security"
:
 
[
{
"BearerAuth"
:
 
[
]
}
]
,

                    
"parameters"
:
 
[

                        
{

                            
"name"
:
 
"q"
,

                            
"in"
:
 
"query"
,

                            
"required"
:
 
True
,

                            
"schema"
:
 
{
"type"
:
 
"string"
}

                        
}
,

                        
{

                            
"name"
:
 
"limit"
,

                            
"in"
:
 
"query"
,

                            
"schema"
:
 
{
"type"
:
 
"integer"
,
 
"default"
:
 
20
}

                        
}

                    
]
,

                    
"responses"
:
 
{

                        
"200"
:
 
{

                            
"description"
:
 
"Search results"
,

                            
"content"
:
 
{

                                
"application/json"
:
 
{

                                    
"schema"
:
 
{

                                        
"type"
:
 
"object"
,

                                        
"properties"
:
 
{

                                            
"results"
:
 
{
"type"
:
 
"array"
}
,

                                            
"total"
:
 
{
"type"
:
 
"integer"
}

                                        
}

                                    
}

                                
}

                            
}

                        
}

                    
}

                
}

            
}

        
}

    
    
def
 
generate_openapi_spec
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
 Dict
[
str
,
 Any
]
:

        
"""Generate complete OpenAPI specification."""

        features 
=
 requirements
.
get
(
"features"
,
 
[
]
)

        tech_stack 
=
 requirements
.
get
(
"tech_stack"
,
 
{
}
)

        
        spec 
=
 
{

            
"openapi"
:
 
"3.0.0"
,

            
"info"
:
 
{

                
"title"
:
 
"API Specification"
,

                
"version"
:
 
"1.0.0"
,

                
"description"
:
 
"Generated API specification"

            
}
,

            
"servers"
:
 
[

                
{

                    
"url"
:
 
f"http://localhost:
{
'8000'
 
if
 tech_stack
.
get
(
'backend'
)
 
==
 
'fastapi'
 
else
 
'3000'
}
"
,

                    
"description"
:
 
"Development server"

                
}

            
]
,

            
"paths"
:
 
{
}
,

            
"components"
:
 
{

                
"schemas"
:
 
{
}
,

                
"securitySchemes"
:
 
{

                    
"BearerAuth"
:
 
{

                        
"type"
:
 
"http"
,

                        
"scheme"
:
 
"bearer"
,

                        
"bearerFormat"
:
 
"JWT"

                    
}

                
}

            
}

        
}

        
        
# Add paths based on features

        
for
 feature 
in
 features
:

            feature_name 
=
 feature
[
"name"
]

            
if
 
"auth"
 
in
 feature_name
:

                spec
[
"paths"
]
.
update
(
self
.
_generate_user_paths
(
)
)

            
elif
 
any
(
x 
in
 feature_name 
for
 x 
in
 
[
"product"
,
 
"post"
,
 
"article"
,
 
"order"
,
 
"item"
]
)
:

                entity 
=
 feature
.
get
(
"entity"
,
 
"item"
)

                spec
[
"paths"
]
.
update
(
self
.
_generate_crud_paths
(
entity
)
)

        
        
return
 spec


### execution/__init__.py

```python

# Execution package
"""
Sandbox module for safe code execution.
"""


import
 asyncio

import
 resource

import
 subprocess

import
 sys

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
 
SandboxResult
:

    success
:
 
bool

    output
:
 
str

    error
:
 Optional
[
str
]

    execution_time
:
 
float

    memory_used
:
 
int



class
 
Sandbox
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
enabled 
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

        self
.
memory_limit_mb 
=
 config
[
"limits"
]
.
get
(
"memory_limit_mb"
,
 
512
)

        self
.
allowed_dirs 
=
 
[

            Path
(
config
[
"paths"
]
[
"projects_root"
]
)
,

            Path
(
config
[
"paths"
]
[
"temp"
]
)

        
]

    
    
def
 
_setup_resource_limits
(
self
)
:

        
"""Set up resource limits for sandbox."""

        
if
 
not
 self
.
enabled
:

            
return

        
        
try
:

            
# Memory limit (in bytes)

            memory_limit 
=
 self
.
memory_limit_mb 
*
 
1024
 
*
 
1024

            resource
.
setrlimit
(
resource
.
RLIMIT_AS
,
 
(
memory_limit
,
 memory_limit
)
)

            
            
# CPU time limit (in seconds)

            cpu_limit 
=
 self
.
timeout
            resource
.
setrlimit
(
resource
.
RLIMIT_CPU
,
 
(
cpu_limit
,
 cpu_limit
)
)

            
            
# Max number of open files

            resource
.
setrlimit
(
resource
.
RLIMIT_NOFILE
,
 
(
64
,
 
64
)
)

            
        
except
 Exception 
as
 e
:

            
print
(
f"Warning: Could not set resource limits: 
{
e
}
"
)

    
    
async
 
def
 
execute_python_code
(
self
,
 code
:
 
str
)
 
-
>
 SandboxResult
:

        
"""Execute Python code in sandbox."""

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

        
        
# Write code to temp file

        temp_dir 
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
"temp"
]
)

        temp_dir
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

        
        temp_file 
=
 temp_dir 
/
 
f"sandbox_
{
id
(
code
)
}
.py"

        temp_file
.
write_text
(
code
)

        
        
try
:

            
# Run in subprocess with resource limits

            env 
=
 os
.
environ
.
copy
(
)

            env
[
"PYTHONPATH"
]
 
=
 
str
(
Path
.
cwd
(
)
)

            
            process 
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

                
str
(
temp_file
)
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
,

                env
=
env
            
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
 SandboxResult
(

                    success
=
process
.
returncode 
==
 
0
,

                    output
=
stdout
.
decode
(
)
,

                    error
=
stderr
.
decode
(
)
 
if
 process
.
returncode 
!=
 
0
 
else
 
None
,

                    execution_time
=
execution_time
,

                    memory_used
=
0
  
# Could track via psutil

                
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
 SandboxResult
(

                    success
=
False
,

                    output
=
""
,

                    error
=
f"Execution timed out after 
{
self
.
timeout
}
 seconds"
,

                    execution_time
=
self
.
timeout
,

                    memory_used
=
0

                
)

        
        
finally
:

            
# Clean up temp file

            
if
 temp_file
.
exists
(
)
:

                temp_file
.
unlink
(
)

    
    
async
 
def
 
execute_file
(
self
,
 file_path
:
 Path
,
 args
:
 List
[
str
]
 
=
 
None
)
 
-
>
 SandboxResult
:

        
"""Execute a file in sandbox."""

        
if
 
not
 self
.
_is_path_allowed
(
file_path
)
:

            
return
 SandboxResult
(

                success
=
False
,

                output
=
""
,

                error
=
f"Access to 
{
file_path
}
 is not allowed"
,

                execution_time
=
0
,

                memory_used
=
0

            
)

        
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

        
        
try
:

            cmd 
=
 
[
sys
.
executable
,
 
str
(
file_path
)
]

            
if
 args
:

                cmd
.
extend
(
args
)

            
            env 
=
 os
.
environ
.
copy
(
)

            env
[
"PYTHONPATH"
]
 
=
 
str
(
Path
.
cwd
(
)
)

            
            process 
=
 
await
 asyncio
.
create_subprocess_exec
(

                
*
cmd
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
,

                env
=
env
,

                cwd
=
str
(
file_path
.
parent
)

            
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
 SandboxResult
(

                    success
=
process
.
returncode 
==
 
0
,

                    output
=
stdout
.
decode
(
)
,

                    error
=
stderr
.
decode
(
)
 
if
 process
.
returncode 
!=
 
0
 
else
 
None
,

                    execution_time
=
execution_time
,

                    memory_used
=
0

                
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
 SandboxResult
(

                    success
=
False
,

                    output
=
""
,

                    error
=
f"Execution timed out after 
{
self
.
timeout
}
 seconds"
,

                    execution_time
=
self
.
timeout
,

                    memory_used
=
0

                
)

        
        
except
 Exception 
as
 e
:

            
return
 SandboxResult
(

                success
=
False
,

                output
=
""
,

                error
=
f"Execution error: 
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
0
,

                memory_used
=
0

            
)

    
    
def
 
_is_path_allowed
(
self
,
 path
:
 Path
)
 
-
>
 
bool
:

        
"""Check if a path is allowed for execution."""

        
if
 
not
 self
.
enabled
:

            
return
 
True

        
        
try
:

            
# Resolve to absolute path

            abs_path 
=
 path
.
resolve
(
)

            
            
# Check if path is in allowed directories

            
for
 allowed_dir 
in
 self
.
allowed_dirs
:

                
try
:

                    abs_path
.
relative_to
(
allowed_dir
.
resolve
(
)
)

                    
return
 
True

                
except
 ValueError
:

                    
continue

            
            
return
 
False

        
        
except
 Exception
:

            
return
 
False

    
    
async
 
def
 
validate_code
(
self
,
 code
:
 
str
)
 
-
>
 
bool
:

        
"""Validate code for dangerous patterns."""

        dangerous_patterns 
=
 
[

            
"import os"
,

            
"import sys"
,

            
"eval("
,

            
"exec("
,

            
"subprocess"
,

            
"__import__"
,

            
"open("
,

            
"file("
,

            
"input("
,

            
"raw_input("
,

        
]

        
        
for
 pattern 
in
 dangerous_patterns
:

            
if
 pattern 
in
 code
:

                
return
 
False

        
        
return
 
True

    
    
def
 
create_isolated_env
(
self
,
 project_path
:
 Path
)
 
-
>
 Dict
[
str
,
 
str
]
:

        
"""Create an isolated execution environment."""

        env 
=
 os
.
environ
.
copy
(
)

        
        
# Restrict environment

        env
[
"PATH"
]
 
=
 
"/usr/bin:/usr/local/bin"

        env
[
"PYTHONPATH"
]
 
=
 
str
(
project_path
)

        
        
# Remove potentially dangerous variables

        dangerous_vars 
=
 
[
"SUDO_COMMAND"
,
 
"SUDO_USER"
,
 
"SUDO_UID"
,
 
"SUDO_GID"
]

        
for
 var 
in
 dangerous_vars
:

            env
.
pop
(
var
,
 
None
)

        
        
return
 env


### execution/error_handler.py

```python

"""
Error handling module for comprehensive error management.
"""


import
 asyncio

import
 traceback

from
 datetime 
import
 datetime

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
 
ErrorReport
:

    error_id
:
 
str

    timestamp
:
 
str

    error_type
:
 
str

    message
:
 
str

    stack_trace
:
 
str

    context
:
 Dict
[
str
,
 Any
]

    severity
:
 
str

    recovery_suggestion
:
 
str




class
 
ErrorHandler
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
error_history
:
 List
[
ErrorReport
]
 
=
 
[
]

        self
.
max_history_size 
=
 
100

    
    
def
 
handle_error
(

        self
,

        error
:
 Exception
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
,

        severity
:
 
str
 
=
 
"medium"

    
)
 
-
>
 ErrorReport
:

        
"""Handle an error and generate a report."""

        error_id 
=
 
f"ERR_
{
int
(
datetime
.
now
(
)
.
timestamp
(
)
)
}
_
{
id
(
error
)
}
"

        
        
# Generate stack trace

        stack_trace 
=
 
""
.
join
(
traceback
.
format_exception
(
type
(
error
)
,
 error
,
 error
.
__traceback__
)
)

        
        
# Get error type

        error_type 
=
 
type
(
error
)
.
__name__
        
        
# Get message

        message 
=
 
str
(
error
)

        
        
# Generate recovery suggestion

        recovery_suggestion 
=
 self
.
_suggest_recovery
(
error_type
,
 message
)

        
        report 
=
 ErrorReport
(

            error_id
=
error_id
,

            timestamp
=
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

            error_type
=
error_type
,

            message
=
message
,

            stack_trace
=
stack_trace
,

            context
=
context 
or
 
{
}
,

            severity
=
severity
,

            recovery_suggestion
=
recovery_suggestion
        
)

        
        
# Store in history

        self
.
error_history
.
append
(
report
)

        
        
# Keep only recent errors

        
if
 
len
(
self
.
error_history
)
 
>
 self
.
max_history_size
:

            self
.
error_history 
=
 self
.
error_history
[
-
self
.
max_history_size
:
]

        
        
return
 report
    
    
def
 
_suggest_recovery
(
self
,
 error_type
:
 
str
,
 message
:
 
str
)
 
-
>
 
str
:

        
"""Suggest recovery action based on error type."""

        error_type 
=
 error_type
.
lower
(
)

        message 
=
 message
.
lower
(
)

        
        
if
 
"import"
 
in
 error_type 
or
 
"module"
 
in
 message
:

            
return
 
"Install missing dependencies using pip or npm"

        
elif
 
"syntax"
 
in
 error_type
:

            
return
 
"Check code syntax and fix errors before retrying"

        
elif
 
"connection"
 
in
 error_type 
or
 
"connect"
 
in
 message
:

            
return
 
"Verify database and external services are running"

        
elif
 
"permission"
 
in
 error_type 
or
 
"permission"
 
in
 message
:

            
return
 
"Check file permissions and run with appropriate privileges"

        
elif
 
"timeout"
 
in
 error_type
:

            
return
 
"Increase timeout or optimize the operation"

        
elif
 
"memory"
 
in
 error_type
:

            
return
 
"Reduce memory usage or increase available memory"

        
elif
 
"disk"
 
in
 error_type 
or
 
"space"
 
in
 message
:

            
return
 
"Free up disk space or change storage location"

        
else
:

            
return
 
"Check logs for details and retry with fixes"

    
    
async
 
def
 
handle_task_failure
(
self
,
 task
,
 error
:
 Exception
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

        
"""Handle task execution failure."""

        context 
=
 
{

            
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

            
"agent_type"
:
 task
.
agent_type
        
}

        
        report 
=
 self
.
handle_error
(
error
,
 context
,
 severity
=
"high"
)

        
        
# Log error details

        
print
(
f"Task Failed: 
{
task
.
title
}
"
)

        
print
(
f"Error: 
{
report
.
message
}
"
)

        
print
(
f"Recovery: 
{
report
.
recovery_suggestion
}
"
)

        
        
return
 
{

            
"action"
:
 
"retry_or_skip"
,

            
"retry_count"
:
 
0
,

            
"max_retries"
:
 
3
,

            
"suggestion"
:
 report
.
recovery_suggestion
        
}

    
    
def
 
get_error_stats
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

        
"""Get error statistics."""

        
if
 
not
 self
.
error_history
:

            
return
 
{

                
"total_errors"
:
 
0
,

                
"error_types"
:
 
{
}
,

                
"most_common"
:
 
None

            
}

        
        error_types 
=
 
{
}

        
        
for
 report 
in
 self
.
error_history
:

            error_type 
=
 report
.
error_type
            error_types
[
error_type
]
 
=
 error_types
.
get
(
error_type
,
 
0
)
 
+
 
1

        
        most_common 
=
 
max
(
error_types
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
)
[
0
]

        
        
return
 
{

            
"total_errors"
:
 
len
(
self
.
error_history
)
,

            
"error_types"
:
 error_types
,

            
"most_common"
:
 most_common
        
}

    
    
def
 
should_retry
(
self
,
 error
:
 Exception
,
 retry_count
:
 
int
)
 
-
>
 
bool
:

        
"""Determine if an operation should be retried."""

        
if
 retry_count 
>=
 
3
:

            
return
 
False

        
        error_type 
=
 
type
(
error
)
.
__name__
        
        
# Retryable errors

        retryable_errors 
=
 
[

            
"ConnectionError"
,

            
"TimeoutError"
,

            
"DatabaseError"
,

            
"NetworkError"

        
]

        
        
if
 error_type 
in
 retryable_errors
:

            
return
 
True

        
        
# Check error message

        
if
 
any
(
word 
in
 
str
(
error
)
.
lower
(
)
 
for
 word 
in
 
[
"timeout"
,
 
"connection"
,
 
"temporary"
]
)
:

            
return
 
True

        
        
return
 
False

    
    
def
 
classify_severity
(
self
,
 error
:
 Exception
)
 
-
>
 
str
:

        
"""Classify error severity."""

        error_type 
=
 
type
(
error
)
.
__name__
        message 
=
 
str
(
error
)
.
lower
(
)

        
        
# Critical errors

        
if
 error_type 
in
 
[
"SystemError"
,
 
"MemoryError"
,
 
"ImportError"
]
:

            
return
 
"critical"

        
        
# High severity

        
if
 
any
(
word 
in
 message 
for
 word 
in
 
[
"critical"
,
 
"fatal"
,
 
"cannot"
,
 
"unable"
]
)
:

            
return
 
"high"

        
        
# Medium severity

        
if
 
any
(
word 
in
 message 
for
 word 
in
 
[
"warning"
,
 
"failed"
,
 
"error"
]
)
:

            
return
 
"medium"

        
        
# Low severity

        
return
 
"low"



### versioning/__init__.py

```python

# Versioning package
"""
Git manager for version control operations.
"""


import
 subprocess

from
 pathlib 
import
 Path

from
 datetime 
import
 datetime

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
 
GitManager
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
 
is_git_repo
(
self
,
 path
:
 Path
)
 
-
>
 
bool
:

        
"""Check if a directory is a Git repository."""

        
try
:

            subprocess
.
run
(

                
[
"git"
,
 
"rev-parse"
,
 
"--git-dir"
]
,

                cwd
=
path
,

                check
=
True
,

                stdout
=
subprocess
.
PIPE
,

                stderr
=
subprocess
.
PIPE
            
)

            
return
 
True

        
except
 subprocess
.
CalledProcessError
:

            
return
 
False

    
    
def
 
init_repo
(
self
,
 path
:
 Path
)
 
-
>
 
bool
:

        
"""Initialize a Git repository."""

        
try
:

            subprocess
.
run
(

                
[
"git"
,
 
"init"
]
,

                cwd
=
path
,

                check
=
True
,

                stdout
=
subprocess
.
PIPE
,

                stderr
=
subprocess
.
PIPE
            
)

            
return
 
True

        
except
 subprocess
.
CalledProcessError
:

            
return
 
False

    
    
def
 
add_all
(
self
,
 path
:
 Path
)
 
-
>
 
bool
:

        
"""Add all files to staging."""

        
try
:

            subprocess
.
run
(

                
[
"git"
,
 
"add"
,
 
"."
]
,

                cwd
=
path
,

                check
=
True
,

                stdout
=
subprocess
.
PIPE
,

                stderr
=
subprocess
.
PIPE
            
)

            
return
 
True

        
except
 subprocess
.
CalledProcessError
:

            
return
 
False

    
    
def
 
commit
(
self
,
 path
:
 Path
,
 message
:
 
str
)
 
-
>
 
bool
:

        
"""Create a commit."""

        
try
:

            subprocess
.
run
(

                
[
"git"
,
 
"commit"
,
 
"-m"
,
 message
]
,

                cwd
=
path
,

                check
=
True
,

                stdout
=
subprocess
.
PIPE
,

                stderr
=
subprocess
.
PIPE
            
)

            
return
 
True

        
except
 subprocess
.
CalledProcessError
:

            
return
 
False

    
    
def
 
get_status
(
self
,
 path
:
 Path
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

        
"""Get Git status."""

        
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
 
"status"
,
 
"--porcelain"
]
,

                cwd
=
path
,

                capture_output
=
True
,

                text
=
True
,

                check
=
True

            
)

            
            status_lines 
=
 result
.
stdout
.
strip
(
)
.
split
(
"\\n"
)
 
if
 result
.
stdout
.
strip
(
)
 
else
 
[
]

            staged 
=
 
[
]

            unstaged 
=
 
[
]

            
            
for
 line 
in
 status_lines
:

                
if
 line
:

                    status 
=
 line
[
:
2
]

                    filename 
=
 line
[
3
:
]

                    
                    
if
 status
[
0
]
 
in
 
"MADRC"
:

                        staged
.
append
(
filename
)

                    
if
 status
[
1
]
 
in
 
"MD"
:

                        unstaged
.
append
(
filename
)

            
            
return
 
{

                
"is_clean"
:
 
len
(
staged
)
 
==
 
0
 
and
 
len
(
unstaged
)
 
==
 
0
,

                
"staged"
:
 staged
,

                
"unstaged"
:
 unstaged
,

                
"branch"
:
 self
.
get_current_branch
(
path
)

            
}

        
        
except
 subprocess
.
CalledProcessError
:

            
return
 
{

                
"is_clean"
:
 
True
,

                
"staged"
:
 
[
]
,

                
"unstaged"
:
 
[
]
,

                
"branch"
:
 
"unknown"

            
}

    
    
def
 
get_current_branch
(
self
,
 path
:
 Path
)
 
-
>
 
str
:

        
"""Get current Git branch."""

        
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
 
"rev-parse"
,
 
"--abbrev-ref"
,
 
"HEAD"
]
,

                cwd
=
path
,

                capture_output
=
True
,

                text
=
True
,

                check
=
True

            
)

            
return
 result
.
stdout
.
strip
(
)

        
except
 subprocess
.
CalledProcessError
:

            
return
 
"unknown"

    
    
def
 
create_branch
(
self
,
 path
:
 Path
,
 branch_name
:
 
str
)
 
-
>
 
bool
:

        
"""Create and switch to a new branch."""

        
try
:

            subprocess
.
run
(

                
[
"git"
,
 
"checkout"
,
 
"-b"
,
 branch_name
]
,

                cwd
=
path
,

                check
=
True
,

                stdout
=
subprocess
.
PIPE
,

                stderr
=
subprocess
.
PIPE
            
)

            
return
 
True

        
except
 subprocess
.
CalledProcessError
:

            
return
 
False

    
    
def
 
switch_branch
(
self
,
 path
:
 Path
,
 branch_name
:
 
str
)
 
-
>
 
bool
:

        
"""Switch to an existing branch."""

        
try
:

            subprocess
.
run
(

                
[
"git"
,
 
"checkout"
,
 branch_name
]
,

                cwd
=
path
,

                check
=
True
,

                stdout
=
subprocess
.
PIPE
,

                stderr
=
subprocess
.
PIPE
            
)

            
return
 
True

        
except
 subprocess
.
CalledProcessError
:

            
return
 
False

    
    
def
 
get_commit_history
(
self
,
 path
:
 Path
,
 limit
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

        
"""Get recent commit history."""

        
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
 
"log"
,
 
f"-
{
limit
}
"
,
 
"--pretty=format:%h|%an|%ae|%s|%cd"
,
 
"--date=iso"
]
,

                cwd
=
path
,

                capture_output
=
True
,

                text
=
True
,

                check
=
True

            
)

            
            commits 
=
 
[
]

            
for
 line 
in
 result
.
stdout
.
strip
(
)
.
split
(
"\\n"
)
:

                
if
 line
:

                    parts 
=
 line
.
split
(
"|"
,
 
4
)

                    
if
 
len
(
parts
)
 
==
 
5
:

                        commits
.
append
(
{

                            
"hash"
:
 parts
[
0
]
,

                            
"author"
:
 parts
[
1
]
,

                            
"email"
:
 parts
[
2
]
,

                            
"message"
:
 parts
[
3
]
,

                            
"date"
:
 parts
[
4
]

                        
}
)

            
            
return
 commits
        
        
except
 subprocess
.
CalledProcessError
:

            
return
 
[
]

    
    
def
 
commit_with_message
(
self
,
 path
:
 Path
,
 changes
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

        
"""Auto-generate commit message based on changes."""

        
if
 
not
 changes
:

            
return
 
False

        
        
# Generate commit message

        message 
=
 self
.
_generate_commit_message
(
changes
)

        
        
return
 self
.
commit
(
path
,
 message
)

    
    
def
 
_generate_commit_message
(
self
,
 changes
:
 List
[
str
]
)
 
-
>
 
str
:

        
"""Generate a commit message based on changes."""

        
if
 
len
(
changes
)
 
==
 
1
:

            
return
 
f"feat: add 
{
changes
[
0
]
}
"

        
elif
 
any
(
"auth"
 
in
 c 
for
 c 
in
 changes
)
:

            
return
 
"feat: implement authentication system"

        
elif
 
any
(
"api"
 
in
 c 
for
 c 
in
 changes
)
:

            
return
 
"feat: add API endpoints"

        
elif
 
any
(
"ui"
 
in
 c 
for
 c 
in
 changes
)
:

            
return
 
"feat: build UI components"

        
else
:

            
return
 
f"feat: update 
{
len
(
changes
)
}
 components"

    
    
def
 
revert_last_commit
(
self
,
 path
:
 Path
)
 
-
>
 
bool
:

        
"""Revert the last commit."""

        
try
:

            subprocess
.
run
(

                
[
"git"
,
 
"reset"
,
 
"--soft"
,
 
"HEAD~1"
]
,

                cwd
=
path
,

                check
=
True
,

                stdout
=
subprocess
.
PIPE
,

                stderr
=
subprocess
.
PIPE
            
)

            
return
 
True

        
except
 subprocess
.
CalledProcessError
:

            
return
 
False

    
    
def
 
get_diff
(
self
,
 path
:
 Path
)
 
-
>
 
str
:

        
"""Get diff of uncommitted changes."""

        
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
 
"diff"
]
,

                cwd
=
path
,

                capture_output
=
True
,

                text
=
True
,

                check
=
True

            
)

            
return
 result
.
stdout
        
except
 subprocess
.
CalledProcessError
:

            
return
 
""

    
    
def
 
create_tag
(
self
,
 path
:
 Path
,
 tag_name
:
 
str
,
 message
:
 
str
 
=
 
None
)
 
-
>
 
bool
:

        
"""Create a Git tag."""

        
try
:

            
if
 message
:

                cmd 
=
 
[
"git"
,
 
"tag"
,
 
"-a"
,
 tag_name
,
 
"-m"
,
 message
]

            
else
:

                cmd 
=
 
[
"git"
,
 
"tag"
,
 tag_name
]

            
            subprocess
.
run
(

                cmd
,

                cwd
=
path
,

                check
=
True
,

                stdout
=
subprocess
.
PIPE
,

                stderr
=
subprocess
.
PIPE
            
)

            
return
 
True

        
except
 subprocess
.
CalledProcessError
:

            
return
 
False



### versioning/diff_engine.py

```python

"""
Diff engine for intelligent file comparison and merging.
"""


import
 difflib

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
 
DiffEngine
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
 
compare_files
(
self
,
 old_file
:
 Path
,
 new_file
:
 Path
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

        
"""Compare two files and return differences."""

        
if
 
not
 old_file
.
exists
(
)
:

            
return
 
{

                
"status"
:
 
"new_file"
,

                
"diff"
:
 
[
]
,

                
"stats"
:
 
{
"added"
:
 
0
,
 
"removed"
:
 
0
,
 
"modified"
:
 
0
}

            
}

        
        old_content 
=
 old_file
.
read_text
(
)
.
splitlines
(
)

        new_content 
=
 new_file
.
read_text
(
)
.
splitlines
(
)

        
        
return
 self
.
compare_content
(
old_content
,
 new_content
,
 old_file
.
name
)

    
    
def
 
compare_content
(

        self
,

        old_content
:
 List
[
str
]
,

        new_content
:
 List
[
str
]
,

        filename
:
 
str
 
=
 
"file"

    
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

        
"""Compare two content lists."""

        diff 
=
 
list
(
difflib
.
unified_diff
(

            old_content
,

            new_content
,

            fromfile
=
f"
{
filename
}
.old"
,

            tofile
=
f"
{
filename
}
.new"
,

            lineterm
=
""

        
)
)

        
        
# Calculate stats

        added 
=
 
sum
(
1
 
for
 line 
in
 diff 
if
 line
.
startswith
(
"+"
)
 
and
 
not
 line
.
startswith
(
"+++"
)
)

        removed 
=
 
sum
(
1
 
for
 line 
in
 diff 
if
 line
.
startswith
(
"-"
)
 
and
 
not
 line
.
startswith
(
"---"
)
)

        
        
return
 
{

            
"status"
:
 
"modified"
 
if
 diff 
else
 
"unchanged"
,

            
"diff"
:
 diff
,

            
"stats"
:
 
{

                
"added"
:
 added
,

                
"removed"
:
 removed
,

                
"modified"
:
 
max
(
added
,
 removed
)

            
}

        
}

    
    
def
 
apply_diff
(
self
,
 original_file
:
 Path
,
 diff
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

        
"""Apply a diff to a file."""

        
if
 
not
 original_file
.
exists
(
)
:

            
return
 
False

        
        original_content 
=
 original_file
.
read_text
(
)
.
splitlines
(
)

        
        
# Parse diff

        new_content 
=
 self
.
_apply_diff_to_content
(
original_content
,
 diff
)

        
        
if
 new_content 
is
 
None
:

            
return
 
False

        
        
# Write back

        original_file
.
write_text
(
"\n"
.
join
(
new_content
)
)

        
return
 
True

    
    
def
 
_apply_diff_to_content
(

        self
,

        original
:
 List
[
str
]
,

        diff
:
 List
[
str
]

    
)
 
-
>
 Optional
[
List
[
str
]
]
:

        
"""Apply diff to content."""

        
try
:

            
# Simple line-based application (doesn't handle all cases)

            result 
=
 original
.
copy
(
)

            line_num 
=
 
0

            
            
for
 diff_line 
in
 diff
:

                
if
 diff_line
.
startswith
(
"@@"
)
:

                    
# Parse line numbers

                    parts 
=
 diff_line
.
split
(
" "
)

                    new_range 
=
 parts
[
1
]

                    start_line 
=
 
int
(
new_range
.
split
(
","
)
[
0
]
[
1
:
]
)
 
-
 
1

                    line_num 
=
 start_line
                
                
elif
 diff_line
.
startswith
(
"+"
)
:

                    
# Add line

                    result
.
insert
(
line_num
,
 diff_line
[
1
:
]
)

                    line_num 
+=
 
1

                
                
elif
 diff_line
.
startswith
(
"-"
)
:

                    
# Remove line

                    
if
 line_num 
<
 
len
(
result
)
:

                        
del
 result
[
line_num
]

            
            
return
 result
        
        
except
 Exception
:

            
return
 
None

    
    
def
 
merge_files
(

        self
,

        base_file
:
 Path
,

        our_file
:
 Path
,

        their_file
:
 Path
    
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

        
"""Three-way merge of files."""

        
if
 
not
 base_file
.
exists
(
)
:

            
return
 
{

                
"success"
:
 
False
,

                
"conflicts"
:
 
[
]
,

                
"merged_content"
:
 
None

            
}

        
        base_content 
=
 base_file
.
read_text
(
)
.
splitlines
(
)

        our_content 
=
 our_file
.
read_text
(
)
.
splitlines
(
)

        their_content 
=
 their_file
.
read_text
(
)
.
splitlines
(
)

        
        
return
 self
.
merge_content
(
base_content
,
 our_content
,
 their_content
)

    
    
def
 
merge_content
(

        self
,

        base
:
 List
[
str
]
,

        ours
:
 List
[
str
]
,

        theirs
:
 List
[
str
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

        
"""Three-way merge of content."""

        merger 
=
 difflib
.
Differ
(
)

        
        
# Get differences

        our_diff 
=
 
list
(
merger
.
compare
(
base
,
 ours
)
)

        their_diff 
=
 
list
(
merger
.
compare
(
base
,
 theirs
)
)

        
        
# Simple merge strategy

        merged 
=
 base
.
copy
(
)

        conflicts 
=
 
[
]

        
        
for
 i
,
 
(
our_line
,
 their_line
)
 
in
 
enumerate
(
zip
(
our_diff
,
 their_diff
)
)
:

            
if
 our_line
.
startswith
(
"  "
)
 
and
 their_line
.
startswith
(
"  "
)
:

                
# No changes

                
continue

            
            
elif
 our_line
.
startswith
(
"+ "
)
 
and
 their_line
.
startswith
(
"+ "
)
:

                
# Both added (same line)

                
if
 our_line 
==
 their_line
:

                    merged
.
append
(
our_line
[
2
:
]
)

                
else
:

                    
# Conflict

                    conflicts
.
append
(
{

                        
"line"
:
 i
,

                        
"ours"
:
 our_line
[
2
:
]
,

                        
"theirs"
:
 their_line
[
2
:
]
,

                        
"base"
:
 base
[
i
]
 
if
 i 
<
 
len
(
base
)
 
else
 
""

                    
}
)

            
            
elif
 our_line
.
startswith
(
"+ "
)
:

                
# Only we added

                merged
.
append
(
our_line
[
2
:
]
)

            
            
elif
 their_line
.
startswith
(
"+ "
)
:

                
# Only they added

                merged
.
append
(
their_line
[
2
:
]
)

            
            
elif
 our_line
.
startswith
(
"- "
)
 
and
 their_line
.
startswith
(
"- "
)
:

                
# Both removed

                
if
 i 
<
 
len
(
merged
)
:

                    
del
 merged
[
i
]

        
        
return
 
{

            
"success"
:
 
len
(
conflicts
)
 
==
 
0
,

            
"conflicts"
:
 conflicts
,

            
"merged_content"
:
 merged 
if
 
len
(
conflicts
)
 
==
 
0
 
else
 
None

        
}

    
    
def
 
generate_merge_conflict_markers
(

        self
,

        base
:
 List
[
str
]
,

        ours
:
 List
[
str
]
,

        theirs
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
str
]
:

        
"""Generate merge conflict markers."""

        result 
=
 
[
]

        in_conflict 
=
 
False

        
        
for
 i 
in
 
range
(
max
(
len
(
base
)
,
 
len
(
ours
)
,
 
len
(
theirs
)
)
)
:

            base_line 
=
 base
[
i
]
 
if
 i 
<
 
len
(
base
)
 
else
 
None

            our_line 
=
 ours
[
i
]
 
if
 i 
<
 
len
(
ours
)
 
else
 
None

            their_line 
=
 theirs
[
i
]
 
if
 i 
<
 
len
(
theirs
)
 
else
 
None

            
            
if
 our_line 
==
 their_line
:

                
# No conflict

                
if
 in_conflict
:

                    result
.
append
(
">>>>>>> theirs"
)

                    in_conflict 
=
 
False

                result
.
append
(
our_line 
or
 
""
)

            
            
elif
 base_line 
==
 our_line 
and
 base_line 
!=
 their_line
:

                
# Their change

                
if
 
not
 in_conflict
:

                    result
.
append
(
"<<<<<<< ours"
)

                    in_conflict 
=
 
True

                result
.
append
(
their_line 
or
 
""
)

            
            
elif
 base_line 
==
 their_line 
and
 base_line 
!=
 our_line
:

                
# Our change

                
if
 
not
 in_conflict
:

                    result
.
append
(
"<<<<<<< ours"
)

                    in_conflict 
=
 
True

                result
.
append
(
our_line 
or
 
""
)

            
            
else
:

                
# Both changed

                
if
 
not
 in_conflict
:

                    result
.
append
(
"<<<<<<< ours"
)

                    in_conflict 
=
 
True

                result
.
append
(
our_line 
or
 
""
)

                result
.
append
(
"======="
)

                result
.
append
(
their_line 
or
 
""
)

        
        
if
 in_conflict
:

            result
.
append
(
">>>>>>> theirs"
)

        
        
return
 result
    
    
def
 
intelligent_diff
(
self
,
 old
:
 
str
,
 new
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

        
"""Generate intelligent diff with context."""

        old_lines 
=
 old
.
splitlines
(
)

        new_lines 
=
 new
.
splitlines
(
)

        
        
# Find changes

        diff 
=
 difflib
.
SequenceMatcher
(
None
,
 old_lines
,
 new_lines
)

        
        changes 
=
 
[
]

        
        
for
 tag
,
 i1
,
 i2
,
 j1
,
 j2 
in
 diff
.
get_opcodes
(
)
:

            
if
 tag 
==
 
"replace"
:

                changes
.
append
(
{

                    
"type"
:
 
"modified"
,

                    
"old_lines"
:
 old_lines
[
i1
:
i2
]
,

                    
"new_lines"
:
 new_lines
[
j1
:
j2
]
,

                    
"old_start"
:
 i1
,

                    
"new_start"
:
 j1
                
}
)

            
elif
 tag 
==
 
"delete"
:

                changes
.
append
(
{

                    
"type"
:
 
"removed"
,

                    
"lines"
:
 old_lines
[
i1
:
i2
]
,

                    
"start"
:
 i1
                
}
)

            
elif
 tag 
==
 
"insert"
:

                changes
.
append
(
{

                    
"type"
:
 
"added"
,

                    
"lines"
:
 new_lines
[
j1
:
j2
]
,

                    
"start"
:
 j1
                
}
)

        
        
return
 
{

            
"changes"
:
 changes
,

            
"total_changes"
:
 
len
(
changes
)
,

            
"old_line_count"
:
 
len
(
old_lines
)
,

            
"new_line_count"
:
 
len
(
new_lines
)

        
}



### interface/cli.py

```python

"""
CLI interface for the autonomous AI system.
"""


import
 asyncio

import
 argparse

from
 pathlib 
import
 Path

from
 typing 
import
 Optional
,
 Dict
,
 Any


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
        
        
print
(
"="
 
*
 
60
)

        
print
(
"Autonomous AI Web Developer"
)

        
print
(
"="
 
*
 
60
)

        
print
(
"Type 'help' for commands or 'exit' to quit"
)

        
print
(
"="
 
*
 
60
)

        
        
while
 
True
:

            
try
:

                command 
=
 
input
(
"\nAI> "
)
.
strip
(
)

                
                
if
 command
.
lower
(
)
 
in
 
[
"exit"
,
 
"quit"
]
:

                    
print
(
"Shutting down..."
)

                    
await
 brain
.
shutdown
(
)

                    
break

                
                
elif
 command
.
lower
(
)
 
==
 
"help"
:

                    self
.
_show_help
(
)

                
                
elif
 command
.
lower
(
)
 
==
 
"status"
:

                    
await
 self
.
_show_status
(
)

                
                
elif
 command
.
startswith
(
"create"
)
:

                    
await
 self
.
_handle_create
(
command
)

                
                
elif
 command
.
startswith
(
"list"
)
:

                    
await
 self
.
_handle_list
(
)

                
                
elif
 command
.
startswith
(
"start"
)
:

                    
await
 self
.
_handle_start
(
)

                
                
elif
 command
.
lower
(
)
 
==
 
"pause"
:

                    
await
 self
.
_handle_pause
(
)

                
                
elif
 command
.
lower
(
)
 
==
 
"resume"
:

                    
await
 self
.
_handle_resume
(
)

                
                
elif
 command
.
startswith
(
"cancel"
)
:

                    
await
 self
.
_handle_cancel
(
command
)

                
                
elif
 command
.
startswith
(
"show"
)
:

                    
await
 self
.
_handle_show
(
command
)

                
                
elif
 command
.
startswith
(
"config"
)
:

                    self
.
_handle_config
(
command
)

                
                
else
:

                    
print
(
"Unknown command. Type 'help' for available commands."
)

            
            
except
 KeyboardInterrupt
:

                
print
(
"\\nUse 'exit' to quit"
)

            
except
 Exception 
as
 e
:

                
print
(
f"Error: 
{
e
}
"
)

    
    
def
 
_show_help
(
self
)
:

        
"""Show available commands."""

        
print
(
"""
Available Commands:
  create <description>     Create a new development goal
  list                     List all goals
  start                    Start autonomous execution
  pause                    Pause current execution
  resume                   Resume paused execution
  cancel <goal_id>         Cancel a specific goal
  show <goal_id>           Show goal details
  status                   Show system status
  config                   Show configuration
  help                     Show this help
  exit/quit                Exit the application
"""
)

    
    
async
 
def
 
_show_status
(
self
)
:

        
"""Show system status."""

        
if
 
not
 self
.
brain 
or
 
not
 self
.
goal_manager
:

            
print
(
"System not initialized"
)

            
return

        
        
# Brain status

        
print
(
f"Brain State: 
{
self
.
brain
.
state
.
value
}
"
)

        
print
(
f"Current Goal: 
{
self
.
brain
.
current_goal_id 
or
 
'None'
}
"
)

        
        
# Agent status

        
if
 
hasattr
(
self
.
brain
,
 
'manager_agent'
)
:

            agent_status 
=
 self
.
brain
.
manager_agent
.
get_agent_status
(
)

            
print
(
"\\nAgent Status:"
)

            
for
 agent
,
 status 
in
 agent_status
.
items
(
)
:

                
print
(
f"  
{
agent
}
: 
{
status
}
"
)

        
        
# Pending goals

        pending 
=
 self
.
goal_manager
.
get_pending_goals
(
)

        
print
(
f"\\nPending Goals: 
{
len
(
pending
)
}
"
)

        
        
if
 pending
:

            
print
(
"Top 3 priorities:"
)

            
for
 goal 
in
 pending
[
:
3
]
:

                
print
(
f"  - 
{
goal
.
title
}
 (Priority: 
{
goal
.
priority
}
)"
)

        
        
# Recent memory

        recent 
=
 
await
 self
.
brain
.
short_term_memory
.
get_recent
(
3
)

        
if
 recent
:

            
print
(
"\\nRecent Activity:"
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
}
"
)

    
    
async
 
def
 
_handle_create
(
self
,
 command
:
 
str
)
:

        
"""Handle create goal command."""

        parts 
=
 command
.
split
(
" "
,
 
1
)

        
if
 
len
(
parts
)
 
<
 
2
:

            
print
(
"Error: Please provide a goal description"
)

            
print
(
"Usage: create <description>"
)

            
return

        
        description 
=
 parts
[
1
]

        
        
# Ask for priority

        
try
:

            priority_input 
=
 
input
(
"Priority (1.0-10.0, default 5.0): "
)
.
strip
(
)

            priority 
=
 
float
(
priority_input
)
 
if
 priority_input 
else
 
5.0

        
except
 ValueError
:

            
print
(
"Invalid priority, using default 5.0"
)

            priority 
=
 
5.0

        
        
# Ask for project name

        project_name 
=
 
input
(
"Project name (optional): "
)
.
strip
(
)

        
        context 
=
 
{
}

        
if
 project_name
:

            context
[
"project_name"
]
 
=
 project_name
        
        
# Create goal

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
=
description
[
:
50
]
 
+
 
"..."
 
if
 
len
(
description
)
 
>
 
50
 
else
 description
,

            description
=
description
,

            priority
=
priority
,

            context
=
context
        
)

        
        
print
(
f"Goal created successfully!"
)

        
print
(
f"Goal ID: 
{
goal_id
}
"
)

        
        
# Offer to start immediately

        start_now 
=
 
input
(
"Start working on this goal now? (y/n): "
)
.
strip
(
)
.
lower
(
)

        
if
 start_now 
==
 
"y"
:

            
await
 self
.
_handle_start
(
)

    
    
async
 
def
 
_handle_list
(
self
)
:

        
"""Handle list goals command."""

        goals 
=
 self
.
goal_manager
.
goals
        
        
if
 
not
 goals
:

            
print
(
"No goals found"
)

            
return

        
        
print
(
f"\\nTotal Goals: 
{
len
(
goals
)
}
"
)

        
print
(
"-"
 
*
 
60
)

        
        
for
 goal_id
,
 goal 
in
 goals
.
items
(
)
:

            status_icon 
=
 
{

                
"pending"
:
 
"⏳"
,

                
"executing"
:
 
"🚀"
,

                
"completed"
:
 
"✅"
,

                
"failed"
:
 
"❌"
,

                
"paused"
:
 
"⏸️"

            
}
.
get
(
goal
.
status
.
value
,
 
"❓"
)

            
            
print
(
f"
{
status_icon
}
 
{
goal_id
[
:
8]
}
 | 
{
goal
.
title
[
:
40]
}
"
)

            
print
(
f"   Priority: 
{
goal
.
priority
}
 | Status: 
{
goal
.
status
.
value
}
"
)

            
            
if
 goal
.
progress_percentage 
>
 
0
:

                
print
(
f"   Progress: 
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
"-"
 
*
 
40
)

    
    
async
 
def
 
_handle_start
(
self
)
:

        
"""Handle start execution command."""

        
if
 self
.
brain
.
state
.
value 
==
 
"executing"
:

            
print
(
"Already executing. Use 'pause' to stop."
)

            
return

        
        
print
(
"Starting autonomous execution..."
)

        asyncio
.
create_task
(
self
.
_run_autonomous_loop
(
)
)

    
    
async
 
def
 
_run_autonomous_loop
(
self
)
:

        
"""Run autonomous execution in background."""

        
while
 
True
:

            
try
:

                
await
 self
.
brain
.
think_and_act
(
)

                
await
 asyncio
.
sleep
(
1
)

            
except
 KeyboardInterrupt
:

                
break

            
except
 Exception 
as
 e
:

                
print
(
f"Error in autonomous loop: 
{
e
}
"
)

                
await
 asyncio
.
sleep
(
5
)
  
# Wait before retry

    
    
async
 
def
 
_handle_pause
(
self
)
:

        
"""Handle pause command."""

        
if
 self
.
brain
.
state
.
value 
!=
 
"executing"
:

            
print
(
"Not currently executing"
)

            
return

        
        
# This would pause the current goal

        
if
 self
.
brain
.
current_goal_id
:

            
await
 self
.
goal_manager
.
pause_goal
(
self
.
brain
.
current_goal_id
)

            
print
(
"Execution paused"
)

        
else
:

            
print
(
"No active goal to pause"
)

    
    
async
 
def
 
_handle_resume
(
self
)
:

        
"""Handle resume command."""

        paused_goals 
=
 
[

            g 
for
 g 
in
 self
.
goal_manager
.
goals
.
values
(
)

            
if
 g
.
status
.
value 
==
 
"paused"

        
]

        
        
if
 
not
 paused_goals
:

            
print
(
"No paused goals to resume"
)

            
return

        
        
if
 
len
(
paused_goals
)
 
==
 
1
:

            goal 
=
 paused_goals
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
goal
.
goal_id
)

            
print
(
f"Resumed goal: 
{
goal
.
title
}
"
)

        
else
:

            
print
(
"Multiple paused goals:"
)

            
for
 i
,
 goal 
in
 
enumerate
(
paused_goals
)
:

                
print
(
f"  
{
i
+
1
}
. 
{
goal
.
title
}
"
)

            
            choice 
=
 
input
(
"Select goal to resume (number): "
)
.
strip
(
)

            
try
:

                choice_idx 
=
 
int
(
choice
)
 
-
 
1

                
if
 
0
 
<=
 choice_idx 
<
 
len
(
paused_goals
)
:

                    goal 
=
 paused_goals
[
choice_idx
]

                    
await
 self
.
goal_manager
.
resume_goal
(
goal
.
goal_id
)

                    
print
(
f"Resumed goal: 
{
goal
.
title
}
"
)

                
else
:

                    
print
(
"Invalid selection"
)

            
except
 ValueError
:

                
print
(
"Invalid input"
)

    
    
async
 
def
 
_handle_cancel
(
self
,
 command
:
 
str
)
:

        
"""Handle cancel goal command."""

        parts 
=
 command
.
split
(
)

        
if
 
len
(
parts
)
 
<
 
2
:

            
print
(
"Error: Please provide a goal ID"
)

            
print
(
"Usage: cancel <goal_id>"
)

            
return

        
        goal_id 
=
 parts
[
1
]

        
        
# Confirm cancellation

        confirm 
=
 
input
(
f"Cancel goal 
{
goal_id
}
? This cannot be undone. (y/n): "
)
.
strip
(
)
.
lower
(
)

        
if
 confirm 
!=
 
"y"
:

            
print
(
"Cancellation aborted"
)

            
return

        
        
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
f"Goal 
{
goal_id
}
 cancelled"
)

    
    
async
 
def
 
_handle_show
(
self
,
 command
:
 
str
)
:

        
"""Handle show goal details command."""

        parts 
=
 command
.
split
(
)

        
if
 
len
(
parts
)
 
<
 
2
:

            
print
(
"Error: Please provide a goal ID"
)

            
print
(
"Usage: show <goal_id>"
)

            
return

        
        goal_id 
=
 parts
[
1
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
f"Goal 
{
goal_id
}
 not found"
)

            
return

        
        
print
(
f"\\nGoal Details: 
{
goal_id
}
"
)

        
print
(
"-"
 
*
 
40
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
description
:

            
print
(
f"\\nDescription:"
)

            
print
(
goal
.
description
)

        
        
if
 goal
.
plan
:

            
print
(
f"\\nTasks (
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
):"
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
 
{

                    
"pending"
:
 
"⏳"
,

                    
"in_progress"
:
 
"🔄"
,

                    
"completed"
:
 
"✅"
,

                    
"failed"
:
 
"❌"

                
}
.
get
(
task
.
status
,
 
"❓"
)

                
                
print
(
f"  
{
status_icon
}
 
{
task
.
title
}
"
)

                
print
(
f"     Agent: 
{
task
.
agent_type
}
 | Priority: 
{
task
.
priority
}
"
)

                
                
if
 task
.
result
:

                    
print
(
f"     Files: 
{
len
(
task
.
result
.
get
(
'files_generated'
,
 
[
]
)
)
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
f"\\nRequirements:"
)

            req 
=
 goal
.
analyzed_requirements
            
print
(
f"  Features: 
{
len
(
req
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
f"  Tech Stack: {req.get('tech_stack', {}).get('backend', 'Not set')}"
)

    
    
def
 
_handle_config
(
self
,
 command
:
 
str
)
:

        
"""Handle config command."""

        parts 
=
 command
.
split
(
)

        
        
if
 
len
(
parts
)
 
==
 
1
:

            
# Show config

            
print
(
"Configuration:"
)

            
print
(
"-"
 
*
 
40
)

            
for
 key
,
 value 
in
 self
.
config
.
items
(
)
:

                
if
 
isinstance
(
value
,
 
dict
)
:

                    
print
(
f"
{
key
}
:"
)

                    
for
 k
,
 v 
in
 value
.
items
(
)
:

                        
print
(
f"  
{
k
}
: 
{
v
}
"
)

                
else
:

                    
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
"Config modification not yet implemented"
)

            
print
(
"Usage: config (shows current config)"
)



async
 
def
 
main
(
)
:

    
"""CLI entry point."""

    
# This would be called from main.py

    
pass



### interface/dashboard.py

```python

"""
Web dashboard interface (optional, for future enhancement).
"""


# This is a placeholder for a future web dashboard


# Implementation would use FastAPI/Flask to provide a web interface


# For now, CLI is the primary interface



print
(
"Web dashboard module - placeholder for future implementation"
)


# Would include:


# - FastAPI app


# - WebSocket for real-time updates


# - HTML/CSS/JS frontend


# - Goal management UI


# - Code editor integration


# - Logs and metrics visualization



# Not implemented as per requirements (CLI is mandatory, dashboard is optional)
#!/usr/bin/env python3


"""
Setup script for AutonomousAI Web Developer
"""



from
 setuptools 
import
 setup
,
 find_packages

setup
(

    name
=
"autonomous-ai-web-developer"
,

    version
=
"1.0.0"
,

    description
=
"An autonomous AI system for full-stack web development"
,

    packages
=
find_packages
(
)
,

    install_requires
=
[

        
"fastapi>=0.100.0"
,

        
"uvicorn>=0.20.0"
,

        
"sqlalchemy>=2.0.0"
,

        
"pydantic>=2.0.0"
,

        
"jose>=3.3.0"
,

        
"passlib>=1.7.0"
,

        
"pytest>=7.0.0"
,

        
"PyYAML>=6.0"
,

        
"psutil>=5.8.0"
,

        
"requests>=2.28.0"
,

        
"aiohttp>=3.8.0"
,

        
"python-dotenv>=1.0.0"
,

        
"redis>=4.0.0"
,

    
]
,

    extras_require
=
{

        
"dev"
:
 
[

            
"pylint>=2.17.0"
,

            
"bandit>=1.7.0"
,

            
"black>=23.0.0"
,

        
]
,

        
"playwright"
:
 
[

            
"playwright>=1.35.0"
,

        
]
,

        
"mongodb"
:
 
[

            
"mongoengine>=0.27.0"
,

        
]
,

    
}
,

    python_requires
=
">=3.8"
,

    entry_points
=
{

        
"console_scripts"
:
 
[

            
"autonomous-ai=main:main"
,

        
]
,

    
}
,

    classifiers
=
[

        
"Development Status :: 4 - Beta"
,

        
"Intended Audience :: Developers"
,

        
"License :: OSI Approved :: MIT License"
,

        
"Programming Language :: Python :: 3"
,

        
"Programming Language :: Python :: 3.8"
,

        
"Programming Language :: Python :: 3.9"
,

        
"Programming Language :: Python :: 3.10"
,

        
"Programming Language :: Python :: 3.11"
,

    
]
,


)
#!/usr/bin/env python3


"""
Simple launcher for the Autonomous AI Web Developer
"""



import
 sys

import
 subprocess


def
 
main
(
)
:

    
"""Run the main application."""

    
try
:

        subprocess
.
run
(
[
sys
.
executable
,
 
"main.py"
]
 
+
 sys
.
argv
[
1
:
]
,
 check
=
True
)

    
except
 KeyboardInterrupt
:

        
print
(
"\n\nOperation cancelled by user"
)

        sys
.
exit
(
0
)

    
except
 subprocess
.
CalledProcessError 
as
 e
:

        
print
(
f"\nError: Application exited with code 
{
e
.
returncode
}
"
)

        sys
.
exit
(
e
.
returncode
)



if
 __name__ 
==
 
"__main__"
:

    main
(
)
# Minimal required packages

fastapi
>=
0.100
.0

uvicorn
>=
0.20
.0

sqlalchemy
>=
2.0
.0

pydantic
>=
2.0
.0

python
-
jose
[
cryptography
]
>=
3.3
.0

passlib
>=
1.7
.0

pytest
>=
7.0
.0

PyYAML
>=
6.0

psutil
>=
5.8
.0

requests
>=
2.28
.0

aiohttp
>=
3.8
.0

python
-
dotenv
>=
1.0
.0

redis
>=
4.0
.0
# Autonomous AI Web Developer


An autonomous full
-
stack AI system that can independently develop web applications 
from
 vague human ideas
.



## Features



-
 🤖 
**
Autonomous Decision Making
**
:
 AI brain decides 
next
 actions based on context

-
 🎯 
**
Goal Management
**
:
 Multi
-
goal tracking 
with
 priority 
and
 progress

-
 📋 
**
Requirement Interpretation
**
:
 Converts vague ideas into technical specs

-
 📐 
**
Architecture Design
**
:
 Designs full
-
stack architecture

-
 🎨 
**
Frontend Generation
**
:
 Creates React
/
Next
.
js components

-
 ⚙️ 
**
Backend Generation
**
:
 Builds FastAPI
/
Flask APIs

-
 🗄️ 
**
Database Design
**
:
 SQL 
and
 NoSQL schema generation

-
 🔐 
**
Auth Integration
**
:
 JWT 
and
 OAuth authentication

-
 🧪 
**
Testing Suite
**
:
 Automated unit
,
 integration
,
 
and
 UI tests

-
 🔍 
**
Code Review
**
:
 Static analysis 
and
 quality scoring

-
 🧠 
**
Learning System
**
:
 Memory 
and
 experience
-
based improvement

-
 🛡️ 
**
Safe Execution
**
:
 Sandboxed code execution

-
 📊 
**
Metrics 
&
 Analytics
**
:
 Performance tracking 
and
 self
-
scoring


## Quick Start



### Installation


```bash
git clone 
<
repository
>

cd autonomous
-
ai
-
web
-
developer
pip install 
-
r requirements
.
txt
# Interactive CLI mode

python main.py 
--mode
 cli


# Autonomous mode

python main.py 
--mode
 autonomous


# With custom config

python main.py 
--config
 custom-config.yaml
AI> create Build a task management app with user authentication
Priority: 5.0
Project name: taskmaster
.
├── main.py                      # Entry point
├── config/
│   └── config.yaml             # Configuration
├── core/                       # Core engines
│   ├── ai_brain.py
│   ├── goal_manager.py
│   ├── requirement_engine.py
│   ├── planner.py
│   ├── reflection_engine.py
│   ├── code_quality_engine.py
│   ├── metrics_engine.py
│   └── testing_engine.py
├── agents/                     # Specialized agents
│   ├── manager_agent.py
│   ├── architect_agent.py
│   ├── backend_agent.py
│   ├── frontend_agent.py
│   ├── database_agent.py
│   ├── qa_agent.py
│   ├── reviewer_agent.py
│   └── devops_agent.py
├── memory/                     # Memory systems
│   ├── short_term.py
│   ├── long_term.py
│   ├── experience_memory.py
│   └── user_preferences.py
├── tools/                      # Utility tools
│   ├── file_tool.py
│   ├── code_generator.py
│   ├── code_editor.py
│   ├── command_runner.py
│   ├── test_runner.py
│   └── browser_tool.py
├── web_intelligence/           # Code generation intelligence
│   ├── frontend_intel.py
│   ├── backend_intel.py
│   ├── database_intel.py
│   ├── auth_intel.py
│   └── api_designer.py
├── execution/                  # Safe execution
│   ├── sandbox.py
│   └── error_handler.py
├── versioning/                 # Git integration
│   ├── git_manager.py
│   └── diff_engine.py
└── interface/
    └── cli.py                  # CLI interface