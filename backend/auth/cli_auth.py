"""
CLI Authentication Manager
Handles authentication for the command-line interface.

Author: Nik Jois
"""

import asyncio
import getpass
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from pathlib import Path
import json

from rich.console import Console
from rich.prompt import Prompt, Confirm

from backend.core.config import get_config


class CLIAuthManager:
    """Handles CLI authentication and session management"""
    
    def __init__(self):
        self.config = get_config()
        self.console = Console()
        self.current_user: Optional[Dict] = None
        self.session_file = Path.home() / ".govsecure_session"
        
    async def authenticate(self) -> bool:
        """Main authentication method"""
        # In development mode, use bypass authentication
        if self.config.is_development:
            return await self.bypass_authentication()
        
        # Check for existing valid session
        if await self.check_existing_session():
            return True
        
        # Perform interactive authentication
        return await self.interactive_authentication()
    
    async def bypass_authentication(self) -> bool:
        """Bypass authentication for development mode"""
        self.current_user = {
            "user_id": "dev_user",
            "username": "developer",
            "roles": ["admin", "user"],
            "clearance": "public",
            "authenticated_at": datetime.now().isoformat(),
            "session_expires": (datetime.now() + timedelta(hours=8)).isoformat()
        }
        
        self.console.print("Development mode: Authentication bypassed", style="yellow")
        return True
    
    async def check_existing_session(self) -> bool:
        """Check if there's a valid existing session"""
        try:
            if not self.session_file.exists():
                return False
            
            with open(self.session_file, 'r') as f:
                session_data = json.load(f)
            
            # Check if session is expired
            expires_at = datetime.fromisoformat(session_data.get('session_expires', '2000-01-01'))
            if datetime.now() > expires_at:
                self.session_file.unlink()  # Remove expired session
                return False
            
            # Session is valid
            self.current_user = session_data
            self.console.print(f"Welcome back, {session_data.get('username', 'user')}!", style="green")
            return True
            
        except Exception as e:
            # Remove corrupted session file
            if self.session_file.exists():
                self.session_file.unlink()
            return False
    
    async def interactive_authentication(self) -> bool:
        """Interactive authentication flow for CLI"""
        import getpass
        
        try:
            self.console.print("GovSecure AI Platform - User Authentication", style="bold blue")
            self.console.print("Note: Using development authentication for testing", style="yellow")
            
            username = input("Username: ")
            password = getpass.getpass("Password: ")
            
            # Use validate_credentials for consistency
            if self.validate_credentials(username, password):
                user_data = {
                    "user_id": username,
                    "username": username,
                    "roles": ["user", "analyst"],
                    "clearance_level": "public",
                    "login_time": datetime.now().isoformat(),
                    "session_type": "interactive"
                }
                
                self.current_user = user_data
                await self.create_session(username)
                
                self.console.print(f"Welcome, {username}!", style="green")
                return True
            else:
                self.console.print("Authentication failed", style="red")
                return False
                
        except KeyboardInterrupt:
            self.console.print("\nAuthentication cancelled", style="yellow")
            return False
        except Exception as e:
            self.console.print(f"Authentication error: {e}", style="red")
            return False
    
    async def validate_credentials(self, username: str, password: str) -> bool:
        """Validate user credentials (mock implementation)"""
        # Mock validation - accepts any non-empty username/password
        if not username or not password:
            return False
        
        # Simulate network delay
        await asyncio.sleep(1)
        
        # In production, this would check against LDAP, Active Directory, or other auth systems
        mock_users = {
            "admin": {"password": "admin123", "roles": ["admin", "user"], "clearance": "secret"},
            "user": {"password": "user123", "roles": ["user"], "clearance": "public"},
            "analyst": {"password": "analyst123", "roles": ["analyst", "user"], "clearance": "confidential"}
        }
        
        user_data = mock_users.get(username.lower())
        if user_data and user_data["password"] == password:
            return True
        
        return False
    
    async def create_session(self, username: str) -> bool:
        """Create authenticated session"""
        # Mock user data - in production, this would come from auth system
        user_data = {
            "admin": {"roles": ["admin", "user"], "clearance": "secret"},
            "user": {"roles": ["user"], "clearance": "public"},
            "analyst": {"roles": ["analyst", "user"], "clearance": "confidential"}
        }.get(username.lower(), {"roles": ["user"], "clearance": "public"})
        
        self.current_user = {
            "user_id": f"user_{username}",
            "username": username,
            "roles": user_data["roles"],
            "clearance": user_data["clearance"],
            "authenticated_at": datetime.now().isoformat(),
            "session_expires": (datetime.now() + timedelta(hours=8)).isoformat()
        }
        
        # Save session to file
        try:
            with open(self.session_file, 'w') as f:
                json.dump(self.current_user, f, indent=2)
            
            self.console.print(f"Welcome, {username}! Authentication successful.", style="green")
            return True
            
        except Exception as e:
            self.console.print(f"Failed to save session: {e}", style="red")
            return False
    
    def is_authenticated(self) -> bool:
        """Check if user is currently authenticated"""
        return self.current_user is not None
    
    def get_current_user(self) -> Optional[Dict]:
        """Get current user information"""
        return self.current_user.copy() if self.current_user else None
    
    def has_role(self, role: str) -> bool:
        """Check if current user has specific role"""
        if not self.current_user:
            return False
        return role in self.current_user.get("roles", [])
    
    def has_any_role(self, roles: List[str]) -> bool:
        """Check if current user has any of the specified roles"""
        if not self.current_user:
            return False
        user_roles = set(self.current_user.get("roles", []))
        return bool(user_roles.intersection(set(roles)))
    
    def has_clearance(self, required_clearance: str) -> bool:
        """Check if user has required security clearance"""
        if not self.current_user:
            return False
        
        clearance_levels = {"public": 1, "confidential": 2, "secret": 3, "top_secret": 4}
        user_level = clearance_levels.get(self.current_user.get("clearance", "public"), 1)
        required_level = clearance_levels.get(required_clearance, 1)
        
        return user_level >= required_level
    
    async def logout(self) -> None:
        """Logout current user"""
        if self.session_file.exists():
            self.session_file.unlink()
        
        if self.current_user:
            username = self.current_user.get("username", "user")
            self.current_user = None
            self.console.print(f"Goodbye, {username}! You have been logged out.", style="yellow")
        else:
            self.console.print("No active session to logout.", style="yellow")
    
    async def show_session_status(self):
        """Display current session status"""
        if not self.current_user:
            self.console.print("No active session", style="red")
            return
        
        self.console.print("Current Session Status:", style="bold blue")
        self.console.print(f"  Username: {self.current_user.get('username')}")
        self.console.print(f"  User ID: {self.current_user.get('user_id')}")
        self.console.print(f"  Roles: {', '.join(self.current_user.get('roles', []))}")
        self.console.print(f"  Clearance: {self.current_user.get('clearance')}")
        self.console.print(f"  Authenticated: {self.current_user.get('authenticated_at')}")
        self.console.print(f"  Expires: {self.current_user.get('session_expires')}")
    
    async def refresh_session(self) -> bool:
        """Refresh current session"""
        if not self.current_user:
            return False
        
        # Extend session expiration
        self.current_user["session_expires"] = (datetime.now() + timedelta(hours=8)).isoformat()
        
        try:
            with open(self.session_file, 'w') as f:
                json.dump(self.current_user, f, indent=2)
            return True
        except Exception:
            return False 