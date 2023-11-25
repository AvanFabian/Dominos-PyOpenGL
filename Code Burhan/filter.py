import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

rotasiX = 0
rotasiY = 0
scale = 3


# create 3d cube
verticies = (
    (1, 1, 1), # 0
    (-1,  1, 1), # 1
    (-1,  -1, 1), # 2
    (1, -1, 1), # 3
    (1, 1, -1), # 4
    (-1,  1,  -1), # 5
    (-1, -1,  -1), # 6
    (1,  -1,  -1), # 7
    )

surfaces = (
    (0,1,2,3), #surface 0
    (4,5,6,7), #surface 1
    (0,3,7,4), #surface 2
    (1,2,6,5), #surface 3
    (0,1,5,4), #surface 4
    (3,2,6,7), #surface 5
    )


normals = [
    ( 0,  0, -1),  # surface 0
    ( 0,  0,  1),  # surface 1
    ( -1,  0,  0),  # surface 2
    ( 1,  0,  0),  # surface 3
    ( 0, -1,  0),  # surface 4
    ( 0, 1,  0)   # surface 5
]

colors = (
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (1,1,0),
    (1,0,1),
    (0,1,1)
    )
coords = [
    (0, 0),
    (1, 0),
    (1, 1),
    (0, 1)
]
# Load the texture
def load_texture():
    textureSurface = pygame.image.load('TextureImage/06.jpg')
    textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
    width = textureSurface.get_width()
    height = textureSurface.get_height()

    glEnable(GL_TEXTURE_2D)
    textureId = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textureId)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)


    # Pengaturan filtrasi tekstur warp mode
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)


    # flitter menggunakan mag dan min menggunakan linear
    # penggunaan GL_LINEAR akan membuat gambar menjadi blur atau halus baik di dekat maupun di jauh
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # flitter menggunakan mag dan min menggunakan linear
    # penggunaan GL_NEAREST akan membuat gambar menjadi pecah-pecah atau kasar baik di dekat maupun di jauh
    # glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    # glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)


    # glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    # glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    # glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    # glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    return textureId


def cube(texture):
    glBindTexture(GL_TEXTURE_2D, texture)
    glBegin(GL_QUADS)
    for i_surface, surface in enumerate(surfaces):
        x = 0
        glNormal3fv(normals[i_surface])
        for vertex in surface:
            x+=1
            glTexCoord2fv(coords[surface.index(vertex)])
            glVertex3fv(verticies[vertex])
    glEnd()

def show(Texture):
    glPushMatrix()
    glRotatef(rotasiX, 1, 0, 0)
    glRotatef(rotasiY, 0, 1, 0)
    glScalef(scale,scale,scale)
    cube(Texture)
    glPopMatrix()

def main():
    global rotasiX, rotasiY, scale
    material_ambient = (0.1, 0.1, 0.1, 1.0)
    material_diffuse = (0.7, 0.7, 0.7, 1.0)
    material_specular = (0.5, 0.5, 0.5, 1)
    material_shininess = 20

    pygame.init()
    display = (1000, 1000)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Gundam")
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_BLEND)

    # Set material properties
    glMaterialfv(GL_FRONT, GL_AMBIENT, material_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, material_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, material_specular)
    # glMaterialfv(GL_FRONT, GL_SHININESS, material_shininess)


    # glLightfv(GL_LIGHT0, GL_EMISSION, (1,0,0,1))
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5.0)
    glLightfv(GL_LIGHT0, GL_POSITION, (1, 1, -1, 0))    # Directional light dari (x, y, z), w

    # Load the texture
    textureId = load_texture()

    middle_mouse = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 2 :
                    middle_mouse = True
                elif event.button == 4 :
                    scale += 0.1
                elif event.button == 5 :
                    if scale <= 0 :
                        scale = 0
                    else :
                        scale -= 0.1
            if event.type == MOUSEBUTTONUP:
                if event.button == 2 :
                    middle_mouse = False
            if event.type == pygame.MOUSEMOTION:
                if middle_mouse:
                    mouse_dx, mouse_dy = event.rel
                    rotasiX += mouse_dy
                    rotasiY -= mouse_dx


        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        show(textureId)
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()