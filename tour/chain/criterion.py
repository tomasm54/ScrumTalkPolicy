import abc
from rasa.shared.core.trackers import DialogueStateTracker


class Criterion(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def check(self, tracker: DialogueStateTracker) -> bool:
        raise NotImplementedError


class EqualIntent(Criterion):

    def __init__(self, compare: str) -> None:
        self._compare = compare

    def check(self, tracker: DialogueStateTracker) -> bool:
        return self._compare == tracker.latest_message.intent['name']


class EqualAction(Criterion):

    def __init__(self, compare: str) -> None:
        self._compare = compare

    def check(self, tracker: DialogueStateTracker) -> bool:
        return self._compare == tracker.latest_action_name


class EqualEntity(Criterion):

    def __init__(self, compare: str) -> None:
        self._compare = compare

    def check(self, tracker: DialogueStateTracker) -> bool:
        return self._compare == next(tracker.get_latest_entity_values("tema"), None)


class EqualPenultimateIntent(Criterion):

    def __init__(self, compare: str) -> None:
        self._compare = compare

    def check(self, tracker: DialogueStateTracker) -> bool:
        if len(tracker.as_dialogue().events) > 5:
            penultimate_intent = str(tracker.as_dialogue().events[-4])
        else:
            penultimate_intent = None
        if penultimate_intent is not None and penultimate_intent.find(self._compare) != -1:
            return True
        else:
            return False


class AndCriterion(Criterion):

    def __init__(self, criterion1: Criterion, criterion2: Criterion) -> None:
        self._criterion1 = criterion1
        self._criterion2 = criterion2

    def check(self, tracker: DialogueStateTracker) -> bool:
        return self._criterion1.check(tracker) and self._criterion2.check(tracker)


class NotCriterion(Criterion):

    def __init__(self, criterion1: Criterion) -> None:
        self._criterion1 = criterion1

    def check(self, tracker: DialogueStateTracker) -> bool:
        return not self._criterion1.check(tracker)


class OrCriterion(Criterion):

    def __init__(self, criterion1: Criterion, criterion2: Criterion) -> None:
        self._criterion1 = criterion1
        self._criterion2 = criterion2

    def check(self, tracker: DialogueStateTracker) -> bool:
        return self._criterion1.check(tracker) or self._criterion2.check(tracker)