SCENARIOS = {
    'A': [(0, 5), (1, 3), (2, 8), (3, 6)],
    'B': [(0, 10), (0, 10), (0, 10)],
    'C': [(0, 20), (1, 2), (2, 2), (3, 2)],
    'D': [(0, 10), (1, 10), (2, 10)],
    'E': [
        ('1', '0', '-5', '4', 'Invalid Burst Time'),
        ('1', '0', '5', '4', 'Valid P1 (to test duplicate next)'),
        ('1', '2', '3', '4', 'Duplicate PID P1'),
        ('2', '0', '', '4', 'Missing Burst Time'),
        ('3', '0', '4', 'abc', 'Invalid Quantum Value')
    ]
}

SCENARIO_NAMES = {
    'A': 'Basic Workload',
    'B': 'Quantum Sensitivity',
    'C': 'Short Job Heavy',
    'D': 'Interactive Fairness',
    'E': 'Validation (Errors)'
}
