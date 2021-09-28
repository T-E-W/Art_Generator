# Project Title

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)

## About <a name = "about"></a>

Basic Art Generator.

From https://github.com/benyaminahmed/nft-image-generator/blob/main/generate.ipynb With Modifications for simplistic layer and asset additions.

## Getting Started <a name = "getting_started"></a>

		Naming Scheme:

		For New or Changing Layer Folders:

			Place in layers folder.

			Ensure name is as follows:

			[Layername]_[LayerPositionXX]
			(e.g. background_01 would have the files in this layer placed first in the image, as a background should.
			ENSURE THE LAYER POSITION IS TWO DIGIT. So with this naming scheme, you could essentially have up to 100
				layers starting with 00, ending in 99.)

		For New or Changing Asset Files:

			Place in desired layer.

			Ensure name is as follows:

			-[assetname)_[WeightXX].png
			(e.g. redhat_1_25.png has the name of (redhat_1) and the weight of (25%), always ending in (.png)
			Weights can be any float so long as it's after the first '_'. So with four assets in a layer, you could do 50, 25, 24.5, .05)

### Prerequisites

pip install pillow

### Creating layers and importing assets:

Included are the folders you'll need. 

1) Create new layer folders under the given "layers" folder per the naming scheme above.
	- e.g. (./layers/shirts_03)  This would create a new layer called Shirts at the third layer.

2) Name/Rename images based on the naming scheme above. Import into desired layer.
	- e.g. (./layers/shirts_03/red_shirt_.05)  This would add in a new asset called red_shirt with a weight of .05 in layer 03.

-Modify the 'config.ini' to set number of images you wish to create. This will only be as many unique images you can create. 

-Run

Images will be generated and saved in the given ./images folder.
