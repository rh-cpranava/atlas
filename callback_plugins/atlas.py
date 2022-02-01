# 2022 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = '''
    author: Chandrahasa Pranava
    name: atlas
    type: stdout
    requirements:
      - set as main display callback
    short_description: print code coverage for an Ansible run
    description:
      - This callback allows users to determine the total number of tasks that have been executed by an Ansible run
      - Information is displayed as stdout at the end of each Ansible execution 
'''

EXAMPLES = """
"""

from ansible import constants as C
from ansible.plugins.callback import CallbackBase

def determine_code_coverage(total_tasks, run_tasks):
    if run_tasks > total_tasks:
        coverage = 100.0
    elif total_tasks > 0:
        coverage = run_tasks * 100.0 / total_tasks
    elif run_tasks == 0:
        coverage = 0.0
    return coverage 

class CallbackModule(CallbackBase):
    """atlas.py callback plugin."""

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'aggregate'
    CALLBACK_NAME = 'atlas'
    def __init__(self, display=None):
         """selective.py callback plugin."""
         super(CallbackModule, self).__init__(display)
         self.total_tasks = 0
         self.run_tasks = 0
         self.play_dict = []

    def v2_playbook_on_play_start(self, play):
        self._play = play

    def v2_playbook_on_start(self, playbook):
        self.plays = playbook.get_plays()
        for i in self.plays:
            play_total_tasks = len(i.get_tasks()[0])
            name = i.get_name().strip()
            self.play_dict.append({"name": name, "play_total_tasks": play_total_tasks})

    def v2_playbook_on_task_start(self, task, **kwargs):
        """Run when a task starts."""
        self.run_tasks += 1

    def v2_playbook_on_stats(self, stats):
        self._display.display("", screen_only=True)
        self._display.display('************** Atlas Results **************', color='yellow')
        self.total_tasks = sum([ len(i.get_tasks()[0]) for i in self.plays])
        self.display_stats = self.run_tasks
        self.coverage = determine_code_coverage(self.total_tasks, self.run_tasks)
        self._display.display('Total Coverage  : %.0f%% (%d of %d tasks are tested)' % (self.coverage, self.run_tasks, self.total_tasks), color='yellow')
        self._display.display("", screen_only=True)
        self._display.display('***** Play Wise Breakdown *****', color='yellow')
        sum_tasks = 0 
        for i in self.play_dict:
            sum_tasks += i["play_total_tasks"]
            code_coverage_sum = abs(self.run_tasks - sum_tasks) 
            self._display.display('Play name: {0}'.format(i["name"]), color='yellow')
            self._display.display('Play Tasks: {0}'.format(i["play_total_tasks"]), color='yellow')
            if code_coverage_sum < 0:
                self._display.display('Tasks Executed: {0}'.format(i["play_total_tasks"]), color='yellow')
                self._display.display('Coverage  : 100%'.format(), color='yellow')
            else:
                self._display.display('Tasks Executed: {0}'.format(code_coverage_sum), color='yellow')
                task_coverage = determine_code_coverage(i["play_total_tasks"], abs(code_coverage_sum))
                self._display.display('Coverage  : %.0f%%' % (task_coverage), color='yellow')
            self._display.display('*****', color='yellow')
        self._display.display('************** Atlas End ******************', color='yellow')
