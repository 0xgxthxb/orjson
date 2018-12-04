# SPDX-License-Identifier: (Apache-2.0 OR MIT)
# coding=UTF-8

import unittest
import datetime

import orjson


class TypeTests(unittest.TestCase):

    def test_fragment(self):
        """
        ValueError on fragments
        """
        for val in ('n', '{', '[', 't'):
            self.assertRaises(ValueError, orjson.loads, val)

    def test_invalid(self):
        """
        ValueError on invalid
        """
        for val in ('{"age", 44}', '[31337,]', '[,31337]', '[]]', '[,]'):
            self.assertRaises(ValueError, orjson.loads, val)

    def test_bool(self):
        """
        bool
        """
        for (obj, ref) in ((True, 'true'), (False, 'false')):
            self.assertEqual(orjson.dumps(obj), ref.encode('utf-8'))
            self.assertEqual(orjson.loads(ref), obj)

    def test_bool_array(self):
        """
        bool array
        """
        obj = [True] * 256
        ref = ('[' + ('true,' * 255) + 'true]').encode('utf-8')
        self.assertEqual(orjson.dumps(obj), ref)
        self.assertEqual(orjson.loads(ref), obj)

    def test_none(self):
        """
        null
        """
        obj = None
        ref = u'null'
        self.assertEqual(orjson.dumps(obj), ref.encode('utf-8'))
        self.assertEqual(orjson.loads(ref), obj)

    def test_null_array(self):
        """
        null array
        """
        obj = [None] * 256
        ref = ('[' + ('null,' * 255) + 'null]').encode('utf-8')
        self.assertEqual(orjson.dumps(obj), ref)
        self.assertEqual(orjson.loads(ref), obj)

    def test_int_64(self):
        """
        int  64-bit
        """
        for val in (9223372036854775807, -9223372036854775807):
            self.assertEqual(orjson.loads(str(val)), val)
            self.assertEqual(orjson.dumps(val), str(val).encode('utf-8'))

    def test_int_128(self):
        """
        int 128-bit

        These are an OverflowError in ujson, but valid in stdlib json.
        """
        for val in (9223372036854775809, -9223372036854775809):
            self.assertRaises(TypeError, orjson.dumps, val)

    def test_float(self):
        """
        float
        """
        self.assertEqual(-1.1234567893, orjson.loads("-1.1234567893"))
        self.assertEqual(-1.234567893, orjson.loads("-1.234567893"))
        self.assertEqual(-1.34567893, orjson.loads("-1.34567893"))
        self.assertEqual(-1.4567893, orjson.loads("-1.4567893"))
        self.assertEqual(-1.567893, orjson.loads("-1.567893"))
        self.assertEqual(-1.67893, orjson.loads("-1.67893"))
        self.assertEqual(-1.7893, orjson.loads("-1.7893"))
        self.assertEqual(-1.893, orjson.loads("-1.893"))
        self.assertEqual(-1.3, orjson.loads("-1.3"))

        self.assertEqual(1.1234567893, orjson.loads("1.1234567893"))
        self.assertEqual(1.234567893, orjson.loads("1.234567893"))
        self.assertEqual(1.34567893, orjson.loads("1.34567893"))
        self.assertEqual(1.4567893, orjson.loads("1.4567893"))
        self.assertEqual(1.567893, orjson.loads("1.567893"))
        self.assertEqual(1.67893, orjson.loads("1.67893"))
        self.assertEqual(1.7893, orjson.loads("1.7893"))
        self.assertEqual(1.893, orjson.loads("1.893"))
        self.assertEqual(1.3, orjson.loads("1.3"))

    def test_float_notation(self):
        """
        float notation
        """
        for val in ('1.337E40', '1.337e+40', '1337e40', '1.337E-4'):
            obj = orjson.loads(val)
            self.assertEqual(obj, float(val))
            self.assertEqual(orjson.dumps(val), ('"%s"' % val).encode('utf-8'))

    def test_list(self):
        """
        list
        """
        obj = ['a', '😊', True, {'b': 1.1}, 2]
        ref = '["a","😊",true,{"b":1.1},2]'
        self.assertEqual(orjson.dumps(obj), ref.encode('utf-8'))
        self.assertEqual(orjson.loads(ref), obj)

    def test_tuple(self):
        """
        tuple
        """
        obj = ('a', '😊', True, {'b': 1.1}, 2)
        ref = '["a","😊",true,{"b":1.1},2]'
        self.assertEqual(orjson.dumps(obj), ref.encode('utf-8'))
        self.assertEqual(orjson.loads(ref), list(obj))

    def test_dict(self):
        """
        dict
        """
        obj = {'key': 'value'}
        ref = '{"key":"value"}'
        self.assertEqual(orjson.dumps(obj), ref.encode('utf-8'))
        self.assertEqual(orjson.loads(ref), obj)

    def test_dict_large(self):
        """
        dict with >512 keys
        """
        obj = {'key_%s' % idx: 'value' for idx in range(513)}
        self.assertEqual(len(obj), 513)
        self.assertEqual(orjson.loads(orjson.dumps(obj)), obj)

    def test_dict_invalid_key(self):
        """
        dict invalid key
        """
        with self.assertRaises(TypeError):
            orjson.dumps({1: 'value'})
        with self.assertRaises(TypeError):
            orjson.dumps({b'key': 'value'})
