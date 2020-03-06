import requests

BASE_URL = "http://127.0.0.1:8000/interface"
ADD_ROLE_ENDPOINT = f"{BASE_URL}/role/add"
CREATE_DAG_ENDPOINT = f"{BASE_URL}/create_dag"

def generate_random_roles_and_privs(num_roles, privs_per_role, session):
    for i in range(num_roles):
        session.post(ADD_ROLE_ENDPOINT, json={'role': f"n{i}"})
    
    return session.get(CREATE_DAG_ENDPOINT)

if __name__ == "__main__":
    # setup requests session using correct csrf_token
    session = requests.session()
    session.get(BASE_URL)
    csrf_token = session.cookies['csrftoken']
    session.headers.update({'X-CSRFToken': csrf_token})

    dag = generate_random_roles_and_privs(5, 10, session)
    print(dag)