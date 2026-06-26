chat_histories: dict[str, list[dict[str, str]]] = {}

MAX_HISTORY_MESSAGES = 6


def get_history(session_id: str) -> list[dict[str, str]]:
    return chat_histories.get(session_id, [])


def save_message(session_id: str, role: str, content: str) -> None:
    history = chat_histories.get(session_id, [])

    history.append(
        {
            "role": role,
            "content": content,
        }
    )

    chat_histories[session_id] = history[-MAX_HISTORY_MESSAGES:]