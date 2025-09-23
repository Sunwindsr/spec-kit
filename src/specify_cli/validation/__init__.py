"""
重构验证模块 - 提供强制验证功能
"""

from .refactoring_validation import (
    RefactoringValidationSystem,
    RealityValidator,
    BehaviorPreservationValidator,
    ProgressiveRefactoringValidator,
    ValidationResult,
    ValidationSeverity
)

__all__ = [
    'RefactoringValidationSystem',
    'RealityValidator', 
    'BehaviorPreservationValidator',
    'ProgressiveRefactoringValidator',
    'ValidationResult',
    'ValidationSeverity'
]