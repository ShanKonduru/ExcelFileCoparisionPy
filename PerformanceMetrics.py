import sys
import time

class PerformanceMetrics:
    def __init__(self):
        self._timers = {}
        self._reports = []

    def start(self, token):
        if token in self._timers:
            print("Error: Timer with token '{}' already exists.".format(token))
            return
        self._timers[token] = time.time()

    def stop(self, token):
        if token not in self._timers:
            print("Error: Timer with token '{}' does not exist.".format(token))
            return
        elapsed_time = time.time() - self._timers.pop(token)
        elapsed_time_string = "Elapsed time for '{}': {:.6f} seconds".format(token, elapsed_time)
        self._reports.append(elapsed_time_string)
        return elapsed_time

    def report(self, save_to_file=True):
        html_report = "<html><head><title>Performance Metrics Report</title></head><body>"
        for elapsed_time_string in self._reports:
            html_report += "<p>{}</p>".format(elapsed_time_string)
        html_report += "</body></html>"
        if save_to_file:
            self.save_report_to_html(html_report, file_path="performance_report.html")
        else:
            for elapsed_time_string in self._reports:
                print (elapsed_time_string)
        
        return html_report

    def save_report_to_html(self, html_report, file_path="performance_report.html"):
        with open(file_path, "w") as file:
            file.write(html_report)

def main():
    performance_metrics = PerformanceMetrics()
    performance_metrics.start(token="TokenString1")
    time.sleep(1)  # Simulate some process
    performance_metrics.start(token="TokenString2")
    time.sleep(2)  # Simulate some nested process
    performance_metrics.start(token="TokenString3")
    time.sleep(0.5)  # Simulate some nested process
    performance_metrics.stop(token="TokenString3")
    time.sleep(1)  # Simulate some more nested process
    performance_metrics.stop(token="TokenString2")
    time.sleep(1)  # Simulate some more process
    performance_metrics.stop(token="TokenString1")

    performance_metrics.report(save_to_file=False)
    # Save performance report to HTML
    # performance_metrics.save_report_to_html()

if __name__ == "__main__":
    main()
