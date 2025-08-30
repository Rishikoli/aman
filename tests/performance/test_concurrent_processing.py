"""
Performance tests for concurrent deal processing
"""
import pytest
import asyncio
import time
import threading
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from unittest.mock import Mock, patch
import sys
import os
import psutil
import statistics

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'agents'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))
cl
ass TestConcurrentProcessing:
    
    @pytest.fixture
    def system_monitor(self):
        """System resource monitoring fixture"""
        class SystemMonitor:
            def __init__(self):
                self.initial_cpu = psutil.cpu_percent()
                self.initial_memory = psutil.virtual_memory().percent
                self.peak_cpu = 0
                self.peak_memory = 0
            
            def update_peaks(self):
                current_cpu = psutil.cpu_percent()
                current_memory = psutil.virtual_memory().percent
                self.peak_cpu = max(self.peak_cpu, current_cpu)
                self.peak_memory = max(self.peak_memory, current_memory)
            
            def get_resource_usage(self):
                return {
                    'peak_cpu': self.peak_cpu,
                    'peak_memory': self.peak_memory,
                    'cpu_increase': self.peak_cpu - self.initial_cpu,
                    'memory_increase': self.peak_memory - self.initial_memory
                }
        
        return SystemMonitor()
    
    @pytest.fixture
    def mock_deal_data(self):
        """Generate mock deal data for performance testing"""
        def generate_deal(deal_id):
            return {
                'deal_id': f'perf-test-{deal_id}',
                'acquirer': f'Acquirer Corp {deal_id}',
                'target': f'Target Corp {deal_id}',
                'deal_value': 1000000000 + (deal_id * 100000000),
                'analysis_scope': ['financial', 'legal', 'synergy', 'reputation', 'operations']
            }
        return generate_deal
    
    @pytest.mark.performance
    def test_concurrent_deal_processing_throughput(self, mock_deal_data, system_monitor, performance_timer):
        """Test system throughput with multiple concurrent deals"""
        
        async def mock_agent_analysis(agent_type, deal_id, processing_time=0.1):
            """Mock agent analysis with configurable processing time"""
            await asyncio.sleep(processing_time)
            return {
                'agent_type': agent_type,
                'deal_id': deal_id,
                'risk_score': 30 + (hash(f"{agent_type}{deal_id}") % 40),
                'processing_time': processing_time,
                'status': 'completed'
            }
        
        async def process_deal(deal_id):
            """Process a single deal with all agents"""
            agents = ['financial', 'legal', 'synergy', 'reputation', 'operations']
            
            # Execute all agents for this deal concurrently
            tasks = [mock_agent_analysis(agent, deal_id, 0.05) for agent in agents]
            results = await asyncio.gather(*tasks)
            
            return {
                'deal_id': deal_id,
                'status': 'completed',
                'agent_results': results,
                'total_agents': len(results)
            }
        
        async def concurrent_deal_processing(num_deals):
            """Process multiple deals concurrently"""
            performance_timer.start()
            
            # Create tasks for all deals
            deal_tasks = [process_deal(i) for i in range(num_deals)]
            
            # Monitor system resources during processing
            monitor_task = asyncio.create_task(self._monitor_resources(system_monitor))
            
            # Execute all deals concurrently
            deal_results = await asyncio.gather(*deal_tasks)
            
            # Stop monitoring
            monitor_task.cancel()
            
            performance_timer.stop()
            
            return deal_results
        
        # Test with different concurrency levels
        concurrency_tests = [5, 10, 20]
        results = {}
        
        for num_deals in concurrency_tests:
            deal_results = asyncio.run(concurrent_deal_processing(num_deals))
            
            # Calculate performance metrics
            total_time = performance_timer.elapsed_seconds
            throughput = num_deals / total_time if total_time > 0 else 0
            
            results[num_deals] = {
                'total_deals': len(deal_results),
                'successful_deals': len([d for d in deal_results if d['status'] == 'completed']),
                'total_time': total_time,
                'throughput': throughput,
                'resource_usage': system_monitor.get_resource_usage()
            }
            
            # Verify all deals completed successfully
            assert len(deal_results) == num_deals
            assert all(deal['status'] == 'completed' for deal in deal_results)
            assert all(len(deal['agent_results']) == 5 for deal in deal_results)
        
        # Verify throughput scales reasonably
        assert results[5]['throughput'] > 0
        assert results[10]['throughput'] > 0
        assert results[20]['throughput'] > 0
        
        # Resource usage should be reasonable
        for num_deals, metrics in results.items():
            assert metrics['resource_usage']['peak_cpu'] < 90  # Should not max out CPU
            assert metrics['resource_usage']['peak_memory'] < 90  # Should not max out memory
    
    async def _monitor_resources(self, system_monitor):
        """Continuously monitor system resources"""
        try:
            while True:
                system_monitor.update_peaks()
                await asyncio.sleep(0.1)
        except asyncio.CancelledError:
            pass
    
    @pytest.mark.performance
    def test_agent_processing_latency(self, performance_timer):
        """Test individual agent processing latency"""
        
        def mock_finance_agent_heavy(deal_data):
            """Mock finance agent with heavy processing"""
            # Simulate complex financial calculations
            time.sleep(0.2)  # 200ms processing time
            return {
                'risk_score': 25,
                'processing_time': 0.2,
                'calculations_performed': 1000
            }
        
        def mock_legal_agent_heavy(deal_data):
            """Mock legal agent with document processing"""
            # Simulate document analysis
            time.sleep(0.3)  # 300ms processing time
            return {
                'risk_score': 35,
                'processing_time': 0.3,
                'documents_processed': 50
            }
        
        # Test individual agent latencies
        agents = {
            'finance': mock_finance_agent_heavy,
            'legal': mock_legal_agent_heavy
        }
        
        latencies = {}
        deal_data = {'deal_id': 'latency-test', 'complexity': 'high'}
        
        for agent_name, agent_func in agents.items():
            performance_timer.start()
            result = agent_func(deal_data)
            performance_timer.stop()
            
            latencies[agent_name] = {
                'actual_latency': performance_timer.elapsed_seconds,
                'expected_latency': result['processing_time'],
                'result': result
            }
        
        # Verify latencies are within acceptable ranges
        for agent_name, metrics in latencies.items():
            assert metrics['actual_latency'] > 0
            assert metrics['actual_latency'] < 1.0  # Should complete within 1 second
            
            # Actual latency should be close to expected (within 50ms tolerance)
            latency_diff = abs(metrics['actual_latency'] - metrics['expected_latency'])
            assert latency_diff < 0.05  # 50ms tolerance
    
    @pytest.mark.performance
    def test_memory_usage_under_load(self, mock_deal_data, system_monitor):
        """Test memory usage patterns under heavy load"""
        
        def memory_intensive_analysis(deal_id, data_size_mb=10):
            """Simulate memory-intensive analysis"""
            # Create large data structures to simulate real analysis
            large_dataset = [i for i in range(data_size_mb * 100000)]  # ~10MB per deal
            
            # Simulate processing
            processed_data = {
                'deal_id': deal_id,
                'data_points': len(large_dataset),
                'analysis_result': sum(large_dataset) / len(large_dataset),
                'memory_footprint_mb': data_size_mb
            }
            
            # Clean up large dataset
            del large_dataset
            
            return processed_data
        
        # Monitor memory before test
        initial_memory = psutil.virtual_memory().percent
        
        # Process multiple deals with memory-intensive operations
        results = []
        for i in range(10):
            system_monitor.update_peaks()
            result = memory_intensive_analysis(i, 5)  # 5MB per deal
            results.append(result)
        
        final_memory = psutil.virtual_memory().percent
        peak_memory = system_monitor.peak_memory
        
        # Verify memory usage
        assert len(results) == 10
        memory_increase = peak_memory - initial_memory
        
        # Memory increase should be reasonable (less than 20% for this test)
        assert memory_increase < 20
        
        # Memory should not continuously grow (indicating memory leaks)
        assert final_memory <= peak_memory
    
    @pytest.mark.performance
    def test_database_connection_pooling(self):
        """Test database connection pooling under concurrent load"""
        
        class MockDatabasePool:
            def __init__(self, max_connections=10):
                self.max_connections = max_connections
                self.active_connections = 0
                self.total_requests = 0
                self.connection_waits = []
            
            def get_connection(self):
                self.total_requests += 1
                wait_time = 0
                
                if self.active_connections >= self.max_connections:
                    # Simulate waiting for available connection
                    wait_time = 0.01  # 10ms wait
                    time.sleep(wait_time)
                
                self.active_connections += 1
                self.connection_waits.append(wait_time)
                return f"connection_{self.active_connections}"
            
            def release_connection(self, connection):
                self.active_connections = max(0, self.active_connections - 1)
            
            def get_stats(self):
                return {
                    'total_requests': self.total_requests,
                    'max_concurrent': max(10 - len([w for w in self.connection_waits if w == 0]), 0),
                    'average_wait_time': statistics.mean(self.connection_waits) if self.connection_waits else 0,
                    'connection_waits': len([w for w in self.connection_waits if w > 0])
                }
        
        def database_operation(db_pool, operation_id):
            """Simulate database operation"""
            conn = db_pool.get_connection()
            
            # Simulate query execution
            time.sleep(0.02)  # 20ms query time
            
            result = {
                'operation_id': operation_id,
                'connection': conn,
                'status': 'completed'
            }
            
            db_pool.release_connection(conn)
            return result
        
        # Test with different pool sizes
        pool_sizes = [5, 10, 20]
        concurrent_operations = 50
        
        for pool_size in pool_sizes:
            db_pool = MockDatabasePool(max_connections=pool_size)
            
            # Execute concurrent database operations
            with ThreadPoolExecutor(max_workers=concurrent_operations) as executor:
                futures = [
                    executor.submit(database_operation, db_pool, i) 
                    for i in range(concurrent_operations)
                ]
                
                results = [future.result() for future in futures]
            
            stats = db_pool.get_stats()
            
            # Verify all operations completed
            assert len(results) == concurrent_operations
            assert all(r['status'] == 'completed' for r in results)
            
            # Verify connection pooling efficiency
            assert stats['total_requests'] == concurrent_operations
            
            # Smaller pools should have more connection waits
            if pool_size < concurrent_operations:
                assert stats['connection_waits'] > 0
    
    @pytest.mark.performance
    @pytest.mark.slow
    def test_stress_testing_system_limits(self, mock_deal_data, system_monitor, performance_timer):
        """Stress test to find system limits"""
        
        async def stress_test_scenario(num_deals, agents_per_deal, processing_time):
            """Execute stress test scenario"""
            
            async def heavy_agent_processing(agent_id, deal_id):
                # Simulate CPU-intensive processing
                await asyncio.sleep(processing_time)
                
                # Simulate some CPU work
                result = sum(i * i for i in range(1000))
                
                return {
                    'agent_id': agent_id,
                    'deal_id': deal_id,
                    'result': result,
                    'processing_time': processing_time
                }
            
            # Create all tasks
            all_tasks = []
            for deal_id in range(num_deals):
                for agent_id in range(agents_per_deal):
                    task = heavy_agent_processing(f"agent_{agent_id}", f"deal_{deal_id}")
                    all_tasks.append(task)
            
            # Execute all tasks concurrently
            performance_timer.start()
            results = await asyncio.gather(*all_tasks)
            performance_timer.stop()
            
            return results
        
        # Progressive stress test scenarios
        stress_scenarios = [
            {'deals': 10, 'agents': 5, 'processing_time': 0.01},   # Light load
            {'deals': 25, 'agents': 5, 'processing_time': 0.02},   # Medium load
            {'deals': 50, 'agents': 5, 'processing_time': 0.01},   # High concurrency
        ]
        
        stress_results = {}
        
        for i, scenario in enumerate(stress_scenarios):
            system_monitor.update_peaks()
            
            try:
                results = asyncio.run(stress_test_scenario(
                    scenario['deals'], 
                    scenario['agents'], 
                    scenario['processing_time']
                ))
                
                total_tasks = scenario['deals'] * scenario['agents']
                execution_time = performance_timer.elapsed_seconds
                throughput = total_tasks / execution_time if execution_time > 0 else 0
                
                stress_results[f"scenario_{i+1}"] = {
                    'scenario': scenario,
                    'total_tasks': total_tasks,
                    'completed_tasks': len(results),
                    'execution_time': execution_time,
                    'throughput': throughput,
                    'success_rate': len(results) / total_tasks,
                    'resource_usage': system_monitor.get_resource_usage()
                }
                
                # Verify all tasks completed
                assert len(results) == total_tasks
                
            except Exception as e:
                # Record failure point
                stress_results[f"scenario_{i+1}"] = {
                    'scenario': scenario,
                    'status': 'failed',
                    'error': str(e),
                    'resource_usage': system_monitor.get_resource_usage()
                }
        
        # Analyze stress test results
        successful_scenarios = [r for r in stress_results.values() if r.get('status') != 'failed']
        
        # Should handle at least the light and medium load scenarios
        assert len(successful_scenarios) >= 2
        
        # Throughput should generally increase with lighter processing times
        if len(successful_scenarios) >= 2:
            scenario_1 = successful_scenarios[0]
            scenario_2 = successful_scenarios[1]
            
            # Resource usage should scale with load
            assert scenario_2['resource_usage']['peak_cpu'] >= scenario_1['resource_usage']['peak_cpu']
    
    @pytest.mark.performance
    def test_api_response_times(self):
        """Test API endpoint response times under load"""
        
        def mock_api_endpoint(endpoint_type, request_data):
            """Mock API endpoint with realistic processing times"""
            processing_times = {
                'create_deal': 0.05,      # 50ms
                'get_deal_status': 0.01,  # 10ms
                'get_deal_results': 0.03, # 30ms
                'search_deals': 0.02      # 20ms
            }
            
            processing_time = processing_times.get(endpoint_type, 0.02)
            time.sleep(processing_time)
            
            return {
                'endpoint': endpoint_type,
                'status': 'success',
                'processing_time': processing_time,
                'data': request_data
            }
        
        # Test different API endpoints under concurrent load
        endpoints = ['create_deal', 'get_deal_status', 'get_deal_results', 'search_deals']
        concurrent_requests = 20
        
        response_times = {}
        
        for endpoint in endpoints:
            with ThreadPoolExecutor(max_workers=concurrent_requests) as executor:
                start_time = time.time()
                
                # Submit concurrent requests
                futures = [
                    executor.submit(mock_api_endpoint, endpoint, {'request_id': i})
                    for i in range(concurrent_requests)
                ]
                
                # Collect results
                results = [future.result() for future in futures]
                
                end_time = time.time()
                total_time = end_time - start_time
                
                response_times[endpoint] = {
                    'total_requests': len(results),
                    'successful_requests': len([r for r in results if r['status'] == 'success']),
                    'total_time': total_time,
                    'average_response_time': total_time / len(results),
                    'requests_per_second': len(results) / total_time
                }
        
        # Verify API performance requirements
        for endpoint, metrics in response_times.items():
            assert metrics['successful_requests'] == concurrent_requests
            assert metrics['average_response_time'] < 0.5  # Should average under 500ms
            assert metrics['requests_per_second'] > 10     # Should handle at least 10 RPS
    
    @pytest.mark.performance
    def test_cache_performance_impact(self):
        """Test performance impact of caching mechanisms"""
        
        class MockCache:
            def __init__(self):
                self.cache = {}
                self.hits = 0
                self.misses = 0
            
            def get(self, key):
                if key in self.cache:
                    self.hits += 1
                    return self.cache[key]
                else:
                    self.misses += 1
                    return None
            
            def set(self, key, value):
                self.cache[key] = value
            
            def get_stats(self):
                total_requests = self.hits + self.misses
                hit_rate = self.hits / total_requests if total_requests > 0 else 0
                return {
                    'hits': self.hits,
                    'misses': self.misses,
                    'hit_rate': hit_rate,
                    'cache_size': len(self.cache)
                }
        
        def expensive_operation(cache, operation_id):
            """Simulate expensive operation with caching"""
            cache_key = f"operation_{operation_id % 10}"  # 10 unique operations
            
            # Check cache first
            cached_result = cache.get(cache_key)
            if cached_result:
                return cached_result
            
            # Simulate expensive computation
            time.sleep(0.1)  # 100ms expensive operation
            
            result = {
                'operation_id': operation_id,
                'result': operation_id * operation_id,
                'computed': True
            }
            
            # Cache the result
            cache.set(cache_key, result)
            
            return result
        
        # Test with and without caching
        cache = MockCache()
        num_operations = 50
        
        # Execute operations (some will be cache hits due to modulo)
        start_time = time.time()
        
        results = []
        for i in range(num_operations):
            result = expensive_operation(cache, i)
            results.append(result)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        cache_stats = cache.get_stats()
        
        # Verify caching effectiveness
        assert len(results) == num_operations
        assert cache_stats['hits'] > 0  # Should have some cache hits
        assert cache_stats['hit_rate'] > 0.5  # Should have good hit rate due to modulo
        
        # With caching, should be faster than if all operations were computed
        max_expected_time = num_operations * 0.1  # If no caching
        assert total_time < max_expected_time * 0.7  # Should be at least 30% faster