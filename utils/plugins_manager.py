import os
import importlib.util

class PluginManager:
    def __init__(self, plugins_dir='plugins'):
        """
        Initialize the PluginManager by loading plugins from the specified directory.

        Args:
            plugins_dir (str): The directory where plugins are stored.
        """
        self.plugins = {}
        self.load_plugins(plugins_dir)

    def discover_plugin_files(self, plugins_dir):
        """
        Discover all Python files in the plugins directory.

        Args:
            plugins_dir (str): The directory where plugins are stored.

        Returns:
            list: A list of plugin filenames ending with '.py'.
        """
        plugin_files = []
        for filename in os.listdir(plugins_dir):
            if filename.endswith('.py'):
                plugin_files.append(filename)
        return plugin_files

    def load_plugin_module(self, plugin_name, module_path):
        """
        Dynamically load a plugin module from the given file path.

        Args:
            plugin_name (str): The name of the plugin.
            module_path (str): The file path to the plugin module.

        Returns:
            module: The loaded plugin module.
        """
        spec = importlib.util.spec_from_file_location(plugin_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def get_plugin_functions(self, module):
        """
        Retrieve the required functions from the plugin module.

        Args:
            module (module): The loaded plugin module.

        Returns:
            tuple: A tuple containing the 'is_plugin_applicable' and 'augment_message_content' functions.
        """
        is_applicable = getattr(module, 'is_plugin_applicable', None)
        augment_content = getattr(module, 'augment_message_content', None)
        return is_applicable, augment_content

    def register_plugin(self, plugin_name, is_applicable, augment_content):
        """
        Register the plugin in the plugins dictionary.

        Args:
            plugin_name (str): The plugin name.
            is_applicable (function): The 'is_plugin_applicable' function.
            augment_content (function): The 'augment_message_content' function.
        """
        self.plugins[plugin_name] = {
            'is_plugin_applicable': is_applicable,
            'augment_message_content': augment_content,
        }

    def load_plugins(self, plugins_dir):
        """
        Load plugins from the plugins directory and build the plugins dictionary.

        Args:
            plugins_dir (str): The directory where plugins are stored.
        """
        plugin_files = self.discover_plugin_files(plugins_dir)

        for filename in plugin_files:
            plugin_name = filename[:-3]  # Remove '.py' extension
            module_path = os.path.join(plugins_dir, filename)
            module = self.load_plugin_module(plugin_name, module_path)

            is_applicable, augment_content = self.get_plugin_functions(module)

            if is_applicable and augment_content:
                self.register_plugin(plugin_name, is_applicable, augment_content)
                print(f"Plugin '{plugin_name}' successfully loaded.")
            else:
                # Skip plugins that don't have the required functions
                print(f"Plugin '{plugin_name}' is missing required functions and will be skipped.")

    def find_applicable_plugin(self, user_input):
        """
        Find the first applicable plugin for the given user input.

        Args:
            user_input (str): The user's input message.

        Returns:
            tuple: A tuple containing the plugin name and its functions, or (None, None) if no applicable plugin is found.
        """
        for plugin_name, functions in self.plugins.items():
            is_applicable = functions['is_plugin_applicable']
            if is_applicable(user_input):
                return plugin_name, functions
        return None, None

    def process_input(self, message_content):
        """
        Process the message content using the applicable plugin, if any.

        Args:
            message_content (list): The message content structure.

        Returns:
            list: The (possibly) augmented message content.
        """
        user_input = message_content[0]["text"]
        plugin_name, functions = self.find_applicable_plugin(user_input)

        if functions:
            augment_content = functions['augment_message_content']
            print(f"Processing input with plugin '{plugin_name}'.")
            message_content = augment_content(message_content)
        else:
            # print("No applicable plugin found for the message. Proceeding without augmentation.")
            pass

        return message_content
