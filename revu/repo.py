

class Repo(object):

    def is_clean(self):
        """
        Is this method clean (ready to be used to do PR review; no unstaged
        changes)
        """
        raise NotImplementedError("Implement me")

    def restore(self):
        raise NotImplementedError("Implement me")

    def review(self, review):
        """
        Apply and checkout the review.
        """
        raise NotImplementedError("Implement me")

    def reviews(self):
        """
        Iterate over open reviews for this repo.
        """
        raise NotImplementedError("Implement me")


class Review(object):

    def comment(self):
        """
        Dispatch a comment to this review submitter
        """
        raise NotImplementedError("Implement me")

    def diff(self):
        """
        View the changeset
        """
        raise NotImplementedError("Implement me")

    def merge(self):
        """
        Preform the merge
        """
        raise NotImplementedError("Implement me")

    def push(self):
        """
        Do the push
        """
        raise NotImplementedError("Implement me")
