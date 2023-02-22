import yaml

from kubernetes import client
from kubernetes.client import Configuration
from kubernetes.config import kube_config


class K8s(object):
    def __init__(self, configuration_yaml):
        self.configuration_yaml = configuration_yaml
        self._configuration_yaml = None

    @property
    def config(self):
        with open(self.configuration_yaml, 'r') as f:
            if self._configuration_yaml is None:
                self._configuration_yaml = yaml.safe_load(f)
        return self._configuration_yaml

    @property
    def client(self):
        k8_loader = kube_config.KubeConfigLoader(self.config)
        call_config = type.__call__(Configuration)
        k8_loader.load_and_set(call_config)
        Configuration.set_default(call_config)
        return client.CoreV1Api()

    @property
    def simple_client(self):
        k8_loader = kube_config.KubeConfigLoader(self.config)
        call_config = type.__call__(Configuration)
        k8_loader.load_and_set(call_config)
        Configuration.set_default(call_config)
        return client

    @property
    def custom_client(self):
        k8_loader = kube_config.KubeConfigLoader(self.config)
        call_config = type.__call__(Configuration)
        k8_loader.load_and_set(call_config)
        Configuration.set_default(call_config)
        return client.CustomObjectsApi()
    @property
    def autoscaling_client(self):
        k8_loader = kube_config.KubeConfigLoader(self.config)
        call_config = type.__call__(Configuration)
        k8_loader.load_and_set(call_config)
        Configuration.set_default(call_config)
        return client.AutoscalingV2Api()


# Instantiate your kubernetes class and pass in config
kube_one = K8s(configuration_yaml='')

def get_existing_app_hpa(maxpods,app_name):
    hpa_error = 0
    pod_cpu_threshold = 0
    current_replicas = maxpods
    # see if there are any existing hpa
    v2 = kube_one.autoscaling_client
    name = app_name  # str | name of the HorizontalPodAutoscaler
    namespace = 'openfaas-fn'  # str | object name and auth scope, such as for teams and projects
    pretty = 'true'
    try:
        item = v2.read_namespaced_horizontal_pod_autoscaler(name, namespace, pretty=pretty)
        if (item.metadata.name == app_name):
            for condition in item.status.conditions:
                # print("%s\t%s\t%s\t%s" % (condition.status, condition.reason, condition.type, condition.message))
                if condition.reason != 'DesiredWithinRange' and condition.status == str(False):
                    hpa_error = 1
                    return [hpa_error, pod_cpu_threshold]
                metrics = item.spec.metrics
                for metric in metrics:
                    if metric.resource.name == 'cpu':
                        pod_cpu_threshold = metric.resource.target.average_utilization
            current_replicas = item.status.current_replicas
            return [hpa_error, pod_cpu_threshold,
                    current_replicas]
    except Exception as e:
        print("Exception when calling AutoscalingV2beta2Api->read_namespaced_horizontal_pod_autoscaler:")
        print(e)
        return [hpa_error, pod_cpu_threshold,
                current_replicas]

def get_hpa_current_replicas(maxpods, app_name):
    hpa_error = 0
    pod_cpu_threshold = 0
    current_replicas = maxpods
    # see if there are any existing hpa
    v2 = kube_one.autoscaling_client
    name = app_name  # str | name of the HorizontalPodAutoscaler
    namespace = 'openfaas-fn'  # str | object name and auth scope, such as for teams and projects
    pretty = 'true'
    try:
        item = v2.read_namespaced_horizontal_pod_autoscaler(name, namespace, pretty=pretty)
        if (item.metadata.name == app_name):
            for condition in item.status.conditions:
                if condition.reason != 'DesiredWithinRange' and condition.status == str(False):
                    hpa_error = 1
                    return [hpa_error, pod_cpu_threshold]
                metrics = item.spec.metrics
                for metric in metrics:
                    if metric.resource.name == 'cpu':
                        pod_cpu_threshold = metric.resource.target.average_utilization
            current_replicas = item.status.current_replicas
            return [hpa_error,
                    current_replicas]
    except Exception as e:
        print("Exception when calling AutoscalingV2beta2Api->read_namespaced_horizontal_pod_autoscaler:")
        print(e)
        return [hpa_error,
                current_replicas]

def get_deployment_avg_CPU():
    api = kube_one.custom_client
    resource = api.list_namespaced_custom_object(group="metrics.k8s.io", version="v1beta1", namespace="openfaas-fn", plural="pods")
    overall = []
    quota = 0
    single = []
    for pod in resource["items"]:
        f = pod['containers'][0]['usage']['cpu']
        order = f[-1]
        cpu = float(f[:-1])
        if order == 'n':
            cpu = cpu / 1000000
        if order == 'u':
            cpu = cpu / 1000
        quota = quota + cpu
        single.append(cpu)   
    return quota, len(resource["items"]), single #tot cpu, num replicas, cpu per replica

def get_deployment_avg_mem():
    api = kube_one.custom_client
    resource = api.list_namespaced_custom_object(group="metrics.k8s.io", version="v1beta1", namespace="openfaas-fn", plural="pods")
    quota = 0
    single = []
    for pod in resource["items"]:
        f = pod['containers'][0]['usage']['memory']
        order = f[-2:]
        if order == "Ki":
            mem = float(f[:-2]) / 1000
        elif order == "Mi":
            mem = float(f[:-2])
        quota = quota + mem
        single.append(mem)
    return quota, len(resource["items"]), single #tot memory, num replicas, memory per replica


def get_nodes_avg_cpu():
    api = kube_one.custom_client
    k8s_nodes = api.list_cluster_custom_object("metrics.k8s.io", "v1beta1", "nodes")
    cpu_list=[]
    for stats in k8s_nodes['items']:
        f = stats['usage']['cpu']
        order = f[-1]
        cpu = float(f[:-1])
        if order == 'n':
            cpu = cpu / 1000000
        if order == 'u':
            cpu = cpu / 1000
        cpu_list.append(cpu)
    return cpu_list


def get_nodes_avg_mem():
    api = kube_one.custom_client
    k8s_nodes = api.list_cluster_custom_object("metrics.k8s.io", "v1beta1", "nodes")
    mem_list=[]
    for stats in k8s_nodes['items']:
        f = stats['usage']['memory']
        order = f[-2:]
        if order == "Ki":
            mem = float(f[:-2]) / 1000
        elif order == "Mi":
            mem = float(f[:-2])
        mem_list.append(mem)
    return mem_list



def update_hpa(app_name, thrs, maxrep, downscale):
    v2 = kube_one.autoscaling_client
    my_metrics = []
    client = kube_one.simple_client
    try:
        my_metrics.append(client.V2MetricSpec(type='Resource',
                                                  resource=client.V2ResourceMetricSource(name='cpu',
                                                                                         target=client.V2MetricTarget(
                                                                                             average_utilization=thrs,
                                                                                             type='Utilization'))))
    except Exception as e:
        print("Exception in metrics")
        print(e)

    if (len(my_metrics) > 0):
        my_conditions = []
        my_conditions.append(client.V2HorizontalPodAutoscalerCondition(status="True", type='AbleToScale'))
        down_policy = client.V2HPAScalingRules(stabilization_window_seconds=downscale) # INT32
        custom_behavior = client.V2HorizontalPodAutoscalerBehavior(scale_down=down_policy)
        body = client.V2HorizontalPodAutoscaler(
                api_version='autoscaling/v2',
                kind='HorizontalPodAutoscaler',
                metadata=client.V1ObjectMeta(name=app_name),
                spec=client.V2HorizontalPodAutoscalerSpec(
                    max_replicas=maxrep,
                    min_replicas=1,
                    behavior = custom_behavior,
                    metrics=my_metrics,
                    scale_target_ref=client.V2CrossVersionObjectReference(kind='Deployment', name=app_name,
                                                                          api_version='apps/v1'),
                ))

        try:
            api_response = v2.replace_namespaced_horizontal_pod_autoscaler(name=app_name, namespace='openfaas-fn', body=body,
                                                                              pretty=True)
            return 1
        except Exception as e:
            print("Exception when calling AutoscalingV2api->replace_namespaced_horizontal_pod_autoscaler")
            print(e)








