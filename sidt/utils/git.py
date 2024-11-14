import sys
import time
import subprocess


class GitController():
    """
    A controller class to manage local and remote Git repository operations.

    Attributes:
        path (str): The file system path to the Git repository.
        is_repo (bool): Indicates whether the specified directory is a Git repository.
        local_commit (dict or None): Stores the latest local commit information.
        remote_commit (dict or None): Stores the latest remote commit information.
    """

    def __init__(self, path="."):
        """
        Initializes the GitController by checking if the specified directory is a Git repository
        and setting the initial local and remote commit information to None.

        Args:
            path (str): Path to the directory to manage. Defaults to current directory.
        """

        self.path = path
        self.is_git_repo = self.get_is_git_repo()
        self.local_commit = None
        self.remote_commit = None
        self.is_outdated = False
        if self.is_git_repo:
            self.get_local_commit()
            self.get_remote_commit()
            self.get_commit_difference()


    def get_is_git_repo(self):
        """
        Check if the specified directory is a git repository.

        Returns:
            bool: True if the directory is a git repository, False otherwise.
        """

        return self.run_command("rev-parse", "--is-inside-work-tree") == "true"


    def run_command(self, *args):
        """
        Execute a git command in the specified directory and return its output or handle errors.

        Args:
            *args: Variable length argument list for git command components.

        Returns:
            str or None: Output of the git command if successful, None if an error occurred.
        """

        try:
            result = subprocess.run(["git", "-C", self.path] + list(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                print(f"Error running git command {' '.join(args)}: {result.stderr}")
                return None
            return result.stdout.strip()
        except Exception as e:
            print(f"Exception running git command {' '.join(args)}: {str(e)}")
            return None


    def get_local_commit(self):
        """
        Retrieve the current commit information from the local git repository.

        Returns:
            dict or None: Dictionary containing the commit hash, message, author, and date if the repository is a git repo, None otherwise.
        """

        commit_hash = self.run_command("rev-parse", "HEAD")
        if commit_hash is None:
            return None
        
        commit_message = self.run_command("log", "-1", "--pretty=format:%B")
        author = self.run_command("log", "-1", "--pretty=format:%an")
        date = self.run_command("log", "-1", "--pretty=format:%ad")

        self.local_commit = {
            "hash": commit_hash,
            "message": commit_message,
            "author": author,
            "date": date,
        }
        return self.local_commit


    def get_remote_commit(self, remote="origin", branch="main"):
        """
        Retrieve the current commit information from the specified remote branch and determine divergence from local.

        Args:
            remote (str): The name of the remote repository (default is 'origin').
            branch (str): The branch to fetch the commit from (default is 'main').

        Returns:
            dict or None: Dictionary containing the commit hash, message, author, and date if remote exists, None otherwise.
        """

        self.run_command("fetch", remote)
        commit_hash = self.run_command("rev-parse", f"{remote}/{branch}")
        if commit_hash is None:
            return None
        
        commit_message = self.run_command("log", "-1", f"{remote}/{branch}", "--pretty=format:%B")
        author = self.run_command("log", "-1", f"{remote}/{branch}", "--pretty=format:%an")
        date = self.run_command("log", "-1", f"{remote}/{branch}", "--pretty=format:%ad")

        self.remote_commit = {
            "hash": commit_hash,
            "message": commit_message,
            "author": author,
            "date": date
        }
        return self.remote_commit


    def get_commit_difference(self, remote="origin", branch="main"):
        """
        Compares the latest commits of the local and remote repositories to determine the commit difference.
        Updates the commits_ahead and commits_behind attributes to reflect the number of commits:
            - commits_ahead: Number of commits the local is ahead of the remote.
            - commits_behind: Number of commits the local is behind the remote.

        Args:
            remote (str): The name of the remote repository (default is 'origin').
            branch (str): The branch to compare (default is 'main').

        Returns:
            None: Updates class attributes directly.
        """

        if self.local_commit is None or self.remote_commit is None:
            self.commits_ahead = 0
            self.commits_behind = 0
            self.is_outdated = False
            return

        # Determine how many commits local is ahead of remote
        self.commits_ahead = int(self.run_command("rev-list", "--count", f"{remote}/{branch}..HEAD").strip())
        self.commits_behind = int(self.run_command("rev-list", "--count", f"HEAD..{remote}/{branch}").strip())

        # Update outdated status based on whether local is behind
        if self.commits_behind > 0:
            self.is_outdated = True
        else:
            self.is_outdated = False


    def hard_reset_to_remote(self, remote="origin", branch="main"):
        """
        Reset the local repository to exactly match the specified remote branch, discarding any local changes.
        WARNING: This operation is destructive and will remove any local changes.

        Args:
            remote (str): The name of the remote repository (default is 'origin').
            branch (str): The branch from which to reset (default is 'main').

        Returns:
            None
        """

        print("Fetching latest changes from the remote...")
        self.get_remote_commit(remote, branch)
        self.get_commit_difference(remote, branch)

        if self.is_outdated:
            print("Resetting local branch to match remote branch...")
            result = self.run_command("reset", "--hard", f"{remote}/{branch}")
            if result is not None:
                print("Local branch reset successfully to remote branch.")
            else:
                print("Failed to reset local branch.")
        else:
            print("Local branch is already up to date with the remote branch.")


    def pip_update_from_requirements(self, force_update_sidt=True):
        """Update all installed packages to the latest versions specified in the requirements.txt file.
        
        Args:
            force_include_sidt (bool): Whether to force reinstall the SIDT package from its Git repository.
        """
        
        print("Updating installed packages to match requirements.txt...")
        try:
            # First, update packages from requirements.txt
            result = subprocess.run(["pip", "install", "-r", f"{self.path}/requirements.txt", "--upgrade"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                print("Packages updated successfully.")
            else:
                print(f"Failed to update packages: {result.stderr}")

            # Optionally install SIDT from Git
            if force_update_sidt:
                print("Installing SIDT from Git repository...")
                sidt_result = subprocess.run(["pip", "install", "git+https://github.com/searchintelligence/sidt.git", "--force-reinstall", "--no-deps"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if sidt_result.returncode == 0:
                    print("SIDT installed successfully.")
                else:
                    print(f"Failed to install SIDT: {sidt_result.stderr}")

        except Exception as e:
            print(f"Exception occurred: {str(e)}")
    

    @staticmethod
    def check_for_app_updates(root_dir, allow_force_update=True):
        """
        Check for updates to a git repository and update if necessary. Shortcut method to check for updates and prompt the user to update.
        args:
            root_dir (str): The root directory of the project containing the Git repository.
            allow_force_update (bool): Whether to allow the user to force update the app.
        return:
            GitController: The GitController object for the project. Contains commit information and update status.
        """

        from sidt.utils.io import CLIF

        print(CLIF.fmt(f"\n\nChecking Github for updates to the app...", CLIF.Format.BOLD, CLIF.Color.GREEN))
        git = GitController(root_dir)
        
        # If the app is up to date, continue
        if not git.is_outdated:
            print(CLIF.fmt(f"\nApp is up to date. Continuing...", CLIF.Format.BOLD, CLIF.Color.GREEN))
            time.sleep(1)
            return git

        # If the app is outdated, prompt the user to update
        print(f"Your commit: {git.local_commit['date']} - {git.local_commit['message']}")
        print(f"Latest commit: {git.local_commit['date']} - {git.remote_commit['message']} ({git.commits_behind} commits ahead)")
        print(CLIF.fmt(f"The app is outdated. Please update the app to the latest version.", CLIF.Format.BOLD, CLIF.Color.YELLOW))

        # Allow the user to either continue with the outdated app or exit if allow_force_update is False
        if not allow_force_update:
            cont = input(
                CLIF.fmt(f"\nType 'y' to continue with the outdated app or any other key to exit.\n", CLIF.Format.BOLD, CLIF.Color.MAGENTA)
                )
            if cont.lower() != "y":
                print(CLIF.fmt(f"\nApp Aborted", CLIF.Format.BOLD, CLIF.Color.RED))
                sys.exit()

        # If force update is allowed, prompt the user to continue, force update, or exit
        cont = input(
            CLIF.fmt(f"\nType 'y' to continue with the outdated app, 'f' to force update, or any other key to exit.\n", CLIF.Format.BOLD, CLIF.Color.MAGENTA)
            )
        
        # Exit if user does not want to continue
        if cont.lower() not in ["y", "f"]:
            print(CLIF.fmt(f"\nApp Aborted", CLIF.Format.BOLD, CLIF.Color.RED))
            sys.exit()
        
        # Force update the app if user chooses to
        if cont.lower() == "f":

            # Confirm force update
            conf = input(
                CLIF.fmt(f"\nWarning - Force updating will reset the app code to the latest version.\n", CLIF.Color.RED) +
                "This will delete your local changes and synchronise your code with the most recent version.\nYour projects and config files will not be affected.\n" +
                CLIF.fmt(f"\nAre you sure you want to force update the app? Type 'y' to confirm.\n", CLIF.Format.BOLD, CLIF.Color.MAGENTA)
                )
            if conf.lower() == "y":
                
                # Reset the app to the latest version
                git.hard_reset_to_remote()

                # Update pip requirements
                print(CLIF.fmt(f"\nUpdating pip requirements...", CLIF.Format.BOLD, CLIF.Color.GREEN))
                git.pip_update_from_requirements()

                print(CLIF.fmt(f"\nApp updated to latest version. Run again to continue with updated app.", CLIF.Format.BOLD, CLIF.Color.GREEN))
            print(CLIF.fmt(f"\nApp Aborted", CLIF.Format.BOLD, CLIF.Color.RED))
            sys.exit()

        # Continue with outdated app
        return git