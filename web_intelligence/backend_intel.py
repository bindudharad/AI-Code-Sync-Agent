"""
Frontend intelligence module for generating React/Next.js code.
"""
import json
from typing import Dict, List, Any


class FrontendIntel:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.framework = "react"  # Default
    
    def generate_login_component(self) -> str:
        """Generate a React login component."""
        return '''import React, { useState } from 'react';
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
    
    def generate_register_component(self) -> str:
        """Generate a React register component."""
        return '''import React, { useState } from 'react';
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
    
    def generate_auth_service(self) -> str:
        """Generate authentication service."""
        return '''import axios from 'axios';

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
    
    def generate_list_component(self, entity: str) -> str:
        """Generate a list component for an entity."""
        entity_cap = entity.capitalize()
        
        return f'''import React, {{ useState, useEffect }} from 'react';
import {{ {entity_cap}API }} from '../services/{entity}API';

function {entity_cap}List() {{
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {{
    fetchItems();
  }}, []);

  const fetchItems = async () => {{
    try {{
      setLoading(true);
      const data = await {entity_cap}API.getAll();
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
        await {entity_cap}API.delete(id);
        fetchItems();
      }} catch (err) {{
        setError(err.message);
      }}
    }}
  }};

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {{error}}</div>;

  return (
    <div className="{entity}-list">
      <h2>{entity_cap}s</h2>
      <button onClick={{() => window.location.href = '/{entity}s/new'}}>
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
                <button onClick={{() => window.location.href = '/{entity}s/{{item.id}}/edit'}}>
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

export default {entity_cap}List;
'''
    
    def generate_form_component(self, entity: str) -> str:
        """Generate a form component for an entity."""
        entity_cap = entity.capitalize()
        
        return f'''import React, {{ useState }} from 'react';
import {{ useNavigate, useParams }} from 'react-router-dom';
import {{ {entity_cap}API }} from '../services/{entity}API';

function {entity_cap}Form() {{
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
      const item = await {entity_cap}API.getById(itemId);
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
        await {entity_cap}API.update(id, formData);
      }} else {{
        await {entity_cap}API.create(formData);
      }}
      navigate('/{entity}s');
    }} catch (err) {{
      setError(err.message);
    }}
  }};

  return (
    <div className="{entity}-form">
      <h2>{{id ? 'Edit' : 'Create'}} {entity_cap}</h2>
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
        <button type="button" onClick={{() => navigate('/{entity}s')}}>
          Cancel
        </button>
      </form>
    </div>
  );
}}

export default {entity_cap}Form;
'''
    
    def generate_api_service(self, entity: str) -> str:
        """Generate API service for an entity."""
        entity_cap = entity.capitalize()
        
        return f'''import axios from 'axios';
import {{ authService }} from './auth';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

class {entity_cap}API {{
  async getAll() {{
    const response = await axios.get(`${{API_URL}}/{entity}s`, {{
      headers: authService.getAuthHeader()
    }});
    return response.data;
  }}

  async getById(id) {{
    const response = await axios.get(`${{API_URL}}/{entity}s/${{id}}`, {{
      headers: authService.getAuthHeader()
    }});
    return response.data;
  }}

  async create(data) {{
    const response = await axios.post(`${{API_URL}}/{entity}s`, data, {{
      headers: authService.getAuthHeader()
    }});
    return response.data;
  }}

  async update(id, data) {{
    const response = await axios.put(`${{API_URL}}/{entity}s/${{id}}`, data, {{
      headers: authService.getAuthHeader()
    }});
    return response.data;
  }}

  async delete(id) {{
    await axios.delete(`${{API_URL}}/{entity}s/${{id}}`, {{
      headers: authService.getAuthHeader()
    }});
  }}
}}

export const {entity_cap}API = new {entity_cap}API();
'''
    
    def generate_navigation_component(self) -> str:
        """Generate navigation component."""
        return '''import React from 'react';
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
    
    def generate_layout_component(self) -> str:
        """Generate layout component."""
        return '''import React from 'react';
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
    
    def generate_react_app(self) -> str:
        """Generate main App.js."""
        return '''import React from 'react';
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
    
    def generate_app_css(self) -> str:
        """Generate App.css with basic styling."""
        return '''* {
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
    
    def generate_frontend_module(self, description: str) -> str:
        """Generate a generic frontend module."""
        return f'''// Generated frontend module
// Description: {description}

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
import json
from typing import Dict, List, Any


class BackendIntel:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.framework = "fastapi"  # Default
    
    def generate_jwt_handler(self) -> str:
        """Generate JWT authentication handler."""
        return '''from datetime import datetime, timedelta
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
    
    def generate_auth_api(self) -> str:
        """Generate authentication API endpoints."""
        return '''from fastapi import APIRouter, Depends, HTTPException, status
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
    
    def generate_user_model(self) -> str:
        """Generate User model."""
        return '''from sqlalchemy import Column, String, DateTime
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
    
    def generate_crud_api(self, entity: str) -> str:
        """Generate CRUD API endpoints for an entity."""
        entity_cap = entity.capitalize()
        
        return f'''from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models.{entity} import {entity_cap}
from ..schemas.{entity} import {entity_cap}Create, {entity_cap}Response

router = APIRouter(prefix="/{entity}s", tags=["{entity}s"])

@router.get("/", response_model=List[{entity_cap}Response])
def list_items(db: Session = Depends(get_db)):
    items = db.query({entity_cap}).all()
    return items

@router.post("/", response_model={entity_cap}Response)
def create_item(item: {entity_cap}Create, db: Session = Depends(get_db)):
    db_item = {entity_cap}(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/{{item_id}}", response_model={entity_cap}Response)
def get_item(item_id: str, db: Session = Depends(get_db)):
    item = db.query({entity_cap}).filter({entity_cap}.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="{entity_cap} not found")
    return item

@router.put("/{{item_id}}", response_model={entity_cap}Response)
def update_item(item_id: str, item: {entity_cap}Create, db: Session = Depends(get_db)):
    db_item = db.query({entity_cap}).filter({entity_cap}.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="{entity_cap} not found")
    
    for key, value in item.dict().items():
        setattr(db_item, key, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/{{item_id}}")
def delete_item(item_id: str, db: Session = Depends(get_db)):
    item = db.query({entity_cap}).filter({entity_cap}.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="{entity_cap} not found")
    
    db.delete(item)
    db.commit()
    return {{ "message": "{entity_cap} deleted successfully" }}
'''
    
    def generate_service_layer(self, entity: str) -> str:
        """Generate service layer for an entity."""
        entity_cap = entity.capitalize()
        
        return f'''from sqlalchemy.orm import Session
from typing import List, Optional

from ..models.{entity} import {entity_cap}
from ..schemas.{entity} import {entity_cap}Create

class {entity_cap}Service:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self) -> List[{entity_cap}]:
        return self.db.query({entity_cap}).all()
    
    def get_by_id(self, item_id: str) -> Optional[{entity_cap}]:
        return self.db.query({entity_cap}).filter({entity_cap}.id == item_id).first()
    
    def create(self, item: {entity_cap}Create) -> {entity_cap}:
        db_item = {entity_cap}(**item.dict())
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item
    
    def update(self, item_id: str, item: {entity_cap}Create) -> Optional[{entity_cap}]:
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
    return {entity_cap}Service(db)
'''
    
    def generate_model(self, entity: str) -> str:
        """Generate SQLAlchemy model for an entity."""
        entity_cap = entity.capitalize()
        
        return f'''from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
import uuid
from datetime import datetime

Base = declarative_base()

class {entity_cap}(Base):
    __tablename__ = "{entity}s"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    user = relationship("User", back_populates="{entity}s")

    def to_dict(self):
        return {{
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "user_id": str(self.user_id)
        }}
'''
    
    def generate_backend_module(self, description: str) -> str:
        """Generate a generic backend module."""
        return f'''"""
Generated backend module
Description: {description}
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def read_root():
    return {{"message": "Generated endpoint for: {description}"}}

@router.post("/")
def create_item(item: dict):
    return {{"message": "Item created", "data": item}}
'''
    
    def generate_jwt_middleware(self) -> str:
        """Generate JWT authentication middleware."""
        return '''from fastapi import Request, HTTPException
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
import json
from typing import Dict, List, Any


class DatabaseIntel:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.preferred_db = config.get("preferred_database", "postgresql")
    
    def generate_sql_schema(self, schema: Dict[str, Any]) -> str:
        """Generate SQL schema from schema definition."""
        tables = schema.get("tables", [])
        
        sql_statements = []
        
        for table in tables:
            table_name = table["name"]
            columns = table["columns"]
            
            # Generate CREATE TABLE
            column_defs = []
            for col in columns:
                col_def = f"{col['name']} {col['type']}"
                if col.get("primary_key"):
                    col_def += " PRIMARY KEY"
                if col.get("unique"):
                    col_def += " UNIQUE"
                if col.get("nullable") is False:
                    col_def += " NOT NULL"
                column_defs.append(col_def)
            
            create_table = f"CREATE TABLE {table_name} (\n    " + ",\n    ".join(column_defs) + "\n);"
            sql_statements.append(create_table)
            
            # Add indexes
            indexes = table.get("indexes", [])
            for idx in indexes:
                sql_statements.append(f"CREATE INDEX idx_{table_name}_{idx} ON {table_name} ({idx});")
        
        # Add relationships
        relationships = schema.get("relationships", [])
        for rel in relationships:
            if rel["type"] == "foreign_key":
                sql_statements.append(
                    f"ALTER TABLE {rel['from_table']} "
                    f"ADD CONSTRAINT fk_{rel['from_table']}_{rel['to_table']} "
                    f"FOREIGN KEY ({rel['from_column']}) "
                    f"REFERENCES {rel['to_table']}({rel['to_column']});"
                )
        
        return "\n\n".join(sql_statements)
    
    def generate_migration_script(self, schema: Dict[str, Any], db_type: str = "postgresql") -> str:
        """Generate database migration script."""
        return f'''"""
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
    
    def generate_mongodb_schema(self, schema: Dict[str, Any]) -> str:
        """Generate MongoDB schema."""
        collections = schema.get("tables", [])
        
        js_statements = []
        
        for collection in collections:
            collection_name = collection["name"]
            js_statements.append(f"// Collection: {collection_name}")
            js_statements.append(f'db.createCollection("{collection_name}");')
            
            # Add indexes
            indexes = collection.get("indexes", [])
            for idx in indexes:
                js_statements.append(f'db.{collection_name}.createIndex({{ "{idx}": 1 }});')
        
        return "\n\n".join(js_statements)
    
    def generate_db_config(self, db_type: str) -> str:
        """Generate database configuration."""
        if db_type == "postgresql":
            return '''from sqlalchemy import create_engine
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
        elif db_type == "mongodb":
            return '''from pymongo import MongoClient
import os

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")

client = MongoClient(MONGODB_URL)
db = client.app

def get_db():
    return db
'''
        else:
            return f'# Database configuration for {db_type}\n# TODO: Implement config\n'
    
    def generate_orm_models(self, schema: Dict[str, Any], db_type: str) -> str:
        """Generate ORM models."""
        if db_type == "postgresql":
            return self._generate_sqlalchemy_models(schema)
        elif db_type == "mongodb":
            return self._generate_mongoengine_models(schema)
        else:
            return f'# ORM models for {db_type}\n# TODO: Implement models\n'
    
    def _generate_sqlalchemy_models(self, schema: Dict[str, Any]) -> str:
        """Generate SQLAlchemy models."""
        tables = schema.get("tables", [])
        
        code = [
            "from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean",
            "from sqlalchemy.dialects.postgresql import UUID",
            "from sqlalchemy.orm import declarative_base, relationship",
            "import uuid",
            "from datetime import datetime",
            "",
            "Base = declarative_base()",
            ""
        ]
        
        for table in tables:
            table_name = table["name"]
            table_class = ''.join(word.capitalize() for word in table_name.rstrip('s').split('_'))
            
            code.append(f"class {table_class}(Base):")
            code.append(f'    __tablename__ = "{table_name}"')
            code.append("")
            
            for col in table["columns"]:
                col_def = f'    {col["name"]} = Column('
                
                col_type = col["type"]
                if "UUID" in col_type:
                    col_def += "UUID(as_uuid=True)"
                elif "VARCHAR" in col_type:
                    col_def += "String"
                elif "TIMESTAMP" in col_type:
                    col_def += "DateTime"
                elif "BOOLEAN" in col_type:
                    col_def += "Boolean"
                elif "INTEGER" in col_type:
                    col_def += "Integer"
                else:
                    col_def += "String"
                
                if col.get("primary_key"):
                    col_def += ", primary_key=True"
                if col.get("unique"):
                    col_def += ", unique=True"
                if col.get("nullable") is False:
                    col_def += ", nullable=False"
                if "default" in col:
                    col_def += f', default={col["default"]}'
                
                col_def += ")"
                code.append(col_def)
            
            code.append("")
        
        return "\n".join(code)
    
    def _generate_mongoengine_models(self, schema: Dict[str, Any]) -> str:
        """Generate MongoEngine models."""
        return '''from mongoengine import Document, StringField, DateTimeField, UUIDField
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
    
    def generate_connection_manager(self, db_type: str) -> str:
        """Generate database connection manager."""
        if db_type == "postgresql":
            return '''import os
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
        else:
            return f'# Connection manager for {db_type}\n# TODO: Implement\n'
    
    def generate_seed_script(self, schema: Dict[str, Any]) -> str:
        """Generate database seed script."""
        return '''"""
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
    
    def generate_database_module(self, description: str) -> str:
        """Generate a generic database module."""
        return f'''"""
Generated database module
Description: {description}
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
import json
from typing import Dict, List, Any


class AuthIntel:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    
    def generate_jwt_auth_system(self) -> Dict[str, str]:
        """Generate complete JWT authentication system."""
        return {
            "jwt_handler.py": self._generate_jwt_handler(),
            "auth_middleware.py": self._generate_auth_middleware(),
            "auth_routes.py": self._generate_auth_routes(),
            "user_model.py": self._generate_user_model()
        }
    
    def _generate_jwt_handler(self) -> str:
        """Generate JWT handler utility."""
        return '''"""
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
    
    def _generate_auth_middleware(self) -> str:
        """Generate authentication middleware."""
        return '''"""
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
    
    def _generate_auth_routes(self) -> str:
        """Generate authentication routes."""
        return '''"""
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
    
    def _generate_user_model(self) -> str:
        """Generate User model for authentication."""
        return '''"""
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
    
    def generate_oauth_integration(self, provider: str) -> str:
        """Generate OAuth integration for a provider."""
        return f'''"""
OAuth Integration for {provider}
"""

import os
from fastapi import APIRouter, HTTPException
from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request
from starlette.responses import RedirectResponse

router = APIRouter(prefix="/oauth/{provider.lower()}", tags=["oauth"])

oauth = OAuth()

oauth.register(
    name="{provider.lower()}",
    client_id=os.getenv("{provider.upper()}_CLIENT_ID"),
    client_secret=os.getenv("{provider.upper()}_CLIENT_SECRET"),
    access_token_url="{self._get_oauth_token_url(provider)}",
    authorize_url="{self._get_oauth_auth_url(provider)}",
    client_kwargs={{"scope": "openid email profile"}},
)

@router.get("/login")
async def login(request: Request):
    """Redirect to OAuth provider."""
    redirect_uri = request.url_for("auth_{provider.lower()}_callback")
    return await oauth.{provider.lower()}.authorize_redirect(request, redirect_uri)

@router.get("/callback")
async def callback(request: Request):
    """Handle OAuth callback."""
    try:
        token = await oauth.{provider.lower()}.authorize_access_token(request)
        user_info = await oauth.{provider.lower()}.userinfo(token=token)
        
        # TODO: Create/update user in database
        # TODO: Generate JWT token
        
        return {{"user": user_info, "token": token}}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
'''
    
    def _get_oauth_token_url(self, provider: str) -> str:
        """Get OAuth token URL for provider."""
        urls = {
            "google": "https://accounts.google.com/o/oauth2/token",
            "github": "https://github.com/login/oauth/access_token",
            "facebook": "https://graph.facebook.com/v12.0/oauth/access_token"
        }
        return urls.get(provider.lower(), "")
    
    def _get_oauth_auth_url(self, provider: str) -> str:
        """Get OAuth authorization URL for provider."""
        urls = {
            "google": "https://accounts.google.com/o/oauth2/auth",
            "github": "https://github.com/login/oauth/authorize",
            "facebook": "https://www.facebook.com/v12.0/dialog/oauth"
        }
        return urls.get(provider.lower(), "")
    
    def generate_password_reset_flow(self) -> Dict[str, str]:
        """Generate password reset flow components."""
        return {
            "reset_request.py": self._generate_reset_request(),
            "reset_token.py": self._generate_reset_token_handler(),
            "email_sender.py": self._generate_email_sender()
        }
    
    def _generate_reset_request(self) -> str:
        """Generate password reset request handler."""
        return '''"""
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
    
    def _generate_reset_token_handler(self) -> str:
        """Generate reset token handler."""
        return '''"""
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
    
    def _generate_email_sender(self) -> str:
        """Generate email sender utility."""
        return '''"""
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
import json
from typing import Dict, List, Any


class APIDesigner:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    
    def design(self, features: List[Dict], user_flows: List[Dict]) -> Dict[str, Any]:
        """Design API based on features and user flows."""
        api_spec = {
            "openapi": "3.0.0",
            "info": {
                "title": "AutonomousAI Generated API",
                "version": "1.0.0"
            },
            "paths": {},
            "components": {
                "schemas": {},
                "securitySchemes": {
                    "BearerAuth": {
                        "type": "http",
                        "scheme": "bearer",
                        "bearerFormat": "JWT"
                    }
                }
            }
        }
        
        # Design paths based on features
        for feature in features:
            feature_name = feature["name"]
            if "user" in feature_name:
                api_spec["paths"].update(self._generate_user_paths())
            elif any(x in feature_name for x in ["product", "post", "article", "order"]):
                entity = feature.get("entity", feature_name.split("_")[0])
                api_spec["paths"].update(self._generate_crud_paths(entity))
        
        # Design paths based on user flows
        for flow in user_flows:
            flow_name = flow["name"]
            if "payment" in flow_name:
                api_spec["paths"].update(self._generate_payment_paths())
            elif "search" in flow_name:
                api_spec["paths"].update(self._generate_search_paths())
        
        return api_spec
    
    def _generate_user_paths(self) -> Dict[str, Any]:
        """Generate user-related API paths."""
        return {
            "/auth/login": {
                "post": {
                    "summary": "User login",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["email", "password"],
                                    "properties": {
                                        "email": {"type": "string", "format": "email"},
                                        "password": {"type": "string", "format": "password"}
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Login successful",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "access_token": {"type": "string"},
                                            "token_type": {"type": "string"}
                                        }
                                    }
                                }
                            }
                        },
                        "401": {"description": "Invalid credentials"}
                    }
                }
            },
            "/auth/register": {
                "post": {
                    "summary": "User registration",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["email", "password", "name"],
                                    "properties": {
                                        "email": {"type": "string", "format": "email"},
                                        "password": {"type": "string", "format": "password"},
                                        "name": {"type": "string"}
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "201": {"description": "User created"},
                        "400": {"description": "Email already exists"}
                    }
                }
            }
        }
    
    def _generate_crud_paths(self, entity: str) -> Dict[str, Any]:
        """Generate CRUD paths for an entity."""
        base_path = f"/{entity}s"
        entity_id_path = f"/{entity}s/{{id}}"
        
        return {
            base_path: {
                "get": {
                    "summary": f"List {entity}s",
                    "security": [{"BearerAuth": []}],
                    "responses": {
                        "200": {
                            "description": f"List of {entity}s",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {"$ref": f"#/components/schemas/{entity.capitalize()}"}
                                    }
                                }
                            }
                        }
                    }
                },
                "post": {
                    "summary": f"Create {entity}",
                    "security": [{"BearerAuth": []}],
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {"$ref": f"#/components/schemas/{entity.capitalize()}Create"}
                            }
                        }
                    },
                    "responses": {
                        "201": {
                            "description": f"{entity.capitalize()} created",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": f"#/components/schemas/{entity.capitalize()}"}
                                }
                            }
                        }
                    }
                }
            },
            entity_id_path: {
                "get": {
                    "summary": f"Get {entity} by ID",
                    "security": [{"BearerAuth": []}],
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": f"{entity.capitalize()} details",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": f"#/components/schemas/{entity.capitalize()}"}
                                }
                            }
                        },
                        "404": {"description": f"{entity.capitalize()} not found"}
                    }
                },
                "put": {
                    "summary": f"Update {entity}",
                    "security": [{"BearerAuth": []}],
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string"}
                        }
                    ],
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {"$ref": f"#/components/schemas/{entity.capitalize()}Create"}
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": f"{entity.capitalize()} updated",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": f"#/components/schemas/{entity.capitalize()}"}
                                }
                            }
                        }
                    }
                },
                "delete": {
                    "summary": f"Delete {entity}",
                    "security": [{"BearerAuth": []}],
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string"}
                        }
                    ],
                    "responses": {
                        "204": {"description": f"{entity.capitalize()} deleted"}
                    }
                }
            }
        }
    
    def _generate_payment_paths(self) -> Dict[str, Any]:
        """Generate payment API paths."""
        return {
            "/payments/create": {
                "post": {
                    "summary": "Create payment intent",
                    "security": [{"BearerAuth": []}],
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["amount", "currency"],
                                    "properties": {
                                        "amount": {"type": "number"},
                                        "currency": {"type": "string", "default": "usd"}
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Payment intent created",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "client_secret": {"type": "string"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/payments/confirm": {
                "post": {
                    "summary": "Confirm payment",
                    "security": [{"BearerAuth": []}],
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["payment_intent_id"],
                                    "properties": {
                                        "payment_intent_id": {"type": "string"}
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {"description": "Payment confirmed"},
                        "400": {"description": "Payment failed"}
                    }
                }
            }
        }
    
    def _generate_search_paths(self) -> Dict[str, Any]:
        """Generate search API paths."""
        return {
            "/search": {
                "get": {
                    "summary": "Search across resources",
                    "security": [{"BearerAuth": []}],
                    "parameters": [
                        {
                            "name": "q",
                            "in": "query",
                            "required": True,
                            "schema": {"type": "string"}
                        },
                        {
                            "name": "limit",
                            "in": "query",
                            "schema": {"type": "integer", "default": 20}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Search results",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "results": {"type": "array"},
                                            "total": {"type": "integer"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    
    def generate_openapi_spec(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Generate complete OpenAPI specification."""
        features = requirements.get("features", [])
        tech_stack = requirements.get("tech_stack", {})
        
        spec = {
            "openapi": "3.0.0",
            "info": {
                "title": "API Specification",
                "version": "1.0.0",
                "description": "Generated API specification"
            },
            "servers": [
                {
                    "url": f"http://localhost:{'8000' if tech_stack.get('backend') == 'fastapi' else '3000'}",
                    "description": "Development server"
                }
            ],
            "paths": {},
            "components": {
                "schemas": {},
                "securitySchemes": {
                    "BearerAuth": {
                        "type": "http",
                        "scheme": "bearer",
                        "bearerFormat": "JWT"
                    }
                }
            }
        }
        
        # Add paths based on features
        for feature in features:
            feature_name = feature["name"]
            if "auth" in feature_name:
                spec["paths"].update(self._generate_user_paths())
            elif any(x in feature_name for x in ["product", "post", "article", "order", "item"]):
                entity = feature.get("entity", "item")
                spec["paths"].update(self._generate_crud_paths(entity))
        
        return spec

### execution/__init__.py
```python
# Execution package