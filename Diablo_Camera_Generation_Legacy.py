bl_info = {"name": "Diablo Reference Generation",
            "author": "Rut Bivrin",
            "version": (0, 0, 1),
            "blender": (2, 80, 0),
            "location": "3D Viewport > Sidebar > Diablo Reference Generation",
            "description": "Adding a button to automatically generate a reference camera, player and ground plane when working with Diablo metrics",
            "category": "Development"}


import bpy
import os
import urllib.request

def download_latest_version(url, file_path):
    try:
        response = urllib.request.urlopen(url)
        data = response.read()
        with open(file_path, 'wb') as file:
            file.write(data)
        return True
    except Exception as e:
        print(f"Failed to download the latest version: {e}")
        return False

def replace_addon_script():
    script_path = os.path.realpath(__file__)

    # Define the URL of the latest version of your add-on script
    latest_version_url = "https://raw.githubusercontent.com/Smileyfejs-Git/Reference-Generator/main/Diablo_Camera_Generation_Legacy.py"

    # Download the latest version
    if download_latest_version(latest_version_url, script_path):
        # Reload the add-on
        bpy.ops.script.reload()
        print("Add-on updated and reloaded successfully.")
    else:
        print("Failed to update the add-on.")

# Update Operator
class OBJECT_OT_UpdateAddon(bpy.types.Operator):
    bl_idname = "object.update_addon"
    bl_label = "Update Add-on"
    bl_description = "Download and update to the latest version of the add-on"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        replace_addon_script()
        return {'FINISHED'}


def add_diablo_ref(should_player_generate, should_ground_generate):

    if should_player_generate:
         # Create cube with player proportions for reference's sake
        bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(0.5, 0.5, 1), scale=(0.5, 0.5, 1))
         # Rename cube to "Player unit cube"
        bpy.context.object.name = "Player_Unit_Cube"

    if should_ground_generate:
         # Create ground reference plane
        bpy.ops.mesh.primitive_plane_add(enter_editmode=False, align='WORLD', location=(0,0,0))
         # Make ground plane large and in charge
        bpy.ops.transform.resize(value=(100, 100, 1), orient_type='LOCAL')
         # Rename the plane to "Ground plane"
        bpy.context.object.name = "Ground_Plane"

     # Generate reference camera for diablo metrics
    bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=((-19.459), (-19.459), 27.6), rotation=(0.785398, 0, -0.785398), scale=(1, 1, 1))
     # Rename reference camera
    bpy.context.object.name = "Diablo_Camera_Ref"

    bpy.ops.object.select_all(action='DESELECT')

     # Find every object (o) in the scene with these names
    for o in ("Player_Unit_Cube", "Ground_Plane", "Diablo_Camera_Ref"):
       obj = bpy.context.scene.objects.get(o) # Save found objects to a variable
       if obj: obj.select_set(True) # Select the found objects

     # Move selected objects to a new collection, inside the scene collection(collection_index=0)
    bpy.ops.object.move_to_collection(collection_index=0, is_new=True, new_collection_name='Generated_Reference_Objects')

     # Make the generated collection non-selectable to aid usability
    bpy.data.collections["Generated_Reference_Objects"].hide_select = True


class MESH_OT_add_diablo_ref(bpy.types.Operator):
    """Create a Player reference 1 unit wide and 2 units tall and slightly off center to mimic diablo"""
    """And generate a ground plane if necessary"""
    """And add a camera with the correct angle and distance"""

    bl_idname = "mesh.add_diablo_ref"
    bl_label = "Add Diablo Reference Objects"
    bl_options = {"REGISTER", "UNDO"}

    playerGeneration: bpy.props.BoolProperty(name="Include Player Reference", default=True, description="Do you want to include a player size reference?")
    groundGeneration: bpy.props.BoolProperty(name="Include Ground Plane", default=True, description="Do you want to include a Ground Plane?")

    def execute(self, context):

        add_diablo_ref(should_player_generate=self.playerGeneration, should_ground_generate=self.groundGeneration)

        return {"FINISHED"}


# Define the prefixes for highest order of category
environment_prefix = "EN_"
characters_prefix = "CH_"

# Define prefixes for lower order of category under "Environment"
wall_prefix = "W_" # w-bool property
ground_prefix = "G_" # g-bool property
destruction_prefix = "PH_" # ph-bool property
prop_Prefix = "P_" # p-bool property
sprite_prefix = "S_" # s-bool property

# Define prefixes for lower order of category under "Characters"
player_prefix = "PL_" # pl-bool property
npc_prefix = "NPC_" # npc-bool property
weapon_prefix = "WP_" # wp-bool property
gear_prefix = "GE_" # ge-bool property

# Define suffix for all categories
suffix = "_23G2"

replace_char = "."

def add_prefix_and_suffix(w, g, ph, p, s, pl, npc, wp, ge):

    # Loop through the selected objects
    for obj in bpy.context.selected_objects:

        obj.name = obj.name.replace(".", "_")

        obj.name = obj.name + suffix

        # add prefix depending on which option is chosen
        if w:
            obj.name = environment_prefix + wall_prefix + obj.name

        elif g:
            obj.name = environment_prefix + ground_prefix + obj.name

        elif ph:
            obj.name = environment_prefix + destruction_prefix + obj.name

        elif p:
            obj.name = environment_prefix + prop_Prefix + obj.name

        elif s:
            obj.name = environment_prefix + sprite_prefix + obj.name

        elif pl:
            obj.name = characters_prefix + player_prefix + obj.name

        elif npc:
            obj.name = characters_prefix + npc_prefix + obj.name

        elif wp:
            obj.name = characters_prefix + weapon_prefix + obj.name

        elif ge:
            obj.name = characters_prefix + gear_prefix + obj.name

class MESH_OT_add_prefix_and_suffix(bpy.types.Operator):
    bl_idname = "mesh.prefix_and_suffix"
    bl_label = "Add Prefixes and Suffixes"
    bl_options = {"REGISTER", "UNDO"}

    w: bpy.props.BoolProperty(name="Wall", default=False)
    g: bpy.props.BoolProperty(name="Ground", default=False)
    ph: bpy.props.BoolProperty(name="Destruction", default=False)
    p: bpy.props.BoolProperty(name="Prop", default=False)
    s: bpy.props.BoolProperty(name="Sprite", default=False)
    pl: bpy.props.BoolProperty(name="Player", default=False)
    npc: bpy.props.BoolProperty(name="NPC", default=False)
    wp: bpy.props.BoolProperty(name="Weapon", default=False)
    ge: bpy.props.BoolProperty(name="Gear", default=False)

    def execute(self, context):
        add_prefix_and_suffix(w=self.w, g=self.g, ph=self.ph, p=self.p, s=self.s, pl=self.pl, npc=self.npc, wp=self.wp, ge=self.ge)

        return {"FINISHED"}

class VIEW3D_PT_Generate_Diablo_Reference(bpy.types.Panel):

    # Where to add the panel in the UI
    bl_space_type = "VIEW_3D" # 3D Viewport area
    bl_region_type = "UI" # Sidebar region

    # Add labels
    bl_category = "Generate Diablo Reference" # Found in the sidebar
    bl_label = "Generate Diablo Reference" # Found at the top of the panel

    def draw(self, context):
        """Define the layout of the panel"""
        layout = self.layout

        row = self.layout.row()
        row.operator("mesh.add_diablo_ref", text="Add Diablo Reference")

        column = self.layout.column()
        column.operator("mesh.prefix_and_suffix", text="Add Prefixes and Suffixes")

         # Update Add-on
        self.layout.separator()
        row = layout.row()
        row.operator("object.update_addon", text="Update Add-on")

# Register the panel with Blender
def register():
    bpy.utils.register_class(VIEW3D_PT_Generate_Diablo_Reference)
    bpy.utils.register_class(MESH_OT_add_diablo_ref)
    bpy.utils.register_class(MESH_OT_add_prefix_and_suffix)
    bpy.utils.register_class(OBJECT_OT_UpdateAddon)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_UpdateAddon)
    bpy.utils.unregister_class(MESH_OT_add_prefix_and_suffix)
    bpy.utils.unregister_class(MESH_OT_add_diablo_ref)
    bpy.utils.unregister_class(VIEW3D_PT_Generate_Diablo_Reference)

if __name__ == "__main__":
    register()