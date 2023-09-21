import bpy

class TagSuggestPanel(bpy.types.Panel):
    bl_label = "Discovery Asset"
    bl_idname = "PT_DiscoveryAssetPanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene, "tag_input")
        
        layout.prop(scene, "selected_tags", text="Select Tags")
        layout.operator("object.add_tags", text="Add Tags")
        
        selected_tags = [tag for i, tag in enumerate(scene.tag_vector) if tag]
        for tag in selected_tags:
            layout.label(text=tag)


def register():
    bpy.utils.register_class(TagSuggestPanel)
    bpy.types.Scene.tag_input = bpy.props.StringProperty(name="Tag Input")
    bpy.types.Scene.selected_tags = bpy.props.EnumProperty(
        items=get_suggestions_enum_items,
        name="Selected Tags"
    )
    bpy.types.Scene.tag_list = bpy.props.StringProperty(name="Tag List")
    bpy.types.Scene.tag_vector = bpy.props.BoolVectorProperty(size=3, name="Tag Vector")

def unregister():
    bpy.utils.unregister_class(TagSuggestPanel)
    del bpy.types.Scene.tag_input
    del bpy.types.Scene.selected_tags
    del bpy.types.Scene.tag_list
    del bpy.types.Scene.tag_vector

def get_suggestions(input_text):
    existing_tags = ["animation", "animal", "sport"]
    suggestions = [tag for tag in existing_tags if tag.startswith(input_text)]
    return suggestions

def get_suggestions_enum_items(self, context):
    suggestions = get_suggestions(self.tag_input)
    return [(tag, tag, "") for tag in suggestions]

def add_tags(self, context):
    if self.selected_tags:
        selected_tags = self.selected_tags.split(',')
        
        tag_vector = [False, False, False]
        for i, tag in enumerate(selected_tags[:3]):
            tag_vector[i] = True
        bpy.context.scene.tag_vector = tag_vector

        if self.tag_list:
            self.tag_list += f", {self.selected_tags}"
        else:
            self.tag_list = self.selected_tags
        
        self.selected_tags = ""

if __name__ == "__main__":
    register()
