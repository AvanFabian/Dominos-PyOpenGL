import pygame  # Mengimpor modul pygame untuk mengakses fitur permainan
from pygame.locals import *
from OpenGL.GL import *  # Mengimpor fungsi-fungsi OpenGL untuk penggambaran 3D
from OpenGL.GLU import *  # Mengimpor modul OpenGL GLU untuk transformasi geometri

# Inisialisasi rotasi, skala, dan variabel-variabel lainnya
rotasiX = 45  # Sudut rotasi sepanjang sumbu X
rotasiZ = 45  # Sudut rotasi sepanjang sumbu Z
scale = 1.2  # Faktor skala objek
display = (1000, 1000) # ukuran layar

# Definisi verteks-verteks untuk membuat kubus 3D
verticies = (
    (1, 1, 1),   # 0
    (-1, 1, 1),  # 1
    (-1, -1, 1),  # 2
    (1, -1, 1),  # 3
    (1, 1, -1),  # 4
    (-1, 1, -1),  # 5
    (-1, -1, -1),  # 6
    (1, -1, -1),  # 7
)

# Definisi permukaan (surfaces) kubus
surfaces = (
    (0, 1, 2, 3),  # surface 0
    (4, 5, 6, 7),  # surface 1
    (0, 3, 7, 4),  # surface 2
    (1, 2, 6, 5),  # surface 3
    (0, 1, 5, 4),  # surface 4
    (3, 2, 6, 7),  # surface 5
)

# Normal vektor untuk masing-masing permukaan kubus
normals = [
    (0, 0, -1),  # surface 0
    (0, 0, 1),   # surface 1
    (-1, 0, 0),  # surface 2
    (1, 0, 0),   # surface 3
    (0, -1, 0),  # surface 4
    (0, 1, 0)    # surface 5
]

# Koordinat tekstur untuk masing-masing verteks
coords = [
    (0, 0), #0
    (1, 0), #1
    (1, 1), #2
    (0, 1) #3
]

def Linear_only():
    # Fungsi untuk mengatur filter tekstur menjadi GL_LINEAR
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)  # Pengaturan filter magnifikasi
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)  # Pengaturan filter minifikasi

def Nearest_Only():
    # Fungsi untuk mengatur filter tekstur menjadi GL_NEAREST
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

def Nearest_mipmap_only():
    # Fungsi untuk mengatur filter tekstur menjadi GL_NEAREST
    # dan juga menghasilkan mipmap dengan metode GL_NEAREST_MIPMAP_NEAREST.
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_NEAREST)
    glGenerateMipmap(GL_TEXTURE_2D)  # Menghasilkan mipmap untuk tekstur

def Nearest_mipmap_Linear():
    # Fungsi untuk mengatur filter tekstur menjadi GL_NEAREST
    # dan juga menghasilkan mipmap dengan metode GL_NEAREST_MIPMAP_LINEAR.
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_LINEAR)
    glGenerateMipmap(GL_TEXTURE_2D)

def Linear_mipmap_only():
    # Fungsi untuk mengatur filter tekstur menjadi GL_LINEAR
    # dan juga menghasilkan mipmap dengan metode GL_LINEAR_MIPMAP_LINEAR.
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glGenerateMipmap(GL_TEXTURE_2D)

def Linear_mipmap_Nearest():
    # Fungsi untuk mengatur filter tekstur menjadi GL_LINEAR
    # dan juga menghasilkan mipmap dengan metode GL_LINEAR_MIPMAP_NEAREST.
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_NEAREST)
    glGenerateMipmap(GL_TEXTURE_2D)


# Load the texture
def load_texture():
    textureSurface = pygame.image.load('TextureImage/texture_mipmap.png')                                                # Memuat gambar tekstur dari file 'texture_mipmap.png'
    textureData = pygame.image.tostring(textureSurface, "RGBA", 1)                                          # Mengambil data tekstur sebagai string dengan format RGBA

    # Mendapatkan lebar dan tinggi tekstur
    width = textureSurface.get_width()
    height = textureSurface.get_height()

    glEnable(GL_TEXTURE_2D)                                                                                 # Mengaktifkan penggunaan tekstur dalam mode OpenGL
    textureId = glGenTextures(1)                                                                            # Membuat ID tekstur
    glBindTexture(GL_TEXTURE_2D, textureId)                                                                 # mengikat ID tekstur yang baru dibuat (textureId) ke target GL_TEXTURE_2D.
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)       # Mengisi data tekstur ke dalam buffer OpenGL

    # memanggil fungsi filter ATAU mipmap
    # Panggil fungsi filter di bawah sini
    #Linear_only()
    #Nearest_Only()
    # Panggil fungsi mipmap di bawah sini
    # Linear_mipmap_only()
    # Linear_mipmap_Nearest()
    # Nearest_mipmap_only()
    Nearest_mipmap_Linear()

    return textureId

def cube(texture):
    glBindTexture(GL_TEXTURE_2D, texture)                   # mengikat ID tekstur yang akan digunakan saat menggambar kubus dengan tekstur.
    glBegin(GL_QUADS)                                       # Memulai menggambar dengan jenis poligon GL_QUADS
    for i_surface, surface in enumerate(surfaces):          # Loop melalui permukaan (surfaces) kubus
        glNormal3fv(normals[i_surface])                     # Mengatur vektor normal untuk permukaan saat ini
        for vertex in surface:                              # Loop melalui verteks-verteks dalam permukaan saat ini
            glTexCoord2fv(coords[surface.index(vertex)])    # Mengatur koordinat tekstur untuk verteks saat ini
            glVertex3fv(verticies[vertex])                  # Menggambar verteks dalam koordinat 3D
    glEnd()                                                 # Selesai menggambar poligon


def show(Texture):                  #Menampilkan kubus
    glPushMatrix()
    glRotatef(rotasiX, 1, 0, 0)     #Menetapkan rotasi sumbu X
    glRotatef(rotasiZ, 0, 0, 1)     #Menetapkan rotasi sumbu Z
    glScalef(scale,scale,scale)     #Menetapkan interaksi zoom in zoom out
    cube(Texture)                   #Menggambar kubus
    glPopMatrix()

def main():
    global rotasiX, rotasiZ, scale  # Variabel global untuk rotasi dan skala
    material_ambient = (0.1, 0.1, 0.1, 1.0)  # Sifat ambient material
    material_diffuse = (0.7, 0.7, 0.7, 1.0)  # Sifat diffuse material
    material_specular = (0.5, 0.5, 0.5, 1)  # Sifat specular material

    pygame.init()  # Inisialisasi modul Pygame
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)  # Membuat jendela OpenGL
    pygame.display.set_caption("Percobaan Mapping Texture Mipmap")  # Menetapkan judul jendela
    glEnable(GL_DEPTH_TEST)  # Mengaktifkan uji kedalaman
    glEnable(GL_COLOR_MATERIAL)  # Mengaktifkan bahan warna
    glEnable(GL_LIGHTING)  # Mengaktifkan pencahayaan
    glEnable(GL_LIGHT0)  # Mengaktifkan cahaya 0
    glEnable(GL_BLEND)  # Mengaktifkan blending

    # Mengatur properti material
    glMaterialfv(GL_FRONT, GL_AMBIENT, material_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, material_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, material_specular)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)  # Mengatur perspektif
    glTranslatef(0.0, 0.0, -5.0)  # Menggeser objek dalam sumbu Z negatif
    glRotatef(180, 0, 0, 1)  # Memutar objek 180 derajat sekitar sumbu Z
    glLightfv(GL_LIGHT0, GL_POSITION, (-1, 1, 1, 0))  # Mengatur posisi cahaya

    # Memuat tekstur
    textureId = load_texture()

    left_mouse = False  # Untuk melacak tombol kiri mouse

    while True:  # Loop utama
        for event in pygame.event.get():  # Mendapatkan peristiwa Pygame
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == MOUSEBUTTONDOWN:  # Ketika tombol mouse ditekan
                if event.button == 1:  # Tombol kiri
                    left_mouse = True
                elif event.button == 4:  # Tombol gulir ke atas
                    scale += 0.01  # Menambahkan faktor skala
                elif event.button == 5:  # Tombol gulir ke bawah
                    if scale <= 0:
                        scale = 0
                    else:
                        scale -= 0.01  # Mengurangkan faktor skala
            if event.type == MOUSEBUTTONUP:  # Ketika tombol mouse dilepaskan
                if event.button == 1:  # Tombol kiri
                    left_mouse = False
            if event.type == pygame.MOUSEMOTION:  # Ketika mouse bergerak
                if left_mouse:  # Jika tombol kiri mouse ditekan
                    mouse_dx, mouse_dy = event.rel
                    rotasiX += -mouse_dy  # Merotasi sekitar sumbu X
                    rotasiZ -= mouse_dx  # Merotasi sekitar sumbu Z

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Menghapus buffer warna dan kedalaman
        show(textureId)  # Menampilkan objek kubus dengan tekstur
        pygame.display.flip()  # Memperbarui tampilan
        pygame.time.wait(10)  # Menunggu 10 milidetik

if __name__ == "__main__":
    main()
