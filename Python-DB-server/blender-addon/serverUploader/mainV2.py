import os
import tempfile
import json

from requests_toolbelt import MultipartEncoder
import requests

import bpy

# DB_SERVER_ADDRESS = "http://127.0.0.1:8000"
# IPFS_ADDRESS = "http://10.252.107.31:5001"

CATEGORY_SUB_CATEGORY_MAPPING = {
    "3D Printable": ["Model 1", "Model 2", "Model 3", "Model 4", "Model 5"],
    "Anatomy": ["Human Anatomy", "Animal Anatomy", "Plant Anatomy", "Microscopic Anatomy", "Comparative Anatomy"],
    "Animals": ["Mammals", "Birds", "Reptiles", "Amphibians", "Fish"],
    "Animation": ["2D Animation", "3D Animation", "Stop Motion", "Motion Graphics", "Visual Effects"],
    "Architecture": ["Residential", "Commercial", "Landscape", "Interior Design", "Urban Design"],
    "Asset Libraries": ["3D Models", "Textures", "Materials", "Scripts", "Templates"],
    "Base Meshes": ["Humanoid", "Animals", "Buildings", "Vehicles", "Furniture"],
    "Buildings": ["Residential Buildings", "Commercial Buildings", "Historical Buildings", "Modern Buildings", "Futuristic Buildings"],
    "Characters": ["Human Characters", "Animal Characters", "Fantasy Characters", "Sci-Fi Characters", "Cartoon Characters"],
    "Clothes & Accessories": ["Clothing", "Footwear", "Jewelry", "Bags", "Accessories"],
    "Creatures": ["Fantasy Creatures", "Mythical Creatures", "Alien Creatures", "Aquatic Creatures", "Hybrid Creatures"],
    "Decals": ["Wall Decals", "Floor Decals", "Vehicle Decals", "Window Decals", "Custom Decals"],
    "Design Elements": ["Typography", "Icons", "Logos", "Banners", "Infographics"],
    "Electronics": ["Computers", "Mobile Devices", "Home Appliances", "Audio Devices", "Gaming Consoles"],
    "Engines & Parts": ["Engine Components", "Transmission", "Suspension", "Brakes", "Exhaust"],
    "Fantasy & Fiction": ["Fantasy Worlds", "Fictional Characters", "Mythical Creatures", "Fantasy Weapons", "Fictional Technologies"],
    "Food & Drinks": ["Fruits", "Vegetables", "Meat", "Beverages", "Desserts"],
    "Furnishings": ["Living Room", "Bedroom", "Kitchen", "Office", "Outdoor"],
    "Game Ready": ["Characters", "Environments", "Props", "Vehicles", "Weapons"],
    "Humans": ["Anatomy", "Clothing", "Expressions", "Poses", "Accessories"],
    "Miscellaneous": ["Tools", "Utilities", "Decor", "Stationery", "Misc Items"],
    "Motion Graphics": ["Transitions", "Titles", "Backgrounds", "Particles", "Effects"],
    "Music": ["Instruments", "Genres", "Album Covers", "Music Videos", "Concert Stages"],
    "Nature": ["Plants", "Animals", "Landscapes", "Weather", "Natural Phenomena"],
    "Parametric Models": ["Architectural", "Mechanical", "Electrical", "Civil", "Aerospace"],
    "Products": ["Electronics", "Furniture", "Clothing", "Food Items", "Accessories"],
    "Science": ["Physics", "Chemistry", "Biology", "Astronomy", "Geology"],
    "Sci-Fi": ["Spaceships", "Aliens", "Futuristic Cities", "Robots", "Weapons"],
    "Sports": ["Team Sports", "Individual Sports", "Outdoor Sports", "Indoor Sports", "Water Sports"],
    "Tools": ["Hand Tools", "Power Tools", "Gardening Tools", "Mechanical Tools", "Electrical Tools"],
    "Toys & Games": ["Action Figures", "Board Games", "Dolls", "Puzzles", "Video Games"],
    "Urban": ["Buildings", "Transportation", "Parks", "Street Furniture", "Monuments"],
    "Vehicles": ["Cars", "Motorcycles", "Aircraft", "Ships", "Trains"],
    "Weapons & Armor": ["Swords", "Guns", "Shields", "Armor", "Artillery"]
}



class ServerStatusPanel(bpy.types.Panel):
    """A panel in the Blender UI to manage server status and upload content to the server."""
    bl_idname = "OBJECT_PT_server_status_panel_custom"
    bl_label = "Server Uploader"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"


    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Server and IPFS address rows
        row = layout.row()
        row.label(text="Server Address:")
        row.prop(scene, "server_address", text="")
        
        row = layout.row()
        row.label(text="IPFS Address:")
        row.prop(scene, "ipfs_address", text="")
        
        # Sever Status indicator row
        row = layout.row()
        row.label(text="Server Status:")
        status_label = row.column(align=True)
        status_label.enabled = False
        status_label.operator("object.check_server", text=scene.server_status_label, icon='QUESTION')
        
        # IPFS Status indicator row
        row = layout.row()
        row.label(text="IPFS Status:")
        status_label = row.column(align=True)
        status_label.enabled = False
        status_label.operator("object.check_server", text=scene.ipfs_status_label, icon='QUESTION')

        # Check server button
        row = layout.row()
        row.operator("object.check_server", text="Check Server Status")

        # Selected Object display
        obj = context.object
        row = layout.row()
        row.label(text="Active object is: " + obj.name)

        # Content ID row
        row = layout.row()
        row.label(text="Content ID:")
        content_id = row.column(align=True)
        content_id.enabled = False
        content_id.operator("object.ipfs_upload", text=scene.content_id)

        # Upload to IPFS button
        row = layout.row()
        row.operator("object.ipfs_upload", text="Upload obj to IPFS")

        # Copy IPFS hash button
        ipfs_hash = scene.content_id
        if ipfs_hash:
            row = layout.row()
            row.operator("object.copy_ipfs_hash", text="Copy IPFS Hash", icon='COPYDOWN').ipfs_hash = ipfs_hash

        # API row
        row = layout.row()
        row.label(text="API Key:")
        row.prop(scene, "server_APIKey", text="")

        # Name row
        row = layout.row()
        row.label(text="Name:")
        row.prop(scene, "server_name", text="")

        # Tag row with box and column_flow
        box = layout.box()
        box.label(text="Hierarchy")
        col = box.column_flow(columns=1, align=True)
        col.prop(scene, "selected_category", text="Category")
        col.prop(scene, "selected_sub_category", text="Sub Category")
        
        col.label(text="Attributes")
        col.prop(scene, "attributes", text="")

        # Upload server button
        row = layout.row()
        row.operator("object.server_upload", text="Upload")



class ServerCheckOperator(bpy.types.Operator):
    """An operator in Blender to check the status of the server and IPFS connection."""
    bl_idname = "object.check_server"
    bl_label = "Check Server"

    def execute(self, context):
        """Execute the operator to check the server and IPFS status."""
        server_address = context.scene.server_address
        ipfs_address = context.scene.ipfs_address

        # Perform server availability check using an HTTP GET request
        is_server_available = self.check_server_availability(server_address)
        is_ipfs_available = self.check_ipfs_availability(ipfs_address)

        if is_server_available:
            context.scene.server_status_label = "Connected"
        else:
            context.scene.server_status_label = "Disconnected"

        if is_ipfs_available:
            context.scene.ipfs_status_label = "Connected"
        else:
            context.scene.ipfs_status_label = "Disconnected"

        return {'FINISHED'}

    def check_server_availability(self, server_address):
        """Check the availability of the server by sending a GET request to the server address."""
        try:
            # Send an HTTP GET request to the server
            response = requests.get(server_address)

            # Check the response status code
            return response.status_code == 200
        except requests.exceptions.RequestException:
            # An error occurred during the request
            return False

    def check_ipfs_availability(self, ipfs_address):
        """Check the availability of the IPFS by sending a POST request to the IPFS address."""
        try:
            # Send an HTTP POST request to the IPFS
            response = requests.post(f"{ipfs_address}/api/v0/version")

            # Check the response status code
            return response.status_code == 200
        except requests.exceptions.RequestException:
            # An error occurred during the request
            return False


class IPFSUploadOperator(bpy.types.Operator):
    """An operator in Blender to upload the selected object to IPFS."""
    bl_idname = "object.ipfs_upload"
    bl_label = "IPFS Upload"

    def execute(self, context):
        """Execute the operator to upload the selected object to IPFS."""
        ipfs_address = context.scene.ipfs_address
        obj = bpy.context.active_object

        # Check if the active object is a mesh object
        if obj.type == 'MESH':
            
            with tempfile.TemporaryDirectory() as temp_dir:
                # Set the export file paths
                obj_file_path = os.path.join(temp_dir, obj.name + ".obj")                

                # Set the export options
                export_options = {
                    'use_selection': True,
                    'check_existing': False,
                    'axis_forward': 'Y',
                    'axis_up': 'Z',
                    'use_materials': True,
#                    'use_triangles': True
                }

                # Export the object as OBJ
                bpy.ops.export_scene.obj(
                    filepath=obj_file_path,
                    **export_options
                )

                # Add a camera to the scene if not exists
                if not any(obj.type == 'CAMERA' for obj in bpy.data.objects):
                    bpy.ops.object.camera_add()
                    bpy.context.scene.camera = bpy.context.object

                # Upload the directory to IPFS
                ipfs_hash = self.upload_to_ipfs(ipfs_address, temp_dir)
                if ipfs_hash:
                    context.scene.content_id = f"{ipfs_hash}"
                else:
                    context.scene.content_id = "Failed to upload to IPFS"
        else:
            context.scene.content_id = "No valid OBJ file associated with the active object"

        return {'FINISHED'}

    def upload_to_ipfs(self, ipfs_address, dir_path):
        """Upload the directory containing the object files to IPFS."""
        try:
            # Get the list of files in the directory
            files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]

            # Create a MultipartEncoder object and add the files to it
            multipart_encoder = MultipartEncoder(
                fields={file: (file, open(os.path.join(dir_path, file), 'rb')) for file in files}
            )

            # Create a header with the content type from the MultipartEncoder
            headers = {'Content-Type': multipart_encoder.content_type}

            # Send a POST request to IPFS with the MultipartEncoder as the data
            response = requests.post(
                f"{ipfs_address}/api/v0/add?wrap-with-directory=true&pin=true",
                data=multipart_encoder,
                headers=headers
            )

            # Check the response status code
            if response.status_code == 200:
                # Parse the response as a JSON stream
                response_jsons = [
                    json.loads(line) for line in response.iter_lines(decode_unicode=True) if line
                ]

                # Extract the directory hash (the hash with an empty "Name" field)
                directory_cid = next(item for item in response_jsons if item["Name"] == "")["Hash"]
                return directory_cid
            
            print(f"Failed to upload to IPFS. Response code: {response.status_code}, Response text: {response.text}")
            return None

        except requests.exceptions.RequestException as err:
            # An error occurred during the request
            print(f"Request error: {err}")
            return None
        except Exception as err:
            # Catch any other exceptions
            print(f"An error occurred: {err}")
            return None


class CopyIPFSHashOperator(bpy.types.Operator):
    """An operator in Blender to copy the IPFS hash to the clipboard."""
    bl_idname = "object.copy_ipfs_hash"
    bl_label = "Copy IPFS Hash"

    ipfs_hash: bpy.props.StringProperty()

    def execute(self, context):
        """Execute the operator to copy the IPFS hash to the clipboard."""
        context.window_manager.clipboard = self.ipfs_hash
        self.report({'INFO'}, "IPFS Hash copied to clipboard")
        return {'FINISHED'}


class ServerUploadOperator(bpy.types.Operator):
    """An operator in Blender to upload the content data to the server."""    
    bl_idname = "object.server_upload"
    bl_label = "Upload"

    def execute(self, context):
        """Execute the operator to upload the content data to the server."""
        server_address = context.scene.server_address
        api_key = context.scene.server_APIKey
        content_id = context.scene.content_id
        name = context.scene.server_name
        category = context.scene.category
        sub_category = context.scene.sub_category
        attributes_text = context.scene.attributes
        attributes = sorted(attributes_text.split(','), reverse=True)
        
        # Construct the JSON data to be sent
        data = {
            "api_key": api_key,
            "content_id": content_id,
            "name": name,
            "category": category,
            "sub_category": sub_category,
            "attributes": attributes
        }

        try:
            # Send the HTTP POST request to the server
            response = requests.post(f"{server_address}/create/upload_data", json=data)

            # Check the response status code
            if response.status_code == 200:
                # The data was uploaded successfully
                self.report({'INFO'}, "Data uploaded successfully")
            else:
                # There was an error during the upload
                self.report({'ERROR'}, "Failed to upload data")
        except requests.exceptions.RequestException as err:
            # An error occurred during the request
            self.report({'ERROR'}, f"Request error: {err}")

        return {'FINISHED'}

    def check_server_availability(self, server_address):
        """(This method seems to be unused, consider removing it or adding functionality to check server availability.)"""
        # Replace this with your own server availability check logic
        # Return True if server is available, False otherwise
        # You can use libraries like requests or urllib to perform the check
        # Example:
        # import requests
        # try:
        #     response = requests.get(server_address)
        #     return response.status_code == 200
        # except requests.exceptions.RequestException:
        #     return False

classes = (
    ServerStatusPanel,
    ServerCheckOperator,
    IPFSUploadOperator,
    CopyIPFSHashOperator,
    ServerUploadOperator,
)


def register_classes_and_properties():
    """Register the classes and properties in Blender."""
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.server_address = bpy.props.StringProperty(name="Server Address")
    bpy.types.Scene.ipfs_address = bpy.props.StringProperty(name="IPFS Address")

    bpy.types.Scene.server_status_label = bpy.props.StringProperty(name="Server Status Label")
    bpy.types.Scene.ipfs_status_label = bpy.props.StringProperty(name="IPFS Status Label")

    bpy.types.Scene.content_id = bpy.props.StringProperty(name="Content Id")
    bpy.types.Scene.server_APIKey = bpy.props.StringProperty(name="API key", subtype='FILE_NAME')
    bpy.types.Scene.server_name = bpy.props.StringProperty(name="Name", subtype='FILE_NAME')
    
    bpy.types.Scene.category = bpy.props.StringProperty(name="Category")
    bpy.types.Scene.selected_category = bpy.props.EnumProperty(
        items=[(category, category, "") for category in list(CATEGORY_SUB_CATEGORY_MAPPING.keys())],
        name="Selected Category",
        update=lambda self, context: setattr(context.scene, "category", self.selected_category)
    )

    bpy.types.Scene.sub_category = bpy.props.StringProperty(name="Sub-Category")
    bpy.types.Scene.selected_sub_category = bpy.props.EnumProperty(
        items=lambda self, context: [
            (sub_category, sub_category, "") for sub_category in CATEGORY_SUB_CATEGORY_MAPPING.get(
                context.scene.selected_category, []
            )
        ],
        name="Selected Sub Category",
        update=lambda self, context: setattr(
            context.scene, "sub_category", self.selected_sub_category
        )
    )

    bpy.types.Scene.attributes = bpy.props.StringProperty(name="Attributes")


def unregister_classes_and_properties():
    """Unregister the classes and properties in Blender."""
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.server_address
    del bpy.types.Scene.server_status_label
    del bpy.types.Scene.category
    del bpy.types.Scene.sub_category
    del bpy.types.Scene.attributes


if __name__ == "__main__":
    register_classes_and_properties()
