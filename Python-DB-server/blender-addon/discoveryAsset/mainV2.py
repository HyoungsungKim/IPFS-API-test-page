import json
import bpy
import requests
import webbrowser


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

class QueryByTagsPannel(bpy.types.Panel):
    bl_label = "Discovery Asset"
    bl_idname = "PT_DiscoveryAssetPanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

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

        # Tag row with box and column_flow
        box = layout.box()
        box.label(text="Hierarchy")
        col = box.column_flow(columns=1, align=True)
        col.prop(scene, "selected_category", text="Category")
        col.prop(scene, "selected_sub_category", text="Sub Category")
            
        # Query to IPFS button
        row = layout.row()
        row.operator("object.query_to_ipfs", text="Query to IPFS")
        
        # Display query result
        row = layout.row()
        
        # Display query result
        if context.scene.query_response:
            response_json = json.loads(context.scene.query_response)
            box = self.layout.box()
            box.label(text="Query Results")
            
            row = box.row()
            row.label(text="Content ID")
            row.label(text="Name")
            row.label(text="Category")
            row.label(text="Sub Category")
            row.label(text="Attributes")
            row.label(text="Open in Browser")  # New column for the button
            
            for i, item in enumerate(response_json):
                row = box.row()
                row.label(text=str(item['content_id']))
                row.label(text=str(item['name']))
                row.label(text=str(item['category']))
                row.label(text=str(item['sub_category']))
                row.label(text=str(item['attributes']))
                
                 # Add button to open IPFS URL
                ipfs_url = f"https://ipfs.io/ipfs/{item['content_id']}"
                row.operator("wm.open_url", text="Open").url = ipfs_url

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

class QueryToIPFSOperator(bpy.types.Operator):
    bl_idname = "object.query_to_ipfs"
    bl_label = "Query to IPFS"
    
    def execute(self, context):
        '''TO BE DEFINED'''
        self.query_by_tags(context)
        return {'FINISHED'}
        
    def query_by_tags(self, context):
        selected_category = context.scene.selected_category
        selected_sub_category = context.scene.selected_sub_category
        server_address = context.scene.server_address
        
        if not selected_category:
            return {'FINISHED'}
        
        if selected_sub_category:
            '''Use category only for a query'''
            response = requests.get(f"{server_address}/query/categories?category={selected_category}&sub_category={selected_sub_category}")
        else:
            '''Use category and sub_category for a query'''
            response = requests.get(f"{server_address}/query/categories?category={selected_category}")
        
        context.scene.query_response = json.dumps(response.json())        
        return {'FINISHED'}
 
class OpenURLOperator(bpy.types.Operator):
    bl_idname = "wm.open_url"
    bl_label = "Open URL"

    url: bpy.props.StringProperty()

    def execute(self, context):
        webbrowser.open(self.url)
        return {'FINISHED'}

classes = (
    QueryByTagsPannel,
    ServerCheckOperator,
    QueryToIPFSOperator,
    OpenURLOperator,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
    bpy.types.Scene.server_address = bpy.props.StringProperty(name="Server Address")
    bpy.types.Scene.ipfs_address = bpy.props.StringProperty(name="IPFS Address")

    bpy.types.Scene.server_status_label = bpy.props.StringProperty(name="Server Status Label")
    bpy.types.Scene.ipfs_status_label = bpy.props.StringProperty(name="IPFS Status Label")
    bpy.types.Scene.query_response = bpy.props.StringProperty(name="Query Response")
    
    bpy.types.Scene.selected_category = bpy.props.EnumProperty(
        items=[(category, category, "") for category in list(CATEGORY_SUB_CATEGORY_MAPPING.keys())],
        name="Selected Category",
        update=lambda self, context: setattr(context.scene, "main_category", self.selected_category)
    )

    bpy.types.Scene.SUB_Category = bpy.props.StringProperty(name="Sub-Category")
    bpy.types.Scene.selected_sub_category = bpy.props.EnumProperty(
        items=lambda self, context: [
            (sub_category, sub_category, "") for sub_category in sorted(CATEGORY_SUB_CATEGORY_MAPPING.get(
                context.scene.selected_category, []
            ))
        ],
        name="Selected Sub Category",
        update=lambda self, context: setattr(
            context.scene, "sub_category", self.selected_sub_category
        )
    )

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        
    del bpy.types.Scene.server_address

    del bpy.types.Scene.server_status_label
    del bpy.types.ipfs_status_label
    
    del bpy.types.Scene.query_response
    del bpy.types.Scene.category
    del bpy.types.Scene.sub_category
    del bpy.types.Scene.main_category
    del bpy.types.Scene.sub_category
    

if __name__ == "__main__":
    register()
