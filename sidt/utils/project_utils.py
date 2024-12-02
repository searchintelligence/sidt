import os
import sys
import stat
import shutil
import inspect
from datetime import datetime


class Prutils:
    """
    Utility class for managing project directories and files.
    Includes methods for creating, running, and setting project names.
    """

    from sidt.utils.io import CLIF, read_json, write_json
    from sidt.utils.os import open_dir, get_available_funcs
    from sidt.utils.git import GitController

    def __init__(self):
        """Initializes the Prutils class with the caller's directory, project name, and config settings."""

        self.caller_dir = os.path.dirname(os.path.realpath(inspect.stack()[1].filename))
        self.project_name = self._load_project_name()
        self.config = Prutils.read_json(os.path.join(self.caller_dir, "config.json"))


    def _load_project_name(self, file_name="config.json"):
        """Loads the project name from 'config.json' in the caller's directory."""

        file_path = os.path.join(self.caller_dir, file_name)
        if not os.path.exists(file_path):
            print(Prutils.CLIF.fmt(f"No config file found. Creating default config at '{file_path}'", Prutils.CLIF.Color.YELLOW))
            self._set_project_name("Default_Project", file_name)
        config = Prutils.read_json(file_path)
        return config.get("current_project_name", "Default_Project")


    def _set_project_name(self, new_name, file_name="config.json"):
        """Sets the project name in 'config.json' in the caller's directory."""

        file_path = os.path.join(self.caller_dir, file_name)
        self.config.update({"current_project_name": new_name})
        Prutils.write_json(self.config, file_path)
        self.project_name = new_name
        print(Prutils.CLIF.fmt(f"Project name set to '{new_name}'", Prutils.CLIF.Color.GREEN))


    def _get_template_dir(self):
        """Returns the path to the project template directory specified in the config."""
        return os.path.join(self.caller_dir, self.config.get("template_path", "Application/project_template"))


    def _get_project_dir(self, folder_name):
        """Returns the path to the project directory in the caller's directory."""
        normalised_path = os.path.normpath(folder_name)
        parts = normalised_path.split(os.sep)
        
        if len(parts) > 1:
            parent_folder_name = os.path.join(*parts[:-1])
            folder_name = parts[-1]
        else:
            parent_folder_name = datetime.now().strftime("%Y-%m")

        return os.path.join(self.caller_dir, "Projects", parent_folder_name, folder_name)


    def _check_for_updates(self):
        """Check for updates if 'check_for_git_updates' is enabled in the config and update 'git_version' in config.json."""
        
        if self.config.get("check_for_git_updates", False):
            git = Prutils.GitController()
            if not git.is_git_repo:
                print(Prutils.CLIF.fmt(f"Directory is not a git repository. Skipping update check.", Prutils.CLIF.Color.YELLOW))
                return

            git = git.check_for_app_updates(root_dir=self.caller_dir)
            if git is None:
                print(Prutils.CLIF.fmt(f"Failed to check for updates.", Prutils.CLIF.Color.RED))
                git_info = {
                    "is_repo": git.is_git_repo
                }
            else:
                git_info = {
                    "local_commit": git.local_commit,
                    "remote_commit": git.remote_commit,
                    "is_outdated": git.is_outdated,
                    "is_repo": git.is_git_repo,
                }

            # Update config with git version details
            config_path = os.path.join(self.caller_dir, "config.json")
            self.config["git_version"] = git_info
            Prutils.write_json(self.config, config_path)

    
    def _sync_project_template(self, src_dir, dest_dir):
        """
        Sync the contents of src_dir into dest_dir.
        Removes files/folders not in src_dir and confirms overwrites for existing items.

        Args:
            src_dir (str): Path to the template directory.
            dest_dir (str): Path to the project directory.
        """

        def _on_rm_error(func, path, exc_info):
            """
            Handle errors during file or directory removal.
            Changes permissions and retries the operation.
            """
            os.chmod(path, stat.S_IWRITE)  # Grant write permissions
            func(path)  # Retry the removal

        # Remove items in dest_dir that are not in src_dir
        for item in os.listdir(dest_dir):
            if item not in os.listdir(src_dir):
                item_path = os.path.join(dest_dir, item)
                user_input = input(Prutils.CLIF.fmt(
                    f"'{item}' in the project directory does not exist in the template. Remove? (y/n): ",
                    Prutils.CLIF.Color.YELLOW
                )).lower()
                if user_input == "y":
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path, onerror=_on_rm_error)
                    else:
                        os.remove(item_path)
                    print(Prutils.CLIF.fmt(
                        f"Removed '{item}' from project directory.",
                        Prutils.CLIF.Color.GREEN
                    ))
                else:
                    print(Prutils.CLIF.fmt(
                        f"Skipping removal of '{item}'.",
                        Prutils.CLIF.Color.YELLOW
                    ))

        # Copy contents from src_dir to dest_dir
        for item in os.listdir(src_dir):
            src_path = os.path.join(src_dir, item)
            dest_path = os.path.join(dest_dir, item)

            if os.path.exists(dest_path):
                user_input = input(Prutils.CLIF.fmt(
                    f"'{item}' already exists. Overwrite? (y/n): ",
                    Prutils.CLIF.Color.YELLOW
                )).lower()
                if user_input != "y":
                    print(Prutils.CLIF.fmt(
                        f"Skipping '{item}'.",
                        Prutils.CLIF.Color.YELLOW
                    ))
                    continue
                if os.path.isdir(dest_path):
                    shutil.rmtree(dest_path)
                else:
                    os.remove(dest_path)

            if os.path.isdir(src_path):
                shutil.copytree(src_path, dest_path)
            else:
                shutil.copy(src_path, dest_path)

            print(Prutils.CLIF.fmt(
                f"Copied '{item}' into project directory.",
                Prutils.CLIF.Color.GREEN
            ))


    def run(self, project_class, name=None, open=False):
        """
        Public method to run a project.
        Initializes the project, runs it, and opens the project directory if specified.
        """

        # Check for updates before running
        self._check_for_updates()

        # Use provided name or fall back to the instance's project name
        if name is not None:
            self._set_project_name(name)
        project_dir = self._get_project_dir(self.project_name)

        # Get important directories
        project_dir = self._get_project_dir(self.project_name)
        app_dir = os.path.join(self.caller_dir, "Application")
        data_dir = os.path.join(app_dir, "data")
        app_config = Prutils.read_json(os.path.join(self.caller_dir, "config.json"))

        # Initialize and run the project
        project = project_class(
            project_dir=project_dir,
            root_dir=self.caller_dir,
            app_dir=app_dir,
            data_dir=data_dir,
            project_name=self.project_name,
            app_config=app_config
        )
        project.initialise()
        project.run()

        # Open the project directory if specified
        if open:
            Prutils.open_dir(project_dir)


    def create(self, name=None, open=True):
        """
        Public method to create a project with template files.
        Ensures the project directory matches the contents of the template directory.

        Args:
            name (str, optional): Name of the project directory. Defaults to None, which uses self.project_name.
            open (bool, optional): Whether to open the project directory after creation. Defaults to True.
        """

        # Check for updates before creating new project
        self._check_for_updates()

        # Use provided name or fall back to the instance's project name
        if name is not None:
            self._set_project_name(name)        

        project_dir = self._get_project_dir(self.project_name)
        os.makedirs(project_dir, exist_ok=True)
        print(Prutils.CLIF.fmt(
            f"Ensured project directory exists.",
            Prutils.CLIF.Color.GREEN
        ))

        # Get the template directory
        template_dir = self._get_template_dir()
        if not os.path.exists(template_dir) or not os.listdir(template_dir):
            print(Prutils.CLIF.fmt(
                "No template files found. Project created as an empty directory.",
                Prutils.CLIF.Color.YELLOW
            ))
            return

        # Sync template contents into the project directory
        self._sync_project_template(template_dir, project_dir)

        # Open the project directory if specified
        if open:
            print(Prutils.CLIF.fmt(
                f"Opening project directory: {project_dir}",
                Prutils.CLIF.Color.GREEN
            ))
            Prutils.open_dir(project_dir)


    def set_name(self, new_name):
        """Public method to set the project name."""
        self._set_project_name(new_name)


    def get_name(self):
        """Public method to get the project name."""
        print(Prutils.CLIF.fmt(f"Current project name: '{self.project_name}'", Prutils.CLIF.Color.GREEN))


    def help(self):
        """Public method to print the available commands."""
        available_methods = Prutils.get_available_funcs(self.__class__, exclude_module=True)
        print(Prutils.CLIF.fmt(f"Available commands: {', '.join(available_methods)}", Prutils.CLIF.Color.GREEN))
