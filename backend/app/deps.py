from .services.vector_store import FaissStore
from .config import settings


store = FaissStore(settings.VECTORSTORE_DIR)