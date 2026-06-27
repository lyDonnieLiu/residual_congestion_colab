"""
Multi-prompt circuit definitions for standard MI benchmarks.

Each circuit provides a list of {clean, corrupt, answer} triplets.
Using multiple prompts per circuit enables statistical reliability
and contrastive steering direction training.

Design principle: data (dict/list), not class hierarchy.
"""
from __future__ import annotations

# ── IOI: Indirect Object Identification ──────────────────────────────
# Pattern: "When [A] and [B] went to [place], [B] gave [object] to"
# Clean: B gives → expect " A" (indirect object = A)
# Corrupt: A gives → answer changes
IOI_PROMPTS = [
    ("When Mary and John went to the store, John gave a bottle to",
     "When Mary and John went to the store, Mary gave a bottle to",
     " Mary"),
    ("When Alice and Bob went to the park, Bob gave a book to",
     "When Alice and Bob went to the park, Alice gave a book to",
     " Alice"),
    ("When Emma and James went to the cafe, James gave a flower to",
     "When Emma and James went to the cafe, Emma gave a flower to",
     " Emma"),
    ("When Olivia and Liam went to the library, Liam gave a pen to",
     "When Olivia and Liam went to the library, Olivia gave a pen to",
     " Olivia"),
    ("When Sophia and Ethan went to the museum, Ethan gave a map to",
     "When Sophia and Ethan went to the museum, Sophia gave a map to",
     " Sophia"),
    ("When Ava and Noah went to the theater, Noah gave a ticket to",
     "When Ava and Noah went to the theater, Ava gave a ticket to",
     " Ava"),
    ("When Isabella and Mason went to the market, Mason gave a coin to",
     "When Isabella and Mason went to the market, Isabella gave a coin to",
     " Isabella"),
    ("When Mia and Lucas went to the beach, Lucas gave a shell to",
     "When Mia and Lucas went to the beach, Mia gave a shell to",
     " Mia"),
    ("When Charlotte and Logan went to the office, Logan gave a key to",
     "When Charlotte and Logan went to the office, Charlotte gave a key to",
     " Charlotte"),
    ("When Amelia and Jack went to the park, Jack gave a ball to",
     "When Amelia and Jack went to the park, Amelia gave a ball to",
     " Amelia"),
    ("When Harper and Aiden went to the garden, Aiden gave a rose to",
     "When Harper and Aiden went to the garden, Harper gave a rose to",
     " Harper"),
    ("When Evelyn and Caden went to the bakery, Caden gave a cake to",
     "When Evelyn and Caden went to the bakery, Evelyn gave a cake to",
     " Evelyn"),
]


# ── Greater-Than: Numerical Comparison ───────────────────────────────
# Pattern: "The war lasted from the year [Y] to the year"
# Clean: predict Y+1
# Corrupt: different year → different answer
GT_PROMPTS = [
    ("The war lasted from the year 1741 to the year",
     "The war lasted from the year 1841 to the year",
     " 1742"),
    ("The conflict began in the year 1623 and continued to the year",
     "The conflict began in the year 1723 and continued to the year",
     " 1624"),
    ("The dynasty ruled from the year 1102 to the year",
     "The dynasty ruled from the year 1202 to the year",
     " 1103"),
    ("The treaty was signed in the year 1918 and remained valid to the year",
     "The treaty was signed in the year 1818 and remained valid to the year",
     " 1919"),
    ("The king reigned from the year 1558 to the year",
     "The king reigned from the year 1658 to the year",
     " 1559"),
    ("The expedition departed in the year 1492 and returned in the year",
     "The expedition departed in the year 1592 and returned in the year",
     " 1493"),
    ("The empire expanded from the year 1280 to the year",
     "The empire expanded from the year 1380 to the year",
     " 1281"),
    ("The constitution was adopted in the year 1787 and amended in the year",
     "The constitution was adopted in the year 1887 and amended in the year",
     " 1788"),
    ("The plague lasted from the year 1347 to the year",
     "The plague lasted from the year 1447 to the year",
     " 1348"),
    ("The artist flourished from the year 1605 to the year",
     "The artist flourished from the year 1705 to the year",
     " 1606"),
]


# ── Docstring: Code Documentation Completion ─────────────────────────
# Pattern: "def [func_name](args):\n    [body]\n    # This function"
# Clean: signature with correct body → model predicts function name
# Corrupt: wrong body → changes prediction
DOCSTRING_PROMPTS = [
    ("def add(a, b):\n    return a + b\n    # This function",
     "def sub(a, b):\n    return a - b\n    # This function",
     " add"),
    ("def multiply(x, y):\n    return x * y\n    # This function",
     "def divide(x, y):\n    return x / y\n    # This function",
     " multiply"),
    ("def square(n):\n    return n * n\n    # This function",
     "def sqrt(n):\n    import math\n    return math.sqrt(n)\n    # This function",
     " square"),
    ("def concat(a, b):\n    return str(a) + str(b)\n    # This function",
     "def split(s, sep):\n    return s.split(sep)\n    # This function",
     " concat"),
    ("def max_val(a, b):\n    return a if a > b else b\n    # This function",
     "def min_val(a, b):\n    return a if a < b else b\n    # This function",
     " max_val"),
    ("def is_even(n):\n    return n % 2 == 0\n    # This function",
     "def is_odd(n):\n    return n % 2 == 1\n    # This function",
     " is_even"),
    ("def first_char(s):\n    return s[0]\n    # This function",
     "def last_char(s):\n    return s[-1]\n    # This function",
     " first_char"),
    ("def absolute(x):\n    return -x if x < 0 else x\n    # This function",
     "def negate(x):\n    return -x\n    # This function",
     " absolute"),
    ("def repeat(s, n):\n    return s * n\n    # This function",
     "def trim(s):\n    return s.strip()\n    # This function",
     " repeat"),
    ("def length(seq):\n    return len(seq)\n    # This function",
     "def reverse(seq):\n    return seq[::-1]\n    # This function",
     " length"),
]


# ── Registry ─────────────────────────────────────────────────────────
CIRCUIT_REGISTRY = {
    "ioi": {
        "prompts": IOI_PROMPTS,
        "description": "Indirect Object Identification",
    },
    "greater_than": {
        "prompts": GT_PROMPTS,
        "description": "Greater-Than numerical comparison",
    },
    "docstring": {
        "prompts": DOCSTRING_PROMPTS,
        "description": "Docstring function-name completion",
    },
}


def get_circuit(name: str) -> list[tuple[str, str, str]]:
    """Return the list of (clean, corrupt, answer) triplets for a circuit."""
    if name not in CIRCUIT_REGISTRY:
        raise ValueError(
            f"Unknown circuit: {name}. "
            f"Options: {list(CIRCUIT_REGISTRY.keys())}"
        )
    return CIRCUIT_REGISTRY[name]["prompts"]


def get_held_out_prompts(
    name: str, n_held_out: int = 3
) -> list[tuple[str, str, str]]:
    """Reserve held-out prompts for resample ablation."""
    all_prompts = get_circuit(name)
    return all_prompts[:n_held_out]  # first N are held-out
