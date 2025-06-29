import glfw
import moderngl as gl

class Window:
    def __init__(self):
        if not glfw.init():
            raise RuntimeError("Couldn't initialise glfw")

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        #glfw.window_hint(glfw.SAMPLES, 8)

        self.window = glfw.create_window(640, 480, "Hello World", None, None)
        if not self.window:
            glfw.terminate()
            raise RuntimeError("Couldn't create window")

        glfw.make_context_current(self.window)

        self.glContext = gl.create_context()

    def swapBuffers(self):
        glfw.swap_buffers(self.window)

    def pollEvents(self):
        glfw.poll_events()

    def shouldClose(self):
        return glfw.window_should_close(self.window)