"""A Python Pulumi program"""
import os
import pulumi
import pulumi_docker as docker

# get configuration
config = pulumi.Config()
frontend_port = config.require_int("frontend_port")
backend_port = config.require_int("backend_port")
mongo_port = config.require_int("mongo_port")
mongo_host = config.require("mongo_host")
database = config.require("database")
node_environment = config.require("node_environment")


stack = pulumi.get_stack()

# build our backend image!
backend_image_name = "backend"
backend = docker.Image('backend',
                       build=docker.DockerBuild(context=f'{os.getcwd()}/app/backend'),
                       image_name=f'{backend_image_name}:{stack}',
                       skip_push=True
                       )
# build our frontend image
frontend_image_name = 'frontend'
frontend = docker.Image('frontend',
                        build=docker.DockerBuild(context=f'{os.getcwd()}/app/frontend'),
                        image_name=f'{frontend_image_name}:{stack}',
                        skip_push=True
                        )

# build our mongodb image!
mongo_image = docker.RemoteImage("mongo", name="mongo:bionic")

# create a network!
network = docker.Network("network", name=f'services-{stack}')

# create the mongo container!
mongo_container = docker.Container("mongo_container",
                                   image=mongo_image.latest,
                                   name=f'mongo-{stack}',
                                   ports=[docker.ContainerPortArgs(
                                       internal=mongo_port,
                                       external=mongo_port
                                   )],
                                   networks_advanced=[docker.ContainerNetworksAdvancedArgs(
                                       name=network.name,
                                       aliases=["mongo"]
                                   )]
                                   )

# create the backend container!
backend_container = docker.Container("backend_container",
                                     name=f'backend-{stack}',
                                     image=backend.base_image_name,
                                     ports=[docker.ContainerPortArgs(
                                         internal=backend_port,
                                         external=backend_port
                                     )],
                                     envs=[
                                         f'DATABASE_HOST={mongo_host}',
                                         f'DATABASE_NAME={database}',
                                         f'NODE_ENV={node_environment}'
                                     ],
                                     networks_advanced=[docker.ContainerNetworksAdvancedArgs(
                                         name=network.name
                                     )],
                                     opts=pulumi.ResourceOptions(depends_on=[mongo_container])
                                     )

# create the frontend container!
frontend_container = docker.Container("frontend_container",
                                      image=frontend.base_image_name,
                                      name=f'frontend-{stack}',
                                      ports=[docker.ContainerPortArgs(
                                          internal=frontend_port,
                                          external=frontend_port
                                      )],
                                      envs=[
                                          f'LISTEN_PORT={frontend_port}',
                                          f'PROXY_PROTOCOL=http://',
                                          f'HTTP_PROXY=backend-{stack}:{backend_port}'
                                      ],
                                      networks_advanced=[docker.ContainerNetworksAdvancedArgs(
                                          name=network.name
                                      )]
                                      )