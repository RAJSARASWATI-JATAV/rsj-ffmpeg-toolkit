#!/usr/bin/env python3
"""
RSJ-FFMPEG v2.2 Feature Tests
Comprehensive test suite for new features

Author: RAJSARASWATI JATAV
Version: 2.2.0
"""

import unittest
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from rsj_ffmpeg import (
    GPTDirector,
    MontageEngine,
    CloudProcessor,
    ContentAnalyzer
)
from rsj_ffmpeg.plugin_v2 import PluginManagerV2, PluginV2
from rsj_ffmpeg.video_templates import VideoTemplates
from automation.scheduler_v2 import AdvancedScheduler, Priority


class TestGPTDirector(unittest.TestCase):
    """Test GPT Director functionality"""
    
    def setUp(self):
        self.director = GPTDirector(config={})
    
    def test_initialization(self):
        """Test GPT Director initialization"""
        self.assertIsNotNone(self.director)
        self.assertEqual(len(self.director.templates), 4)
    
    def test_parse_with_rules(self):
        """Test rule-based prompt parsing"""
        prompt = "Create a cinematic video with slow motion"
        instructions = self.director._parse_with_rules(prompt)
        
        self.assertEqual(instructions['style'], 'cinematic')
        self.assertIn('slow_motion', instructions['effects'])
    
    def test_template_loading(self):
        """Test template loading"""
        templates = self.director.templates
        
        self.assertIn('highlight_reel', templates)
        self.assertIn('cinematic', templates)
        self.assertIn('vlog', templates)


class TestMontageEngine(unittest.TestCase):
    """Test Montage Engine functionality"""
    
    def setUp(self):
        self.engine = MontageEngine(config={})
    
    def test_initialization(self):
        """Test Montage Engine initialization"""
        self.assertIsNotNone(self.engine)
        self.assertGreater(len(self.engine.styles), 0)
    
    def test_styles_loaded(self):
        """Test style templates"""
        styles = self.engine.styles
        
        self.assertIn('cinematic', styles)
        self.assertIn('sports', styles)
        self.assertIn('music_video', styles)
    
    def test_transition_loading(self):
        """Test transition filters"""
        transitions = self.engine.transitions
        
        self.assertIn('fade', transitions)
        self.assertIn('wipe', transitions)


class TestCloudProcessor(unittest.TestCase):
    """Test Cloud Processor functionality"""
    
    def test_initialization(self):
        """Test Cloud Processor initialization"""
        cloud = CloudProcessor(provider="aws", credentials={})
        
        self.assertEqual(cloud.provider, "aws")
        self.assertIsNotNone(cloud.jobs)
    
    def test_job_id_generation(self):
        """Test job ID generation"""
        cloud = CloudProcessor(provider="aws", credentials={})
        
        job_id1 = cloud._generate_job_id("test1.mp4")
        job_id2 = cloud._generate_job_id("test2.mp4")
        
        self.assertNotEqual(job_id1, job_id2)
        self.assertEqual(len(job_id1), 16)


class TestContentAnalyzer(unittest.TestCase):
    """Test Content Analyzer functionality"""
    
    def setUp(self):
        self.analyzer = ContentAnalyzer(config={})
    
    def test_initialization(self):
        """Test Content Analyzer initialization"""
        self.assertIsNotNone(self.analyzer)
    
    def test_fps_parsing(self):
        """Test FPS parsing"""
        fps = self.analyzer._parse_fps("30/1")
        self.assertEqual(fps, 30.0)
        
        fps = self.analyzer._parse_fps("60000/1001")
        self.assertAlmostEqual(fps, 59.94, places=2)


class TestPluginSystemV2(unittest.TestCase):
    """Test Plugin System v2"""
    
    def setUp(self):
        self.manager = PluginManagerV2(plugins_dir="./test_plugins")
    
    def test_initialization(self):
        """Test Plugin Manager initialization"""
        self.assertIsNotNone(self.manager)
        self.assertEqual(len(self.manager.plugins), 0)
    
    def test_plugin_discovery(self):
        """Test plugin discovery"""
        plugins = self.manager.discover_plugins()
        self.assertIsInstance(plugins, list)


class TestVideoTemplates(unittest.TestCase):
    """Test Video Templates"""
    
    def setUp(self):
        self.templates = VideoTemplates(config={})
    
    def test_initialization(self):
        """Test Video Templates initialization"""
        self.assertIsNotNone(self.templates)
        self.assertGreater(len(self.templates.templates), 0)
    
    def test_template_info(self):
        """Test template information"""
        info = self.templates.get_template_info("youtube_intro")
        
        self.assertIsNotNone(info)
        self.assertEqual(info['duration'], 5)
        self.assertEqual(info['resolution'], "1920x1080")
    
    def test_list_templates(self):
        """Test listing templates"""
        template_list = self.templates.list_templates()
        
        self.assertIn('youtube_intro', template_list)
        self.assertIn('instagram_story', template_list)
        self.assertIn('tiktok_video', template_list)


class TestAdvancedScheduler(unittest.TestCase):
    """Test Advanced Scheduler"""
    
    def setUp(self):
        self.scheduler = AdvancedScheduler(max_workers=2)
    
    def tearDown(self):
        if self.scheduler.running:
            self.scheduler.stop()
    
    def test_initialization(self):
        """Test scheduler initialization"""
        self.assertIsNotNone(self.scheduler)
        self.assertEqual(self.scheduler.max_workers, 2)
    
    def test_job_scheduling(self):
        """Test job scheduling"""
        def test_job():
            return "completed"
        
        job_id = self.scheduler.schedule_job(
            job_id="test_job_1",
            function=test_job,
            priority=Priority.NORMAL
        )
        
        self.assertEqual(job_id, "test_job_1")
        self.assertIn(job_id, self.scheduler.jobs)
    
    def test_job_cancellation(self):
        """Test job cancellation"""
        def test_job():
            return "completed"
        
        job_id = self.scheduler.schedule_job(
            job_id="test_job_2",
            function=test_job
        )
        
        success = self.scheduler.cancel_job(job_id)
        self.assertTrue(success)
    
    def test_statistics(self):
        """Test statistics"""
        stats = self.scheduler.get_statistics()
        
        self.assertIn('total_jobs', stats)
        self.assertIn('completed', stats)
        self.assertIn('failed', stats)


class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    def test_full_workflow(self):
        """Test complete workflow"""
        # This would test a complete workflow
        # For now, just verify all components can be imported
        
        from rsj_ffmpeg import (
            RSJToolkit,
            GPTDirector,
            MontageEngine,
            CloudProcessor,
            ContentAnalyzer
        )
        
        toolkit = RSJToolkit()
        self.assertIsNotNone(toolkit)


def run_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("RSJ-FFMPEG v2.2 Test Suite")
    print("Author: RAJSARASWATI JATAV")
    print("="*60 + "\n")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestGPTDirector))
    suite.addTests(loader.loadTestsFromTestCase(TestMontageEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestCloudProcessor))
    suite.addTests(loader.loadTestsFromTestCase(TestContentAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestPluginSystemV2))
    suite.addTests(loader.loadTestsFromTestCase(TestVideoTemplates))
    suite.addTests(loader.loadTestsFromTestCase(TestAdvancedScheduler))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*60 + "\n")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)