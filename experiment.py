import requests
import random

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

    dag = generate_random_roles_and_privs(3, 3, session)
    print(dag.json())