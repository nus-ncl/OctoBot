import docker
import os

#returns true if image_name present in env
def find_job(image_name):
    c = docker.from_env()
    try:
        return bool(c.images.get(image_name))
    except:
        return False
        

def run_job(image, *params):
    if (not find_job(image)):
        raise Exception("Image {} not found".format(image))

    client = docker.from_env()
    paramsForContainer = params.join(" ")

    client.containers.run(image, paramsForContainer)

def listener():
    
    while(1):
        
        user_input = input() 
        user_input = user_input.split()

        imageName = user_input[0]
        params = user_input[1:]

        pid = os.fork()

        if (pid == 0):
            run_job(imageName, params)
        else:
            continue


