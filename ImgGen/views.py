from django.shortcuts import render
from .apiAi import api_work
# Create your views here.
import os
import io
import time
import random
import warnings
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

def home(request):
    try:
        # answers = api_work()
        stability_api = client.StabilityInference(
                key=os.environ['STABILITY_KEY'], # API Key reference.
                verbose=True, # Print debug messages.
                engine="stable-diffusion-v1-5",
            )
        number = random.randint(0, 2147483647)
        # data = str(input("Enter description of your Image: "))
        # Set up our initial generation parameters.
        answers = stability_api.generate(
            prompt="deamon car with black metallic color",
            seed=1590788272, 
            steps=30, 
            cfg_scale=8.0, 
            width=512,
            height=512,
            samples=1, # Number of images to generate, defaults to 1 if not included.
            sampler=generation.SAMPLER_K_DPMPP_2M                                       
        )
        
        for resp in answers:
            for artifact in resp.artifacts:
                if artifact.finish_reason == generation.FILTER:
                    warnings.warn(
                        "Your request activated the API's safety filters and could not be processed."
                        "Please modify the prompt and try again.")
                    return render(request, 'errorPage.html',{'msg':"Censored content are not allowed!!"})
                if artifact.type == generation.ARTIFACT_IMAGE:
                    img = Image.open(io.BytesIO(artifact.binary))
                    img.save("./static/img/"+str(artifact.seed)+ ".png")
        images = os.listdir('./static/img/')
        # Generate the img tags for each image
        import base64
        img_tags = []
        img_tags = []
        for image in images:
            with open('./static/img/' + image, 'rb') as f:
                image_data = f.read()
                image_data_base64 = base64.b64encode(image_data).decode('utf-8')
                img_tag = '<img src="data:image/png;base64,{}">'.format(image_data_base64)
                img_tags.append(img_tag)
        
        # Add the images and img_tags variables to the template context
        return render(request, 'home.html',{ 'img_tags': img_tags})
    except:
        return render(request, 'errorPage.html', {'msg':"Something went off!!"})