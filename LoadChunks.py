from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

chunk_size = 10  # Define the size of each chunk
loaded_chunks = {}  # Keep track of loaded chunks

class Voxel(Button):
    def __init__(self, position=(0,0,0), 
                 texture='grass',
                 default_color=color.green,
                 ):
        super().__init__(parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture=texture,
            highlight_color=color.red,
            color=default_color,
        )

def load_chunk(chunk_x, chunk_z):
    # Load a chunk of voxels at the given chunk coordinates
    for z in range(chunk_size):
        for x in range(chunk_size):
            voxel = Voxel(position=(chunk_x * chunk_size + x, 0, chunk_z * chunk_size + z))

def input(key):
    global player
    hit_info = raycast(camera.world_position, camera.forward, distance=100)

    if key == 'e' and hit_info.hit:  # Check if something was hit
        player.x = hit_info.entity.position.x
        player.y = hit_info.entity.position.y
        player.z = hit_info.entity.position.z

    if key == 'left mouse down':
        if hit_info.hit:
            Voxel(position=hit_info.entity.position + hit_info.normal, 
                  texture='brick',
                  default_color=color.orange,
                )
            
    if key == 'right mouse down' and mouse.hovered_entity:
        destroy(mouse.hovered_entity)

    if key == 'escape':  # Check for the escape key
        app.quit()  # Exit the game

def update():
    global player
    if player.y < -5:
        player.y = 75 
    
    chunk_x = int(player.x // chunk_size)
    chunk_z = int(player.z // chunk_size)
    
    # Load surrounding chunks
    for dz in range(-1, 2):
        for dx in range(-1, 2):
            chunk_pos = (chunk_x + dx, chunk_z + dz)
            if chunk_pos not in loaded_chunks:
                load_chunk(chunk_x + dx, chunk_z + dz)
                loaded_chunks[chunk_pos] = True

window.fullscreen = 1
player = FirstPersonController(gravity = 0.5)

Sky()
app.run()
