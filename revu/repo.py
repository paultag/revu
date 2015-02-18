import abc


class Repo(object):
    __metaclass__ = ABCMeta

    @abc.abstractmethod
    def is_clean(self):
        """
        Is this method clean (ready to be used to do PR review; no unstaged
        changes)
        """
        pass

    @abc.abstractmethod
    def reviews(self):
        """
        Iterate over open reviews for this repo.
        """
        pass


class Review(object):
    __metaclass__ = ABCMeta

    @abc.abstractmethod
    def comment(self):
        """
        Dispatch a comment to this review submitter
        """
        pass

    @abc.abstractmethod
    def diff(self):
        """
        View the changeset
        """
        pass

    @abc.abstractmethod
    def merge(self):
        """
        Preform the merge
        """
        pass

    @abc.abstractmethod
    def push(self):
        """
        Do the push
        """
        pass
