"""
Test suite for the audit logging system.
"""

import unittest
import tempfile
import os
import json
from datetime import datetime
from .audit_logger import AuditLogger
from .audit_context import AuditContext

class TestAuditLogger(unittest.TestCase):
    """Test cases for the AuditLogger class."""
    
    def setUp(self):
        """Set up test environment with temporary database."""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_audit.db")
        self.audit_logger = AuditLogger(self.db_path)
    
    def tearDown(self):
        """Clean up test environment."""
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        os.rmdir(self.temp_dir)
    
    def test_database_initialization(self):
        """Test that the database is properly initialized."""
        # Check that database file exists
        self.assertTrue(os.path.exists(self.db_path))
        
        # Check that tables are created
        with self.audit_logger._get_connection() as conn:
            cursor = conn.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name IN ('audit_log', 'data_lineage', 'agent_decisions', 'system_events')
            """)
            tables = [row[0] for row in cursor.fetchall()]
            
            expected_tables = ['audit_log', 'data_lineage', 'agent_decisions', 'system_events']
            for table in expected_tables:
                self.assertIn(table, tables)
    
    def test_log_action_basic(self):
        """Test basic action logging functionality."""
        log_id = self.audit_logger.log_action(
            agent_id="test_agent",
            action_type="TEST_ACTION",
            action_description="Test action description",
            deal_id="deal_123",
            status="SUCCESS"
        )
        
        self.assertIsNotNone(log_id)
        self.assertIsInstance(log_id, str)
        
        # Verify the log was stored
        with self.audit_logger._get_connection() as conn:
            cursor = conn.execute("SELECT * FROM audit_log WHERE id = ?", (log_id,))
            log_entry = cursor.fetchone()
            
            self.assertIsNotNone(log_entry)
            self.assertEqual(log_entry['agent_id'], "test_agent")
            self.assertEqual(log_entry['action_type'], "TEST_ACTION")
            self.assertEqual(log_entry['deal_id'], "deal_123")
            self.assertEqual(log_entry['status'], "SUCCESS")
    
    def test_log_action_with_data(self):
        """Test action logging with input and output data."""
        input_data = {"param1": "value1", "param2": 123}
        output_data = {"result": "success", "score": 0.95}
        metadata = {"version": "1.0", "model": "test_model"}
        
        log_id = self.audit_logger.log_action(
            agent_id="test_agent",
            action_type="DATA_PROCESSING",
            action_description="Process test data",
            input_data=input_data,
            output_data=output_data,
            execution_time_ms=1500,
            metadata=metadata
        )
        
        # Verify data hashes are calculated
        with self.audit_logger._get_connection() as conn:
            cursor = conn.execute("SELECT * FROM audit_log WHERE id = ?", (log_id,))
            log_entry = cursor.fetchone()
            
            self.assertIsNotNone(log_entry['input_data_hash'])
            self.assertIsNotNone(log_entry['output_data_hash'])
            self.assertEqual(log_entry['execution_time_ms'], 1500)
            
            # Verify metadata is stored as JSON
            stored_metadata = json.loads(log_entry['metadata'])
            self.assertEqual(stored_metadata, metadata)
    
    def test_log_data_lineage(self):
        """Test data lineage logging."""
        # First create an audit log entry
        log_id = self.audit_logger.log_action(
            agent_id="test_agent",
            action_type="DATA_TRANSFORM",
            action_description="Transform data"
        )
        
        # Add lineage information
        input_schema = {"fields": ["name", "value"], "types": ["string", "number"]}
        output_schema = {"fields": ["processed_name", "normalized_value"], "types": ["string", "number"]}
        
        lineage_id = self.audit_logger.log_data_lineage(
            audit_log_id=log_id,
            source_type="API",
            source_id="external_api_v1",
            transformation_type="NORMALIZATION",
            transformation_description="Normalize field values",
            input_schema=input_schema,
            output_schema=output_schema,
            data_quality_score=0.92
        )
        
        self.assertIsNotNone(lineage_id)
        
        # Verify lineage was stored
        with self.audit_logger._get_connection() as conn:
            cursor = conn.execute("SELECT * FROM data_lineage WHERE id = ?", (lineage_id,))
            lineage_entry = cursor.fetchone()
            
            self.assertIsNotNone(lineage_entry)
            self.assertEqual(lineage_entry['audit_log_id'], log_id)
            self.assertEqual(lineage_entry['source_type'], "API")
            self.assertEqual(lineage_entry['transformation_type'], "NORMALIZATION")
            self.assertEqual(lineage_entry['data_quality_score'], 0.92)
            
            # Verify schemas are stored as JSON
            stored_input_schema = json.loads(lineage_entry['input_schema'])
            stored_output_schema = json.loads(lineage_entry['output_schema'])
            self.assertEqual(stored_input_schema, input_schema)
            self.assertEqual(stored_output_schema, output_schema)
    
    def test_log_agent_decision(self):
        """Test agent decision logging."""
        # First create an audit log entry
        log_id = self.audit_logger.log_action(
            agent_id="test_agent",
            action_type="DECISION_MAKING",
            action_description="Make strategic decision"
        )
        
        # Add decision information
        alternatives = ["option_a", "option_b", "option_c"]
        risk_assessment = {"high_risk": 0.2, "medium_risk": 0.5, "low_risk": 0.3}
        
        decision_id = self.audit_logger.log_agent_decision(
            audit_log_id=log_id,
            decision_type="RISK_ASSESSMENT",
            decision_criteria="Financial impact and probability",
            confidence_score=0.87,
            alternatives_considered=alternatives,
            risk_assessment=risk_assessment
        )
        
        self.assertIsNotNone(decision_id)
        
        # Verify decision was stored
        with self.audit_logger._get_connection() as conn:
            cursor = conn.execute("SELECT * FROM agent_decisions WHERE id = ?", (decision_id,))
            decision_entry = cursor.fetchone()
            
            self.assertIsNotNone(decision_entry)
            self.assertEqual(decision_entry['audit_log_id'], log_id)
            self.assertEqual(decision_entry['decision_type'], "RISK_ASSESSMENT")
            self.assertEqual(decision_entry['confidence_score'], 0.87)
            
            # Verify JSON fields
            stored_alternatives = json.loads(decision_entry['alternatives_considered'])
            stored_risk_assessment = json.loads(decision_entry['risk_assessment'])
            self.assertEqual(stored_alternatives, alternatives)
            self.assertEqual(stored_risk_assessment, risk_assessment)
    
    def test_log_system_event(self):
        """Test system event logging."""
        config_before = {"setting1": "value1", "setting2": 100}
        config_after = {"setting1": "new_value1", "setting2": 200}
        
        event_id = self.audit_logger.log_system_event(
            event_type="CONFIGURATION_CHANGE",
            event_description="Updated system configuration",
            component="api_gateway",
            configuration_before=config_before,
            configuration_after=config_after,
            triggered_by="admin_user"
        )
        
        self.assertIsNotNone(event_id)
        
        # Verify event was stored
        with self.audit_logger._get_connection() as conn:
            cursor = conn.execute("SELECT * FROM system_events WHERE id = ?", (event_id,))
            event_entry = cursor.fetchone()
            
            self.assertIsNotNone(event_entry)
            self.assertEqual(event_entry['event_type'], "CONFIGURATION_CHANGE")
            self.assertEqual(event_entry['component'], "api_gateway")
            self.assertEqual(event_entry['triggered_by'], "admin_user")
            
            # Verify configuration JSON
            stored_before = json.loads(event_entry['configuration_before'])
            stored_after = json.loads(event_entry['configuration_after'])
            self.assertEqual(stored_before, config_before)
            self.assertEqual(stored_after, config_after)
    
    def test_log_integrity_chain(self):
        """Test that log entries maintain chain integrity."""
        # Create multiple log entries
        log_ids = []
        for i in range(3):
            log_id = self.audit_logger.log_action(
                agent_id=f"agent_{i}",
                action_type="TEST_ACTION",
                action_description=f"Test action {i}"
            )
            log_ids.append(log_id)
        
        # Verify chain integrity
        integrity_results = self.audit_logger.verify_log_integrity()
        
        self.assertTrue(integrity_results['is_valid'])
        self.assertEqual(integrity_results['total_logs'], 3)
        self.assertEqual(integrity_results['verified_logs'], 3)
        self.assertEqual(len(integrity_results['integrity_violations']), 0)
    
    def test_hash_calculation(self):
        """Test hash calculation consistency."""
        data1 = {"key": "value", "number": 123}
        data2 = {"number": 123, "key": "value"}  # Same data, different order
        
        hash1 = self.audit_logger._calculate_hash(json.dumps(data1, sort_keys=True))
        hash2 = self.audit_logger._calculate_hash(json.dumps(data2, sort_keys=True))
        
        # Hashes should be identical for same data regardless of order
        self.assertEqual(hash1, hash2)
        
        # Different data should produce different hashes
        data3 = {"key": "different_value", "number": 123}
        hash3 = self.audit_logger._calculate_hash(json.dumps(data3, sort_keys=True))
        self.assertNotEqual(hash1, hash3)

class TestAuditContext(unittest.TestCase):
    """Test cases for the AuditContext class."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_audit_context.db")
        self.audit_logger = AuditLogger(self.db_path)
        self.audit_context = AuditContext(self.audit_logger)
    
    def tearDown(self):
        """Clean up test environment."""
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        os.rmdir(self.temp_dir)
    
    def test_context_manager_success(self):
        """Test successful operation with context manager."""
        input_data = {"test": "data"}
        output_data = {"result": "success"}
        
        with self.audit_context.log_operation(
            agent_id="test_agent",
            action_type="TEST_OPERATION",
            action_description="Test context manager",
            input_data=input_data
        ) as audit_log:
            # Simulate operation
            audit_log.set_output(output_data)
            audit_log.add_lineage("FILE", "test.csv", "DATA_LOAD", "Load test data")
            audit_log.add_decision("THRESHOLD_SELECTION", "Statistical analysis", 0.95)
        
        # Verify log was created
        with self.audit_logger._get_connection() as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM audit_log WHERE agent_id = 'test_agent'")
            count = cursor.fetchone()[0]
            self.assertEqual(count, 1)
            
            # Verify lineage was created
            cursor = conn.execute("SELECT COUNT(*) FROM data_lineage")
            lineage_count = cursor.fetchone()[0]
            self.assertEqual(lineage_count, 1)
            
            # Verify decision was created
            cursor = conn.execute("SELECT COUNT(*) FROM agent_decisions")
            decision_count = cursor.fetchone()[0]
            self.assertEqual(decision_count, 1)
    
    def test_context_manager_error(self):
        """Test error handling with context manager."""
        with self.assertRaises(ValueError):
            with self.audit_context.log_operation(
                agent_id="test_agent",
                action_type="ERROR_TEST",
                action_description="Test error handling"
            ) as audit_log:
                raise ValueError("Test error")
        
        # Verify error was logged
        with self.audit_logger._get_connection() as conn:
            cursor = conn.execute("SELECT status, error_message FROM audit_log WHERE agent_id = 'test_agent'")
            result = cursor.fetchone()
            
            self.assertEqual(result['status'], "ERROR")
            self.assertEqual(result['error_message'], "Test error")

if __name__ == '__main__':
    unittest.main()