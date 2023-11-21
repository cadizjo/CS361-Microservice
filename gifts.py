import json

# Your JSON data
json_data = '''
[
    {
        "name": "Gimbal",
        "description": "",
        "interests": ["Photography", "Backpacking"]
    },
    {
        "name": "Portable Photo Printer",
        "description": "",
        "interests": ["Photography"]
    },
    {
        "name": "Polaroid Camera",
        "description": "",
        "interests": ["Photography"]
    },
    {
        "name": "Wireless Headphones",
        "description": "",
        "interests": ["Dance", "Gaming"]
    },
    {
        "name": "Bluetooth Speaker",
        "description": "",
        "interests": ["Dance"]
    },
    {
        "name": "Portable Camping Stove",
        "description": "",
        "interests": ["Backpacking", "Camping"]
    },
    {
        "name": "Portable Hammock",
        "description": "",
        "interests": ["Backpacking", "Camping"]
    },
    {
        "name": "Sketchbook",
        "description": "",
        "interests": ["Drawing"]
    },
    {
        "name": "Art Tote Bag",
        "description": "",
        "interests": ["Drawing", "Painting"]
    },
    {
        "name": "Insulated Mug",
        "description": "",
        "interests": ["Backpacking", "Camping", "Fishing"]
    },
    {
        "name": "Outdoor Hat",
        "description": "",
        "interests": ["Fishing", "Backpacking", "Gardening"]
    },
    {
        "name": "Polarized Sunglasses",
        "description": "",
        "interests": ["Backpacking", "Fishing"]
    },
    {
        "name": "Custom Apron",
        "description": "",
        "interests": ["Cooking", "Painting"]
    },
    {
        "name": "Recipe Cookbook",
        "description": "",
        "interests": ["Cooking"]
    },
    {
        "name": "Garden Kneeler and Seat",
        "description": "",
        "interests": ["Gardening"]
    },
    {
        "name": "Gardening Tool Set",
        "description": "",
        "interests": ["Gardening"]
    },
    {
        "name": "Essential Oils Diffuser",
        "description": "",
        "interests": ["Gardening"]
    },
    {
        "name": "Custom/Team Jersey",
        "description": "",
        "interests": ["Sports"]
    },
    {
        "name": "Game Tickets",
        "description": "",
        "interests": ["Sports"]
    },
    {
        "name": "Sports Apparel",
        "description": "",
        "interests": ["Sports"]
    },
    {
        "name": "Massage Ball",
        "description": "",
        "interests": ["Sports"]
    },
    {
        "name": "Acrylic/Oil Paint Set",
        "description": "",
        "interests": ["Painting"]
    },
    {
        "name": "Plein Air Palette Box",
        "description": "",
        "interests": ["Painting"]
    },
    {
        "name": "Custom Gaming Mouse Pad",
        "description": "",
        "interests": ["Gaming"]
    },
    {
        "name": "Gaming Headset",
        "description": "",
        "interests": ["Gaming"]
    },
    {
        "name": "Custom Controller",
        "description": "",
        "interests": ["Gaming"]
    }
]
'''

# Convert JSON to Python objects
gift_objects = json.loads(json_data)

# Now, python_objects is a list of dictionaries, each representing an item in your JSON array
# You can access individual items like gift_objects[0]["name"]

# If you have a file instead of a string, you can use the following code:
# with open('your_file.json', 'r') as file:
#     gift_objects = json.load(file)

print(gift_objects[0]["name"])