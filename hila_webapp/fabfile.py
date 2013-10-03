from fabric import *
from datetime import datetime
import tempfile

config = ENV
config.basedir = '/home/hila/django'
config.project = 'hila'
config.build_dir = '$(basedir)/$(project)-$(env)'
config.module_dir = '$(build_dir)/$(module)-$(branch)'
config.fab_user = 'www-data'
config.repos = {
    'hila_webapp': 'svn+ssh://openfeedback.org/svn/repos/$(project)/$(module)/$(branch)',
}
config.templates = {
    'hila_webapp': {
        'deploy/dbmigrate.sh': '$(basename)',
        'deploy/env.sh': '$(basename)',
        'deploy/start-fcgi.sh': '$(basename)',
        'deploy/stop-fcgi.sh': '$(basename)',
    }
}

def put_templates(dest_dir='$(module_dir)'):
    from fabric import _lazy_format
    import os
    for source, target in config.templates.get(config.module, {}).items():
        config.path, config.basename = os.path.split(source)
        fd, path = tempfile.mkstemp()
        os.write(fd, _lazy_format(open(_lazy_format(source), 'r').read()))
        os.close(fd)
        put(path, '%s/%s' % (dest_dir, target))
        os.remove(path)

@decorator
def branch(module_name):
    def deco(fun):
        def conf(*args, **kwargs):
            config.module, config.branch = module_name, config.exports[module_name]
            return fun(*args, **kwargs)
        import functools
        functools.update_wrapper(conf, fun)
        return conf
    return deco

def prod():
    if config.get('prod_confirm', None) != 'false':
        prompt('confirm', "Enter 'sesame' to confirm modification of PRODUCTION system",
               validate='sesame')
    config.fab_hosts = ['openfeedback.org']
    config.env = 'prod'
    config.exports = {
        'hila_webapp': 'trunk',
    }
    config.templates['hila_webapp'].update({
        'deploy/$(env)/local_settings.py': '$(basename)',
    })

def export():
    for config.module, config.branch in config.exports.items():
        config.source = config.repos[config.module]
        config.export_dir = '$(module_dir)-%s' % datetime.now().strftime('%Y%m%d%H%M%S')
        run('mkdir -p $(build_dir)')
        run('svn export $(source) $(export_dir)')
        put_templates('$(export_dir)')
        # remove symbolic link

def publish():
    stop()
    run('rm -f $(module_dir)')
    # symlink to latest export
    run('ln -s $(export_dir) $(module_dir)')
    run('sh $(module_dir)/dbmigrate.sh')
    start()

@branch('hila_webapp')
def stop():
    run('sh $(module_dir)/stop-fcgi.sh', fail='ignore')

@branch('hila_webapp')
def start():
    run('sh $(module_dir)/start-fcgi.sh')

def restart():
    stop()
    start()

def deploy():
    require('env', provided_by=['prod'])
    export()
    publish()
