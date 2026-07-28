import pytest
from core.ai_brain import AIBrain
from core.goal_manager import GoalManager

@pytest.mark.asyncio
async def test_ai_brain_initialization():
    """Test AI brain initialization."""
    config = {"paths": {"projects_root": "./test_projects"}, "agents": {"enabled": []}}
    brain = AIBrain(config)
    
    await brain.initialize()
    assert brain.state.value == "idle"

@pytest.mark.asyncio
async def test_goal_manager_create_goal():
    """Test goal creation."""
    config = {"paths": {"projects_root": "./test_projects"}}
    manager = GoalManager(config)
    await manager.initialize()
    
    goal_id = await manager.create_goal("Test Goal", "Test description")
    assert goal_id is not None
    
    goal = manager.get_goal(goal_id)
    assert goal.title == "Test Goal"

### tests/test_agents.py
```python
import pytest
from agents.manager_agent import ManagerAgent

def test_manager_agent_initialization():
    """Test manager agent initialization."""
    config = {"agents": {"enabled": ["frontend", "backend"]}}
    agent = ManagerAgent(config)
    
    assert len(agent.agents) == 2

### tests/test_tools.py
```python
import pytest
from tools.file_tool import FileTool

@pytest.mark.asyncio
async def test_file_tool_write_read():
    """Test file writing and reading."""
    config = {"tools": {"file_tool": {"allowed_extensions": [".txt"], "max_file_size_mb": 10}}}
    tool = FileTool(config)
    
    test_file = "test.txt"
    content = "Hello, World!"
    
    success = await tool.write_file(test_file, content)
    assert success
    
    read_content = await tool.read_file(test_file)
    assert read_content == content
    
    # Cleanup
    Path(test_file).unlink()

### docs/architecture.md
```markdown
# Architecture Overview

## System Architecture

The Autonomous AI Web Developer is built on a multi-agent architecture with deep learning capabilities.

### Core Components

1. **AI Brain**: Central decision-making engine
2. **Goal Manager**: Project lifecycle management
3. **Memory System**: Persistent learning across sessions
4. **Agent System**: Specialized development agents
5. **Tool System**: Plugin-based execution tools

### Data Flow

1. User input → Requirement Interpreter → Technical specs
2. Technical specs → Planner → Execution plan
3. Plan → Manager Agent → Specialized agents
4. Agents → Tools → Code generation
5. Code → Quality Engine → Review & feedback
6. Results → Experience Memory → Learning

### Technology Stack

- **Backend**: FastAPI, SQLAlchemy, Redis
- **ML**: OpenAI/Anthropic APIs, ChromaDB for vector storage
- **Frontend**: React/Next.js (generated)
- **DevOps**: Docker, Kubernetes integration