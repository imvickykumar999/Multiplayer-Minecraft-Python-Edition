
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

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

for z in range(10):
    for x in range(10):
        voxel = Voxel(position=(x,0,z))

def input(key):
    global player
    hit_info = raycast(camera.world_position, camera.forward, distance=100)

    if key == 'e': 
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

    if key == 'escape':
        exit()

window.fullscreen = 1
player = FirstPersonController(gravity = 0.5)

def update():
    if player.y < -5:
        player.y = 75 

Sky()
app.run()
