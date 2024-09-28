from threading import Lock

class ProgressTracker:
    def __init__(self):
        self.progress = 0
        self.lock = Lock()

    def update_progress(self, current, total):
        with self.lock:
            self.progress = min(int((current / total) * 100), 100)

    def get_progress(self):
        with self.lock:
            return self.progress

progress_tracker = ProgressTracker()