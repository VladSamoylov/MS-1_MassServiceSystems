import simpy

COLOR_ANSI_RED = '\033[31m'
COLOR_ANSI_GREEN = '\033[32m'
COLOR_ANSI_BLUE = '\033[34m'
COLOR_ANSI_YELLOW = '\033[33m'
COLOR_ANSI_FIOL = '\033[35m'
COLOR_ANSI_RESET = '\033[0m'

N = 15
ARRIVEINTERVAL = N
SERVICETIME = N * 2
SIMTIME = N * 10

def CustomerLifecycle(env, name):
    """
    Моделюється життєвий цикл однієї заявки в системі масового обслуговування

    :param env: Середовище моделювання, яке керує перебігом симуляції в часі
    :type env: simpy.Environment
    :param name: Ідентифікатор заявки
    :type name: str
    :yield: env.timeout(SERVICETIME) - Призупиняє процес на детермінований час, що дозволяє
    імітувати час обслуговування заявки
    """  
      
    arriveTime = env.now
    print(f"{COLOR_ANSI_YELLOW}{arriveTime:>8.2f}{COLOR_ANSI_RESET}: {COLOR_ANSI_GREEN}{name:<8}{COLOR_ANSI_RESET} прибула у систему")

    yield env.timeout(SERVICETIME)
    complatedTime = env.now
    appSystemTime = complatedTime - arriveTime
    print(f"{COLOR_ANSI_YELLOW}{complatedTime:>8.2f}{COLOR_ANSI_RESET}: {COLOR_ANSI_RED}{name:<8}{COLOR_ANSI_RESET} покинула систему / загальний час у системі {COLOR_ANSI_YELLOW}{appSystemTime}{COLOR_ANSI_RESET}")
    
def CustomerGenerator(env):
    """
    Генераторна функція, що реалізує процес надходження нових заявок до системи
    масового обслуговування за детермінований інтервал часу

    :param env: Ядро, яке керує модельним часом і планує події
    :type env: simpy.Environment
    :yield: env.timeout(ARRIVEINTERVAL) - Призупиняється генерація надходження нових заявок
    до СМО на детермінований час
    """    

    nCustomer = 0
    while True:
        yield env.timeout(ARRIVEINTERVAL)
        nCustomer += 1
        customerName = f"Заявка #{nCustomer}"
        env.process(CustomerLifecycle(env, customerName))

env = simpy.Environment()
env.process(CustomerGenerator(env))
print(f"{COLOR_ANSI_FIOL}Початок імітації!{COLOR_ANSI_RESET} Час моделювання: {COLOR_ANSI_YELLOW}{SIMTIME}{COLOR_ANSI_RESET}")
env.run(until = SIMTIME)
print(f"{COLOR_ANSI_RED}Моделювання завершено, час моделювання системи - {SIMTIME}{COLOR_ANSI_RESET}")