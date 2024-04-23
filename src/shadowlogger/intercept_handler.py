import logging


class InterceptHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.logs = []

    def emit(self, record):
        # Capture the log
        log_entry = self.format(record)

        # Store all the information about the log
        self.logs.append({
            'name': record.name,
            'level': record.levelname,
            'message': log_entry,
            'module': record.module,
            'filename': record.filename,
            'lineno': record.lineno,
            'funcName': record.funcName,
            'created': record.created,
        })

    def get_latest_log(self):
        return self.logs[-1] if self.logs else None


class LogHandler:
    def handle(self, log):
        # Nicely format the log
        formatted_log = f"{log['name']} ({log['module']}:{log['lineno']}) {log['level']}: {log['message']}"
        print(formatted_log)
