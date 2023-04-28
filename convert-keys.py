#!/usr/bin/env python3

import re
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any
import json

@dataclass
class KeyCodeOsFlags:
    windows: bool = True
    linux: bool = True
    android: bool = True
    macos: bool = True
    ios: bool = True


@dataclass
class KeyCode:
    names: List[str]
    description: Optional[str]
    context: str = "Keyboard"
    carify: bool = False
    documentation: Optional[str] = None
    os: KeyCodeOsFlags = KeyCodeOsFlags()
    footnotes: Dict[str, Any] = field(default_factory=dict)


mapping_re = re.compile(r'#define\s+(?P<name>[A-Z][A-Z0-9_]+)\s+(?P<target>[A-Z0-9_]+)\s*(//\s*(?P<descr>.*))?$', re.I)
key_codes: List[KeyCode] = []

file = "config/keys_de.h"
orig_input =  "../zmk-keymap-editor/api/services/zmk/data/zmk-keycodes.orig.json"
output = "../zmk-keymap-editor/api/services/zmk/data/zmk-keycodes.json"

with open(file, 'r') as fp:
    for line in fp:
        pass

        m = mapping_re.match(line)
        if not m:
            continue

        kc = KeyCode(
            names=[m.group("name").strip()],
            description=f'{m.group("descr").strip() or ""} -> {m.group("target")}',
        )
        key_codes.append(kc)

with open(orig_input, 'r') as fp:
    orig = json.load(fp)

with open(output, 'w') as fp:
    obj = map(lambda kc: asdict(kc), key_codes)
    json.dump(orig + list(obj), fp, indent=2)

