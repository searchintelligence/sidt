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