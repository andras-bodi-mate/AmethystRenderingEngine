import threading
import glfw
from pyglm import glm

from window import Window
from camera import Camera
from materials import Material
from environment import Environment
from gltfLoader import GltfLoader

class App:
    def __init__(self):
        self.window = Window()
        self.camera = Camera(cameraPath = "res/models/cameraPath2.obj", cameraPathScale = 1.0)
        self.gltfLoader = GltfLoader("res/environments/mountain.hdr")
        self.scene = self.gltfLoader.loadScene("res/scenes/Scifi Helmet/scifiHelmet.gltf")

        self.isRunning = True

    def draw(self):
        Material.updateUniformForAllMaterials("u_viewTransform", self.camera.viewTransform)
        Material.updateUniformForAllMaterials("u_projectionTransform", self.camera.projectionTransform)
        Material.updateUniformForAllMaterials("u_cameraPosition", self.camera.position)

        self.scene.render()

    def renderLoop(self):
        glfw.make_context_current(self.window.window)
        self.window.glContext.multisample = True
        self.window.glContext.depth_func = "<="
        self.window.glContext.enable(self.window.glContext.DEPTH_TEST)

        while self.isRunning and not self.window.shouldClose():
            width, height = glfw.get_framebuffer_size(self.window.window)
            self.window.glContext.viewport = (0, 0, width, height)

            self.camera.updateMatrices(width / height if height != 0 else 1.0)

            self.window.glContext.clear(0.7, 0.7, 0.7)
            self.draw()
            self.window.swapBuffers()

        glfw.make_context_current(None)
        glfw.set_window_should_close(self.window.window, True)
        print("Window should close soon.")

    def eventLoop(self):
        while not self.window.shouldClose():
            self.window.pollEvents()

    def mainLoop(self):
        self.draw()
        self.window.swapBuffers()
        self.window.pollEvents()

    def start(self):
        glfw.make_context_current(None)

        renderThread = threading.Thread(target = self.renderLoop)
        renderThread.start()

        self.eventLoop()

        self.isRunning = False
        print("Waiting for rendering thread to stop...")
        renderThread.join()
        print("Rendering thread successfully stopped.")

        print("Terminating GLFW...")
        glfw.terminate()
        print("GLFW terminated.")