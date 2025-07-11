import glfw
import moderngl as gl

class Window:
    def __init__(self):
        if not glfw.init():
            raise RuntimeError("Couldn't initialise glfw")

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 2)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.SAMPLES, 4)

        self.monitor = glfw.get_primary_monitor()
        defaultVideoMode = glfw.get_video_mode(self.monitor)
        self.window = glfw.create_window(defaultVideoMode.size.width, defaultVideoMode.size.height, "Amethyst Rendering Engine", self.monitor, None)
        if not self.window:
            glfw.terminate()
            raise RuntimeError("Couldn't create window")
        
        self.isInFullscreen = True
        self.lastWindowPos = (100, 100)
        self.lastWindowSize = (640, 480)

        self.switchToWindowed()

        glfw.make_context_current(self.window)

        self.glContext = gl.create_context()

    def swapBuffers(self):
        glfw.swap_buffers(self.window)

    def pollEvents(self):
        glfw.poll_events()

    def shouldClose(self):
        return glfw.window_should_close(self.window)
    
    def getAspectRation(self):
        width, height = glfw.get_framebuffer_size(self.window)
        return width / height if height != 0 else 1.0
    
    def switchToFullscreen(self):
        self.lastWindowPos = glfw.get_window_pos(self.window)
        self.lastWindowSize = glfw.get_window_size(self.window)

        videoMode = glfw.get_video_mode(self.monitor)
        glfw.set_window_monitor(self.window, self.monitor, 0, 0, videoMode.size.width, videoMode.size.height, videoMode.refresh_rate)
        self.isInFullscreen = True

    def switchToWindowed(self):
        glfw.set_window_monitor(self.window, None, self.lastWindowPos[0], self.lastWindowPos[1], self.lastWindowSize[0], self.lastWindowSize[1], 0)
        self.isInFullscreen = False