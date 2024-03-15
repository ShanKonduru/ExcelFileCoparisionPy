import time

class PerformanceMetrics:
    _timers = {}

    @classmethod
    def start(cls, token):
        if token in cls._timers:
            print("Error: Timer with token '{}' already exists.".format(token))
            return
        cls._timers[token] = time.time()

    @classmethod
    def stop(cls, token):
        if token not in cls._timers:
            print("Error: Timer with token '{}' does not exist.".format(token))
            return
        elapsed_time = time.time() - cls._timers.pop(token)
        print("Token '{}': {:.6f} seconds".format(token, elapsed_time))

if __name__ == "__main__":
    # Example usage
    PerformanceMetrics.start("TokenString1")
    time.sleep(1)  # Simulate some process
    PerformanceMetrics.start("TokenString2")
    time.sleep(2)  # Simulate some nested process
    PerformanceMetrics.start("TokenString3")
    time.sleep(0.5)  # Simulate some nested process
    PerformanceMetrics.stop("TokenString3")
    time.sleep(1)  # Simulate some more nested process
    PerformanceMetrics.stop("TokenString2")
    time.sleep(1)  # Simulate some more process
    PerformanceMetrics.stop("TokenString1")
