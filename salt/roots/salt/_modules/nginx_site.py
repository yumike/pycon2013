import os

from salt.exceptions import CommandNotFoundError
from salt.utils import check_or_die


def __virtual__():
    try:
        check_or_die('nginx')
    except CommandNotFoundError:
        return False
    return 'nginx_site'


def enable(name):
    if not exists(name):
        return False, '{} site does not exist'.format(name)
    if is_enabled(name):
        return True, '{} site is already enabled'.format(name)
    path = _get_path(name, enabled=True)
    target = _get_path(name)
    if os.path.exists(path):
        return False, (
            'Can not enable {} site, as {} file exists'.format(name, path)
        )
    os.symlink(target, path)
    __salt__['nginx.signal']('reload')
    return True, '{} site is enabled. Nginx is reloaded'.format(name)


def disable(name):
    if not exists(name):
        return False, '{} site does not exist'.format(name)
    if not is_enabled(name):
        return True, '{} site is already disabled'.format(name)
    os.remove(_get_path(name, enabled=True))
    __salt__['nginx.signal']('reload')
    return True, '{} site is disabled. Nginx is reloaded'.format(name)


def check_managed(
        name,
        source=None,
        source_hash=None,
        template=None,
        context=None,
        defaults=None,
        env='base',
        **kwargs):
    path = _get_path(name)
    result, comment = __salt__['file.check_managed'](
        name=path,
        source=source,
        source_hash=source_hash,
        template=template,
        user=None,
        group=None,
        mode=None,
        makedirs=None,
        context=context,
        defaults=defaults,
        env=env,
        **kwargs
    )
    if not result:
        return result, comment
    return True, '{} site is in the correct state'.format(name)


def manage(
        name,
        source=None,
        source_hash=None,
        template=None,
        context=None,
        defaults=None,
        env='base',
        **kwargs):
    ret = {'changes': {}, 'comment': '', 'name': name, 'result': True}
    path = _get_path(name)
    sfn, source_sum, comment = __salt__['file.get_managed'](
        name=path,
        source=source,
        source_hash=source_hash,
        template=template,
        user=None,
        group=None,
        mode=None,
        context=context,
        defaults=defaults,
        env=env,
        **kwargs
    )
    if comment:
        ret['result'] = False
        ret['comment'] = comment
        return ret
    ret = __salt__['file.manage_file'](
        name=path,
        sfn=sfn,
        ret=ret,
        source=source,
        source_sum=source_sum,
        user=None,
        group=None,
        mode=None,
        env=env,
        backup=None,
    )
    if ret['result']:
        if not ret['changes']:
            ret['comment'] = '{} site is in the correct state'.format(name)
        elif is_enabled(name):
            __salt__['nginx.signal']('reload')
            ret['changes'].update(reloaded='nginx')
            ret['comment'] = '{} site is updated. Nginx is reloaded'.format(name)
        else:
            ret['comment'] = '{} site is created or updated'.format(name)
    return ret


def remove(name):
    if not exists(name):
        return True, '{} site does not exist'.format(name)
    if is_enabled(name):
        disable(name)
        comment = '{} site is disabled and removed. Nginx is reloaded'
    else:
        comment = '{} site is removed'
    os.remove(_get_path(name))
    return True, comment.format(name)


def exists(name):
    return os.path.exists(_get_path(name))


def is_enabled(name):
    path = _get_path(name, enabled=True)
    target = _get_path(name)
    return os.path.islink(path) and os.readlink(path) == target


def _get_path(name, enabled=False):
    return '/etc/nginx/sites-{type}/{name}'.format(
        type='enabled' if enabled else 'available',
        name=name,
    )
