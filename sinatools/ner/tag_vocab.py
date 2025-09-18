"""Utilities for loading and converting legacy torchtext tag vocabularies."""
from __future__ import annotations

import pickle
import sys
import types
from collections import Counter
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple, Union

if sys.version_info >= (3, 8):  # pragma: no branch - typing guard
    from typing import TYPE_CHECKING
else:  # pragma: no cover - Py<3.8 fallback
    TYPE_CHECKING = False

if TYPE_CHECKING:  # pragma: no cover - type checking only
    from sinatools.ner.data_format import Vocab

LegacyVocabSequence = Sequence[object]


def load_tag_vocab(
    path: Union[str, Path],
    *,
    convert_legacy: bool = True,
    return_metadata: bool = False,
) -> Union[List["Vocab"], Tuple[List["Vocab"], dict]]:
    """Load ``tag_vocab.pkl`` while remaining robust to legacy torchtext pickles.

    Args:
        path: Filesystem path to ``tag_vocab.pkl``.
        convert_legacy: When ``True`` (default) legacy torchtext objects are translated
            to SinaTools' lightweight :class:`~sinatools.ner.data_format.Vocab`.

    Returns:
        List of vocabulary objects usable by the inference pipeline.
    """

    path = Path(path)

    converted = False

    try:
        with path.open("rb") as fh:
            tag_vocab = pickle.load(fh)
    except (ModuleNotFoundError, AttributeError) as exc:
        if not _mentions_torchtext(exc):
            raise
        legacy_vocab = _load_with_shims(path)
        if convert_legacy:
            tag_vocab = _convert_legacy_vocab(legacy_vocab)
            converted = True
        else:
            tag_vocab = legacy_vocab
    else:
        if convert_legacy and _looks_like_legacy(tag_vocab):
            tag_vocab = _convert_legacy_vocab(tag_vocab)
            converted = True

    if return_metadata:
        return tag_vocab, {"converted": converted}

    return tag_vocab


def convert_tag_vocab_file(
    model_dir: Union[str, Path],
    *,
    backup_suffix: str = ".legacy",
    dry_run: bool = False,
) -> Tuple[bool, Path | None]:
    """Convert ``tag_vocab.pkl`` in-place to the internal :class:`Vocab` format.

    Args:
        model_dir: Directory containing ``tag_vocab.pkl``.
        backup_suffix: Suffix used when stashing the original pickle. Set to ``None``
            to skip creating a backup copy.
        dry_run: When ``True`` only report whether conversion is required.

    Returns:
        Tuple of ``(converted, backup_path)`` where ``converted`` indicates whether a
        rewrite happened (or would happen for ``dry_run``). ``backup_path`` is the path
        to the backup file when one is created, otherwise ``None``.
    """

    model_dir = Path(model_dir)
    pickle_path = model_dir / "tag_vocab.pkl"

    tag_vocab, metadata = load_tag_vocab(
        pickle_path, convert_legacy=True, return_metadata=True
    )

    needs_conversion = metadata["converted"]

    if dry_run or not needs_conversion:
        return needs_conversion, None

    backup_path: Path | None = None

    if backup_suffix is not None:
        backup_path = pickle_path.with_suffix(pickle_path.suffix + backup_suffix)
        if backup_path.exists():
            raise FileExistsError(f"Backup file already exists: {backup_path}")
        pickle_path.replace(backup_path)

    with pickle_path.open("wb") as fh:
        pickle.dump(tag_vocab, fh)

    return True, backup_path


def _mentions_torchtext(exc: BaseException) -> bool:
    message = str(exc)
    return "torchtext" in message


def _load_with_shims(path: Path) -> LegacyVocabSequence:
    created_modules = _install_shims()

    try:
        with path.open("rb") as fh:
            return pickle.load(fh)
    finally:
        _remove_shims(created_modules)


def _install_shims() -> Tuple[str, ...]:
    created = []

    if "torchtext" not in sys.modules:
        torchtext_module = types.ModuleType("torchtext")
        sys.modules["torchtext"] = torchtext_module
        created.append("torchtext")
    else:
        torchtext_module = sys.modules["torchtext"]

    if not hasattr(torchtext_module, "vocab"):
        vocab_module = types.ModuleType("torchtext.vocab")
        torchtext_module.vocab = vocab_module
        sys.modules["torchtext.vocab"] = vocab_module
        created.append("torchtext.vocab")
    else:
        vocab_module = torchtext_module.vocab

    if not hasattr(vocab_module, "vocab"):
        vocab_vocab_module = types.ModuleType("torchtext.vocab.vocab")
        vocab_module.vocab = vocab_vocab_module
        sys.modules["torchtext.vocab.vocab"] = vocab_vocab_module
        created.append("torchtext.vocab.vocab")
    else:
        vocab_vocab_module = vocab_module.vocab

    if "torchtext._torchtext" not in sys.modules:
        backend_module = types.ModuleType("torchtext._torchtext")
        sys.modules["torchtext._torchtext"] = backend_module
        created.append("torchtext._torchtext")
    else:
        backend_module = sys.modules["torchtext._torchtext"]

    vocab_class = _TorchtextVocabShim
    vocab_vocab_module.Vocab = vocab_class
    backend_module.Vocab = vocab_class

    return tuple(created)


def _remove_shims(created_modules: Tuple[str, ...]) -> None:
    for name in created_modules:
        sys.modules.pop(name, None)


def _looks_like_legacy(obj: object) -> bool:
    if isinstance(obj, (list, tuple)):
        return any(_looks_like_legacy(item) for item in obj)
    module = getattr(obj.__class__, "__module__", "")
    if module.startswith("torchtext"):
        return True
    if hasattr(obj, "vocab"):
        return _looks_like_legacy(getattr(obj, "vocab"))
    return False


def _convert_legacy_vocab(raw_vocab: LegacyVocabSequence) -> List[Vocab]:
    VocabCls = _get_vocab_class()
    converted: List["Vocab"] = []
    for entry in _ensure_sequence(raw_vocab):
        tokens = _extract_tokens(entry)
        counter = Counter(tokens)
        converted.append(VocabCls(counter))
    return converted


def _extract_tokens(entry: object) -> List[str]:
    if hasattr(entry, "itos") and isinstance(getattr(entry, "itos"), Iterable):
        return list(getattr(entry, "itos"))

    nested = getattr(entry, "vocab", None)
    if nested is not None:
        return _extract_tokens(nested)

    if hasattr(entry, "stoi") and isinstance(entry.stoi, dict):
        # Sort by index to recover original ordering.
        return [token for token, _ in sorted(entry.stoi.items(), key=lambda item: item[1])]

    raise TypeError("Unsupported legacy vocab structure")


def _ensure_sequence(obj: object) -> Sequence[object]:
    if isinstance(obj, (list, tuple)):
        return obj
    raise TypeError("Expected sequence of vocabulary entries")


class _TorchtextVocabShim:
    """Minimal object to satisfy torchtext pickle references."""

    def __init__(self, *args, **kwargs):
        pass

    def __setstate__(self, state):
        # store raw state for debugging, but all meaningful attributes are captured
        # via ``vocab`` or the tuple state handled in ``_extract_tokens``.
        if isinstance(state, tuple) and len(state) == 4:
            version, unk_tokens, itos, specials = state
            self.version = version
            self.unk_tokens = unk_tokens
            self.itos = list(itos)
            self.specials = specials
        elif isinstance(state, dict):
            self.__dict__.update(state)
        else:
            self.state = state

    def __getstate__(self):  # pragma: no cover - compatibility only
        return getattr(self, "state", {})


def _get_vocab_class():
    from sinatools.ner.data_format import Vocab

    return Vocab
