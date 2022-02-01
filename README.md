# Atlas


## Description

Code coverage tool for Ansible that helps to determine the total executed tasks

## Installation steps:
* Copy the callback_plugins in the directory of your playbook

## Sample output

Following is a sample playbook to be tested:
```bash
---
- hosts: localhost
  gather_facts: no
  tasks:
    - name: Task 1 execution
      debug:
        msg: "This is my first task"

    - name: Task 2 execution
      debug:
        msg: "This is my second task"

    - fail:
       msg: "Sad"

    - name: Task 4 execution
      debug:
        msg: "This is my fourth task"
end
```

On running the playbook, Atlas shows the code coverage:

```bash
[WARNING]: Skipping plugin (/home/cpranava/atlast/callback_plugins/_init_.py) as it seems to be invalid: module 'ansible.plugins.callback._init_'
has no attribute 'CallbackModule'

PLAY [localhost] *********************************************************************************************************************************

TASK [Task 1 execution] **************************************************************************************************************************
ok: [localhost] => {
    "msg": "This is my first task"
}

TASK [Task 2 execution] **************************************************************************************************************************
ok: [localhost] => {
    "msg": "This is my second task"
}

TASK [fail] **************************************************************************************************************************************
fatal: [localhost]: FAILED! => {"changed": false, "msg": "Sad"}

PLAY RECAP ***************************************************************************************************************************************
localhost                  : ok=2    changed=0    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0

*** Atlas Results ***
Coverage  : 75% (3 of 4 tasks are tested)
end
```
