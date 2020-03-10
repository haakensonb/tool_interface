import requests
import random
import sys
import os

# must be same filename as used in run_experiment.sh
# LOGFILE = "log3.txt"
LOGFILE = os.environ.get("EXP_LOGFILE")

BASE_URL = "http://127.0.0.1:8000/interface"
ADD_ROLE_ENDPOINT = f"{BASE_URL}/role/add"
ADD_PRIV_ENDPOINT = f"{BASE_URL}/possibleprivilege/add"
ASSIGN_ROLE_PRIV_ENDPOINT = f"{BASE_URL}/assign"
CREATE_DAG_ENDPOINT = f"{BASE_URL}/create_dag"
CREATE_DAG_EXP_2_ENDPOINT = f"{BASE_URL}/create_dag_experiment_2"

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

# redundant code, should be changed later
def create_key_derivation_graph(num_roles, session):
    nodes = {}
    # create roles
    for i in range(num_roles):
        node_name = f"n{i}"
        nodes[node_name] = None
        session.post(ADD_ROLE_ENDPOINT, json={'role': node_name})
    # create priv objects
    objects = [f"object {i}" for i in range(num_roles)]
    for obj in objects:
        session.post(ADD_PRIV_ENDPOINT, json={'add_priv': obj})
    # create mapping
    for i, node_name in enumerate(nodes):
        session.post(ASSIGN_ROLE_PRIV_ENDPOINT, data={'role': node_name, 'priv': objects[i]})

    return session.post(CREATE_DAG_EXP_2_ENDPOINT, json={'num_of_nodes': num_roles})

if __name__ == "__main__":
    # setup requests session using correct csrf_token
    session = requests.session()
    session.get(BASE_URL)
    csrf_token = session.cookies['csrftoken']
    session.headers.update({'X-CSRFToken': csrf_token})   

    num_of_nodes, privs_per_role, experiment_num = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    if(experiment_num == 1):
        generate_random_roles_and_privs(num_of_nodes, privs_per_role, session)
    elif(experiment_num == 2):
        create_key_derivation_graph(num_of_nodes, session)
    else:
        print("invalid input")
