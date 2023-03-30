from PIL import Image 
import random
import json
import os
from collections import defaultdict
from configparser import ConfigParser

configFile = "config.ini"

#read config file
cfg = ConfigParser()
cfg.read(configFile)
numImg = cfg["CONF"]
TOTAL_IMAGES = int(numImg["num_images"])

itemsDict = defaultdict(list)
itemsWeights = defaultdict(list)



path = './layers'
layers_folder = os.listdir(path)

print(f'All Layers: {layers_folder}')
#Dict building
for layer in layers_folder:
    itemsInFolder = os.listdir(path+f'/{layer}')
    for items in itemsInFolder:
        if layer not in itemsDict:
            itemsDict[layer]
        if layer not in itemsWeights:
            itemsWeights[layer] 
        #using naming scheme, we're able to find more than a two digit weight with the following loop. Doubles included.
        g = items[:-4]
        weight = ''
        for c in reversed(g):
            if c == '_':
                break
            else:
                weight += c
                
        weight = weight[::-1] 
        itemsWeights[layer].append(float(weight))
        
        itemsDict[layer].append(items)

#Key generation for ordering the layers. Based on the last two digits of the layer folders
keys = []
i = 1
while len(keys) != len(itemsDict):
    for items in itemsDict:
        if items[-2:] == f'0{i}':
            keys.append(items)
            i+=1
        


all_images = [] 

def create_new_image():

    new_image = {} #

    # For each trait category, select a random trait based on the weightings 
    for i in itemsDict:
        new_image[i] = random.choices(itemsDict[i], itemsWeights[i])[0]
  
    if new_image in all_images:
        return create_new_image()
    else:
        return new_image


# Generate the unique combinations based on trait weighting. Weights generated from end of asset files.
for i in range(TOTAL_IMAGES): 

    new_trait_image = create_new_image()

    all_images.append(new_trait_image)




# Called to test if all images are unique
def all_images_unique(all_images):
    seen = list()
    return not any(i in seen or seen.append(i) for i in all_images)

print("Are all images unique?", all_images_unique(all_images))


#adds a tokenId to each item in the all_images list
i = 0 
for item in all_images:
    item["tokenId"] = i
    i = i + 1


print(all_images)

#Counts of each characteristic used in all images.
counts = {}
for items in itemsDict:
    counts[items] = {}
    for item in itemsDict[items]:
        counts[items][item] = 0

for image in all_images:
    for items in itemsDict:
        for item in itemsDict[items]:
            counts[items][item] += 1


#json dump
METADATA_FILE_NAME = './metadata/all-traits.json'; 
with open(METADATA_FILE_NAME, 'w') as outfile:
    json.dump(all_images, outfile, indent=4)

#Image generation
for item in all_images:
    imgFileDict = {}
    for items in itemsDict:
        imgFileDict[items] = Image.open(f'./layers/{items}/{item[items]}').convert('RGBA')

            

    #Create each composite
    imgCount = 0
    images = []
    for i in range(len(imgFileDict)-1):
        if imgCount == 0:
            images.append(Image.alpha_composite(imgFileDict[keys[i]], imgFileDict[keys[i+1]]))
            imgCount+=1
        else:
            images.append(Image.alpha_composite(images[i-1], imgFileDict[keys[i+1]]))
            imgCount+=1

    #Convert to RGB

    rgb_im = images[-1].convert('RGB')
    file_name = str(item["tokenId"]) + ".png"
    rgb_im.save("./images/" + file_name)



# Metadata generation (Attributes for each image)
f = open('./metadata/all-traits.json',) 
data = json.load(f)

IMAGES_BASE_URI = "ADD_IMAGES_BASE_URI_HERE"
PROJECT_NAME = "SPAWNS"

def getAttribute(key, value):
    return {
        "trait_type": key,
        "value": value
    }
#for i in our data list. we're 
for i in data:
    token_id = i['tokenId']
    token = {
        "image": IMAGES_BASE_URI + str(token_id) + '.png',
        "tokenId": token_id,
        "name": PROJECT_NAME + ' ' + str(token_id),
        "attributes": []
    }
    #For Items in the itemsDict, we're going to set the metadata to say trait_type: key, value: asset
    for items in itemsDict:
        key = items[:-3]
        token["attributes"].append(getAttribute(key, i[items]))
        

    with open('./metadata/' + str(token_id), 'w') as outfile:
        json.dump(token, outfile, indent=4)
f.close()












