"""
Audit Context Manager
Provides easy integration of audit logging into agent operations.
"""

import time
from contextlib import contextmanager
from typing import Dict, Any, Optional
from .audit_logger import AuditLogger

class AuditContext:
    """Context manager for automatic audit logging of agent operations."""
    
    def __init__(self, audit_logger: AuditLogger):
        self.audit_logger = audit_logger
    
    @contextmanager
    def log_operation(self,
                     agent_id: str,
                     action_type: str,
                     action_description: str,
                     deal_id: Optional[str] = None,
                     user_id: Optional[str] = None,
                     session_id: Optional[str] = None,
                     input_data: Optional[Dict[Any, Any]] = None,
                     metadata: Optional[Dict[Any, Any]] = None):
        """
        Context manager for logging agent operations with automatic timing and error handling.
        
        Usage:
            with audit_context.log_operation(
                agent_id="finance_agent",
                action_type="FINANCIAL_ANALYSIS",
                action_description="Calculate financial ratios",
                deal_id="deal_123"
            ) as audit_log:
                # Perform operation
                result = perform_analysis()
                audit_log.set_output(result)
                audit_log.add_lineage("API", "fmp_api", "DATA_FETCH", "Retrieved financial statements")
        """
        start_time = time.time()
        audit_log_id = None
        output_data = None
        error_message = None
        status = "SUCCESS"
        
        class AuditLogContext:
            def __init__(self, context_self):
                self.context = context_self
                self.output_data = None
                self.lineage_entries = []
                self.decisions = []
            
            def set_output(self, data: Dict[Any, Any]):
                """Set the output data for the operation."""
                self.output_data = data
            
            def add_lineage(self, source_type: str, source_id: str, 
                          transformation_type: str, description: str = None,
                          input_schema: Dict[str, Any] = None,
                          output_schema: Dict[str, Any] = None,
                          data_quality_score: float = None):
                """Add data lineage information."""
                self.lineage_entries.append({
                    'source_type': source_type,
                    'source_id': source_id,
                    'transformation_type': transformation_type,
                    'description': description,
                    'input_schema': input_schema,
                    'output_schema': output_schema,
                    'data_quality_score': data_quality_score
                })
            
            def add_decision(self, decision_type: str, criteria: str = None,
                           confidence: float = None, alternatives: list = None,
                           risk_assessment: Dict[str, Any] = None):
                """Add agent decision information."""
                self.decisions.append({
                    'decision_type': decision_type,
                    'criteria': criteria,
                    'confidence': confidence,
                    'alternatives': alternatives,
                    'risk_assessment': risk_assessment
                })
        
        audit_context = AuditLogContext(self)
        
        try:
            yield audit_context
            output_data = audit_context.output_data
        except Exception as e:
            status = "ERROR"
            error_message = str(e)
            raise
        finally:
            # Calculate execution time
            execution_time_ms = int((time.time() - start_time) * 1000)
            
            # Log the main operation
            audit_log_id = self.audit_logger.log_action(
                agent_id=agent_id,
                action_type=action_type,
                action_description=action_description,
                deal_id=deal_id,
                user_id=user_id,
                session_id=session_id,
                input_data=input_data,
                output_data=output_data,
                execution_time_ms=execution_time_ms,
                status=status,
                error_message=error_message,
                metadata=metadata
            )
            
            # Log data lineage entries
            for lineage in audit_context.lineage_entries:
                self.audit_logger.log_data_lineage(
                    audit_log_id=audit_log_id,
                    source_type=lineage['source_type'],
                    source_id=lineage['source_id'],
                    transformation_type=lineage['transformation_type'],
                    transformation_description=lineage['description'],
                    input_schema=lineage['input_schema'],
                    output_schema=lineage['output_schema'],
                    data_quality_score=lineage['data_quality_score']
                )
            
            # Log agent decisions
            for decision in audit_context.decisions:
                self.audit_logger.log_agent_decision(
                    audit_log_id=audit_log_id,
                    decision_type=decision['decision_type'],
                    decision_criteria=decision['criteria'],
                    confidence_score=decision['confidence'],
                    alternatives_considered=decision['alternatives'],
                    risk_assessment=decision['risk_assessment']
                )

# Global audit logger instance
_audit_logger = None
_audit_context = None

def get_audit_logger() -> AuditLogger:
    """Get the global audit logger instance."""
    global _audit_logger
    if _audit_logger is None:
        _audit_logger = AuditLogger()
    return _audit_logger

def get_audit_context() -> AuditContext:
    """Get the global audit context instance."""
    global _audit_context
    if _audit_context is None:
        _audit_context = AuditContext(get_audit_logger())
    return _audit_context