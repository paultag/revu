from revu.repo import Repo, Review
import dulwich.repo


class GitRepo(Repo):

    def __init__(self, *, path):
        self.path = path

    def is_clean(self):
        repo = dulwich.repo.Repo(self.path)
        index = repo.open_index()
        print(index)

        return False

    def reviews(self):
        """
        Iterate over open reviews for this repo.
        """
        raise NotImplementedError("Implement me")
