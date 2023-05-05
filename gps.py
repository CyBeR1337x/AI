tiles_operators = [
    {"action": "swap tile 1 and 4",
     "preconds": ["1-bottom-right", "4-bottom-left"],
     "add": ["1-bottom-left", "4-bottom-right"],
     "delete": ["1-bottom-right", "4-bottom-left"]
     },
    {"action": "swap tile 3 and 2",
     "preconds": ["2-top-left", "3-top-right"],
     "add": ["2-top-right", "3-top-left"],
     "delete": ["2-top-left", "3-top-right"]
     },
    {"action": "swap tile 1 and 3",
     "preconds": ["1-bottom-left", "3-top-left"],
     "add": ["1-top-left", "3-bottom-left"],
     "delete": ["1-bottom-left", "3-top-left"]
     }
]


def gps(initial_states, goal_states, operators):
    prefix = 'EXECUTING '
    for operator in operators:
        operator['action'] = operator['action'].upper()
        operator['add'].append(prefix + operator['action'])
        print('DEBUG: ', operator['add'])
        operator['preconds'] = [pre.upper() for pre in operator['preconds']]
        operator['delete'] = [dlst.upper() for dlst in operator['delete']]
        operator['add'] = [add.upper() for add in operator['add']]
    initial_states = [state.upper() for state in initial_states]
    goal_states = [goal.upper() for goal in goal_states]
    final_states = achieve_all(initial_states, operators, goal_states, [])
    if not final_states:
        return None
    actions = [state for state in final_states if state.startswith(prefix)]
    for a in actions:
        print(a)
    return actions


def achieve_all(states, ops, goals, goal_stack):
    for goal in goals:
        states = achieve(states, ops, goal, goal_stack)
        if not states:
            return None
    for goal in goals:
        if goal not in states:
            return None
    return states


def achieve(states, operators, goal, goal_stack):
    print(len(goal_stack), 'Achieving: %s' % goal)
    if goal in states:
        print(len(goal_stack), 'Achieved: %s' % goal)
        return states
    if goal in goal_stack:
        return None
    for op in operators:
        if goal not in op['add']:
            continue
        result = apply_operator(op, states, operators, goal, goal_stack)
        if result:
            return result


def apply_operator(operator, states, ops, goal, goal_stack):
    print(len(goal_stack), 'Consider: %s' % operator['action'])
    result = achieve_all(states, ops, operator['preconds'], [
                         goal] + goal_stack)
    if not result:
        return None
    print(len(goal_stack), 'Action: %s' %
          operator['action'], '  Achieved: %s' % goal)
    add_list, delete_list = operator['add'], operator['delete']
    return [state for state in result if state not in delete_list] + add_list


gps(['1-bottom-right', '2-top-left', '3-top-right', '4-bottom-left'],
    ['1-top-left', '2-top-right', '3-bottom-left', '4-bottom-right'], tiles_operators)
