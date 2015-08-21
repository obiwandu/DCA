# DCA
A device control agent based on Python gevent aims at control multiple types of remote network devices in a uniform way

## Installation

Deploy all the python files on both master and agent ends.


## Usage

0. start master.py, agent.py on each end respectively
1. Use cfg_cmd(self, ip, command) to configure command mapping on master
2. Use exec_cmd(self, abs_cmd, identity, protocol) or exec_script(self, script_name) to execute a specific command or script remotely on agent
3. Get execution result from agent which is actuall from the corresponding network device


## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## History

08/21/2015: First version released. Support command configuration, comamnd and script translation, comamnd and script execution
