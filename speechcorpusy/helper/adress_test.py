from .adress import extract_name_and_variant


def test_extract_name_and_variant_default():
    """Test `extract_name_and_variant`."""
    # Expects
    true_name = "VCTK"
    true_variant = "ver1_0_0"
    # Inputs
    name_andor_variant = "VCTK"
    default_variant = "ver1_0_0"

    # Outputs
    name, variant = extract_name_and_variant(name_andor_variant, default_variant)

    # Tests
    assert name == true_name
    assert variant == true_variant


def test_extract_name_and_variant_conf():
    """Test `extract_name_and_variant`."""
    # Expects
    true_name = "VCTK"
    true_variant = "ver1_0_0"
    # Inputs
    name_andor_variant = f"VCTK==ver1_0_0"
    default_variant = "ver_default"

    # Outputs
    name, variant = extract_name_and_variant(name_andor_variant, default_variant)

    # Tests
    assert name == true_name
    assert variant == true_variant
