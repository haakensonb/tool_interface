import requests
import random
import sys

# must be same filename as used in run_experiment.sh
LOGFILE = "log2.txt"

BASE_URL = "http://127.0.0.1:8000/interface"
ADD_ROLE_ENDPOINT = f"{BASE_URL}/role/add"
ADD_PRIV_ENDPOINT = f"{BASE_URL}/possibleprivilege/add"
ASSIGN_ROLE_PRIV_ENDPOINT = f"{BASE_URL}/assign"
CREATE_DAG_ENDPOINT = f"{BASE_URL}/create_dag"

def generate_random_roles_and_privs(num_roles, privs_per_role, session):
    nodes = {}
    # create roles
    for i in range(num_roles):
        node_name = f"n{i}"
        nodes[node_name] = None
        session.post(ADD_ROLE_ENDPOINT, json={'role': node_name})
    
    num_privs = num_roles * privs_per_role
    # create privilege objects
    objects = [f"object {i}" for i in range(num_privs)]
    for obj in objects:
        session.post(ADD_PRIV_ENDPOINT, json={'add_priv': obj})

    # randomly map priviledges to roles
    used_objects = set()
    for node_name in nodes:
        keep_going = True
        while keep_going:
            random_privs = random.sample(objects, privs_per_role)
            hashable = str(sorted(random_privs))
            if hashable not in used_objects:
                used_objects.add(hashable)
                nodes[node_name] = random_privs
                for obj in nodes[node_name]:
                    session.post(ASSIGN_ROLE_PRIV_ENDPOINT, data={'role': node_name, 'priv': obj})
                keep_going = False
    
    return session.get(CREATE_DAG_ENDPOINT)

if __name__ == "__main__":
    # setup requests session using correct csrf_token
    session = requests.session()
    session.get(BASE_URL)
    csrf_token = session.cookies['csrftoken']
    session.headers.update({'X-CSRFToken': csrf_token})   

    num_of_nodes, privs_per_role = int(sys.argv[1]), int(sys.argv[2])
    generate_random_roles_and_privs(num_of_nodes, privs_per_role, session)

    # highest_node_num = 20
    # privs_per_role = 10
    # inputs = [x for x in range(10, highest_node_num+1, 10)]
    # for input_value in inputs:
    #     counter = 1
    #     with open(LOGFILE, "a") as f:
    #         f.write(f"Running experiment with {input_value} roles, {privs_per_role} privs per role\n")
    #     for i in range(3):
    #         with open(LOGFILE, "a") as f:
    #             f.write(f"Run number {counter}\n")
    #         # reset the database
    #         # change python3 to whatever path testing system is using for python
    #         Popen("echo 'yes' | python3 manage.py flush", shell=True, stdout=PIPE)
    #         generate_random_roles_and_privs(input_value, privs_per_role, session)
    #         counter += 1
    #     with open(LOGFILE, "a") as f:
    #         f.write(f"Ending experiment with {input_value} roles\n")