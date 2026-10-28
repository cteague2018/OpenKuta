from __future__ import annotations

import hashlib
import hmac
import json
from typing import Any, Dict, Tuple

import sympy as sp

from backend.app.generators.verification_gate import fast_numeric_equivalence


def verify_student_step_transition(
    prev_step: sp.Basic, curr_step: sp.Basic, var: sp.Symbol
) -> Tuple[bool, str]:
    if isinstance(prev_step, sp.Equality) and isinstance(curr_step, sp.Equality):
        try:
            sol_prev = sp.solveset(prev_step, var, domain=sp.S.Reals)
            sol_curr = sp.solveset(curr_step, var, domain=sp.S.Reals)
            if sol_prev == sol_curr and sol_prev != sp.EmptySet:
                return True, "VALID_EQUATION_STEP"

            lhs_prev_moved = prev_step.lhs - prev_step.rhs
            lhs_curr_moved = curr_step.lhs - curr_step.rhs
            if sp.simplify(lhs_prev_moved + lhs_curr_moved) == 0:
                return True, "VALID_NEGATION"
            return False, "SOLUTION_SET_CHANGED"
        except Exception:
            return False, "UNSOLVABLE_TRANSITION"

    if not isinstance(prev_step, sp.Relational) and not isinstance(curr_step, sp.Relational):
        syms = list(prev_step.free_symbols.union(curr_step.free_symbols))
        if fast_numeric_equivalence(prev_step, curr_step, syms):
            return True, "VALID_EXPRESSION_STEP"
        if fast_numeric_equivalence(prev_step, -curr_step, syms):
            return False, "SIGN_ERROR"
        return False, "ALGEBRAIC_MISMATCH"

    return False, "TYPE_MISMATCH"


def encode_secure_qr_payload(
    ws_id: str, form_id: str, seed: int, student_id: str, secret_key: str
) -> str:
    msg = f"{ws_id}:{form_id}:{student_id}".encode("utf-8")
    mask_digest = hmac.new(secret_key.encode("utf-8"), msg, hashlib.sha256).digest()
    seed_mask = int.from_bytes(mask_digest[:4], "big")
    masked_seed = seed ^ seed_mask

    payload: Dict[str, Any] = {"w": ws_id, "f": form_id, "m": masked_seed, "s": student_id}
    raw_json = json.dumps(payload, separators=(",", ":"), sort_keys=True)
    sig = hmac.new(secret_key.encode("utf-8"), raw_json.encode("utf-8"), hashlib.sha256).hexdigest()[:12]
    payload["sig"] = sig
    return json.dumps(payload, separators=(",", ":"))


def decode_secure_qr_payload(qr_json: str, secret_key: str) -> Dict[str, Any]:
    data = json.loads(qr_json)
    sig = data.pop("sig", "")
    raw_json = json.dumps(data, separators=(",", ":"), sort_keys=True)
    expected_sig = hmac.new(secret_key.encode("utf-8"), raw_json.encode("utf-8"), hashlib.sha256).hexdigest()[:12]
    if not hmac.compare_digest(sig, expected_sig):
        raise ValueError("Tampered or invalid worksheet QR signature.")

    msg = f"{data['w']}:{data['f']}:{data['s']}".encode("utf-8")
    mask_digest = hmac.new(secret_key.encode("utf-8"), msg, hashlib.sha256).digest()
    seed_mask = int.from_bytes(mask_digest[:4], "big")
    data["seed"] = data["m"] ^ seed_mask
    result: Dict[str, Any] = data
    return result
