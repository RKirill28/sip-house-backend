import pytest
from pydantic import TypeAdapter, ValidationError

from src.core.schemas import ReadChatModel
from tests.conftest import client


def test_update_chat_list():
    res = client.post("api/v1/chats")
    adapter = TypeAdapter(list[ReadChatModel])

    assert res.status_code == 200
    try:
        adapter.validate_python(res.json())
    except ValidationError:
        pytest.fail("Ошибка валидации")
