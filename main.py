#!/usr/bin/python3

from bottle import Bottle, run, response, request, post
import docker
import json

app = Bottle()
client = docker.from_env()

@app.route('/')
def hello():
    return "Henlo"

@app.route('/api/run/', method='POST')
def start():
    image = request.POST.get('image','')
    container = client.containers.run(image, detach=True)
    return container.logs()

@app.route('/api/stop/', method='POST')
def stop():
    container = request.POST.get('container','')
    while True:
        try:
            client.containers.get(container)
            break
        except docker.errors.NotFound:
            return 'No such container'
    container = client.containers.get(container)
    if container.stop():
        return 'Container stopped'

@app.route('/api/list/images')
def listImages():
    imagesList = []
    for image in client.images.list():
        tag = image.tags
        imagesList.append(tag)
    return {'DockerImages': imagesList}

@app.route('/api/list/containers')
def listContainers():
    containerList = []
    for container in client.containers.list(all):
        tag = container.short_id
        containerList.append(tag)
    return {'DockerContainers': containerList}


@app.route('/api/remove/', method='POST')
def remove():
    container = request.POST.get('container','')
    while True:
        try:
            client.containers.get(container)
            break
        except docker.errors.NotFound:
            return 'No such container'
    container = client.containers.get(container)
    container.remove()
    return 'Container deleted'

run(app, host='localhost', port=8080)
