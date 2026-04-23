from kubernetes import client, config

def get_k8s_client():
    try:
        config.load_incluster_config()
    except:
        config.load_kube_config()

    return client.CoreV1Api()