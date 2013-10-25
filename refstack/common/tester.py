#
# Copyright (c) 2013 Piston Cloud Computing, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import os
import sys
import errno
from refstack.common.tempest_config import TempestConfig
import testrepository.repository.file
from testrepository import ui
from testrepository.commands import run
from testrepository.commands import init


class TestRepositoryUI(ui.AbstractUI):
    """nothing"""
    def __init__(self, here):
        """Create a UI to run a TestRepository command

        :param here: What should the 'here' be for the UI.
        """
        self.here = here



class TestRepositorySource(object):
    """Get test results from a testrepository.

    Reloading asks testr to re-run (and implicitly record) a new 
    test result.

    :ivar testr_directory: path to directory containing .testr repository
    """

    def __init__(self, testr_directory):
        self.testr_directory = os.path.expanduser(testr_directory)
        self._ui = TestRepositoryUI(self.testr_directory)
        
        self.init_repo()


    def get_subunit_stream(self):
        try:
            return self.testrepository_last_stream()
        except KeyError:
            raise NoStreamPresent()


    def init_repo(self):
        """inits a new testrepository repo in the supplied path"""
        #os.chdir(self.testr_directory)
        try:
            cmd = init.init(self._ui)
            cmd.run()
        except OSError:
            # if this happens its fine .. just means the repo is already there
            pass        


    def run(self):
        here = os.getcwd()
        os.chdir(self.testr_directory)
        self._ui.c = self.testr_directory+'tempest.conf'

        cmd = run.run(self._ui)
        try:
            res = cmd.execute()
        finally:
            os.chdir(here)


    def testrepository_last_stream(self):
        factory = testrepository.repository.file.RepositoryFactory()
        repo = factory.open(self.testr_directory)
        # this is poor because it just returns a stringio for the whole 
        # thing; we should instead try to read from it as a file so we can 
        # get nonblocking io
        return repo.get_test_run(repo.latest_id()).get_subunit_stream()



class Tester(object):
    """ Test functions"""
    test_id = None
    sha = None
    cloud_id = None
    _status = None


    def __init__(self,cloud_id=None,test_id=None,sha=None):
        """ init method loads specified id or fails"""
        if not test_id:
            #create a new test id
            self.test_id = 10
        else: 
            # set test id
            self.test_id = id

        self.tempest_config = TempestConfig(cloud_id)
        self.cloud_id = cloud_id
        self.sha = sha
        self.test_path = "/tmp/%s" % self.cloud_id


    def run_remote(self):
        """triggers remote run"""  
        # install tempest in virt env
        # start tests against cloud_id using sha of tempest 
        # no sha indicates trunk


    def run_local():
        """triggers local run"""
        # make sure we have a folder to put a repo in.. 
        if not os.path.exists(self.test_path):
            os.makedirs(self.test_path)
        
        # write the tempest config to that folder
        self.write_config(self.test_path)

        # setup the repo wrapper.. this creates the repo if its not already there
        tr = TestRepositorySource(self.test_path)

        # run tests
        tr.run()
        
        # get back the results 
        result = tr.testrepository_last_stream()

        # write results to database maybe .. or return them .. not sure which .. 
        return result.read()


    def write_config(self, path):
        """writes config to path specified"""
        # get the config
        output = self.tempest_config.build_config_from_keystone()

        with open(path+"tempest.conf", "w") as config_file:
            config_file.write(output)
        

    def cancel(self):
        """ cancels a running test"""


    @property
    def status(self):
        """The status property."""
        def fget(self):
            return self._status
        def fset(self, value):
            self._status = value
        def fdel(self):
            del self._status
        return locals()


    @property
    def config(self):
        """The config property. outputs a tempest config based on settings"""    
        return self.tempest_config.output()
