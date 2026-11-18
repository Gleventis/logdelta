from logdelta.mining.spell import generate_template


def test_spell_template_generation() -> None:
    input1 = ["Application", "started", "on", "server", "1"]
    input2 = ["Application", "started", "on", "server", "2"]

    result = generate_template(input1, input2)

    assert result == ["Application", "started", "on", "server", "<*>"]


def test_spell_with_different_sequence_lengths() -> None:
    input1 = ["Connection", "from", "192.168.1.1", "failed"]
    input2 = ["Connection", "from", "server", "192.168.1.2", "failed"]

    result = generate_template(input1, input2)

    assert result == ["Connection", "from", "<*>", "failed"]

def test_spell_with_between_tokens() -> None:
    input1 = ["A", "B"]
    input2 = ["A", "C", "B"]
    result = generate_template(input1, input2)

    assert result == ["A", "<*>", "B"]

def test_spell_with_multiple_different_tokens() -> None:
    input1 = ["User", "42", "logged", "in", "from", "10.0.0.1"]
    input2 = ["User", "87", "logged", "in", "from", "10.0.0.2"]
    result = generate_template(input1, input2)

    assert result == ["User", "<*>", "logged", "in", "from", "<*>"]

def test_spell_with_same_sequences() -> None:
    input1 = ["User", "deleted"]
    input2 = ["User", "deleted"]
    result = generate_template(input1, input2)

    assert result == ["User", "deleted"]

def test_spell_preservers_existing_wildcard() -> None:
    input1 = ["User", "<*>", "logged", "in"]
    input2 = ["User", "42", "logged", "in"]
    result = generate_template(input1, input2)

    assert result == ["User", "<*>", "logged", "in"]

def test_spell_with_no_common_sequences() -> None:
    input1 = ["User", "deleted"]
    input2 = ["Application", "started"]
    result = generate_template(input1, input2)

    assert result == ["<*>"]

def test_spell_with_empty_sequences() -> None:
    input1 = []
    input2 = []
    result = generate_template(input1, input2)

    assert result == []
