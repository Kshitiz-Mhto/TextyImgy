import os
import io
import random
import warnings
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

# Our Host URL should not be prepended with "https" nor should it have a trailing slash.
# os.environ['STABILITY_HOST'] = 'grpc.stability.ai:443'

# Paste your API Key below.
# os.environ['STABILITY_KEY'] = 'key-goes-here'

def api_work():
# Set up our connection to the API.
    try:
        stability_api = client.StabilityInference(
            key=os.environ['STABILITY_KEY'], # API Key reference.
            verbose=True, # Print debug messages.
            engine="stable-diffusion-v1-5",
        )
    except:
        print("Problem appeared during connection establishment...")

    number = random.randint(0, 2147483647)
    # data = str(input("Enter description of your Image: "))
    # Set up our initial generation parameters.
    answers = stability_api.generate(
        prompt="stunning dupa lipa fashion",
        seed=number, 
        steps=30, 
        cfg_scale=8.0, 
        width=512, # Generation width, defaults to 512 if not included.
        height=512, # Generation height, defaults to 512 if not included.
        samples=3, # Number of images to generate, defaults to 1 if not included.
        sampler=generation.SAMPLER_K_DPMPP_2M 
                                           
    )
    return answers

    # for resp in answers:
    #     for artifact in resp.artifacts:
    #         if artifact.finish_reason == generation.FILTER:
    #             warnings.warn(
    #                 "Your request activated the API's safety filters and could not be processed."
    #                 "Please modify the prompt and try again.")
    #             break
    #         if artifact.type == generation.ARTIFACT_IMAGE:
    #             img = Image.open(io.BytesIO(artifact.binary))
    #             img.save("./images/"+str(artifact.seed)+ ".png") # Save our generated images with their seed number as the filename.

