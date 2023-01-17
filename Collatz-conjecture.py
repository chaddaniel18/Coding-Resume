def modify(n):  # fundamental function of the Collatz Conjecture
    if n % 2 == 0:
        n = n / 2
    else:
        n = 3 * n + 1
    return n


def check_single():
    x = int(input('What value should I check? '))
    steps = 0  # for counting the number of times the 'modify' function is applied
    n = x
    while n != 1:
        print(f'Value at {n}')
        n = modify(n)
        steps += 1
    print(f'Number of steps taken: {steps}')
    if n == 1:
        print('Value resolved to 1')
    else:
        print('Value remains unresolved')


def dynamic_growth_query(start_steps):
    final_value = int(input('How far should we go this time? '))
    if final_value in start_steps:
        print(
            f'Already computed, steps to 1 are {start_steps[final_value]}.\nLess than peak values all solved, see dict')
    elif final_value % 2 == 0 and final_value - 1 in start_steps:
        start_steps['peak'] = final_value
        steps = start_steps[final_value / 2] + 1
        start_steps[final_value] = steps
        # the below print statement is not a definitive conclusion to the code above
        print(f'Shortcut taken, resolved to 1 in {steps}.\nLess than peak values all solved, see dict')
    else:
        x = start_steps['peak']  # this value assigned externally
        num_values = final_value - x
        complete = 0
        threshhold = 10
        bar = '----------'
        print(f'[{bar}]')
        while True:
            complete += 1
            percent = complete / num_values * 100
            if percent >= threshhold:
                tick = int(threshhold / 10)
                bar = tick * '>' + bar[tick:]
                threshhold += 10
                print(f'[{bar}]')
            x += 1
            n = x
            steps = 0
            while steps < 1000000000:
                if n in start_steps:
                    start_steps[x] = steps + start_steps[n]
                    n = 1
                    break
                else:
                    steps += 1
                    n = modify(n)
            if n != 1 and steps == 1000000000:
                print(f'unsolved value found: {x}')
                exit()
            if x == final_value:
                print('[>>>>>>>>>>]')
                print('Complete!')
                break
    return start_steps


while True:
    print('Welcome to the Collatz conjecture')
    print('You can test a single value or a range from 2 to x')
    option = input('(single or range)? ')
    if option == 'single':
        check_single()
    elif option == 'range':
        start_step_dict = {'peak': 1, 1: 0}
        while True:
            dynamic_growth_query(start_step_dict)
            if input('Query dictionary for how many steps a number took? (y/n) ') == 'y':
                while True:
                    try:
                        x = input('pick a number: ')
                        x = int(x)
                    except:
                        if len(x) == 0:
                            break
                        print('Input is not a number')
                        continue
                    try:
                        print(f'Number of steps taken {start_step_dict[x]}')
                    except:
                        print('Input has not been computed')
            if input('Continue? (y/n) ') != 'y':
                break
    else:
        print('invalid input')
    if input('Restart? (y/n) ') != 'y':
        break
