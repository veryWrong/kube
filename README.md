# kube
基于kunernetes容器编排系统的kubernetes-python client和flask web框架开发的服务部署平台API接口
请自行搭建好kubernetes集群，
系统默认将kubernetes的 kubeconfig 配置文件放在./kube目录下，您可以自行修改config.py中的 
config.load_kube_config(path + '/config') 以修改kubeconfig 配置文件地址