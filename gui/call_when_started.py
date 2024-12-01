import dearpygui.dearpygui as dpg


class CallWhenDPGStartedCustom:
    STARTUP_DONE = False
    functions_queue = []

    @classmethod
    def append(cls, func, *args, **kwargs):
        if not cls.STARTUP_DONE:
            cls.functions_queue.append([func, args, kwargs])
            return
        try:
            func(*args, **kwargs)
        except Exception as e:
            print(f"Exception in CallWhenDPGStarted.append: {e}")

    @classmethod
    def execute(cls):
        if not cls.STARTUP_DONE:
            if dpg.get_frame_count() > 1:
                cls.STARTUP_DONE = True
                for func, args, kwargs in cls.functions_queue:
                    try:
                        func(*args, **kwargs)
                    except Exception as e:
                        print(f"Exception in CallWhenDPGStarted.execute: {e}")
                cls.functions_queue.clear()
