from sys import stderr

import bpy
from mathutils import Vector


def calculate_perimeter(vertices):
    """Given vertices in sequence closing a loop, compute the perimeter."""
    # Ensure there are at least two vertices
    if len(vertices) < 2:
        return 0.0
    # We assume that the vertices are stored in the order they should be traversed
    vertices = [vertex.co for vertex in vertices]
    perimeter = 0.0
    # Loop through each vertex and calculate distance to the next vertex
    for i in range(len(vertices)):
        v1 = vertices[i]
        v2 = vertices[(i + 1) % len(vertices)]  # Wrap around to the start
        # Compute the distance between v1 and v2
        distance = (v2 - v1).length
        perimeter += distance
    return perimeter


def bounding_box_center(model: bpy.types.Object):
    """Given a model (3D mesh), compute the center of its bounding box."""
    # Get the bounding box of the model
    bbox = model.bound_box
    center = ((bbox[0][0] + bbox[7][0]) / 2,
              (bbox[0][1] + bbox[7][1]) / 2,
              (bbox[0][2] + bbox[7][2]) / 2)
    return center


def lowest_bbox_point(model: bpy.types.Object):
    """Given a model (3D mesh), return the lowest point along the Z axis of its bounding box."""
    world_bbox_corners = [model.matrix_world @ Vector(corner) for corner in model.bound_box]
    return min(world_bbox_corners, key=lambda x: x[2])


def highest_bbox_point(model: bpy.types.Object):
    """Given a model (3D mesh), return the highest point along the Z axis of its bounding box."""
    world_bbox_corners = [model.matrix_world @ Vector(corner) for corner in model.bound_box]
    return max(world_bbox_corners, key=lambda x: x[2])


def intersect_meshes(main_mesh: bpy.types.Object, other_mesh: bpy.types.Object):
    """Create a modifier for the main mesh with the intersection with the second mesh.
       In the end, applies the modifier, effectively modifying the main mesh.
       Ideally, the main mesh should be manifold
       (see https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/booleans.html)."""
    # Create and apply the intersection boolean modifier
    modifier = main_mesh.modifiers.new(name='Boolean', type='BOOLEAN')
    modifier.operation = 'INTERSECT'
    modifier.object = other_mesh
    modifier.solver = 'FAST'  # OR 'EXACT'
    bpy.ops.object.modifier_apply(modifier=modifier.name)
    # Another way of doing it, works too
    # bpy.ops.object.modifier_add(type='BOOLEAN')
    # bpy.context.object.modifiers['Boolean'].operation = 'INTERSECT'
    # bpy.context.object.modifiers['Boolean'].object = model
    # bpy.context.object.modifiers['Boolean'].solver = 'FAST'  # OR 'EXACT'
    # bpy.ops.object.modifier_apply(modifier='Boolean')  # We didn't define a name, 'Boolean' is the default one?


def keep_top_of_slice(mesh: bpy.types.Object):
    """Given a slice, remove all vertices except the ones at the highest point along the Z axis."""
    # Note: the origin of the mesh is not changed, thus after we remove the vertices, the origin
    # which was the center of slice volume, will probably be displaced from the resulting surface

    # We need first to switch to edit mode, then deselect vertices,
    # then switch to object mode, then select vertices, then back to edit, and they will be selected.
    # This is probably counter-intuitive, but we have to place the Object in OBJECT mode when doing selection
    # via Python, and then flip back to EDIT mode to see the result.
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    z_to_keep = max(vertex.co.z for vertex in mesh.data.vertices)
    for vertex in mesh.data.vertices:
        if abs(vertex.co.z - z_to_keep) > 0.0001:  # NOT almost equal
            vertex.select = True

    bpy.ops.object.mode_set(mode='EDIT')
    # At last, we delete the selected vertices
    bpy.ops.mesh.delete(type='VERT')
    # We could delete the face too, but we would see in blender only one polygon at a time in edit mode
    # (in edit mode we see clearly the vertices of the polygon, but only of the selected polygon)
    # bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
    # bpy.ops.mesh.select_all(action='SELECT')
    # bpy.ops.mesh.delete(type='ONLY_FACE')
    # bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
    # Go back to object mode
    bpy.ops.object.mode_set(mode='OBJECT')


def find_centroid(mesh: bpy.types.Object, update_origin=False):
    """Given a SURFACE mesh, find its center of mass, optionally update the origin to it."""
    # Store the current selection and active object
    previous_selection = bpy.context.selected_objects
    previous_active = bpy.context.view_layer.objects.active

    # Select the mesh and make it active
    bpy.context.view_layer.objects.active = mesh
    # Save the previous origin
    previous_origin = mesh.location.copy()
    # Find the center of mass (this will also move the origin)
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')
    centroid = mesh.location.copy()
    # Optionally revert back the origin
    if not update_origin:
        bpy.context.scene.cursor.location = previous_origin
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='BOUNDS')

    # Restore previous selection and active object
    bpy.context.view_layer.objects.active = previous_active
    bpy.ops.object.select_all(action='DESELECT')
    for ob in previous_selection:
        ob.select_set(True)

    return centroid


def find_intersection_same_Z(point: Vector, direction: Vector, polygon):
    """Given a point, a direction and a convex polygon in the same Z-plane,
       compute the point where a vector starting from the point in the given
       direction would intersect the polygon."""
    x0, y0, z0 = point
    dx, dy = direction.xy

    intersection = None

    for i in range(len(polygon)):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % len(polygon)]

        x1, y1 = p1.co.xy
        x2, y2 = p2.co.xy

        # Direction vector for the edge
        edge_dx = x2 - x1
        edge_dy = y2 - y1

        # Calculate the denominator (parallel check is not needed since no edges are parallel)
        denominator = dx * edge_dy - dy * edge_dx

        # Compute t and s directly
        t = ((x1 - x0) * edge_dy - (y1 - y0) * edge_dx) / denominator
        s = ((x1 - x0) * dy - (y1 - y0) * dx) / denominator

        # Check if the intersection point is within the edge segment (0 <= s <= 1) and is in the correct direction (t>0)
        if 0 <= s <= 1 and t > 0:
            intersection_x = x0 + t * dx
            intersection_y = y0 + t * dy
            intersection = Vector((intersection_x, intersection_y, z0))
            break

    return intersection


def create_slices(model: bpy.types.Object, slices=100):
    """Given a model (3D mesh), create slices along the Z axis and return their top surfaces."""
    name = model.name
    data = model.data

    # Create materials
    mat = bpy.data.materials.new('Neutral')  # apparently, the first material will be the default for new objects
    data.materials.append(mat)
    materials_idx = {'Neutral': len(data.materials) - 1}
    materials = {'Neutral': mat}
    newmat = (('Red', (1, 0, 0, 1.0)), ('Green', (0, 1.0, 0, 1.0)), ('Blue', (0, 0, 1.0, 1.0)))
    for name, rgb in newmat:
        mat = bpy.data.materials.new(name)
        mat.diffuse_color = rgb
        data.materials.append(mat)
        materials_idx[name] = len(data.materials) - 1
        materials[name] = mat

    # Calculate the lowest point of the bounding box in world space
    lowest_point = lowest_bbox_point(model)
    highest_point = highest_bbox_point(model)
    radius = max(int(model.dimensions.x+1), int(model.dimensions.y+1)) * 0.6
    # We round to 5 places, just to make visual inspection easier
    top, base = round(highest_point.z, 5), round(lowest_point.z, 5)
    height = round((top - base) / slices, 5)

    # Create collection to add polygons (just for better organization)
    polygons = bpy.data.collections.new('Polygons')
    bpy.context.scene.collection.children.link(polygons)
    layer_polygons = bpy.context.view_layer.layer_collection.children[polygons.name]
    spheres = bpy.data.collections.new('Spheres')
    bpy.context.scene.collection.children.link(spheres)
    layer_spheres = bpy.context.view_layer.layer_collection.children[spheres.name]
    original_layer = bpy.context.view_layer.active_layer_collection

    # Calculate the center of the bounding box
    center = bounding_box_center(model)

    # Starting from the lowest point, create cylinders (slices) and intersect with the model
    x, y = center[0], center[1]
    for i in range(slices):
        z = base + i * height
        # Set the polygon layer as active
        bpy.context.view_layer.active_layer_collection = layer_polygons
        # Create cylinder for computing the intersection
        bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=height, location=(x, y, z), enter_editmode=False)
        cylinder = bpy.context.active_object
        cylinder.name = 'Poly.%03d' % i
        # Create and apply the intersection boolean modifier
        intersect_meshes(cylinder, model)
        # Then remove all but the top vertices of the slice
        keep_top_of_slice(cylinder)

        # Compute the perimeter
        perimeter = calculate_perimeter(cylinder.data.vertices)
        # Find the centroid
        centroid = find_centroid(cylinder, update_origin=True)
        # Set the sphere layer as active
        bpy.context.view_layer.active_layer_collection = layer_spheres
        # Draw a sphere centered on the centroid
        bpy.ops.mesh.primitive_uv_sphere_add(radius=radius/50, location=centroid)
        sphere = bpy.context.active_object
        sphere.name = 'Sphere.%03d' % i
        # Find where the vector starting from the centroid in the direction of the Y-axis intersects the slice
        intersect = find_intersection_same_Z(centroid, Vector((0, 1, 0)), cylinder.data.vertices)
        if intersect:
            sphere.data.materials.append(materials['Blue'])
            bpy.ops.mesh.primitive_uv_sphere_add(radius=radius / 50, location=intersect)
            sphereb = bpy.context.active_object
            sphereb.name = 'Sphere-b.%03d' % i
            sphereb.data.materials.append(materials['Green'])
        else:
            sphere.data.materials.append(materials['Red'])

        print('%s: perimeter =' % cylinder.name, perimeter, 'centroid =', centroid)

    # Revert back to the original layer
    bpy.context.view_layer.active_layer_collection = original_layer


# TODO: computar centroide e etc
# #        # Find the centroid of the intersected slice
# #        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')
#
# #        # Create a new sphere at the centroid
# #        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.005, location=obj.location)

# import mathutils
# obj = bpy.context.active_object
# origin = obj.location
# # Define the direction of the vector (Y-axis in local space)
# direction = Vector((0.0, 1.0, 0.0))
# # Transform the direction to world space
# direction = obj.matrix_world.to_3x3() @ direction
# # Perform ray casting
# result, location, normal, face_index = obj.ray_cast(origin, direction)

def main():
    # Get the object (there should be only 1 mesh object)
    C = bpy.context
    D = bpy.data
    file = bpy.data.filepath
    objects = [o for o in D.objects.values() if o.type == 'MESH']

    if len(objects) != 1:
        print('ERROR: more than 1 object detected for file %s!' % file, stderr)
        exit(1)

    model = objects[0]
    create_slices(model)


if __name__ == '__main__':
    main()
