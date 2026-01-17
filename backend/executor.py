"""
Executor - Runs SymPy code in a sandboxed environment.
Provides timeout protection and error handling.
"""

import sys
import io
import signal
from contextlib import contextmanager
from typing import Dict, Any
import sympy
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

try:
    from .config import config
except ImportError:
    from config import config


class TimeoutException(Exception):
    """Raised when code execution exceeds timeout."""
    pass


@contextmanager
def timeout(seconds: int):
    """
    Context manager that raises TimeoutException after N seconds.
    Only works on Unix systems. On Windows, just yields without timeout.
    """
    def timeout_handler(signum, frame):
        raise TimeoutException("Code execution timed out")
    
    # Set up the timeout (Unix only)
    if hasattr(signal, 'SIGALRM'):
        old_handler = signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(seconds)
        try:
            yield
        finally:
            signal.alarm(0)
            signal.signal(signal.SIGALRM, old_handler)
    else:
        # Windows fallback: no timeout protection
        yield


class Executor:
    """
    Executes Python code safely using SymPy.
    
    Design choices:
    1. Allow only SymPy imports (no filesystem access, network, etc.)
    2. Capture stdout/stderr to display intermediate steps
    3. Timeout protection (configurable, default from config)
    4. Return structured results (success/failure, output, errors)
    """
    
    def __init__(self, timeout_seconds: int = None):
        """
        Initialize executor.
        
        Args:
            timeout_seconds: Max execution time (uses config default if not specified)
        """
        self.timeout_seconds = timeout_seconds or config.EXECUTOR_TIMEOUT_SECONDS
    
    def execute(self, code: str) -> Dict[str, Any]:
        """
        Execute SymPy code and return results.
        
        Args:
            code: Python code string (should use SymPy)
            
        Returns:
            Dict with:
                - 'success': bool (True if no errors)
                - 'answer': The value of the `answer` variable
                - 'stdout': Captured print statements
                - 'stderr': Captured error messages
                - 'error': Exception message if failed
                - 'error_type': Type of error (SyntaxError, NameError, etc.)
        """
        # Capture stdout/stderr
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        
        try:
            sys.stdout = stdout_capture
            sys.stderr = stderr_capture
            
            # Create restricted namespace
            namespace = self._create_namespace()
            
            # Preprocess code: No text manipulation needed!
            # We handle imports via the custom __import__ in the sandbox.
            # This is cleaner and more robust than regex stripping.
            processed_code = code
            
            # Execute with timeout
            with timeout(self.timeout_seconds):
                exec(processed_code, namespace)
            
            # Extract the answer
            answer = self._extract_answer_dynamic(namespace, stdout_capture.getvalue())
            if answer is None:
                return {
                    "success": False,
                    "answer": None,
                    "stdout": stdout_capture.getvalue(),
                    "stderr": stderr_capture.getvalue(),
                    "error": "No answer found. Use print() or common variable names (answer, result, solution)",
                    "error_type": "MissingAnswerError"
                }
            
            # Extract answer dynamically
            answer = self._extract_answer_dynamic(namespace, stdout_capture.getvalue())
            
            # Convert SymPy objects to readable strings
            if hasattr(answer, '__iter__') and not isinstance(answer, str):
                answer = [str(item) for item in answer]
            else:
                answer = str(answer)
            
            return {
                "success": True,
                "answer": answer,
                "stdout": stdout_capture.getvalue(),
                "stderr": stderr_capture.getvalue(),
                "error": None,
                "error_type": None
            }
            
        except TimeoutException as e:
            return {
                "success": False,
                "answer": None,
                "stdout": stdout_capture.getvalue(),
                "stderr": stderr_capture.getvalue(),
                "error": str(e),
                "error_type": "TimeoutError"
            }
        except SyntaxError as e:
            return {
                "success": False,
                "answer": None,
                "stdout": stdout_capture.getvalue(),
                "stderr": stderr_capture.getvalue(),
                "error": f"Line {e.lineno}: {e.msg}",
                "error_type": "SyntaxError"
            }
        except Exception as e:
            return {
                "success": False,
                "answer": None,
                "stdout": stdout_capture.getvalue(),
                "stderr": stderr_capture.getvalue(),
                "error": str(e),
                "error_type": type(e).__name__
            }
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
    
    def _extract_answer_dynamic(self, namespace, stdout):
        """Extract answer dynamically from stdout or namespace."""
        # 1. Check stdout
        if stdout.strip():
            lines = [l for l in stdout.strip().split('\n') if l.strip()]
            if lines:
                return lines[-1]
        # 2. Common variable names
        for name in ['answer', 'result', 'solution', 'final', 'output']:
            if name in namespace:
                return namespace[name]
        # 3. Last user variable
        user_vars = {k: v for k, v in namespace.items()
                    if not k.startswith('_') and k not in ['__builtins__', 'sympy']
                    and not callable(v) and not isinstance(v, type)}
        if user_vars:
            return list(user_vars.values())[-1]
        return None
    
        return None
    
    def _safe_import(self, name, globals=None, locals=None, fromlist=(), level=0):
        """
        Custom replacement for __import__ in the sandbox.
        Allows harmless imports (redundant ones for libraries already loaded).
        Blocks everything else.
        """
        allowed_modules = set(config.SANDBOX_ALLOWED_MODULES)
        
        # Check if it's a known safe module
        if name in allowed_modules:
            # Return the actual library we've already imported
            if name == 'numpy':
                return np
            if name == 'matplotlib':
                return matplotlib
            if name == 'matplotlib.pyplot':
                return plt
            if name == 'sympy':
                return sympy
            if name == 'math':
                import math
                return math
                
        # For anything else, raising ImportError is correct behavior for a sandbox
        # But we log it to stderr so the user can debug if they tried something weird
        raise ImportError(f"Importing '{name}' is not allowed in this restricted environment.")

    def _create_namespace(self) -> Dict[str, Any]:
        """
        Create a restricted namespace for code execution.
        
        Only allow SymPy and basic Python builtins.
        Explicitly block dangerous operations (file I/O, imports, eval, etc.)
        """
        # Create namespace with SymPy
        # Note: sympy is already imported at module level (line 11)
        namespace = {
            "__builtins__": {
                # Safe builtins
                "abs": abs,
                "all": all,  # Added: needed for SymPy code
                "any": any,  # Added: needed for SymPy code
                "min": min,
                "max": max,
                "pow": pow,
                "round": round,
                "print": print,  # Added: allow printing
                "sum": sum,
                "len": len,
                "range": range,
                "enumerate": enumerate,
                "zip": zip,
                "map": map,
                "filter": filter,
                "sorted": sorted,
                "reversed": reversed,  # Added
                "list": list,
                "tuple": tuple,
                "dict": dict,
                "set": set,
                "str": str,
                "int": int,
                "float": float,
                "bool": bool,
                "isinstance": isinstance,  # Added: type checking
                "type": type,  # Added: type checking
                "callable": callable,  # Added
                "True": True,
                "False": False,
                "None": None,
                "__import__": self._safe_import,  # Added: robust import handling
            },
            "sympy": sympy,
            # Visualization support
            "matplotlib": matplotlib,
            "plt": plt,
            "np": np,
            # Add all SymPy functions to global namespace
            **{name: getattr(sympy, name) for name in dir(sympy) if not name.startswith('_')}
        }
        
        return namespace


if __name__ == "__main__":
    # Test the executor
    executor = Executor()
    
    test_cases = [
        # Valid code
        """
from sympy import *
x = symbols('x')
answer = solve(x**2 - 4, x)
""",
        # Syntax error
        """
from sympy import *
x = symbols('x'
answer = x + 1
""",
        # Missing answer variable
        """
from sympy import *
x = symbols('x')
result = x + 1
""",
        # Long computation (tests timeout)
        """
from sympy import *
x = symbols('x')
# This might take a while
answer = integrate(sin(x**10) * cos(x**5), x)
"""
    ]
    
    for i, code in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"Test Case {i}")
        print(f"{'='*60}")
        result = executor.execute(code)
        
        if result["success"]:
            print(f"✅ Success!")
            print(f"Answer: {result['answer']}")
        else:
            print(f"❌ {result['error_type']}: {result['error']}")
