# Copyright (c) 2012 Spotify AB
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

import getpass
import unittest
import luigi
from luigi import hdfs
import mock


class TestException(Exception):
    pass


class HdfsTestCase(unittest.TestCase):
    def setUp(self):
        self.fs = hdfs.client

    @staticmethod
    def _test_dir():
        return '/tmp/luigi_tmp_testdir_%s' % getpass.getuser()
    
    @staticmethod
    def _test_file(suffix=""):
        return '%s/luigi_tmp_testfile%s' % (HdfsTestCase._test_dir(), suffix)


class ErrorHandling(HdfsTestCase):
    def test_connection_refused(self):
        """ The point of this test is to see if file existence checks
        can distinguish file non-existence from errors

        this test would fail if hdfs would run locally on port 0
        """
        self.assertRaises(
            hdfs.HDFSCliError,
            self.fs.exists,
            'hdfs://127.0.0.1:0/foo'
        )

    def test_mkdir_exists(self):
        path = self._test_dir()
        if not self.fs.exists(path):
            self.fs.mkdir(path)
        self.assertTrue(self.fs.exists(path))
        self.assertRaises(
            luigi.target.FileAlreadyExists,
            self.fs.mkdir,
            path
        )
        self.fs.remove(path, skip_trash=True)


class AtomicHdfsOutputPipeTests(HdfsTestCase):
    def test_atomicity(self):
        testpath = self._test_file()
        if self.fs.exists(testpath):
            self.fs.remove(testpath, skip_trash=True)

        pipe = hdfs.HdfsAtomicWritePipe(testpath)
        self.assertFalse(self.fs.exists(testpath))
        pipe.close()
        self.assertTrue(self.fs.exists(testpath))

    def test_with_close(self):
        testpath = self._test_file()
        if self.fs.exists(testpath):
            self.fs.remove(testpath, skip_trash=True)

        with hdfs.HdfsAtomicWritePipe(testpath) as fobj:
            fobj.write('hej')

        self.assertTrue(self.fs.exists(testpath))

    def test_with_noclose(self):
        testpath = self._test_file()
        if self.fs.exists(testpath):
            self.fs.remove(testpath, skip_trash=True)

        def foo():
            with hdfs.HdfsAtomicWritePipe(testpath) as fobj:
                fobj.write('hej')
                raise TestException('Test triggered exception')
        self.assertRaises(TestException, foo)
        self.assertFalse(self.fs.exists(testpath))


class HdfsAtomicWriteDirPipeTests(HdfsTestCase):
    def setUp(self):
        super(HdfsAtomicWriteDirPipeTests, self).setUp()
        self.path = self._test_file()
        if self.fs.exists(self.path):
            self.fs.remove(self.path, skip_trash=True)

    def test_atomicity(self):
        pipe = hdfs.HdfsAtomicWriteDirPipe(self.path)
        self.assertFalse(self.fs.exists(self.path))
        pipe.close()
        self.assertTrue(self.fs.exists(self.path))

    def test_readback(self):
        pipe = hdfs.HdfsAtomicWriteDirPipe(self.path)
        self.assertFalse(self.fs.exists(self.path))
        pipe.write("foo\nbar")
        pipe.close()
        self.assertTrue(hdfs.exists(self.path))
        dirlist = hdfs.listdir(self.path)
        datapath = '%s/data' % self.path
        returnlist = [d for d in dirlist]
        self.assertTrue(returnlist[0].endswith(datapath))
        pipe = hdfs.HdfsReadPipe(datapath)
        self.assertEqual(pipe.read(), "foo\nbar")

    def test_with_close(self):
        with hdfs.HdfsAtomicWritePipe(self.path) as fobj:
            fobj.write('hej')

        self.assertTrue(self.fs.exists(self.path))

    def test_with_noclose(self):
        def foo():
            with hdfs.HdfsAtomicWritePipe(self.path) as fobj:
                fobj.write('hej')
                raise TestException('Test triggered exception')
        self.assertRaises(TestException, foo)
        self.assertFalse(self.fs.exists(self.path))


# This class is a mixin, and does not inherit from TestCase, in order to avoid running the base class as a test case.
class _HdfsFormatTest(object):
    format = None  # override with luigi.format.Format subclass

    def setUp(self):
        self.target = hdfs.HdfsTarget(self._test_file(), format=self.format)
        if self.target.exists():
            self.target.remove(skip_trash=True)

    def test_with_write_success(self):
        with self.target.open('w') as fobj:
            fobj.write('foo')
        self.assertTrue(self.target.exists())

    def test_with_write_failure(self):
        def dummy():
            with self.target.open('w') as fobj:
                fobj.write('foo')
                raise TestException()

        self.assertRaises(TestException, dummy)
        self.assertFalse(self.target.exists())


class PlainFormatTest(_HdfsFormatTest, HdfsTestCase):
    format = hdfs.Plain


class PlainDirFormatTest(_HdfsFormatTest, HdfsTestCase):
    format = hdfs.PlainDir

    def test_multifile(self):
        with self.target.open('w') as fobj:
            fobj.write('foo\n')
        second = hdfs.HdfsTarget(self.target.path + '/data2', format=hdfs.Plain)

        with second.open('w') as fobj:
            fobj.write('bar\n')
        invisible = hdfs.HdfsTarget(self.target.path + '/_SUCCESS', format=hdfs.Plain)
        with invisible.open('w') as fobj:
            fobj.write('b0rk\n')
        self.assertTrue(second.exists())
        self.assertTrue(invisible.exists())
        self.assertTrue(self.target.exists())
        with self.target.open('r') as fobj:
            parts = fobj.read().strip('\n').split('\n')
            parts.sort()
        self.assertEqual(tuple(parts), ('bar', 'foo'))


class HdfsTargetTests(HdfsTestCase):

    def test_slow_exists(self):
        target = hdfs.HdfsTarget(self._test_file())
        try:
            target.remove(skip_trash=True)
        except:
            pass

        self.assertFalse(self.fs.exists(target.path))
        target.open("w").close()
        self.assertTrue(self.fs.exists(target.path))

        def should_raise():
            self.fs.exists("hdfs://doesnotexist/foo")
        self.assertRaises(hdfs.HDFSCliError, should_raise)

        def should_raise_2():
            self.fs.exists("hdfs://_doesnotexist_/foo")
        self.assertRaises(hdfs.HDFSCliError, should_raise_2)

    def test_atomicity(self):
        target = hdfs.HdfsTarget(self._test_file())
        if target.exists():
            target.remove(skip_trash=True)

        fobj = target.open("w")
        self.assertFalse(target.exists())
        fobj.close()
        self.assertTrue(target.exists())

    def test_readback(self):
        target = hdfs.HdfsTarget(self._test_file())
        if target.exists():
            target.remove(skip_trash=True)

        origdata = 'lol\n'
        fobj = target.open("w")
        fobj.write(origdata)
        fobj.close()

        fobj = target.open('r')
        data = fobj.read()
        self.assertEqual(origdata, data)

    def test_with_close(self):
        target = hdfs.HdfsTarget(self._test_file())
        if target.exists():
            target.remove(skip_trash=True)

        with target.open('w') as fobj:
            fobj.write('hej\n')

        self.assertTrue(target.exists())

    def test_with_exception(self):
        target = hdfs.HdfsTarget(self._test_file())
        if target.exists():
            target.remove(skip_trash=True)

        def foo():
            with target.open('w') as fobj:
                fobj.write('hej\n')
                raise TestException('Test triggered exception')
        self.assertRaises(TestException, foo)
        self.assertFalse(target.exists())

    def test_create_parents(self):
        parent = self._test_dir()
        target = hdfs.HdfsTarget("%s/testfile" % parent)
        if self.fs.exists(parent):
            self.fs.remove(parent, skip_trash=True)
        self.assertFalse(self.fs.exists(parent))
        fobj = target.open('w')
        fobj.write('lol\n')
        fobj.close()
        self.assertTrue(self.fs.exists(parent))
        self.assertTrue(target.exists())

    def test_tmp_cleanup(self):
        path = self._test_file()
        target = hdfs.HdfsTarget(path, is_tmp=True)
        if target.exists():
            target.remove(skip_trash=True)
        with target.open('w') as fobj:
            fobj.write('lol\n')
        self.assertTrue(target.exists())
        del target
        import gc
        gc.collect()
        self.assertFalse(self.fs.exists(path))

    def test_luigi_tmp(self):
        target = hdfs.HdfsTarget(is_tmp=True)
        self.assertFalse(target.exists())
        with target.open('w'):
            pass
        self.assertTrue(target.exists())

    def test_tmp_move(self):
        target = hdfs.HdfsTarget(is_tmp=True)
        target2 = hdfs.HdfsTarget(self._test_file())
        if target2.exists():
            target2.remove(skip_trash=True)
        with target.open('w'):
            pass
        self.assertTrue(target.exists())
        target.move(target2.path)
        self.assertFalse(target.exists())
        self.assertTrue(target2.exists())

    def test_rename_no_parent(self):
        if self.fs.exists("foo"):
            self.fs.remove("foo", skip_trash=True)

        target1 = hdfs.HdfsTarget(is_tmp=True)
        target2 = hdfs.HdfsTarget("foo/bar")
        with target1.open('w'):
            pass
        self.assertTrue(target1.exists())
        target1.move(target2.path)
        self.assertFalse(target1.exists())
        self.assertTrue(target2.exists())

    def test_glob_exists(self):
        target_dir = hdfs.HdfsTarget(self._test_dir())
        if target_dir.exists():
            target_dir.remove(skip_trash=True)
        self.fs.mkdir(target_dir.path)
        t1 = hdfs.HdfsTarget(target_dir.path + "/part-00001")
        t2 = hdfs.HdfsTarget(target_dir.path + "/part-00002")
        t3 = hdfs.HdfsTarget(target_dir.path + "/another")

        with t1.open('w') as f:
            f.write('foo\n')
        with t2.open('w') as f:
            f.write('bar\n')
        with t3.open('w') as f:
            f.write('biz\n')

        files = hdfs.HdfsTarget("%s/part-0000*" % target_dir.path)

        self.assertTrue(files.glob_exists(2))
        self.assertFalse(files.glob_exists(3))
        self.assertFalse(files.glob_exists(1))


class _HdfsClientTest(HdfsTestCase):

    def create_file(self, target):
        fobj = target.open("w")
        fobj.close()

    def put_file(self, local_target, local_filename, target_path):
        if local_target.exists():
            local_target.remove()
        self.create_file(local_target)

        target = hdfs.HdfsTarget(target_path)
        if target.exists():
            target.remove(skip_trash=True)
        self.fs.mkdir(target.path)

        self.fs.put(local_target.path, target_path)
        target_file_path = target_path + "/" + local_filename
        return hdfs.HdfsTarget(target_file_path)

    def test_put(self):
        local_dir = "test/data"
        local_filename = "file1.dat"
        local_path = "%s/%s" % (local_dir, local_filename)
        target_path = self._test_dir()

        local_target = luigi.LocalTarget(local_path)
        target = self.put_file(local_target, local_filename, target_path)
        self.assertTrue(target.exists())
        local_target.remove()

    def test_get(self):
        local_dir = "test/data"
        local_filename = "file1.dat"
        local_path = "%s/%s" % (local_dir, local_filename)
        target_path = self._test_dir()

        local_target = luigi.LocalTarget(local_path)
        target = self.put_file(local_target, local_filename, target_path)
        self.assertTrue(target.exists())
        local_target.remove()

        local_copy_path = "%s/file1.dat.cp" % local_dir
        local_copy = luigi.LocalTarget(local_copy_path)
        if local_copy.exists():
            local_copy.remove()
        self.fs.get(target.path, local_copy_path)
        self.assertTrue(local_copy.exists())
        local_copy.remove()

    def test_getmerge(self):
        local_dir = "test/data"
        local_filename1 = "file1.dat"
        local_path1 = "%s/%s" % (local_dir, local_filename1)
        local_filename2 = "file2.dat"
        local_path2 = "%s/%s" % (local_dir, local_filename2)
        target_dir = self._test_dir()

        local_target1 = luigi.LocalTarget(local_path1)
        target1 = self.put_file(local_target1, local_filename1, target_dir)
        self.assertTrue(target1.exists())
        local_target1.remove()

        local_target2 = luigi.LocalTarget(local_path2)
        target2 = self.put_file(local_target2, local_filename2, target_dir)
        self.assertTrue(target2.exists())
        local_target2.remove()

        local_copy_path = "%s/file.dat.cp" % (local_dir)
        local_copy = luigi.LocalTarget(local_copy_path)
        if local_copy.exists():
            local_copy.remove()
        self.fs.getmerge(target_dir, local_copy_path)
        self.assertTrue(local_copy.exists())
        local_copy.remove()

        local_copy_crc_path = "%s/.file.dat.cp.crc" % (local_dir)
        local_copy_crc = luigi.LocalTarget(local_copy_crc_path)
        self.assertTrue(local_copy_crc.exists())
        local_copy_crc.remove()

    @mock.patch('luigi.hdfs.call_check')
    def test_cdh3_client(self, call_check):
        cdh3_client = luigi.hdfs.HdfsClientCdh3()
        cdh3_client.remove("/some/path/here")
        call_check.assert_called_once_with(['hadoop', 'fs', '-rmr', '/some/path/here'])

        cdh3_client.remove("/some/path/here", recursive=False)
        self.assertEquals(mock.call(['hadoop', 'fs', '-rm', '/some/path/here']), call_check.call_args_list[-1])

    @mock.patch('subprocess.Popen')
    def test_apache1_client(self, popen):
        comm = mock.Mock(name='communicate_mock')
        comm.return_value = "some return stuff", ""

        preturn = mock.Mock(name='open_mock')
        preturn.returncode = 0
        preturn.communicate = comm
        popen.return_value = preturn

        apache_client = luigi.hdfs.HdfsClientApache1()
        returned = apache_client.exists("/some/path/somewhere")
        self.assertTrue(returned)

        preturn.returncode = 1
        returned = apache_client.exists("/some/path/somewhere")
        self.assertFalse(returned)

        preturn.returncode = 13
        self.assertRaises(luigi.hdfs.HDFSCliError, apache_client.exists, "/some/path/somewhere")

if __name__ == "__main__":
    unittest.main()