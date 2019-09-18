from gui_utils.Qt import QtWidgets, QtCore, QtGui
from core.deadline_bootstrap import DeadlineConnection

import sys
import itertools
# sys.path.append(r"C:\extraLibs")

# import ptvsd; reload(ptvsd)


class BackgroundProcess(QtCore.QThread):

    emit_results = QtCore.Signal(list)

    def __init__(self, only_new_jobs=False, parent=None):
        super(BackgroundProcess, self).__init__(parent=parent)

        self._already_analyzed_jobs = list()
        self._deadline_connection = DeadlineConnection()
        if only_new_jobs:
            jobs_ids = self._deadline_connection.get_jobs_in_state("Active")
            self._already_analyzed_jobs = self._get_ids(jobs_ids)

    def reset_analyzed_jobs(self):
        self._already_analyzed_jobs = list()

    def run(self, *args, **kwargs):
        # ptvsd.debug_this_thread()
        jobs_ids = self._deadline_connection.get_jobs_in_state("Active")
        jobs_ids_set = set(self._get_ids(jobs_ids))

        if not self._already_analyzed_jobs:
            self.emit_results.emit(jobs_ids)
            self._already_analyzed_jobs = list(jobs_ids_set)
        else:
            difference_ids = list(jobs_ids_set.difference(set(self._already_analyzed_jobs)))
            # difference = list(itertools.ifilterfalse(lambda x: x in jobs_ids, self._already_analyzed_jobs)) + \
            #     list(itertools.ifilterfalse(lambda x: x in self._already_analyzed_jobs, jobs_ids))
            difference = self._get_jobs(jobs_ids, difference_ids)
            self.emit_results.emit(list(difference))
            self._already_analyzed_jobs.extend(list(jobs_ids_set))

    def _get_ids(self, jobs):
        ids = [job["_id"] for job in jobs]
        return ids

    def _get_jobs(self, jobs, ids):
        matched_jobs = list()
        for id in ids:
            for job in jobs:
                job_id = job.get("_id")
                if id == job_id:
                    matched_jobs.append(job)
        return matched_jobs

if __name__ == "__main__":
    bg = BackgroundProcess()
    bg.start()
    