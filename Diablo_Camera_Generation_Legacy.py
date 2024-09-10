bl_info = {"name": "Diablo Reference Generation", 
            "author": "Rut Bivrin", 
            "version": (0, 0, 1), 
            "blender": (2, 80, 0), 
            "location": "3D Viewport > Sidebar > Diablo Reference Generation",
            "description": "Adding a button to automatically generate a reference camera, player and ground plane when working with Diablo metrics",
            "category": "Development"}


import bpy

def add_diablo_ref(shouldPlGenerate, shouldGrGenerate):
   
    if shouldPlGenerate == True:
         # Create cube with player proportions for reference sake
        bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(0.5, 0.5, 1), scale=(0.5, 0.5, 1))
         # Rename cube to "Player unit cube"
        bpy.context.object.name = "Player_Unit_Cube"
       
    if shouldGrGenerate == True: 
         # Create ground reference plane
        bpy.ops.mesh.primitive_plane_add(enter_editmode=False, align='WORLD', location=(0,0,0))
         # Make ground plane large and in charge
        bpy.ops.transform.resize(value=(100, 100, 1), orient_type='LOCAL')
         # Rename the plane to "Ground plane"
        bpy.context.object.name = "Ground_Plane"
        
     # Generate referance camera for diablo metrics
    bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=((-19.459), (-19.459), 27.6), rotation=(0.785398, 0, -0.785398), scale=(1, 1, 1))
     # Rename referance camera
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
    """And generate a ground plane if nessessary"""
    """And add a camera with the correct angle and distance"""
    
    bl_idname = "mesh.add_diablo_ref"
    bl_label = "Add Diablo Reference Objects"
    bl_options = {"REGISTER", "UNDO"}
    
    playerGeneration: bpy.props.BoolProperty(name="Include Player Reference", default=True, description="Do you want to include a player size reference?")
    groundGeneration: bpy.props.BoolProperty(name="Include Ground Plane", default=True, description="Do you want to include a Ground Plane?")
    
    def execute(self, context):
        
        add_diablo_ref(shouldPlGenerate=self.playerGeneration, shouldGrGenerate=self.groundGeneration)
        
        return {"FINISHED"}
    
    
class VIEW3D_PT_Generate_Diablo_Reference(bpy.types.Panel):
    
    # Where to add the panel in the UI
    bl_space_type = "VIEW_3D" # 3D Viewport area
    bl_region_type = "UI" # Sidebar region
    
    # Add labes
    bl_category = "Generate Diablo Reference" # Found in the sidebar
    bl_label = "Generate Diablo Reference" # Found at the top of the panel
    
    def draw(self, context):
        """Define the layout of the panel"""
        row = self.layout.row()
        row.operator("mesh.add_diablo_ref", text="Add Diablo Reference")
        
# Register the panel with Blender
def register():
    bpy.utils.register_class(VIEW3D_PT_Generate_Diablo_Reference)
    bpy.utils.register_class(MESH_OT_add_diablo_ref)
    
def unregister():
    bpy.utils.register_class(MESH_OT_add_diablo_ref)
    bpy.utils.unregister_class(VIEW3D_PT_Generate_Diablo_Reference)
    
if __name__ == "__main__":
    register()