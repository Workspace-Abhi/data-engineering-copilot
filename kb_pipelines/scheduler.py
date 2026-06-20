"""Scheduler service for running scheduled ingestion pipelines with persistence state logs."""
import os
import json
import time
from typing import Dict, List, Callable, Optional
from config.settings import BASE_DIR
from config.logging_config import get_logger

logger = get_logger("scheduler")

class PipelineScheduler:
    """Manages scheduled pipelines and persists state log info."""

    def __init__(self):
        self.state_file = os.path.join(BASE_DIR, "logs", "scheduler_state.json")
        self.jobs = {}
        self.load_state()

    def load_state(self):
        """Load job execute run records from JSON log."""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r") as f:
                    self.jobs = json.load(f)
            except Exception as e:
                logger.error(f"Failed to load scheduler state: {e}")
                self.jobs = {}

    def save_state(self):
        """Save job execute run records to JSON log."""
        try:
            os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
            with open(self.state_file, "w") as f:
                json.dump(self.jobs, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save scheduler state: {e}")

    def schedule_job(self, job_name: str, schedule: str, task: Callable[[], Dict]):
        """Schedule and run a pipeline ingestion task."""
        logger.info(f"Scheduling task: {job_name} ({schedule})...")
        
        # Simulate execution
        try:
            result = task()
            status = "Success" if result.get("success", False) else "Failed"
            msg = result.get("error", "Task run completed.")
        except Exception as e:
            status = "Error"
            msg = str(e)
            
        self.jobs[job_name] = {
            "schedule": schedule,
            "last_run": time.strftime("%Y-%m-%d %H:%M:%S"),
            "status": status,
            "message": msg
        }
        self.save_state()


def get_scheduler() -> PipelineScheduler:
    """Get Pipeline Scheduler instance."""
    return PipelineScheduler()
