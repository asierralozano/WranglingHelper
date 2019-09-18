DEADLINE_HOST = "SPA351W"
DEADLINE_PORT = 8082


import sys

# TODO::: Add env var
try:
    from Deadline.DeadlineConnect import DeadlineCon
except:
    sys.path.append("T:/deadline/DeadlineRepository10/api/python")
    from Deadline.DeadlineConnect import DeadlineCon

# from pprint import pprint


class DeadlineConnection(object):

    def __init__(self, host=None, port=None):

        if not host:
            host = DEADLINE_HOST

        if not port:
            port = DEADLINE_PORT

        self._host = host
        self._port = port

        self.deadline_connection = DeadlineCon(host, port)

    def get_slaves(self, group=None, pool=None):
        if group:
            return self.deadline_connection.Slaves.GetSlaveNamesInGroup(group=group)
        elif pool:
            return self.deadline_connection.Slaves.GetSlaveNamesInPool(pool=pool)
        else:
            return self.deadline_connection.Slaves.GetSlaveNames()

    def get_slave_infos(self, names=None):
        return self.deadline_connection.Slaves.GetSlaveInfos(names=names)

    def get_slave_reports(self, name):
        return self.deadline_connection.Slaves.GetSlaveReports(name=name)


    def get_job(self, job_id):
        found_job = self.deadline_connection.Jobs.GetJob(job_id)
        if found_job:
            return found_job
        return None
    
    def get_jobs(self, ids=None):
        jobs = self.deadline_connection.Jobs.GetJobs(ids=ids)
        return jobs

    def get_jobs_in_state(self, state=None):
        if isinstance(state, list):
            state = ",".join(state)
        jobs = self.deadline_connection.Jobs.GetJobsInState(state=state)
        return jobs

    def get_job_details(self, ids):
        job_details = self.deadline_connection.Jobs.GetJobDetails(ids=ids)
        return job_details

    def get_job_ids(self):
        job_ids = self.deadline_connection.Jobs.GetJobIds()
        return job_ids

    def get_deleted_jobs_ids(self):
        job_ids = self.deadline_connection.Jobs.GetDeletedJobIDs()
        return job_ids

    def get_group_names(self):
        groups = self.deadline_connection.Groups.GetGroupNames()
        return groups
        
    def get_pools(self):
        pools = self.deadline_connection.Pools.GetPoolNames()
        if pools:
            return pools
        return None

    def submit_job(self, submit_params, plugin_params):
        job = self.deadline_connection.Jobs.SubmitJob(submit_params, plugin_params)
        if job:
            return job
        return None