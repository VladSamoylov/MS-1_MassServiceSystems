import simpy

COLOR_ANSI_RED = '\033[31m'
COLOR_ANSI_GREEN = '\033[32m'
COLOR_ANSI_BLUE = '\033[34m'
COLOR_ANSI_YELLOW = '\033[33m'
COLOR_ANSI_FIOL = '\033[35m'
COLOR_ANSI_RESET = '\033[0m'

N = 15
ARRIVEINTERVALFIRST = N
SERVICETIMEFIRST = N * 2
ARRIVEINTERVALSECOND = 1.5 * N
SERVICETIMESECOND = N * 3
SIMTIME = N * 10

env = simpy.Environment()

def CustomerLifecycle(env, name, serviceTime):
    """
    Моделюється життєвий цикл однієї заявки в системі масового обслуговування

    :param env: Середовище моделювання, яке керує перебігом симуляції в часі
    :type env: simpy.Environment
    :param name: Ідентифікатор заявки
    :type name: str
    :param serviceTime: Тривалість обслуговування заявки
    :type serviceTime: float
    :yield: env.timeout(serviceTime) - Призупиняє процес на детермінований час, що дозволяє
    імітувати час обслуговування заявки
    """    

    arriveTime = env.now
    print(f"{COLOR_ANSI_YELLOW}{arriveTime:>8.2f}{COLOR_ANSI_RESET}: {name:<10} {COLOR_ANSI_GREEN}прибула{COLOR_ANSI_RESET} у систему")

    yield env.timeout(serviceTime)
    complatedTime = env.now
    appSystemTime = complatedTime - arriveTime
    print(f"{COLOR_ANSI_YELLOW}{complatedTime:>8.2f}{COLOR_ANSI_RESET}: {name:<10} {COLOR_ANSI_RED}покинула{COLOR_ANSI_RESET} систему / загальний час у системі {COLOR_ANSI_YELLOW}{appSystemTime}{COLOR_ANSI_RESET}")

def CustomerGeneratorFirstType(env):
    """
    Генераторна функція, що реалізує процес надходження нових заявок першого виду до системи
    масового обслуговування за детермінований інтервал часу

    :param env: Ядро, яке керує модельним часом і планує події
    :type env: simpy.Environment
    :yield: env.timeout(ARRIVEINTERVALFIRST) - Призупиняється генерація надходження нових заявок
    до СМО на детермінований час
    """    

    nCustomer = 0
    while True:
        yield env.timeout(ARRIVEINTERVALFIRST)
        nCustomer += 1
        customerName = f"{COLOR_ANSI_BLUE}Заявка #{nCustomer}{COLOR_ANSI_RESET} (першого типу)"
        env.process(CustomerLifecycle(env, customerName, SERVICETIMEFIRST))
    
def CustomerGeneratorSecondType(env):
    """
    Генераторна функція, що реалізує процес надходження нових заявок другого виду до системи
    масового обслуговування за детермінований інтервал часу

    :param env: Ядро, яке керує модельним часом і планує події
    :type env: simpy.Environment
    :yield: env.timeout(ARRIVEINTERVALSECOND) - Призупиняється генерація надходження нових заявок
    до СМО на детермінований час
    """  

    nCustomer = 0
    yield env.timeout(2)
    while True: 
        yield env.timeout(ARRIVEINTERVALSECOND)
        nCustomer += 1
        customerName = f"{COLOR_ANSI_FIOL}Заявка #{nCustomer}{COLOR_ANSI_RESET} (другого типу)"
        env.process(CustomerLifecycle(env, customerName, SERVICETIMESECOND))

env.process(CustomerGeneratorFirstType(env))
env.process(CustomerGeneratorSecondType(env))
print(f"{COLOR_ANSI_FIOL}Початок імітації!{COLOR_ANSI_RESET} Час моделювання: {COLOR_ANSI_YELLOW}{SIMTIME}{COLOR_ANSI_RESET}")
env.run(until = SIMTIME)
print(f"{COLOR_ANSI_RED}Моделювання завершено{COLOR_ANSI_RESET}")