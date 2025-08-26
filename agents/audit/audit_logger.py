"""
Comprehensive Audit Logging System
Implements SQLite-based immutable audit log storage with action logging and data lineage tracking.
"""

import sqlite3
import json
import hashlib
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path
import threading
from contextlib import contextmanager

class AuditLogger:
    """
    Immutable audit logging system for M&A due diligence operations.
    Provides comprehensive tracking of all agent operations and data transformations.
    """
    
    def __init__(self, db_path: str = "audit-logs/audit_trail.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._init_database()
    
    def _init_database(self):
        """Initialize the SQLite database with immutable audit tables."""
        with self._get_connection() as conn:
            # Main audit log table - immutable once written
            conn.execute("""
                CREATE TABLE IF NOT EXISTS audit_log (
                    id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    deal_id TEXT,
                    agent_id TEXT NOT NULL,
                    action_type TEXT NOT NULL,
                    action_description TEXT NOT NULL,
                    user_id TEXT,
                    session_id TEXT,
                    input_data_hash TEXT,
                    output_data_hash TEXT,
                    execution_time_ms INTEGER,
                    status TEXT NOT NULL,
                    error_message TEXT,
                    metadata TEXT,
                    previous_log_hash TEXT,
                    log_hash TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Data lineage tracking table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS data_lineage (
                    id TEXT PRIMARY KEY,
                    audit_log_id TEXT NOT NULL,
                    source_type TEXT NOT NULL,
                    source_id TEXT NOT NULL,
                    transformation_type TEXT NOT NULL,
                    transformation_description TEXT,
                    input_schema TEXT,
                    output_schema TEXT,
                    data_quality_score REAL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (audit_log_id) REFERENCES audit_log (id)
                )
            """)
            
            # Agent decision tracking
            conn.execute("""
                CREATE TABLE IF NOT EXISTS agent_decisions (
                    id TEXT PRIMARY KEY,
                    audit_log_id TEXT NOT NULL,
                    decision_type TEXT NOT NULL,
                    decision_criteria TEXT,
                    confidence_score REAL,
                    alternatives_considered TEXT,
                    risk_assessment TEXT,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (audit_log_id) REFERENCES audit_log (id)
                )
            """)
            
            # System events and configuration changes
            conn.execute("""
                CREATE TABLE IF NOT EXISTS system_events (
                    id TEXT PRIMARY KEY,
                    event_type TEXT NOT NULL,
                    event_description TEXT NOT NULL,
                    component TEXT NOT NULL,
                    configuration_before TEXT,
                    configuration_after TEXT,
                    triggered_by TEXT,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create indexes for performance
            conn.execute("CREATE INDEX IF NOT EXISTS idx_audit_log_timestamp ON audit_log(timestamp)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_audit_log_deal_id ON audit_log(deal_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_audit_log_agent_id ON audit_log(agent_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_data_lineage_audit_log_id ON data_lineage(audit_log_id)")
            
            conn.commit()
    
    @contextmanager
    def _get_connection(self):
        """Get a database connection with proper locking."""
        with self._lock:
            conn = sqlite3.connect(str(self.db_path))
            conn.row_factory = sqlite3.Row
            try:
                yield conn
            finally:
                conn.close()
    
    def _calculate_hash(self, data: str) -> str:
        """Calculate SHA-256 hash for data integrity."""
        return hashlib.sha256(data.encode('utf-8')).hexdigest()
    
    def _get_previous_log_hash(self) -> Optional[str]:
        """Get the hash of the most recent log entry for chain integrity."""
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT log_hash FROM audit_log ORDER BY timestamp DESC LIMIT 1"
            )
            result = cursor.fetchone()
            return result['log_hash'] if result else None
    
    def log_action(self, 
                   agent_id: str,
                   action_type: str,
                   action_description: str,
                   deal_id: Optional[str] = None,
                   user_id: Optional[str] = None,
                   session_id: Optional[str] = None,
                   input_data: Optional[Dict[Any, Any]] = None,
                   output_data: Optional[Dict[Any, Any]] = None,
                   execution_time_ms: Optional[int] = None,
                   status: str = "SUCCESS",
                   error_message: Optional[str] = None,
                   metadata: Optional[Dict[Any, Any]] = None) -> str:
        """
        Log an agent action with immutable audit trail.
        
        Args:
            agent_id: Identifier of the agent performing the action
            action_type: Type of action (e.g., 'ANALYSIS', 'DATA_FETCH', 'CALCULATION')
            action_description: Detailed description of the action
            deal_id: Associated deal identifier
            user_id: User who initiated the action
            session_id: Session identifier
            input_data: Input data for the action
            output_data: Output data from the action
            execution_time_ms: Execution time in milliseconds
            status: Action status (SUCCESS, ERROR, WARNING)
            error_message: Error message if status is ERROR
            metadata: Additional metadata
            
        Returns:
            str: Unique audit log ID
        """
        log_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        # Calculate data hashes
        input_hash = self._calculate_hash(json.dumps(input_data, sort_keys=True)) if input_data else None
        output_hash = self._calculate_hash(json.dumps(output_data, sort_keys=True)) if output_data else None
        
        # Get previous log hash for chain integrity
        previous_hash = self._get_previous_log_hash()
        
        # Create log entry data for hashing
        log_data = {
            'id': log_id,
            'timestamp': timestamp,
            'deal_id': deal_id,
            'agent_id': agent_id,
            'action_type': action_type,
            'action_description': action_description,
            'previous_log_hash': previous_hash
        }
        
        # Calculate current log hash
        log_hash = self._calculate_hash(json.dumps(log_data, sort_keys=True))
        
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO audit_log (
                    id, timestamp, deal_id, agent_id, action_type, action_description,
                    user_id, session_id, input_data_hash, output_data_hash,
                    execution_time_ms, status, error_message, metadata,
                    previous_log_hash, log_hash
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                log_id, timestamp, deal_id, agent_id, action_type, action_description,
                user_id, session_id, input_hash, output_hash,
                execution_time_ms, status, error_message,
                json.dumps(metadata) if metadata else None,
                previous_hash, log_hash
            ))
            conn.commit()
        
        return log_id
    
    def log_data_lineage(self,
                        audit_log_id: str,
                        source_type: str,
                        source_id: str,
                        transformation_type: str,
                        transformation_description: Optional[str] = None,
                        input_schema: Optional[Dict[str, Any]] = None,
                        output_schema: Optional[Dict[str, Any]] = None,
                        data_quality_score: Optional[float] = None) -> str:
        """
        Log data lineage information for tracking data transformations.
        
        Args:
            audit_log_id: Associated audit log entry ID
            source_type: Type of data source (e.g., 'API', 'FILE', 'DATABASE')
            source_id: Identifier of the data source
            transformation_type: Type of transformation applied
            transformation_description: Detailed description of transformation
            input_schema: Schema of input data
            output_schema: Schema of output data
            data_quality_score: Quality score of the data (0.0 to 1.0)
            
        Returns:
            str: Unique lineage ID
        """
        lineage_id = str(uuid.uuid4())
        
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO data_lineage (
                    id, audit_log_id, source_type, source_id, transformation_type,
                    transformation_description, input_schema, output_schema, data_quality_score
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                lineage_id, audit_log_id, source_type, source_id, transformation_type,
                transformation_description,
                json.dumps(input_schema) if input_schema else None,
                json.dumps(output_schema) if output_schema else None,
                data_quality_score
            ))
            conn.commit()
        
        return lineage_id
    
    def log_agent_decision(self,
                          audit_log_id: str,
                          decision_type: str,
                          decision_criteria: Optional[str] = None,
                          confidence_score: Optional[float] = None,
                          alternatives_considered: Optional[List[str]] = None,
                          risk_assessment: Optional[Dict[str, Any]] = None) -> str:
        """
        Log agent decision-making process for transparency.
        
        Args:
            audit_log_id: Associated audit log entry ID
            decision_type: Type of decision made
            decision_criteria: Criteria used for decision
            confidence_score: Confidence in the decision (0.0 to 1.0)
            alternatives_considered: List of alternatives considered
            risk_assessment: Risk assessment for the decision
            
        Returns:
            str: Unique decision ID
        """
        decision_id = str(uuid.uuid4())
        
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO agent_decisions (
                    id, audit_log_id, decision_type, decision_criteria,
                    confidence_score, alternatives_considered, risk_assessment
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                decision_id, audit_log_id, decision_type, decision_criteria,
                confidence_score,
                json.dumps(alternatives_considered) if alternatives_considered else None,
                json.dumps(risk_assessment) if risk_assessment else None
            ))
            conn.commit()
        
        return decision_id
    
    def log_system_event(self,
                        event_type: str,
                        event_description: str,
                        component: str,
                        configuration_before: Optional[Dict[str, Any]] = None,
                        configuration_after: Optional[Dict[str, Any]] = None,
                        triggered_by: Optional[str] = None) -> str:
        """
        Log system events and configuration changes.
        
        Args:
            event_type: Type of system event
            event_description: Description of the event
            component: System component affected
            configuration_before: Configuration before change
            configuration_after: Configuration after change
            triggered_by: Who or what triggered the event
            
        Returns:
            str: Unique event ID
        """
        event_id = str(uuid.uuid4())
        
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO system_events (
                    id, event_type, event_description, component,
                    configuration_before, configuration_after, triggered_by
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                event_id, event_type, event_description, component,
                json.dumps(configuration_before) if configuration_before else None,
                json.dumps(configuration_after) if configuration_after else None,
                triggered_by
            ))
            conn.commit()
        
        return event_id
    
    def verify_log_integrity(self) -> Dict[str, Any]:
        """
        Verify the integrity of the audit log chain.
        
        Returns:
            Dict containing integrity verification results
        """
        with self._get_connection() as conn:
            cursor = conn.execute("""
                SELECT id, timestamp, previous_log_hash, log_hash,
                       deal_id, agent_id, action_type, action_description
                FROM audit_log 
                ORDER BY timestamp ASC
            """)
            
            logs = cursor.fetchall()
            
            integrity_results = {
                'total_logs': len(logs),
                'verified_logs': 0,
                'integrity_violations': [],
                'is_valid': True
            }
            
            previous_hash = None
            for log in logs:
                # Verify chain integrity
                if log['previous_log_hash'] != previous_hash:
                    integrity_results['integrity_violations'].append({
                        'log_id': log['id'],
                        'timestamp': log['timestamp'],
                        'issue': 'Chain integrity violation',
                        'expected_previous_hash': previous_hash,
                        'actual_previous_hash': log['previous_log_hash']
                    })
                    integrity_results['is_valid'] = False
                else:
                    integrity_results['verified_logs'] += 1
                
                previous_hash = log['log_hash']
            
            return integrity_results