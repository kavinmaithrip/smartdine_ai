from collections import defaultdict, deque

class SessionMemory:
    def __init__(self, max_history=5):
        self.store = defaultdict(lambda: {
            "queries": deque(maxlen=max_history),
            "cuisines": deque(maxlen=max_history),
            "items": deque(maxlen=max_history),
            "moods": deque(maxlen=max_history),
            "city": None
        })

    def get(self, session_id):
        return self.store.get(session_id, {})

    def update(self, session_id, *, query, results, mood, city):
        mem = self.store[session_id]

        mem["queries"].append(query)
        mem["moods"].append(mood)
        mem["city"] = city

        for r in results:
            if r.get("Cuisine"):
                mem["cuisines"].append(r["Cuisine"])
            if r.get("Item_Name"):
                mem["items"].append(r["Item_Name"])
