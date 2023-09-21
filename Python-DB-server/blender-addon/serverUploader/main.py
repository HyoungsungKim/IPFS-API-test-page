import bpy
import requests
import io
import os
import tempfile
import zipfile
import mimetypes
from requests_toolbelt import MultipartEncoder


# DB_SERVER_ADDRESS = "http://127.0.0.1:8000"
# IPFS_ADDRESS = "http://10.252.107.31:5001"

CATEGORIES = [
    "3D Printable",
    "Anatomy",
    "Animals",
    "Animation",
    "Architecture",
    "Asset Libraries",
    "Base Meshes",
    "Buildings",
    "Characters",
    "Clothes & Accessories",
    "Creatures",
    "Decals",
    "Design Elements",
    "Electronics",
    "Engines & Parts",
    "Fantasy & Fiction",
    "Food & Drinks",
    "Furnishings",
    "Game Ready",
    "Humans",
    "Miscellaneous",
    "Motion Graphics",
    "Music",
    "Nature",
    "Parametric Models",
    "Products",
    "Science",
    "Sci-Fi",
    "Sports",
    "Tools",
    "Toys & Games",
    "Urban",
    "Vehicles",
    "Weapons & Armor"
]

# TEST_ANIMALS
SUB_CATEGORIES = [
    "Cat",
    "Dog",
    "Lion",
]


class ServerStatusPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_server_status_panel_custom"
    bl_label = "Server Uploader"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout

        # Server and IPFS address rows
        row = layout.row()
        row.label(text="Server Address:")
        row.prop(context.scene, "server_address", text="")
        
        row = layout.row()
        row.label(text="IPFS Address:")
        row.prop(context.scene, "ipfs_address", text="")
        
        # Sever Status indicator row
        row = layout.row()
        row.label(text="Server Status:")
        status_label = row.column(align=True)
        status_label.enabled = False
        status_label.operator("object.check_server", text=context.scene.server_status_label, icon='QUESTION')
        
        # IPFS Status indicator row
        row = layout.row()
        row.label(text="IPFS Status:")
        status_label = row.column(align=True)
        status_label.enabled = False
        status_label.operator("object.check_server", text=context.scene.ipfs_status_label, icon='QUESTION')

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
        content_id.operator("object.ipfs_upload", text=context.scene.content_id)

        # Upload to IPFS button
        row = layout.row()
        row.operator("object.ipfs_upload", text="Upload obj to IPFS")

        # Copy IPFS hash button
        ipfs_hash = context.scene.content_id
        if ipfs_hash:
            row = layout.row()
            row.operator("object.copy_ipfs_hash", text="Copy IPFS Hash", icon='COPYDOWN').ipfs_hash = ipfs_hash

        # API row
        row = layout.row()
        row.label(text="API Key:")
        row.prop(context.scene, "server_APIKey", text="")

        # Name row
        row = layout.row()
        row.label(text="Name:")
        row.prop(context.scene, "server_name", text="")

        # Tag row with box and column_flow
        box = layout.box()
        box.label(text="Hierarchy")
        col = box.column_flow(columns=1, align=True)
        col.prop(context.scene, "selected_category", text="Category")
        col.prop(context.scene, "selected_sub_category", text="Sub Category")
        
        col.label(text="Attributes")
        col.prop(context.scene, "attributes", text="")

        # Upload server button
        row = layout.row()
        row.operator("object.server_upload", text="Upload")



class OBJECT_OT_CheckServerOperator(bpy.types.Operator):
    bl_idname = "object.check_server"
    bl_label = "Check Server"

    def execute(self, context):
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
        try:
            # Send an HTTP GET request to the server
            response = requests.get(server_address)

            # Check the response status code
            return response.status_code == 200
        except requests.exceptions.RequestException:
            # An error occurred during the request
            return False

    def check_ipfs_availability(self, ipfs_address):
        try:
            # Send an HTTP POST request to the IPFS
            response = requests.post(f"{ipfs_address}/api/v0/version")

            # Check the response status code
            return response.status_code == 200
        except requests.exceptions.RequestException:
            # An error occurred during the request
            return False


class OBJECT_OT_IPFSUploadOperator(bpy.types.Operator):
    bl_idname = "object.ipfs_upload"
    bl_label = "IPFS Upload"

    def execute(self, context):
        ipfs_address = context.scene.ipfs_address
        obj =  obj = bpy.context.active_object

        # Check if the active object is a mesh object
        if obj.type == 'MESH':
            
            with tempfile.TemporaryDirectory() as temp_dir:
                # Set the export file paths
                obj_file_path = os.path.join(temp_dir, obj.name + ".obj")
                mtl_file_path = os.path.join(temp_dir, obj.name + ".mtl")
                zip_file_path = os.path.join(temp_dir, obj.name + ".zip")
                

                # Set the export options
                export_options = {
                    'use_selection': True,
                    'check_existing': False,
                    'axis_forward': 'Y',
                    'axis_up': 'Z',
                    'use_materials': True,
                    'use_triangles': True
                }

                # Export the object as OBJ
                bpy.ops.export_scene.obj(
                    filepath=obj_file_path,
                    **export_options
                )

                # Create a ZIP archive of the OBJ and MTL files
                with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
                    zip_file.write(
                        obj_file_path, arcname=os.path.basename(obj_file_path))
                    zip_file.write(
                        mtl_file_path, arcname=os.path.basename(mtl_file_path))

                
                # Test export file
                '''                
                output_dir = os.path.join("C:/Users/hskim/Documents/", obj.name + ".zip")
                
                bpy.ops.export_scene.obj(
                    filepath=os.path.join(output_dir, obj.name + "123456.obj"),
                    **export_options
                )
                
                with zipfile.ZipFile(output_dir, 'w') as zip_file:
                    zip_file.write(
                        obj_file_path, arcname=os.path.basename(obj_file_path))
                    zip_file.write(
                        mtl_file_path, arcname=os.path.basename(mtl_file_path))
                '''

                
                # Perform the file upload to IPFS
                with open(zip_file_path, 'rb') as zip_file:
                    ipfs_hash = self.upload_to_ipfs(ipfs_address, obj.name + ".zip", zip_file)
                    if ipfs_hash:
                        context.scene.content_id = f"{ipfs_hash}"
                    else:
                        context.scene.content_id = "Failed to upload OBJ to IPFS"
        else:
            context.scene.content_id = "No valid OBJ file associated with the active object"

        return {'FINISHED'}

    def upload_to_ipfs(self, ipfs_address, file_name, file):
        try:
            # Fix mtime to 0 to get a consistent content id
            files = {'file': (file_name, file)}
            response = requests.post(f"{ipfs_address}/api/v0/add?cid-version=1",
                                     files=files,
                                     )

            # Check the response status code
            if response.status_code == 200:
                # Extract the IPFS hash from the response JSON
                ipfs_hash = response.json().get('Hash')
                print(response.json())
                return ipfs_hash
            else:
                print(response.text)

        except requests.exceptions.RequestException:
            # An error occurred during the request
            return None


class OBJECT_OT_CopyIPFSHashOperator(bpy.types.Operator):
    bl_idname = "object.copy_ipfs_hash"
    bl_label = "Copy IPFS Hash"

    ipfs_hash: bpy.props.StringProperty()

    def execute(self, context):
        bpy.context.window_manager.clipboard = self.ipfs_hash
        self.report({'INFO'}, "IPFS Hash copied to clipboard")
        return {'FINISHED'}


class OBJECT_OT_ServerUploadOperator(bpy.types.Operator):
    bl_idname = "object.server_upload"
    bl_label = "Upload"

    def execute(self, context):
        server_address = context.scene.server_address
        api_key = context.scene.server_APIKey
        content_id = context.scene.content_id
        name = context.scene.server_name
        main_category = context.scene.main_category
        sub_category = context.scene.sub_category
        attributes_text = context.scene.attributes
        attributes = attributes_text.split(',').sort()
        
        # Construct the JSON data to be sent
        data = {
            "api_key": api_key,
            "content_id": content_id,
            "name": name,
            "main_category": main_category,
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
        except requests.exceptions.RequestException as e:
            # An error occurred during the request
            self.report({'ERROR'}, f"Request error: {e}")

        return {'FINISHED'}

    def check_server_availability(self, server_address):
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
        pass


classes = (
    ServerStatusPanel,
    OBJECT_OT_CheckServerOperator,
    OBJECT_OT_IPFSUploadOperator,
    OBJECT_OT_CopyIPFSHashOperator,
    OBJECT_OT_ServerUploadOperator,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.server_address = bpy.props.StringProperty(name="Server Address")
    bpy.types.Scene.ipfs_address = bpy.props.StringProperty(name="IPFS Address")

    bpy.types.Scene.server_status_label = bpy.props.StringProperty(name="Server Status Label")
    bpy.types.Scene.ipfs_status_label = bpy.props.StringProperty(name="IPFS Status Label")

    bpy.types.Scene.content_id = bpy.props.StringProperty(name="Content Id")
    bpy.types.Scene.server_APIKey = bpy.props.StringProperty(name="API key", subtype='FILE_NAME')
    bpy.types.Scene.server_name = bpy.props.StringProperty(name="Name", subtype='FILE_NAME')
    
    bpy.types.Scene.main_category = bpy.props.StringProperty(name="Main-Category")
    bpy.types.Scene.selected_category = bpy.props.EnumProperty(
        items=[(category, category, "") for category in CATEGORIES],
        name="Selected Category",
        update=lambda self, context: setattr(context.scene, "main_category", self.selected_category)
    )
    
    bpy.types.Scene.sub_category = bpy.props.StringProperty(name="Sub-Category")
    bpy.types.Scene.selected_sub_category = bpy.props.EnumProperty(
        items=[(sub_category, sub_category, "") for sub_category in SUB_CATEGORIES],
        name="Selected Sub Category",
        update=lambda self, context: setattr(context.scene, "sub_category", self.selected_sub_category)
    )
    
    bpy.types.Scene.attributes = bpy.props.StringProperty(name="Attributes")



def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.server_address
    del bpy.types.Scene.server_status_label
    del bpy.types.Scene.main_category
    del bpy.types.Scene.sub_category
    del bpy.types.Scene.attributes


if __name__ == "__main__":
    register()

