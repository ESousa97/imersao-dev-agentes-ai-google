import pytest

from src.botinho.services.chat_service import ChatService, GeminiClient


class FakeChatSession:
    async def send_message(self, message: str):  # noqa: ANN001, ANN201
        class _Result:
            text = "Resposta fake"

        return _Result()


class FakeModelClient:
    model_name = "fake-model"
    available = True

    async def create_chat(self, history: list) -> FakeChatSession:  # noqa: ANN001
        return FakeChatSession()


class FakeSyncResult:
    text = "Resposta sync"


class FakeSyncChatSession:
    def send_message(self, message: str):  # noqa: ANN001, ANN201
        return FakeSyncResult()


class FakeSyncModelClient:
    model_name = "fake-model-sync"
    available = True

    async def create_chat(self, history: list) -> FakeSyncChatSession:  # noqa: ANN001
        return FakeSyncChatSession()


class FakeAioChats:
    def create(self, model: str, config, history: list):  # noqa: ANN001, ANN201
        return FakeSyncChatSession()


class FakeAioClient:
    chats = FakeAioChats()


class FakeGenAiClient:
    aio = FakeAioClient()


class QuotaExceededModelClient:
    model_name = "fake-model-quota"
    available = True

    def __init__(self) -> None:
        self.calls = 0

    async def create_chat(self, history: list):  # noqa: ANN001, ANN201
        self.calls += 1
        raise RuntimeError(
            "429 RESOURCE_EXHAUSTED. Quota exceeded. Please retry in 45s."
        )


class NotFoundThenSuccessModelClient:
    model_name = "gemini-1.5-flash-lastest"
    available = True

    def __init__(self) -> None:
        self.calls = 0

    async def create_chat(self, history: list):  # noqa: ANN001, ANN201
        self.calls += 1
        if self.model_name == "gemini-1.5-flash-lastest":
            raise RuntimeError(
                "404 NOT_FOUND. models/gemini-1.5-flash-lastest is not found for API version v1beta"
            )
        return FakeSyncChatSession()

    def try_next_model(self) -> bool:
        self.model_name = "gemini-2.0-flash"
        return True


class QuotaThenSuccessModelClient:
    model_name = "gemini-2.0-flash"
    available = True

    def __init__(self) -> None:
        self.calls = 0

    async def create_chat(self, history: list):  # noqa: ANN001, ANN201
        self.calls += 1
        if self.model_name == "gemini-2.0-flash":
            raise RuntimeError(
                "429 RESOURCE_EXHAUSTED. Quota exceeded for model: gemini-2.0-flash. "
                "Please retry in 28s."
            )
        return FakeSyncChatSession()

    def try_next_model(self) -> bool:
        if self.model_name == "gemini-2.0-flash":
            self.model_name = "gemini-2.0-flash-lite"
            return True
        return False


def test_detect_category_procedimentos_ti():
    service = ChatService(model_client=FakeModelClient())

    category = service.detect_category("Preciso resetar minha senha")

    assert category == "procedimentos_ti"


def test_search_knowledge_finds_wifi_guidance():
    service = ChatService(model_client=FakeModelClient())

    knowledge = service.search_knowledge("Meu wifi caiu")

    assert knowledge is not None
    assert "Wi-Fi" in knowledge


@pytest.mark.asyncio
async def test_converse_accepts_sync_send_message():
    service = ChatService(model_client=FakeSyncModelClient())

    result = await service.converse("teste")

    assert result["response"] == "Resposta sync"


@pytest.mark.asyncio
async def test_gemini_client_accepts_non_awaitable_chat_create():
    client = GeminiClient(api_key="fake-key", model_name="fake-model")
    client.available = True
    client._client = FakeGenAiClient()

    chat = await client.create_chat(history=[])

    assert isinstance(chat, FakeSyncChatSession)


@pytest.mark.asyncio
async def test_quota_error_enters_cooldown_and_skips_next_gemini_call():
    model_client = QuotaExceededModelClient()
    service = ChatService(model_client=model_client)

    first_result = await service.converse("teste 1")
    second_result = await service.converse("teste 2")

    assert model_client.calls == 1
    assert "Posso ajudar" in first_result["response"]
    assert "Posso ajudar" in second_result["response"]


@pytest.mark.asyncio
async def test_not_found_model_retries_with_fallback_model():
    model_client = NotFoundThenSuccessModelClient()
    service = ChatService(model_client=model_client)

    result = await service.converse("teste")

    assert model_client.calls == 2
    assert model_client.model_name == "gemini-2.0-flash"
    assert result["response"] == "Resposta sync"


@pytest.mark.asyncio
async def test_quota_error_retries_with_fallback_model_before_cooldown():
    model_client = QuotaThenSuccessModelClient()
    service = ChatService(model_client=model_client)

    result = await service.converse("teste")

    assert model_client.calls == 2
    assert model_client.model_name == "gemini-2.0-flash-lite"
    assert result["response"] == "Resposta sync"
