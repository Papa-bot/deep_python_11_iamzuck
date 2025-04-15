import unittest
from meta_class import CustomClass, CustomMeta
# pylint: disable=no-member
# pylint: disable=protected-access
# pylint: disable=too-few-public-methods


class TestCustomMeta(unittest.TestCase):
    def test_class_attributes(self):
        self.assertEqual(CustomClass.custom_x, 50)
        with self.assertRaises(AttributeError):
            _ = CustomClass.x

        self.assertEqual(CustomClass.custom__protected, "protected")

        self.assertTrue(hasattr(CustomClass, '_CustomClass__private'))
        self.assertEqual(CustomClass._CustomClass__private, "private")

    def test_instance_attributes(self):
        inst = CustomClass()
        self.assertEqual(inst.custom_val, 99)
        with self.assertRaises(AttributeError):
            _ = inst.val

        self.assertEqual(inst.custom__protected_val, "protected_val")

        self.assertTrue(hasattr(inst, '_CustomClass__private_val'))
        self.assertEqual(inst._CustomClass__private_val, "private_val")

    def test_methods(self):
        inst = CustomClass()
        self.assertEqual(inst.custom_line(), 100)
        with self.assertRaises(AttributeError):
            _ = inst.line()

        self.assertEqual(inst.custom__protected_method(), "_protected_method")

        self.assertTrue(hasattr(inst, '_CustomClass__private_method'))
        self.assertEqual(inst._CustomClass__private_method(), "__private_method")

    def test_magic_methods(self):
        inst = CustomClass()
        self.assertEqual(str(inst), "Custom_by_metaclass")
        self.assertTrue(hasattr(inst, '__str__'))
        self.assertFalse(hasattr(inst, 'custom___str__'))

    def test_dynamic_attributes(self):
        inst = CustomClass()
        inst.dynamic = "added later"
        inst._dynamic_protected = "protected added"
        inst._class__dynamic_private = "private added"  # Явное задание приватного атрибута

        self.assertEqual(inst.custom_dynamic, "added later")
        self.assertEqual(inst.custom__dynamic_protected, "protected added")
        self.assertEqual(inst.custom__class__dynamic_private, "private added")

        with self.assertRaises(AttributeError):
            _ = inst.dynamic
        with self.assertRaises(AttributeError):
            _ = inst._dynamic_protected

    def test_inheritance(self):
        class ChildClass(CustomClass):
            child_attr = "child"

            def child_method(self):
                return "child_method"

        child = ChildClass()

        self.assertEqual(child.custom_child_attr, "child")
        self.assertEqual(child.custom_child_method(), "child_method")
        with self.assertRaises(AttributeError):
            _ = child.child_attr
        with self.assertRaises(AttributeError):
            _ = child.child_method()

        self.assertEqual(child.custom_x, 50)

    def test_class_attribute_assignment(self):
        CustomClass.new_attr = "new_attr"
        self.assertEqual(CustomClass.custom_new_attr, "new_attr")
        with self.assertRaises(AttributeError):
            _ = CustomClass.new_attr

    def test_edge_cases(self):
        class EmptyClass(metaclass=CustomMeta):
            pass

        empty = EmptyClass()
        setattr(empty, 'some_attr', 123)
        self.assertEqual(empty.custom_some_attr, 123)
        with self.assertRaises(AttributeError):
            _ = empty.some_attr

        class PrefixedClass(metaclass=CustomMeta):
            custom_attr = "prefixed"

        prefixed = PrefixedClass()
        self.assertEqual(prefixed.custom_custom_attr, "prefixed")
        with self.assertRaises(AttributeError):
            _ = prefixed.custom_attr
