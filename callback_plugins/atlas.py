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

    def v2_playbook_on_play_start(self, play):
        self._play = play
        self.total_tasks = len(self._play.get_tasks()[0])

    def v2_playbook_on_task_start(self, task, **kwargs):
        """Run when a task starts."""
        self.run_tasks += 1

    def v2_playbook_on_stats(self, stats):
        self._display.display('*** Atlas Results ***')
        if self.total_tasks > 0:
            coverage = self.run_tasks * 100.0 / self.total_tasks
        else:
            coverage = 0.0
        self._display.display('Coverage  : %.0f%% (%d of %d tasks are tested)' % (coverage, self.run_tasks, self.total_tasks))
