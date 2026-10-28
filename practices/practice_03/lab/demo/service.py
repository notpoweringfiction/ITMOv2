<<<<<<< Updated upstream
subscribers = set()


def subscribe(name):
    if not name.strip():
        raise ValueError("empty name")
    subscribers.add(name.strip())
    return {"subscribed": True}

=======
subscribers = set()


def subscribe(name):
    # Add a non-empty, trimmed name to the in-memory set
    if not name.strip():
        raise ValueError("empty name")
    subscribers.add(name.strip())
    return {"subscribed": True}


def unsubscribe(name):
    """Remove a subscriber by name.

    Returns {"unsubscribed": True} if the name was present and removed,
    otherwise returns {"unsubscribed": False}. Raises ValueError on empty name.
    """
    trimmed = name.strip()
    if not trimmed:
        raise ValueError("empty name")
    if trimmed in subscribers:
        subscribers.remove(trimmed)
        return {"unsubscribed": True}
    return {"unsubscribed": False}


def list_subscribers(sorted_=True):
    """Return current subscribers.

    By default returns a sorted list for deterministic order in tests/UX.
    Set sorted_=False to get an arbitrary-order list copy.
    """
    return sorted(subscribers) if sorted_ else list(subscribers)
>>>>>>> Stashed changes
