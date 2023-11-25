import pygame as pg
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


# create 3D cube
vertices = (
    (1, 1, 1),  # 0
    (-1, 1, 1),  # 1
    (-1, -1, 1),  # 2
    (1, -1, 1),  # 3
    (1, 1, -1),  # 4
    (-1, 1, -1),  # 5
    (-1, -1, -1),  # 6
    (1, -1, -1),  # 7
)

surfaces = (
    (0, 1, 2, 3),  # surface 0
    (4, 5, 6, 7),  # surface 1
    (0, 3, 7, 4),  # surface 2
    (1, 2, 6, 5),  # surface 3
    (0, 1, 5, 4),  # surface 4
    (3, 2, 6, 7),  # surface 5
)

normals = [
    (0, 0, -1),  # surface 0
    (0, 0, 1),  # surface 1
    (-1, 0, 0),  # surface 2
    (1, 0, 0),  # surface 3
    (0, -1, 0),  # surface 4
    (0, 1, 0)  # surface 5
]

colors = (
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (1, 1, 0),
    (1, 0, 1),
    (0, 1, 1)
)

uv_coords = (
    (1, 1),  # 0
    (0, 1),  # 1
    (0, 0),  # 2
    (1, 0),  # 3
    (1, 1),  # 4
    (0, 1),  # 5
    (0, 0),  # 6
    (1, 0),  # 7
)

def cube():
    glBegin(GL_QUADS)
    for i_surface, surface in enumerate(surfaces):
        glNormal3fv(normals[i_surface])
        for vertex in surface:
            glTexCoord2fv(uv_coords[vertex])
            glVertex3fv(vertices[vertex])
    glEnd()

def load_texture(image_path):
    textureSurface = pg.image.load(image_path)
    textureData = pg.image.tostring(textureSurface, "RGBA", 1)
    width = textureSurface.get_width()
    height = textureSurface.get_height()
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    return texture

def show():
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture)
    glPushMatrix()
    # glRotatef(rotasiX, 1, 0, 0)
    # glRotatef(rotasiY, 0, 1, 0)
    # glScalef(scale, scale, scale)
    cube()
    glPopMatrix()

def main():
    global texture
    material_ambient = (0.1, 0.1, 0.1, 1.0)
    material_diffuse = (0.7, 0.7, 0.7, 1.0)
    material_specular = (0.5, 0.5, 0.5, 1)
    material_shininess = 20    
    # Inisiasi Pygame dan font-nya
    pg.init()
    pg.font.init()
    # Mengatur ukuran layar
    display = (800, 800)
    pg.display.set_mode(display, DOUBLEBUF | OPENGL)
    pg.display.set_caption("Domino Games")
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_BLEND)

    # Set material properties
    glMaterialfv(GL_FRONT, GL_AMBIENT, material_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, material_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, material_specular)

    gluPerspective(70, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5.0)
    glLightfv(GL_LIGHT0, GL_POSITION, (1, 1, -1, 0))

    texture = load_texture("TextureImage/init_bg.png")

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()       

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        show()
        pg.display.flip()
        pg.time.wait(10)

main()