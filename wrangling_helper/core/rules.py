from core.deadline_bootstrap import DeadlineConnection

# from spa_logger import qlogger

# logger = qlogger.getQLogger("AutoWrangling")


class Rule(object):

    def __init__(self, rules, options):
        """This class describes a rule that will try to match and apply some options
        The rule is built with some rules (list of some filters like 'User is Alberto' or 'Dept is comp')
        and some options (like MachineLimit = 5, or ConcurrentTasks -= 5).
        In order to apply the options, the rules must match with a Job
        
        Args:
            rules (list): List of tuples with rules
            Ex:
                [
                    "User", 
                    "is", 
                    "asierra", 
                    false
                ]
            options (dict): Dictionary with all the options
            Ex:
                {
                    "Props":{
                        "Dept":"nuke"
                        "MachLmt" : 5
                    }
                }
        """
        self._rules = rules
        self._options = options

    @property
    def rules(self):
        return self._rules

    @property
    def options(self):
        return self._options

    def update_rules(self, new_rules):
        """Update the rules of the ``Rule`` object with the new rules
        
        Args:
            new_rules (list): list of tuples with the rules
        """
        self._rules = new_rules

    def update_options(self, options):
        """Update the options of the ``Rule`` with the new options
        
        Args:
            options (dict): Dictionary with all the new options
        """
        self._options = options

    def job_match_rule(self, job):
        """This method will try to match the ``Rule`` rules, with the incoming job.
        It will iterate through all the rules, trying to match each other.
        If any of those rules does not match, then the job does not match this Rule
        
        Args:
            job (dict): Deadline job dictionary
        
        Returns:
            bool: Match status
        """
        match = True
        for rule in self.rules:
            key, operator, value, regex = rule
            job_value = job.get(key, job.get("Props").get(key, None))

            if not job_value:
                match = False
                return match

            if operator == "contains":
                match = value in job_value
            elif operator == "not contains":
                match = value not in job_value
            elif operator == "is":
                match = value == job_value
            elif operator == "is not":
                match = value != job_value
            
            if not match:
                return False
        return match

    def _apply_special_rule_option(self,job, key, value, deadline_connection):
        """There are some Options that requires some special behaviour.
        This method will handle all of these.
        
        Args:
            job (dict): Deadline job Dict
            key (str): Option key
            value (str): Option value
            deadline_connection (DeadlineCon): Deadline boostrap to the Deadline Repository
        
        Returns:
            bool: If the key is an special rule or not
        """
        id = job.get("_id")
        special_rule = False

        if key == "MachLmt":
            deadline_connection.deadline_connection.Jobs.SetJobMachineLimitMaximum(id, value)
            special_rule = True

        elif key == "Chunk":
            frames = job["Props"]["Frames"]
            deadline_connection.deadline_connection.Jobs.SetJobFrameRange(id, frames, value)
        
        return special_rule

    def apply_rule_options(self, job):
        """Apply the ``Rule`` options to the Job.
        This process will occur only if the Job matchs the ``Rule`` rules
        It will apply the options, save the Deadline Job (within the Deadline Database),
        and Resubmit the job
        
        Args:
            job (dict): Deadline Job dict
        """
        deadline_connection = DeadlineConnection()

        for k, v in self.options.iteritems():
            if isinstance(v, dict):
                for dk, dv in v.iteritems():
                    special_rule = self._apply_special_rule_option(job, dk, dv, deadline_connection)
                    job[k][dk] = dv
            else:
                job[k] = v
        deadline_connection.deadline_connection.Jobs.SaveJob(job)
        deadline_connection.deadline_connection.Jobs.RequeueJob(job.get("_id"))



    