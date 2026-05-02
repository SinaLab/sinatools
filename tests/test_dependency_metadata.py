import ast
import os
import unittest


ROOT = os.path.dirname(os.path.dirname(__file__))


def load_setup_requirements():
    setup_path = os.path.join(ROOT, "setup.py")
    with open(setup_path, encoding="utf-8") as handle:
        tree = ast.parse(handle.read())

    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                is_requirements = (
                    isinstance(target, ast.Name)
                    and target.id == "requirements"
                )
                if is_requirements:
                    return ast.literal_eval(node.value)
    raise AssertionError("setup.py does not define requirements")


class DependencyMetadataTest(unittest.TestCase):
    def test_torch_is_declared_directly(self):
        requirements = load_setup_requirements()

        self.assertIn("torch>=2.0", requirements)
        has_torchvision = any(
            req.startswith("torchvision") for req in requirements
        )
        self.assertFalse(
            has_torchvision,
            "SinaTools imports torch directly; do not rely on torchvision",
        )

    def test_transformers_range_matches_camel_tools(self):
        requirements = load_setup_requirements()

        self.assertIn("transformers>=4.0,<4.44", requirements)
        self.assertNotIn("transformers==4.47.1", requirements)


if __name__ == "__main__":
    unittest.main()
